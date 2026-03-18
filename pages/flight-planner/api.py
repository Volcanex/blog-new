from flask import Blueprint, jsonify, request
import requests
import aiohttp
import asyncio
from dataclasses import dataclass, asdict
from typing import Dict, List, Set, Tuple, Optional, Callable, Any
from queue import PriorityQueue
import heapq
import json
import time
from datetime import datetime, timedelta
import logging
import uuid
import threading
import os
import pickle
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache file location
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_FILE = CACHE_DIR / "flight_cache.pkl"
AIRPORTS_FILE = CACHE_DIR / "airports.json"

bp = Blueprint('flight_planner', __name__, url_prefix='/api/flight-planner')

# Type aliases
Cost = float
Day = int
AirportCode = str
Certainty = float  # 0.0 to 1.0

# DataForSEO API Configuration
SERP_AUTH = "Basic Y2hyaXNtb3J0QHpvaG8uY29tOjNiOGNjMTcwMjEzYTU1NjI="
SERP_API_URL = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
SERP_API_COST_PER_REQUEST = 0.002  # $0.002 per Live Mode request

# Default airports list
DEFAULT_AIRPORTS = [
    "LHR", "LGW", "CDG", "AMS", "FRA", "IST", "DXB", "JFK", "LAX", "ORD",
    "ATL", "PEK", "HND", "SIN", "BOM", "DEL", "SYD", "MEL", "CPT", "JNB"
]

# Airport geographic coordinates (lat, lon) for visualization positioning
AIRPORT_COORDS = {
    "LHR": (51.4700, -0.4543),    # London Heathrow
    "LGW": (51.1537, -0.1821),    # London Gatwick
    "CDG": (49.0097, 2.5479),     # Paris Charles de Gaulle
    "AMS": (52.3105, 4.7683),     # Amsterdam Schiphol
    "FRA": (50.0379, 8.5622),     # Frankfurt
    "IST": (41.2753, 28.7519),    # Istanbul
    "DXB": (25.2532, 55.3657),    # Dubai
    "JFK": (40.6413, -73.7781),   # New York JFK
    "LAX": (33.9416, -118.4085),  # Los Angeles
    "ORD": (41.9742, -87.9073),   # Chicago O'Hare
    "ATL": (33.6407, -84.4277),   # Atlanta
    "PEK": (40.0799, 116.6031),   # Beijing
    "HND": (35.5494, 139.7798),   # Tokyo Haneda
    "SIN": (1.3644, 103.9915),    # Singapore
    "BOM": (19.0896, 72.8656),    # Mumbai
    "DEL": (28.5665, 77.1031),    # Delhi
    "SYD": (-33.9399, 151.1753),  # Sydney
    "MEL": (-37.6690, 144.8410),  # Melbourne
    "CPT": (-33.9715, 18.6021),   # Cape Town
    "JNB": (-26.1392, 28.2460)    # Johannesburg
}

# Global state for search progress
search_state = {}

# Airport management functions
def load_airports():
    """Load airports from file, or use defaults if file doesn't exist."""
    try:
        if AIRPORTS_FILE.exists():
            with open(AIRPORTS_FILE, 'r') as f:
                data = json.load(f)
                logger.info(f"Loaded {len(data['airports'])} airports from file")
                return data['airports']
        else:
            logger.info("No saved airports file, using defaults")
            return DEFAULT_AIRPORTS.copy()
    except Exception as e:
        logger.error(f"Failed to load airports: {e}")
        return DEFAULT_AIRPORTS.copy()

def save_airports(airports_list):
    """Save airports to file."""
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(AIRPORTS_FILE, 'w') as f:
            json.dump({"airports": airports_list}, f, indent=2)
        logger.info(f"Saved {len(airports_list)} airports to file")
        return True
    except Exception as e:
        logger.error(f"Failed to save airports: {e}")
        return False

@dataclass(frozen=True)
class Node:
    """A node in the flight graph, representing an airport on a specific day."""
    airport: AirportCode
    day: Day

    def __str__(self) -> str:
        return f"{self.airport}@{self.day}"

    def to_dict(self) -> Dict:
        return {"airport": self.airport, "day": self.day}


