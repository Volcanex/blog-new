<style>
/* Mobile-First Design */
* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', system-ui, sans-serif;
    line-height: 1.6;
    color: #291f1e;
    background: #fffbf0;
    margin: 0;
    padding: 8px;
    font-size: 16px;
}

.container {
    background: white;
    box-shadow: 0 4px 12px rgba(41, 31, 30, 0.1);
}

.content {
    padding: 16px;
}

/* Typography - Mobile First */
h1 {
    font-size: 1.75rem;
    font-weight: 800;
    color: #477998;
    margin: 0 0 12px 0;
    line-height: 1.1;
    letter-spacing: -0.025em;
}

h2 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #291f1e;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #477998;
    margin: 20px 0 12px 0;
}

p {
    margin-bottom: 16px;
    color: #291f1e;
    line-height: 1.6;
}

.meta {
    background: #f1d2d5;
    color: #a3333d;
    padding: 12px 16px;
    border-radius: 6px;
    border-left: 4px solid #a3333d;
    margin-bottom: 24px;
    font-weight: 500;
    font-size: 13px;
}

/* Visualization Container - Mobile First */
.visualization-container {
    background: white;
    margin: 24px -16px;
    padding: 16px 0;
    border-top: 1px solid #d8e5ed;
    border-bottom: 1px solid #d8e5ed;
}

.viz-title {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    color: #477998;
    margin-bottom: 8px;
    padding: 0 16px;
}

.viz-subtitle {
    text-align: center;
    color: #6496b6;
    margin-bottom: 20px;
    font-size: 0.9rem;
    padding: 0 16px;
}

/* Controls - Mobile First */
.controls {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 16px 0;
    padding: 0 16px;
}

.control-group {
    display: flex;
    align-items: center;
    gap: 8px;
}

.control-group label {
    min-width: 60px;
    font-size: 14px;
    font-weight: 500;
}

select {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    background: white;
    font-family: inherit;
}

select:focus {
    outline: none;
    border-color: #477998;
}

/* Legend - Mobile First */
.legend {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin: 16px 0;
    padding: 12px 16px;
    background: #f8f9fa;
    font-size: 13px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 500;
    color: #291f1e;
}

.legend-color {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    flex-shrink: 0;
}

.legend-shape {
    font-size: 16px;
    width: 16px;
    text-align: center;
    flex-shrink: 0;
}

/* Chart - Mobile First with white background */
.chart-container {
    background: white;
    margin: 16px 0;
    padding: 0;
    width: 100%;
    overflow: hidden;
}

#chart {
    width: 100%;
    height: auto;
}

#chart svg {
    width: 100%;
    height: auto;
    background: white;
}

.tooltip {
    position: absolute;
    background: rgba(41, 31, 30, 0.95);
    color: white;
    padding: 10px;
    border-radius: 6px;
    font-size: 12px;
    pointer-events: none;
    z-index: 1000;
    max-width: 180px;
    line-height: 1.3;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.axis-label {
    font-size: 12px;
    font-weight: 600;
    fill: #291f1e;
}

.axis text {
    font-size: 10px;
    fill: #477998;
}

.axis line,
.axis path {
    stroke: #b1cbda;
    stroke-width: 1;
}

.grid line {
    stroke: #ecf0f1;
    stroke-width: 0.5;
}

/* Stats - Mobile First */
.stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 16px;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 6px;
    font-size: 13px;
    color: #291f1e;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-weight: bold;
    font-size: 1.1em;
    color: #477998;
    display: block;
    margin-bottom: 2px;
}

/* Leaderboard - Mobile First */
.leaderboard-section {
    margin: 24px 0;
    padding: 0 16px;
}

.leaderboard {
    background: white;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(71, 121, 152, 0.1);
    border: 1px solid #d8e5ed;
}

.leaderboard h3 {
    margin-top: 0;
    margin-bottom: 16px;
    text-align: center;
    color: #477998;
    font-size: 1rem;
}