@dataclass
class Edge:
    """An edge in the flight graph, representing a flight or stay between nodes."""
    source: Node
    target: Node
    cost: Cost
    is_flight: bool  # True for flight, False for stay
    is_estimated: bool  # True if cost is estimated, False if actual
    certainty: Certainty  # How certain we are about the estimated cost
    edge_id: str = None
    url: Optional[str] = None  # Google Flights URL for this flight

    def __post_init__(self):
        if self.edge_id is None:
            self.edge_id = str(uuid.uuid4())

    def to_dict(self) -> Dict:
        return {
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "cost": self.cost,
            "is_flight": self.is_flight,
            "is_estimated": self.is_estimated,
            "certainty": self.certainty,
            "edge_id": self.edge_id,
            "url": self.url
        }


class FlightGraph:
    """Graph representation of flights and stays."""
    def __init__(self):
        self.nodes: Set[Node] = set()
        self.outgoing_edges: Dict[Node, List[Edge]] = {}
        self.incoming_edges: Dict[Node, List[Edge]] = {}
        self.edges_by_id: Dict[str, Edge] = {}

    def add_node(self, node: Node) -> None:
        if node not in self.nodes:
            self.nodes.add(node)
            self.outgoing_edges[node] = []
            self.incoming_edges[node] = []

    def add_edge(self, edge: Edge) -> None:
        self.add_node(edge.source)
        self.add_node(edge.target)
        self.outgoing_edges[edge.source].append(edge)
        self.incoming_edges[edge.target].append(edge)
        self.edges_by_id[edge.edge_id] = edge

    def update_edge(self, edge_id: str, new_cost: Cost, new_certainty: Certainty, is_estimated: bool) -> None:
        if edge_id in self.edges_by_id:
            edge = self.edges_by_id[edge_id]
            edge.cost = new_cost
            edge.certainty = new_certainty
            edge.is_estimated = is_estimated

    def get_outgoing_edges(self, node: Node) -> List[Edge]:
        return self.outgoing_edges.get(node, [])

    def get_node(self, airport: AirportCode, day: Day) -> Optional[Node]:
        for node in self.nodes:
            if node.airport == airport and node.day == day:
                return node
        return None

    def to_dict(self) -> Dict:
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges_by_id.values()]
        }