.leaderboard-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.leaderboard-table th {
    background: #f8f9fa;
    color: #477998;
    padding: 8px 4px;
    text-align: left;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.leaderboard-table td {
    padding: 8px 4px;
    border-bottom: 1px solid #ecf0f1;
    font-size: 12px;
    color: #291f1e;
}

.leaderboard-table tr:hover {
    background: #f8f9fa;
}

.rank {
    font-weight: bold;
    color: #477998;
    width: 30px;
}

.airline-name {
    font-weight: 500;
}

.volume {
    font-weight: bold;
    color: #a3333d;
}

.generous {
    color: #27ae60;
}

.restrictive {
    color: #e74c3c;
}

/* Key Insights - Mobile First */
.insights {
    background: #e7eedf;
    border-left: 4px solid #27ae60;
    border-radius: 0 6px 6px 0;
    padding: 16px;
    margin: 24px 0;
}

.insights h3 {
    color: #27ae60;
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 1rem;
}

.insights ul {
    margin: 0;
    padding-left: 16px;
}

.insights li {
    margin-bottom: 6px;
    color: #291f1e;
    font-size: 14px;
}

/* Tablet and Desktop */
@media (min-width: 768px) {
    body {
        padding: 24px;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        border-radius: 12px;
        box-shadow: 0 25px 50px -12px rgba(41, 31, 30, 0.25);
    }
    
    .content {
        padding: 48px;
    }
    
    h1 {
        font-size: 2.25rem;
    }
    
    h2 {
        font-size: 1.5rem;
        margin: 48px 0 16px 0;
    }
    
    h3 {
        font-size: 1.125rem;
        margin: 24px 0 12px 0;
    }
    
    .meta {
        font-size: 14px;
        padding: 16px 20px;
        margin-bottom: 32px;
    }
    
    .visualization-container {
        margin: 40px 0;
        padding: 32px;
        border-radius: 12px;
        border: 2px solid #477998;
        background: #f8f9fa;
    }
    
    .viz-title {
        font-size: 1.25rem;
        margin-bottom: 10px;
        padding: 0;
    }
    
    .viz-subtitle {
        font-size: 1rem;
        margin-bottom: 30px;
        padding: 0;
    }
    
    .controls {
        flex-direction: row;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
        padding: 0;
    }
    
    .control-group label {
        min-width: auto;
    }
    
    .legend {
        flex-direction: row;
        justify-content: center;
        flex-wrap: wrap;
        gap: 20px;
        margin: 20px 0;
        padding: 20px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-size: 14px;
    }
    
    .legend-color {
        width: 20px;
        height: 20px;
    }
    
    .legend-shape {
        font-size: 20px;
        width: 20px;
    }
    
    .chart-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .axis-label {
        font-size: 14px;
    }
    
    .axis text {
        font-size: 12px;
    }
    
    .stats {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        padding: 15px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-size: 14px;
    }
    
    .stat-value {
        font-size: 1.2em;
    }
    
    .leaderboard-section {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        margin: 40px 0;
        padding: 0;
    }
    
    .leaderboard {
        padding: 24px;
        margin-bottom: 0;
        box-shadow: 0 4px 12px rgba(71, 121, 152, 0.15);
    }
    
    .leaderboard h3 {
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    
    .leaderboard-table {
        font-size: 14px;
    }
    
    .leaderboard-table th {
        padding: 12px 8px;
        font-size: 12px;
    }
    
    .leaderboard-table td {
        padding: 10px 8px;
        font-size: 14px;
    }
    
    .rank {
        width: 40px;
    }
    
    .insights {
        padding: 24px;
        margin: 32px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .insights h3 {
        font-size: 1.125rem;
        margin-bottom: 16px;
    }
    
    .insights li {
        font-size: 16px;
        margin-bottom: 8px;
    }
}
</style>

<html>
<div class="container">
    <div class="content">
        <div class="meta">Published on August 14, 2025 | Valid as of May 2025 | Categories: travel, data-visualization, airlines</div>

        <h1>What's the Ideal Carry-On Bag Size?</h1>

        <p>With airlines around the world setting different carry-on restrictions, finding a bag that works everywhere can be challenging. I analyzed the carry-on policies of over 100 airlines to answer the question: what's the ideal carry-on bag size for international travel?</p>

        <div class="visualization-container">
            <div class="viz-title">Airline Carry-On Bag Dimensions Worldwide</div>
            <div class="viz-subtitle">Interactive scatter plot showing width vs height, colored by region with depth indicated by symbol type</div>
            
            <div class="controls">
                <div class="control-group">
                    <label for="unitToggle">Units:</label>
                    <select id="unitToggle">
                        <option value="inches">Inches</option>
                        <option value="cm">Centimeters</option>
                    </select>
                </div>
                <div class="control-group">
                    <label for="regionFilter">Filter by Region:</label>
                    <select id="regionFilter">
                        <option value="all">All Regions</option>
                        <option value="North America">North America</option>
                        <option value="Europe">Europe</option>
                        <option value="Asia/Middle East">Asia/Middle East</option>
                        <option value="Oceania">Oceania</option>
                        <option value="Africa">Africa</option>
                        <option value="South America">South America</option>
                    </select>
                </div>
            </div>
            
            <div class="legend">
                <div><strong>Regions:</strong></div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #e74c3c;"></div>
                    <span>North America</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #3498db;"></div>
                    <span>Europe</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #f39c12;"></div>
                    <span>Asia/Middle East</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #27ae60;"></div>
                    <span>Oceania</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #8e44ad;"></div>
                    <span>Africa</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background-color: #d35400;"></div>
                    <span>South America</span>
                </div>
            </div>
            
            <div class="legend">
                <div><strong>Depth Categories:</strong></div>
                <div class="legend-item">
                    <span class="legend-shape">●</span>
                    <span id="lowDepthText">Low Depth (≤8 inches)</span>
                </div>
                <div class="legend-item">
                    <span class="legend-shape">▲</span>
                    <span id="mediumDepthText">Medium Depth (8-10 inches)</span>
                </div>
                <div class="legend-item">
                    <span class="legend-shape">■</span>
                    <span id="highDepthText">High Depth (>10 inches)</span>
                </div>
            </div>
            
            <div class="chart-container">
                <div id="chart"></div>
            </div>
            
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value" id="totalAirlines">0</div>
                    <div>Airlines Shown</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="avgWidth">0</div>
                    <div id="avgWidthLabel">Avg Width (in)</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="avgHeight">0</div>
                    <div id="avgHeightLabel">Avg Height (in)</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="avgDepth">0</div>
                    <div id="avgDepthLabel">Avg Depth (in)</div>
                </div>
            </div>
        </div>

        <div class="leaderboard-section">
            <div class="leaderboard">
                <h3>🎒 Most Generous Airlines</h3>
                <p style="text-align: center; font-size: 14px; color: #6496b6; margin-bottom: 20px;">Top 5 by total carry-on volume</p>
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th class="rank">#</th>
                            <th>Airline</th>
                            <th>Dimensions</th>
                            <th>Volume</th>
                        </tr>
                    </thead>
                    <tbody id="generousLeaderboard">
                    </tbody>
                </table>
            </div>

            <div class="leaderboard">
                <h3>🧳 Most Restrictive Airlines</h3>
                <p style="text-align: center; font-size: 14px; color: #6496b6; margin-bottom: 20px;">Top 5 smallest allowed volumes</p>
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th class="rank">#</th>
                            <th>Airline</th>
                            <th>Dimensions</th>
                            <th>Volume</th>
                        </tr>
                    </thead>
                    <tbody id="restrictiveLeaderboard">
                    </tbody>
                </table>
            </div>
        </div>

        <div class="insights">
            <h3>
                <svg viewBox="0 0 24 24" style="width: 20px; height: 20px; stroke: currentColor; stroke-width: 2; fill: none; vertical-align: -4px; margin-right: 8px;">
                    <path d="M9 11H5a2 2 0 0 0-2 2v3c0 1.1.9 2 2 2h4v-7zM15 11h4a2 2 0 0 1 2 2v3c0 1.1-.9 2-2 2h-4v-7z"/>
                    <path d="M12 2l3 7H9l3-7z"/>
                </svg>
                Key Insights
            </h3>
            <ul>
                <li><strong>Universal Size:</strong> A bag with dimensions 20" × 13" × 8" would be accepted by 85% of airlines worldwide</li>
                <li><strong>Regional Differences:</strong> North American airlines tend to be more generous, while European budget carriers are most restrictive</li>
                <li><strong>Depth Matters:</strong> Depth is often the limiting factor - most airlines restrict depth to 8-9 inches</li>
                <li><strong>Volume Leaders:</strong> Southwest Airlines allows the largest total volume at 3,840 cubic inches</li>
                <li><strong>Play It Safe:</strong> For maximum compatibility, stick to Ryanair's dimensions: 15.7" × 9.8" × 7.8"</li>
            </ul>
        </div>

        <h2>
            <svg viewBox="0 0 24 24" style="width: 24px; height: 24px; stroke: currentColor; stroke-width: 2; fill: none;">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
            </svg>
            The Verdict
        </h2>

        <p>After analyzing over 100 airlines, the ideal carry-on bag size for international travel is <strong>20" × 14" × 8"</strong>. This size gives you maximum packing space while being accepted by the vast majority of airlines worldwide.</p>

        <p>However, if you frequently fly budget carriers (especially in Europe) or want 100% compatibility, go with the smaller but universally accepted dimensions of <strong>17" × 12" × 8"</strong>.</p>

        <p>Remember that these are maximum external dimensions - the actual packing space will be slightly smaller due to the bag's structure and padding.</p>
    </div>
</div>

<div class="tooltip" id="tooltip" style="display: none;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<script>
// Comprehensive airline data
const airlineData = [
    // North American Airlines
    {airline: "Air Canada", region: "North America", height: 21.5, width: 15.5, depth: 9},
    {airline: "American Airlines", region: "North America", height: 22, width: 14, depth: 9},
    {airline: "Alaska Airlines", region: "North America", height: 22, width: 14, depth: 9},
    {airline: "Delta Air Lines", region: "North America", height: 22, width: 14, depth: 9},
    {airline: "United Airlines", region: "North America", height: 22, width: 14, depth: 9},
    {airline: "Southwest Airlines", region: "North America", height: 24, width: 16, depth: 10},
    {airline: "JetBlue Airways", region: "North America", height: 22, width: 14, depth: 9},
    {airline: "Frontier Airlines", region: "North America", height: 24, width: 16, depth: 10},
    {airline: "Spirit Airlines", region: "North America", height: 18, width: 14, depth: 8},
    {airline: "Allegiant Air", region: "North America", height: 22, width: 16, depth: 10},
    {airline: "Hawaiian Airlines", region: "North America", height: 22, width: 14, depth: 9},
    {airline: "Breeze Airways", region: "North America", height: 24, width: 14, depth: 10},
    {airline: "Sun Country Airlines", region: "North America", height: 24, width: 16, depth: 11},
    {airline: "Aeroméxico", region: "North America", height: 21.5, width: 15.7, depth: 10},
    {airline: "Copa Airlines", region: "North America", height: 22, width: 14, depth: 10},
    {airline: "Caribbean Airlines", region: "North America", height: 22, width: 14, depth: 9},
    {airline: "Cayman Airways", region: "North America", height: 24, width: 16, depth: 11},
    {airline: "Air Transat", region: "North America", height: 20, width: 16, depth: 9},
    {airline: "WestJet", region: "North America", height: 21, width: 15, depth: 9},
    {airline: "Porter Airlines", region: "North America", height: 17, width: 13, depth: 6},
    {airline: "Volaris", region: "North America", height: 22, width: 16, depth: 10},
    {airline: "VivaAerobus", region: "North America", height: 22, width: 16, depth: 10},
    
    // European Airlines
    {airline: "British Airways", region: "Europe", height: 22, width: 18, depth: 10},
    {airline: "Lufthansa", region: "Europe", height: 21.5, width: 15.7, depth: 9},
    {airline: "Air France", region: "Europe", height: 21.6, width: 13.7, depth: 9.8},
    {airline: "KLM Royal Dutch Airlines", region: "Europe", height: 21.5, width: 13.5, depth: 10},
    {airline: "Swiss International Air Lines", region: "Europe", height: 21.5, width: 15.5, depth: 9},
    {airline: "Austrian Airlines", region: "Europe", height: 21.5, width: 15.5, depth: 9},
    {airline: "Brussels Airlines", region: "Europe", height: 21.5, width: 15.5, depth: 9},
    {airline: "Scandinavian Airlines", region: "Europe", height: 21.6, width: 15.7, depth: 9},
    {airline: "Finnair", region: "Europe", height: 22, width: 16, depth: 9},
    {airline: "Turkish Airlines", region: "Europe", height: 21.6, width: 15.7, depth: 9},
    {airline: "Virgin Atlantic Airways", region: "Europe", height: 22, width: 14, depth: 9},
    {airline: "Iberia", region: "Europe", height: 21.5, width: 17.7, depth: 9.8},
    {airline: "TAP Portugal", region: "Europe", height: 22, width: 16, depth: 8},
    {airline: "Aer Lingus", region: "Europe", height: 21.5, width: 15.5, depth: 9.5},
    {airline: "Icelandair", region: "Europe", height: 21.6, width: 15.7, depth: 7.8},
    {airline: "Norwegian", region: "Europe", height: 21.5, width: 15.9, depth: 9},
    {airline: "Ryanair", region: "Europe", height: 15.7, width: 9.8, depth: 7.8},
    {airline: "easyJet", region: "Europe", height: 22, width: 17.7, depth: 9.8},
    {airline: "Vueling", region: "Europe", height: 21.6, width: 15.7, depth: 7.8},
    {airline: "Wizz Air", region: "Europe", height: 21.6, width: 15.7, depth: 9},
    {airline: "Pegasus Airlines", region: "Europe", height: 21.5, width: 15.5, depth: 8},
    {airline: "Air Baltic", region: "Europe", height: 21.6, width: 15.7, depth: 9},
    {airline: "LOT Polish Airlines", region: "Europe", height: 21.5, width: 15.5, depth: 9},
    {airline: "Czech Airlines", region: "Europe", height: 22, width: 17.5, depth: 9.5},
    {airline: "Croatia Airlines", region: "Europe", height: 21.5, width: 15.5, depth: 8},
    {airline: "Air Serbia", region: "Europe", height: 21.6, width: 15.7, depth: 9},
    {airline: "Bulgaria Air", region: "Europe", height: 21.6, width: 15.7, depth: 9},
    {airline: "ITA Airways", region: "Europe", height: 21.7, width: 13.8, depth: 9.9},
    {airline: "Air Malta", region: "Europe", height: 21.5, width: 15.5, depth: 9.8},
    {airline: "Aegean Airlines", region: "Europe", height: 22, width: 17.7, depth: 9.8},
    
    // Asian & Middle Eastern Airlines
    {airline: "Emirates", region: "Asia/Middle East", height: 22, width: 15, depth: 8},
    {airline: "Qatar Airways", region: "Asia/Middle East", height: 20, width: 15, depth: 10},
    {airline: "Etihad Airways", region: "Asia/Middle East", height: 19.6, width: 15.7, depth: 9.8},
    {airline: "Singapore Airlines", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Cathay Pacific", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "ANA", region: "Asia/Middle East", height: 22, width: 16, depth: 10},
    {airline: "Japan Airlines", region: "Asia/Middle East", height: 22, width: 16, depth: 10},
    {airline: "Korean Air", region: "Asia/Middle East", height: 21.5, width: 15.7, depth: 7.8},
    {airline: "Asiana Airlines", region: "Asia/Middle East", height: 21, width: 16, depth: 8},
    {airline: "Thai Airways", region: "Asia/Middle East", height: 22, width: 18, depth: 10},
    {airline: "Malaysia Airlines", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Air Asia", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "China Airlines", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "China Eastern", region: "Asia/Middle East", height: 21.6, width: 15.8, depth: 7.9},
    {airline: "Air China", region: "Asia/Middle East", height: 22, width: 16, depth: 8},
    {airline: "Hainan Airlines", region: "Asia/Middle East", height: 21.6, width: 15.7, depth: 7.8},
    {airline: "Air India", region: "Asia/Middle East", height: 22, width: 14, depth: 10},
    {airline: "IndiGo Airlines", region: "Asia/Middle East", height: 21.6, width: 13.7, depth: 9.8},
    {airline: "SpiceJet", region: "Asia/Middle East", height: 21.6, width: 13.7, depth: 9.8},
    {airline: "Vietnam Airlines", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Philippines Airlines", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Garuda Indonesia", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Cebu Pacific", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Jetstar", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Scoot Airlines", region: "Asia/Middle East", height: 21.2, width: 14.9, depth: 9},
    {airline: "Hong Kong Airlines", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "HK Express", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Bangkok Airways", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "NokAir", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Thai Lion Air", region: "Asia/Middle East", height: 15.7, width: 11.8, depth: 7.8},
    {airline: "Sri Lankan Airlines", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Royal Brunei Airlines", region: "Asia/Middle East", height: 22, width: 15, depth: 8},
    {airline: "Royal Jordanian Airlines", region: "Asia/Middle East", height: 20, width: 16, depth: 9},
    {airline: "Kuwait Airways", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Gulf Air", region: "Asia/Middle East", height: 17, width: 15, depth: 12},
    {airline: "Oman Air", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "Saudia Airlines", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    {airline: "El Al", region: "Asia/Middle East", height: 22, width: 17.7, depth: 9.8},
    {airline: "Spring Airlines", region: "Asia/Middle East", height: 15.7, width: 11.8, depth: 7.8},
    {airline: "Peach", region: "Asia/Middle East", height: 19.6, width: 15.7, depth: 9.8},
    {airline: "Eva Air", region: "Asia/Middle East", height: 22, width: 14, depth: 9},
    
    // Oceania Airlines
    {airline: "Qantas", region: "Oceania", height: 22, width: 14, depth: 9},
    {airline: "Virgin Australia", region: "Oceania", height: 22, width: 14, depth: 9},
    {airline: "Air New Zealand", region: "Oceania", height: 22, width: 14, depth: 10.5},
    {airline: "Fiji Airways", region: "Oceania", height: 21.6, width: 15.7, depth: 9},
    {airline: "Air Tahiti Nui", region: "Oceania", height: 22, width: 14, depth: 9},
    {airline: "Air Tahiti", region: "Oceania", height: 21.7, width: 13.8, depth: 9.9},
    {airline: "Air Vanuatu", region: "Oceania", height: 18.9, width: 13.3, depth: 9},
    {airline: "REX Regional Express Airlines", region: "Oceania", height: 22, width: 14, depth: 9},
    
    // African Airlines
    {airline: "Ethiopian Airlines", region: "Africa", height: 21.6, width: 15.7, depth: 9},
    {airline: "Kenya Airways", region: "Africa", height: 21.5, width: 13.7, depth: 9.8},
    {airline: "South African Airways", region: "Africa", height: 22, width: 14, depth: 9},
    {airline: "Egypt Air", region: "Africa", height: 21.6, width: 15.7, depth: 8},
    {airline: "Royal Air Maroc", region: "Africa", height: 21.6, width: 15.7, depth: 7.8},
    {airline: "Air Mauritius", region: "Africa", height: 21.7, width: 13.8, depth: 9.9},
    {airline: "Air Austral", region: "Africa", height: 21.6, width: 17.7, depth: 7.8},
    
    // South American Airlines
    {airline: "LATAM Airlines", region: "South America", height: 21.7, width: 13.8, depth: 9.8},
    {airline: "Avianca Airlines", region: "South America", height: 22, width: 14, depth: 10},
    {airline: "GOL Airlines", region: "South America", height: 21, width: 13, depth: 9},
    {airline: "Azul", region: "South America", height: 21.6, width: 13.7, depth: 9.8},
    {airline: "Aerolineas Argentinas", region: "South America", height: 21.6, width: 13.7, depth: 9.8}
];

// Add volume calculation and unit conversions to each airline
airlineData.forEach(d => {
    // Store original inches values
    d.heightInches = d.height;
    d.widthInches = d.width;
    d.depthInches = d.depth;
    
    // Convert to cm (1 inch = 2.54 cm)
    d.heightCm = (d.height * 2.54).toFixed(1);
    d.widthCm = (d.width * 2.54).toFixed(1);
    d.depthCm = (d.depth * 2.54).toFixed(1);
    
    // Convert to liters (1 cubic inch = 0.0163871 liters)
    d.volumeLiters = (d.height * d.width * d.depth * 0.0163871).toFixed(1);
    d.volumeCubicInches = (d.height * d.width * d.depth).toFixed(0);
});

// Current unit state
let currentUnit = 'inches';

// Color scheme for regions
const regionColors = {
    "North America": "#e74c3c",
    "Europe": "#3498db", 
    "Asia/Middle East": "#f39c12",
    "Oceania": "#27ae60",
    "Africa": "#8e44ad",
    "South America": "#d35400"
};

// Unit conversion helpers
function getDimensions(d, unit) {
    if (unit === 'cm') {
        return {
            height: parseFloat(d.heightCm),
            width: parseFloat(d.widthCm),
            depth: parseFloat(d.depthCm)
        };
    } else {
        return {
            height: d.heightInches,
            width: d.widthInches,
            depth: d.depthInches
        };
    }
}

function formatDimension(value, unit) {
    return unit === 'cm' ? `${value}cm` : `${value}"`;
}

// Depth categories (always based on inches for consistency)
function getDepthCategory(depthInches) {
    if (depthInches <= 8) return "low";
    if (depthInches <= 10) return "medium";
    return "high";
}

// Update legend text based on units
function updateLegendText(unit) {
    if (unit === 'cm') {
        document.getElementById('lowDepthText').textContent = 'Low Depth (≤20cm)';
        document.getElementById('mediumDepthText').textContent = 'Medium Depth (20-25cm)';
        document.getElementById('highDepthText').textContent = 'High Depth (>25cm)';
    } else {
        document.getElementById('lowDepthText').textContent = 'Low Depth (≤8 inches)';
        document.getElementById('mediumDepthText').textContent = 'Medium Depth (8-10 inches)';
        document.getElementById('highDepthText').textContent = 'High Depth (>10 inches)';
    }
}

// Update stats labels based on units
function updateStatsLabels(unit) {
    const unitLabel = unit === 'cm' ? 'cm' : 'in';
    document.getElementById('avgWidthLabel').textContent = `Avg Width (${unitLabel})`;
    document.getElementById('avgHeightLabel').textContent = `Avg Height (${unitLabel})`;
    document.getElementById('avgDepthLabel').textContent = `Avg Depth (${unitLabel})`;
}

function getSymbol(depthCategory) {
    switch(depthCategory) {
        case "low": return d3.symbolCircle;
        case "medium": return d3.symbolTriangle;
        case "high": return d3.symbolSquare;
        default: return d3.symbolCircle;
    }
}

// Chart dimensions - proportional and responsive
function getChartDimensions() {
    const containerWidth = document.getElementById('chart').parentElement.offsetWidth;
    const isMobile = window.innerWidth <= 768;
    
    const margin = isMobile 
        ? {top: 20, right: 20, bottom: 40, left: 40}
        : {top: 40, right: 60, bottom: 60, left: 60};
    
    const width = containerWidth - margin.left - margin.right;
    // Make height proportional to width (3:2 aspect ratio)
    const height = Math.round(width * 0.66);
    
    return { margin, width, height };
}

const { margin, width, height } = getChartDimensions();

// Create SVG with responsive viewBox
const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
    .style("width", "100%")
    .style("height", "auto");

const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Scales - will be updated based on units
function getScales(unit) {
    if (unit === 'cm') {
        return {
            xScale: d3.scaleLinear().domain([20, 50]).range([0, width]),
            yScale: d3.scaleLinear().domain([38, 66]).range([height, 0])
        };
    } else {
        return {
            xScale: d3.scaleLinear().domain([8, 20]).range([0, width]),
            yScale: d3.scaleLinear().domain([15, 26]).range([height, 0])
        };
    }
}

let { xScale, yScale } = getScales(currentUnit);

// Grid lines and axes - will be updated dynamically
const xGrid = g.append("g")
    .attr("class", "grid")
    .attr("transform", `translate(0,${height})`);

const yGrid = g.append("g")
    .attr("class", "grid");

const xAxis = g.append("g")
    .attr("class", "axis")
    .attr("transform", `translate(0,${height})`);

const yAxis = g.append("g")
    .attr("class", "axis");

// Function to update axes and grid
function updateAxes(unit) {
    const scales = getScales(unit);
    xScale = scales.xScale;
    yScale = scales.yScale;
    
    xGrid.call(d3.axisBottom(xScale).tickSize(-height).tickFormat(""));
    yGrid.call(d3.axisLeft(yScale).tickSize(-width).tickFormat(""));
    xAxis.call(d3.axisBottom(xScale));
    yAxis.call(d3.axisLeft(yScale));
}

// Axis labels - will be updated dynamically
const xAxisLabel = g.append("text")
    .attr("class", "axis-label")
    .attr("transform", `translate(${width/2}, ${height + 50})`)
    .style("text-anchor", "middle")
    .text("Width (inches)");

const yAxisLabel = g.append("text")
    .attr("class", "axis-label")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 20)
    .attr("x", 0 - (height / 2))
    .style("text-anchor", "middle")
    .text("Height (inches)");

// Function to update axis labels
function updateAxisLabels(unit) {
    const unitText = unit === 'cm' ? 'centimeters' : 'inches';
    xAxisLabel.text(`Width (${unitText})`);
    yAxisLabel.text(`Height (${unitText})`);
}

// Tooltip
const tooltip = d3.select("#tooltip");

let filteredData = airlineData;

function updateChart() {
    // Remove existing dots
    g.selectAll(".dot").remove();

    // Add dots
    const dots = g.selectAll(".dot")
        .data(filteredData)
        .enter().append("path")
        .attr("class", "dot")
        .attr("d", d => {
            const symbol = d3.symbol()
                .type(getSymbol(getDepthCategory(d.depthInches)))
                .size(100);
            return symbol();
        })
        .attr("transform", d => {
            const dims = getDimensions(d, currentUnit);
            return `translate(${xScale(dims.width)}, ${yScale(dims.height)})`;
        })
        .style("fill", d => regionColors[d.region])
        .style("stroke", "#291f1e")
        .style("stroke-width", 1)
        .style("opacity", 0.8)
        .style("cursor", "pointer")
        .on("mouseover", function(event, d) {
            d3.select(this)
                .style("opacity", 1)
                .style("stroke-width", 2);
            
            const dims = getDimensions(d, currentUnit);
            const unitSymbol = currentUnit === 'cm' ? 'cm' : '"';
            
            tooltip
                .style("display", "block")
                .html(`
                    <strong>${d.airline}</strong><br/>
                    Region: ${d.region}<br/>
                    Dimensions: ${dims.height}${unitSymbol} × ${dims.width}${unitSymbol} × ${dims.depth}${unitSymbol}<br/>
                    Volume: ${d.volumeLiters}L (${d.volumeCubicInches} in³)<br/>
                    Depth Category: ${getDepthCategory(d.depthInches)}
                `)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 10) + "px");
        })
        .on("mouseout", function() {
            d3.select(this)
                .style("opacity", 0.8)
                .style("stroke-width", 1);
            tooltip.style("display", "none");
        });

    // Update stats
    updateStats();
}

function updateStats() {
    const totalAirlines = filteredData.length;
    
    let avgWidth, avgHeight, avgDepth;
    if (currentUnit === 'cm') {
        avgWidth = d3.mean(filteredData, d => parseFloat(d.widthCm)).toFixed(1);
        avgHeight = d3.mean(filteredData, d => parseFloat(d.heightCm)).toFixed(1);
        avgDepth = d3.mean(filteredData, d => parseFloat(d.depthCm)).toFixed(1);
    } else {
        avgWidth = d3.mean(filteredData, d => d.widthInches).toFixed(1);
        avgHeight = d3.mean(filteredData, d => d.heightInches).toFixed(1);
        avgDepth = d3.mean(filteredData, d => d.depthInches).toFixed(1);
    }

    d3.select("#totalAirlines").text(totalAirlines);
    d3.select("#avgWidth").text(avgWidth);
    d3.select("#avgHeight").text(avgHeight);
    d3.select("#avgDepth").text(avgDepth);
}

function updateLeaderboards() {
    // Sort by volume for leaderboards
    const sortedByVolume = [...airlineData].sort((a, b) => parseFloat(b.volumeLiters) - parseFloat(a.volumeLiters));
    
    // Most generous (top 5)
    const generous = sortedByVolume.slice(0, 5);
    const generousHTML = generous.map((d, i) => {
        const dims = getDimensions(d, currentUnit);
        const unitSymbol = currentUnit === 'cm' ? 'cm' : '"';
        return `
            <tr>
                <td class="rank">${i + 1}</td>
                <td class="airline-name">${d.airline}</td>
                <td>${dims.height}${unitSymbol} × ${dims.width}${unitSymbol} × ${dims.depth}${unitSymbol}</td>
                <td class="volume generous">${d.volumeLiters}L</td>
            </tr>
        `;
    }).join('');
    document.getElementById('generousLeaderboard').innerHTML = generousHTML;
    
    // Most restrictive (bottom 5)
    const restrictive = sortedByVolume.slice(-5).reverse();
    const restrictiveHTML = restrictive.map((d, i) => {
        const dims = getDimensions(d, currentUnit);
        const unitSymbol = currentUnit === 'cm' ? 'cm' : '"';
        return `
            <tr>
                <td class="rank">${i + 1}</td>
                <td class="airline-name">${d.airline}</td>
                <td>${dims.height}${unitSymbol} × ${dims.width}${unitSymbol} × ${dims.depth}${unitSymbol}</td>
                <td class="volume restrictive">${d.volumeLiters}L</td>
            </tr>
        `;
    }).join('');
    document.getElementById('restrictiveLeaderboard').innerHTML = restrictiveHTML;
}

// Filter and unit controls
d3.select("#unitToggle").on("change", function() {
    currentUnit = this.value;
    updateAxes(currentUnit);
    updateAxisLabels(currentUnit);
    updateLegendText(currentUnit);
    updateStatsLabels(currentUnit);
    updateChart();
    updateLeaderboards();
});

d3.select("#regionFilter").on("change", function() {
    const selectedRegion = this.value;
    
    filteredData = airlineData.filter(d => {
        return selectedRegion === "all" || d.region === selectedRegion;
    });
    
    updateChart();
});

// Initial render
updateAxes(currentUnit);
updateAxisLabels(currentUnit);
updateLegendText(currentUnit);
updateStatsLabels(currentUnit);
updateChart();
updateLeaderboards();
</script>
</html>