class SerpFlightAPI:
    """Flight API using DataForSEO SERP API."""

    def __init__(self):
        self.available_destinations_cache = {}
        self.actual_flight_cache = {}
        self.estimate_cache = {}
        self.airports = load_airports()  # Load from file or use defaults
        self.cache_date = None
        self._load_cache()

    def _format_date(self, day: int) -> str:
        """Convert day number to DD/MM format."""
        date = datetime.now() + timedelta(days=day)
        return date.strftime("%d/%m")

    def _get_today_date(self) -> str:
        """Get today's date as a string for cache validation."""
        return datetime.now().strftime("%Y-%m-%d")

    def _load_cache(self):
        """Load cache from disk if it exists and is from today."""
        try:
            if CACHE_FILE.exists():
                with open(CACHE_FILE, 'rb') as f:
                    cache_data = pickle.load(f)

                # Check if cache is from today
                if cache_data.get('date') == self._get_today_date():
                    self.available_destinations_cache = cache_data.get('available_destinations', {})
                    self.actual_flight_cache = cache_data.get('actual_flights', {})
                    self.estimate_cache = cache_data.get('estimates', {})
                    self.cache_date = cache_data.get('date')
                    logger.info(f"✓ Loaded cache from disk ({len(self.actual_flight_cache)} flight prices)")
                else:
                    logger.info(f"✗ Cache is from {cache_data.get('date')}, invalidating (today is {self._get_today_date()})")
                    self._clear_cache()
            else:
                logger.info("No cache file found, starting with empty cache")
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")
            self._clear_cache()

    def _save_cache(self):
        """Save cache to disk with today's date."""
        try:
            # Create cache directory if it doesn't exist
            CACHE_DIR.mkdir(parents=True, exist_ok=True)

            cache_data = {
                'date': self._get_today_date(),
                'available_destinations': self.available_destinations_cache,
                'actual_flights': self.actual_flight_cache,
                'estimates': self.estimate_cache
            }

            with open(CACHE_FILE, 'wb') as f:
                pickle.dump(cache_data, f)

            logger.debug(f"Cache saved to disk ({len(self.actual_flight_cache)} flight prices)")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    def _clear_cache(self):
        """Clear all cache data."""
        self.available_destinations_cache = {}
        self.actual_flight_cache = {}
        self.estimate_cache = {}
        self.cache_date = None

    async def _search_serp_async(self, session: aiohttp.ClientSession, keyword: str) -> Dict:
        """Search Google Flights via SERP API (async version)."""
        headers = {
            "Authorization": SERP_AUTH,
            "Content-Type": "application/json"
        }

        data = [{
            "keyword": keyword,
            "location_code": 2826,  # UK
            "language_code": "en",
            "device": "desktop",
            "os": "windows",
            "depth": 10
        }]

        try:
            logger.info(f"SERP API Query: {keyword}")
            async with session.post(SERP_API_URL, headers=headers, json=data, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    # Read raw bytes and decompress if needed
                    raw_data = await response.read()

                    # Check content encoding
                    encoding = response.headers.get('Content-Encoding', '').lower()
                    if encoding == 'br':
                        import brotli
                        raw_data = brotli.decompress(raw_data)
                    elif encoding == 'gzip':
                        import gzip
                        raw_data = gzip.decompress(raw_data)

                    # Parse JSON
                    result = json.loads(raw_data.decode('utf-8'))
                    logger.info(f"SERP API Response status: {response.status}, has tasks: {bool(result.get('tasks'))}")
                    if result.get('tasks'):
                        logger.info(f"SERP API tasks: {len(result['tasks'])}, first task result: {bool(result['tasks'][0].get('result'))}")
                    return result
                else:
                    text = await response.text()
                    logger.error(f"SERP API error: {response.status}, Response: {text[:500]}")
                    return {}
        except Exception as e:
            logger.error(f"SERP API exception: {e}")
            return {}

    def _extract_flight_price(self, api_response: Dict) -> Tuple[Optional[float], Optional[str]]:
        """Extract the cheapest flight price and URL from SERP response."""
        try:
            if not api_response.get("tasks"):
                logger.warning("No 'tasks' in API response")
                return (None, None)

            tasks = api_response["tasks"]
            if not tasks or not tasks[0].get("result"):
                logger.warning(f"No result in tasks. Tasks: {tasks}")
                return (None, None)

            result = tasks[0]["result"]
            if not result:
                logger.warning("Result is empty")
                return (None, None)

            items = result[0].get("items", []) if result else []
            logger.info(f"Found {len(items)} items in SERP response")

            # Log item types for debugging
            item_types = [item.get("type") for item in items]
            logger.info(f"Item types: {item_types}")

            for item in items:
                if item.get("type") == "google_flights":
                    flight_items = item.get("items", [])
                    logger.info(f"Found google_flights with {len(flight_items)} sub-items")
                    prices = []
                    flight_data = []  # Store (price, url) tuples

                    for flight in flight_items:
                        if flight.get("type") == "google_flights_element":
                            # Extract price from description (matches original working code)
                            description = flight.get("description", "")
                            url = flight.get("url", "")
                            logger.info(f"Flight description: {description}")

                            # Parse description like: "Multiple airlines  1d 5h+  Connecting  from £157"
                            if "from" in description:
                                try:
                                    parts = description.split("from")
                                    if len(parts) > 1:
                                        price_part = parts[1].strip()
                                        # Remove currency symbol (£, $, etc.) and parse
                                        price_str = ''.join(c for c in price_part.split()[0] if c.isdigit() or c == '.')
                                        if price_str:
                                            price = float(price_str)
                                            flight_data.append((price, url))
                                            logger.info(f"Extracted price: {price}, URL: {url[:50]}...")
                                except Exception as pe:
                                    logger.warning(f"Failed to parse price from '{description}': {pe}")

                    if flight_data:
                        # Sort by price and get cheapest
                        flight_data.sort(key=lambda x: x[0])
                        min_price, best_url = flight_data[0]
                        logger.info(f"Returning minimum price: ${min_price} with URL")
                        return (min_price, best_url)
                    else:
                        logger.warning("No prices found in google_flights items")

            logger.warning("No google_flights item found in response")
            return (None, None)
        except Exception as e:
            logger.error(f"Error extracting price: {e}", exc_info=True)
            return (None, None)

    def get_available_destinations(self, node: Node) -> List[AirportCode]:
        """Get list of available destination airports from a node."""
        cache_key = f"{node.airport}_{node.day}"
        if cache_key in self.available_destinations_cache:
            return self.available_destinations_cache[cache_key]

        # Return all airports except the source
        destinations = [apt for apt in self.airports if apt != node.airport]
        self.available_destinations_cache[cache_key] = destinations
        self._save_cache()
        return destinations

    def estimate_flight_cost(self, source: Node, dest: Node) -> Tuple[Cost, Certainty]:
        """Estimate flight cost between two nodes."""
        cache_key = f"{source.airport}_{dest.airport}_{source.day}"
        if cache_key in self.estimate_cache:
            return self.estimate_cache[cache_key]

        # Simple distance-based estimation (placeholder)
        # In reality, this would use historical data
        base_cost = 200.0
        self.estimate_cache[cache_key] = (base_cost, 0.5)
        self._save_cache()
        return (base_cost, 0.5)

    async def get_actual_flight_cost_async(self, session: aiohttp.ClientSession, source: Node, dest: Node) -> Tuple[Optional[Cost], bool, Optional[str]]:
        """Get actual flight cost and URL via SERP API (async version)."""
        cache_key = f"{source.airport}_{dest.airport}_{source.day}"
        if cache_key in self.actual_flight_cache:
            cached = self.actual_flight_cache[cache_key]
            # Handle backward compatibility: old cache format is (price, found), new is (price, found, url)
            if len(cached) == 2:
                price, found = cached
                return (price, found, None)
            return cached

        # Format search query - use the working format only
        date_str = self._format_date(source.day)
        keyword = f"{source.airport} to {dest.airport} {date_str} ONE WAY"

        logger.info(f"SERP query: {keyword}")
        response = await self._search_serp_async(session, keyword)
        price, url = self._extract_flight_price(response)

        if price:
            logger.info(f"✓ Found price: ${price} for {source.airport} → {dest.airport}")
            self.actual_flight_cache[cache_key] = (price, True, url)
            return (price, True, url)

        # No price found
        logger.warning(f"✗ No price for {source.airport} → {dest.airport}")
        self.actual_flight_cache[cache_key] = (None, False, None)
        return (None, False, None)

    async def batch_get_flight_costs(self, routes: List[Tuple[Node, Node]], max_concurrent: int = 10) -> Dict[Tuple[Node, Node], Tuple[Optional[Cost], bool, Optional[str]]]:
        """Fetch multiple flight costs and URLs in parallel with concurrency limit."""
        results = {}

        # Create aiohttp session with connector that doesn't request brotli
        connector = aiohttp.TCPConnector()
        async with aiohttp.ClientSession(connector=connector, auto_decompress=False) as session:
            # Create semaphore to limit concurrent requests
            semaphore = asyncio.Semaphore(max_concurrent)

            async def fetch_with_limit(route):
                async with semaphore:
                    source, dest = route
                    result = await self.get_actual_flight_cost_async(session, source, dest)
                    return (route, result)

            # Fetch all routes in parallel (with concurrency limit)
            tasks = [fetch_with_limit(route) for route in routes]
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for response in responses:
                if isinstance(response, Exception):
                    logger.error(f"Batch fetch error: {response}")
                    continue
                route, result = response
                results[route] = result

        # Save cache after batch operation
        self._save_cache()

        return results


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points on Earth in km."""
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


def default_heuristic(node: Node, destination: str) -> Cost:
    """Geographic distance-based heuristic for A* search.

    Uses Haversine formula to calculate great circle distance and converts to
    an optimistic flight cost estimate (~$0.10 per km).
    """
    if node.airport == destination:
        return 0.0

    # Get coordinates
    if node.airport not in AIRPORT_COORDS or destination not in AIRPORT_COORDS:
        return 100.0  # Fallback if coordinates not available

    lat1, lon1 = AIRPORT_COORDS[node.airport]
    lat2, lon2 = AIRPORT_COORDS[destination]

    distance_km = haversine_distance(lat1, lon1, lat2, lon2)

    # Optimistic estimate: $0.10 per km (real flights are usually more expensive)
    # This makes it admissible for A* while still providing good guidance
    return distance_km * 0.10


class PathFinder:
    """A* search algorithm for finding optimal flight paths."""

    def __init__(
        self,
        graph: FlightGraph,
        api: SerpFlightAPI,
        heuristic_function: Callable[[Node, AirportCode], Cost],
        max_days: int = 14,
        max_iterations: int = 1000,
        max_api_calls: int = 200,
        stay_cost: float = 100.0,
        stop_after_first_path: bool = True,
        all_routes_available: bool = False,
        search_id: str = None,
        force_indirect: bool = False,
        visualization_delay: float = 0.25  # 250ms delay between batches for visualization
    ):
        self.graph = graph
        self.api = api
        self.heuristic_function = heuristic_function
        self.max_days = max_days
        self.max_iterations = max_iterations
        self.max_api_calls = max_api_calls
        self.stay_cost = stay_cost
        self.stop_after_first_path = stop_after_first_path
        self.all_routes_available = all_routes_available
        self.search_id = search_id
        self.force_indirect = force_indirect
        self.visualization_delay = visualization_delay

        self.api_call_count = 0
        self.iterations = 0
        self.search_log = []

        # Visualization state tracking
        self.explored_nodes = set()  # Nodes fully explored
        self.frontier_nodes = set()  # Nodes in priority queue
        self.current_node = None  # Node being explored right now
        self.discovered_edges = []  # All edges found during search
        self.current_edge = None  # Edge being checked right now

    def log_progress(self, message: str):
        """Log progress message and update search state."""
        self.search_log.append({
            "event": "progress",
            "message": message,
            "iterations": self.iterations,
            "api_calls": self.api_call_count,
            "timestamp": datetime.now().isoformat()
        })

        # Update global search state for live updates
        if self.search_id and self.search_id in search_state:
            search_state[self.search_id]["result"]["log"] = self.search_log
            progress = min(100, int((self.iterations / self.max_iterations) * 100))
            search_state[self.search_id]["progress"] = progress
            self.update_visualization_state()

    def update_visualization_state(self):
        """Update visualization state in global search state."""
        if not self.search_id or self.search_id not in search_state:
            return

        # Prepare visualization data
        viz_state = {
            "explored_nodes": [{"airport": n.airport, "day": n.day} for n in self.explored_nodes],
            "frontier_nodes": [{"airport": n.airport, "day": n.day} for n in self.frontier_nodes],
            "current_node": {"airport": self.current_node.airport, "day": self.current_node.day} if self.current_node else None,
            "edges": [
                {
                    "source": {"airport": e["source"].airport, "day": e["source"].day},
                    "target": {"airport": e["target"].airport, "day": e["target"].day},
                    "cost": e["cost"],
                    "state": e["state"]  # "checking", "found", "not_found", "optimal"
                }
                for e in self.discovered_edges
            ],
            "current_edge": self.current_edge
        }

        # Store current state and append to snapshot queue
        search_state[self.search_id]["result"]["visualization"] = viz_state

        # Accumulate snapshots for buffered playback
        if "viz_snapshots" not in search_state[self.search_id]["result"]:
            search_state[self.search_id]["result"]["viz_snapshots"] = []
        search_state[self.search_id]["result"]["viz_snapshots"].append(viz_state)
        # Update stats in real-time
        search_state[self.search_id]["result"]["iterations"] = self.iterations
        search_state[self.search_id]["result"]["api_calls"] = self.api_call_count
        search_state[self.search_id]["result"]["api_cost"] = self.api_call_count * SERP_API_COST_PER_REQUEST

    async def find_path(self, source: Node, destination_airport: AirportCode) -> Tuple[List[List[Node]], List[Cost]]:
        """Find optimal paths from source to destination using A* search with async batching.

        Returns:
            Tuple of (all_paths, all_costs) where paths are sorted by cost (cheapest first)
        """
        # Priority queue: (f_score, counter, node, path_cost, path)
        counter = 0
        pq = [(self.heuristic_function(source, destination_airport), counter, source, 0.0, [source])]
        visited = set()
        all_paths = []  # Store all paths found
        all_costs = []  # Store corresponding costs
        best_cost = float('inf')

        self.log_progress(f"Starting search: {source.airport} → {destination_airport}")

        while pq and self.iterations < self.max_iterations:
            self.iterations += 1

            f_score, _, current_node, path_cost, path = heapq.heappop(pq)

            # Update visualization: set current node
            self.current_node = current_node

            # Log current exploration
            if self.iterations % 5 == 0:  # Log every 5 iterations
                self.log_progress(f"Exploring {current_node.airport} on Day {current_node.day} | Path cost: ${path_cost:.2f}")

            # Check if we've reached the destination
            if current_node.airport == destination_airport:
                # Add this path to our list of all found paths
                all_paths.append(path)
                all_costs.append(path_cost)
                self.log_progress(f"PATH #{len(all_paths)} FOUND to {destination_airport} | Cost: ${path_cost:.2f}")

                # Track best cost for logging purposes
                if path_cost < best_cost:
                    best_cost = path_cost

                if self.stop_after_first_path:
                    break

                continue

            # Skip if already visited
            if current_node in visited:
                continue

            visited.add(current_node)
            # Update visualization: mark as explored
            self.explored_nodes.add(current_node)

            # Expand node - get available destinations
            available_dests = self.api.get_available_destinations(current_node)
            if self.iterations % 10 == 0:  # Log less frequently
                self.log_progress(f"Checking {len(available_dests)} destinations from {current_node.airport}")

            # Batch collect all routes we want to check for this node
            routes_to_check = []
            route_info = {}  # Map route to (next_node, is_next_day)

            for dest_airport in available_dests:
                # Check day limit
                if current_node.day >= self.max_days:
                    continue

                # Skip direct flight from source to destination if force_indirect is enabled
                if self.force_indirect and current_node.airport == source.airport and dest_airport == destination_airport:
                    continue

                # Same-day flight
                next_node = Node(dest_airport, current_node.day)
                if next_node not in visited and self.api_call_count < self.max_api_calls:
                    routes_to_check.append((current_node, next_node))
                    route_info[(current_node, next_node)] = (next_node, False)
                    self.api_call_count += 1

                # Next-day flight (with overnight stay)
                if current_node.day + 1 <= self.max_days:
                    next_day_node = Node(dest_airport, current_node.day + 1)
                    if next_day_node not in visited and self.api_call_count < self.max_api_calls:
                        routes_to_check.append((current_node, next_day_node))
                        route_info[(current_node, next_day_node)] = (next_day_node, True)
                        self.api_call_count += 1

            # Batch fetch all routes in parallel
            if routes_to_check:
                # Mark edges as "checking" before API calls
                for route in routes_to_check:
                    source_node, target_node = route
                    edge_data = {"source": source_node, "target": target_node, "cost": 0, "state": "checking"}
                    self.discovered_edges.append(edge_data.copy())

                # Update visualization to show what we're checking
                self.update_visualization_state()

                self.log_progress(f"⚡ Batch fetching {len(routes_to_check)} routes (max 10 concurrent API calls)...")
                flight_costs = await self.api.batch_get_flight_costs(routes_to_check, max_concurrent=10)

                # Process results
                new_edges_added = 0
                for route, (cost, found, url) in flight_costs.items():
                    if not found or cost is None:
                        continue

                    source_node, target_node = route
                    next_node, is_next_day = route_info[route]

                    # Add stay cost for overnight connections
                    total_cost = cost + (self.stay_cost if is_next_day else 0)

                    edge = Edge(
                        source=source_node,
                        target=target_node,
                        cost=total_cost,
                        is_flight=True,
                        is_estimated=False,
                        certainty=1.0,
                        url=url
                    )
                    self.graph.add_edge(edge)

                    # Track edge as found (replace "checking" state)
                    edge_data = {"source": source_node, "target": target_node, "cost": total_cost, "state": "found"}
                    self.discovered_edges.append(edge_data.copy())
                    new_edges_added += 1

                    new_path_cost = path_cost + total_cost
                    new_f_score = new_path_cost + self.heuristic_function(target_node, destination_airport)

                    counter += 1
                    heapq.heappush(pq, (new_f_score, counter, target_node, new_path_cost, path + [target_node]))

                # Update frontier nodes (nodes in priority queue)
                self.frontier_nodes = {item[2] for item in pq}

                # Update visualization after processing batch
                self.update_visualization_state()

                # Delay for visualization (250ms default)
                if self.visualization_delay > 0 and new_edges_added > 0:
                    await asyncio.sleep(self.visualization_delay)

        self.log_progress(f"SEARCH COMPLETE | Iterations: {self.iterations} | API Calls: {self.api_call_count}")

        if all_paths:
            # Sort paths by cost (cheapest first)
            sorted_indices = sorted(range(len(all_costs)), key=lambda i: all_costs[i])
            sorted_paths = [all_paths[i] for i in sorted_indices]
            sorted_costs = [all_costs[i] for i in sorted_indices]

            self.log_progress(f"SUCCESS | Found {len(all_paths)} paths | Cheapest: ${sorted_costs[0]:.2f} | Most expensive: ${sorted_costs[-1]:.2f}")
            return sorted_paths, sorted_costs
        else:
            self.log_progress(f"NO PATH FOUND | Tried {self.iterations} iterations, {self.api_call_count} API calls")
            return [], []


def run_search_async(search_id: str, source_airport: str, dest_airport: str, start_day: int, max_days: int, max_api_calls: int = 200, max_iterations: int = 1000, stay_cost: float = 100.0, force_indirect: bool = False):
    """Run search in background thread."""
    try:
        search_state[search_id] = {
            "status": "running",
            "progress": 0,
            "result": {
                "log": []
            },
            "error": None
        }

        # Initialize components
        graph = FlightGraph()
        api = SerpFlightAPI()
        pathfinder = PathFinder(
            graph=graph,
            api=api,
            heuristic_function=default_heuristic,
            max_days=max_days,
            max_iterations=max_iterations,
            max_api_calls=max_api_calls,
            stay_cost=stay_cost,
            stop_after_first_path=False,  # Keep searching for cheaper paths until API limit
            search_id=search_id,  # Pass search_id for live updates
            force_indirect=force_indirect  # Force indirect routes only
        )

        # Create source node
        source_node = Node(source_airport, start_day)

        # Find paths (run async function in event loop)
        all_paths, all_costs = asyncio.run(pathfinder.find_path(source_node, dest_airport))

        # Calculate API cost
        api_cost = pathfinder.api_call_count * SERP_API_COST_PER_REQUEST

        # Format all paths for JSON response
        formatted_paths = []
        for path, cost in zip(all_paths, all_costs):
            formatted_paths.append({
                "path": [n.to_dict() for n in path],
                "cost": cost,
                "num_stops": len(path) - 1,
                "days": path[-1].day - path[0].day if path else 0
            })

        search_state[search_id] = {
            "status": "completed",
            "progress": 100,
            "result": {
                "paths": formatted_paths,  # All paths found, sorted by cost
                "num_paths": len(formatted_paths),
                "iterations": pathfinder.iterations,
                "api_calls": pathfinder.api_call_count,
                "api_cost": api_cost,
                "graph": graph.to_dict(),
                "log": pathfinder.search_log
            },
            "error": None
        }

    except Exception as e:
        logger.error(f"Search error: {e}")
        search_state[search_id] = {
            "status": "error",
            "progress": 0,
            "result": None,
            "error": str(e)
        }


@bp.route('/airports')
def get_airports():
    """Get list of available airports."""
    airports_list = load_airports()
    return jsonify({
        "airports": airports_list,
        "is_default": airports_list == DEFAULT_AIRPORTS
    })


@bp.route('/airport-coords')
def get_airport_coords():
    """Get airport coordinates for visualization."""
    return jsonify({
        "coordinates": {code: {"lat": lat, "lon": lon} for code, (lat, lon) in AIRPORT_COORDS.items()}
    })


@bp.route('/search', methods=['POST'])
def search_flights():
    """Start a flight path search."""
    data = request.json

    source_airport = data.get('source', '').upper()
    dest_airport = data.get('destination', '').upper()
    start_day = int(data.get('start_day', 0))
    max_days = int(data.get('max_days', 7))
    max_api_calls = int(data.get('max_api_calls', 200))
    max_iterations = int(data.get('max_iterations', 1000))
    stay_cost = float(data.get('stay_cost', 100.0))
    force_indirect = bool(data.get('force_indirect', False))

    # Validate inputs
    if not source_airport or not dest_airport:
        return jsonify({"error": "Source and destination required"}), 400

    # Load current airports for validation
    current_airports = load_airports()
    if source_airport not in current_airports or dest_airport not in current_airports:
        return jsonify({"error": "Invalid airport code"}), 400

    # Create search ID
    search_id = str(uuid.uuid4())

    # Start search in background
    thread = threading.Thread(
        target=run_search_async,
        args=(search_id, source_airport, dest_airport, start_day, max_days, max_api_calls, max_iterations, stay_cost, force_indirect)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "search_id": search_id,
        "status": "started"
    })


@bp.route('/status/<search_id>')
def get_search_status(search_id):
    """Get status of a search."""
    if search_id not in search_state:
        return jsonify({"error": "Search not found"}), 404

    return jsonify(search_state[search_id])


@bp.route('/airports/add', methods=['POST'])
def add_airport():
    """Add a new airport to the list."""
    data = request.json
    airport_code = data.get('airport_code', '').upper().strip()

    if not airport_code:
        return jsonify({"error": "Airport code required"}), 400

    if len(airport_code) != 3:
        return jsonify({"error": "Airport code must be 3 characters"}), 400

    # Load current airports
    airports_list = load_airports()

    if airport_code in airports_list:
        return jsonify({"error": "Airport already exists"}), 400

    # Add the airport
    airports_list.append(airport_code)

    # Save to file
    if save_airports(airports_list):
        return jsonify({
            "success": True,
            "message": f"Added airport {airport_code}",
            "airports": airports_list
        })
    else:
        return jsonify({"error": "Failed to save airports"}), 500


@bp.route('/airports/remove', methods=['POST'])
def remove_airport():
    """Remove an airport from the list."""
    data = request.json
    airport_code = data.get('airport_code', '').upper().strip()

    if not airport_code:
        return jsonify({"error": "Airport code required"}), 400

    # Load current airports
    airports_list = load_airports()

    if airport_code not in airports_list:
        return jsonify({"error": "Airport not found"}), 404

    # Remove the airport
    airports_list.remove(airport_code)

    # Save to file
    if save_airports(airports_list):
        return jsonify({
            "success": True,
            "message": f"Removed airport {airport_code}",
            "airports": airports_list
        })
    else:
        return jsonify({"error": "Failed to save airports"}), 500


@bp.route('/airports/reset', methods=['POST'])
def reset_airports():
    """Reset airports to default list."""
    if save_airports(DEFAULT_AIRPORTS.copy()):
        return jsonify({
            "success": True,
            "message": "Reset to default airports",
            "airports": DEFAULT_AIRPORTS
        })
    else:
        return jsonify({"error": "Failed to reset airports"}), 500
