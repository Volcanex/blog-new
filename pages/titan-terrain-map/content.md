<link href="https://fonts.googleapis.com/css2?family=Cardo:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
    .titan-container {
        width: 100%;
        max-width: 1000px;
        margin: 0 auto;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: #2a2a28;
        line-height: 1.7;
    }
    .titan-container h1, .titan-container h2, .titan-container h3 {
        font-family: 'Cardo', Georgia, serif;
        font-weight: 400;
        color: #2a2a28;
    }
    .titan-container h1 { font-size: 2.2em; margin-bottom: 0.3em; font-style: italic; }
    .titan-container h2 { font-size: 1.5em; margin-top: 2em; margin-bottom: 0.5em; }
    .titan-container h3 { font-size: 1.2em; margin-top: 1.5em; margin-bottom: 0.4em; }
    .titan-container p {
        color: #5a5750;
        margin-bottom: 1em;
        font-size: 15px;
        font-weight: 400;
    }
    .titan-container a { color: #5a8bbe; text-decoration: none; }
    .titan-container a:hover { color: #4a7db0; text-decoration: underline; }
    .titan-container strong { color: #2a2a28; font-weight: 600; }
    .titan-container em { font-style: italic; }
    .subtitle {
        font-family: 'Cardo', Georgia, serif;
        font-style: italic;
        color: #5a5750;
        font-size: 17px;
        margin-bottom: 2em;
    }
    #titan-map {
        width: 100%;
        height: 70vh;
        min-height: 500px;
        background: #f5f2ed;
        border-radius: 6px;
        overflow: hidden;
        margin: 1em 0;
        cursor: grab;
        border: 1px solid #ddd8cf;
    }
    .map-controls {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin: 12px 0;
        align-items: center;
    }
    .map-controls button {
        background: #ffffff;
        color: #2a2a28;
        border: 1px solid #ddd8cf;
        padding: 6px 13px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 11px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.15s;
    }
    .map-controls button:hover { background: #ebe7e0; border-color: #5a8bbe; }
    .map-controls button.active {
        background: #5a8bbe;
        color: #fff;
        border-color: #4a7db0;
    }
    .legend {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        margin: 12px 0;
        padding: 12px 16px;
        background: #ffffff;
        border-radius: 6px;
        border: 1px solid #ddd8cf;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 500;
        color: #5a5750;
    }
    .legend-swatch {
        width: 14px;
        height: 14px;
        border-radius: 3px;
        border: 1px solid #ddd8cf;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 12px;
        margin: 16px 0;
    }
    .stat-card {
        background: #ffffff;
        padding: 14px;
        border-radius: 6px;
        border: 1px solid #ddd8cf;
    }
    .stat-card .label {
        font-size: 10px;
        color: #5a5750;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .stat-card .value { font-size: 22px; font-weight: 600; color: #2a2a28; margin-top: 4px; }
    .info-section {
        background: #ffffff;
        padding: 24px 28px;
        border-radius: 6px;
        border: 1px solid #ddd8cf;
        margin: 24px 0;
    }
    .info-section h2, .info-section h3 { margin-top: 0; }
    .loading-overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(245,242,237,0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #5a5750;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        z-index: 1000;
        border-radius: 6px;
    }
    .pipeline-step {
        display: flex;
        gap: 14px;
        margin-bottom: 16px;
        align-items: flex-start;
    }
    .step-num {
        flex-shrink: 0;
        width: 28px;
        height: 28px;
        background: #5a8bbe;
        color: #fff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
        margin-top: 2px;
    }
    .step-content { flex: 1; }
    .step-content strong { display: block; margin-bottom: 2px; font-size: 14px; }
    .step-content p { margin: 0; font-size: 13px; }
    hr {
        border: none;
        border-top: 1px solid #ddd8cf;
        margin: 2em 0;
    }
    .leaflet-container { background: #f5f2ed !important; }
</style>

<html>
<div class="titan-container">

<h1>Titan Terrain Map</h1>
<p class="subtitle">Automated terrain classification of Saturn's largest moon using deep learning on Cassini RADAR imagery</p>

<div class="stats-grid">
    <div class="stat-card">
        <div class="label">Resolution</div>
        <div class="value">351m/px</div>
    </div>
    <div class="stat-card">
        <div class="label">Encoder</div>
        <div class="value">EfficientNet-B4</div>
    </div>
    <div class="stat-card">
        <div class="label">Mean IoU</div>
        <div class="value">0.455</div>
    </div>
    <div class="stat-card">
        <div class="label">Terrain Classes</div>
        <div class="value">6</div>
    </div>
</div>

<div class="legend">
    <div class="legend-item"><div class="legend-swatch" style="background:#F5DEB3"></div> Plains (65%)</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#EDC951"></div> Dunes (12%)</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#8B4513"></div> Hummocky (12%)</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#1E90FF"></div> Lakes/Seas (4%)</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#6B8E23"></div> Labyrinth (4%)</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#DC143C"></div> Craters (&lt;1%)</div>
    <div class="legend-item" style="margin-left:auto; opacity:0.7;">|</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#32C832"></div> Agreement</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#DC2828"></div> Disagreement</div>
</div>

<div class="map-controls">
    <button id="btn-seg" class="active" onclick="setLayer('seg')">Our Model</button>
    <button id="btn-lopes" onclick="setLayer('lopes')">Lopes 2020 (Training Labels)</button>
    <button id="btn-diff" onclick="setLayer('diff')">Agreement Map</button>
    <button id="btn-reset" onclick="resetView()">Reset View</button>
    <span style="color:#5a5750; font-size:11px; margin-left:8px;">Scroll to zoom &middot; Drag to pan &middot; Full 351m/px resolution</span>
</div>

<div id="titan-map" style="position:relative;">
    <div class="loading-overlay" id="loading">Loading Titan map...</div>
</div>

<hr>

<div class="info-section">
    <h2>What is this?</h2>
    <p>This is an interactive, pixel-level terrain classification map of Titan — Saturn's largest moon and the only body in the solar system besides Earth with stable surface liquids. The map covers the entire surface imaged by the Cassini spacecraft's Synthetic Aperture Radar (SAR) instrument at <strong>351 metres per pixel</strong>.</p>
    <p>Unlike previous maps of Titan's surface which were drawn by hand by planetary scientists, this map was generated entirely by a neural network. The model learned to recognise terrain types from their radar backscatter signatures and can classify every pixel independently — producing a far more granular map than manual polygon-based approaches.</p>
    <p>Toggle between <strong>"Our Model"</strong> and <strong>"Lopes 2020"</strong> to see the difference. The Lopes map shows smooth, hand-drawn polygon boundaries. Our model follows the actual pixel-level texture in the SAR data — you can see how terrain types interleave at a much finer scale than any human could practically draw.</p>
</div>

<div class="info-section">
    <h2>How the data was collected</h2>
    <p>Between 2004 and 2017, NASA's <strong>Cassini spacecraft</strong> orbited Saturn and made over 100 close flybys of Titan. On each pass, its RADAR instrument bounced microwave pulses (Ku-band, 13.78 GHz) off Titan's surface and measured the backscattered energy. This technique — called <strong>Synthetic Aperture Radar</strong> — can penetrate Titan's thick, opaque atmosphere of nitrogen and methane, which blocks all visible and infrared light.</p>
    <p>Each flyby imaged a narrow swath of terrain. Over 13 years, these swaths were stitched together by the USGS Astrogeology Science Center into a global mosaic at <strong>128 pixels per degree</strong> (~351 metres per pixel at the equator). This <a href="https://astrogeology.usgs.gov/search/map/titan_cassini_sar_hisar_global_mosaic_351m">HiSAR Global Mosaic</a> covers roughly 24% of Titan's surface — the black regions on the map are areas Cassini never imaged at SAR resolution.</p>
    <p>The brightness of each pixel represents the <strong>radar backscatter coefficient (&#963;&#8320;)</strong> — how strongly the surface reflects radar energy back to the spacecraft. Different terrains have distinctive signatures: smooth lake surfaces reflect almost nothing (appearing dark), sand dunes create moderate returns with characteristic patterns, and rough mountainous terrain scatters strongly (appearing bright).</p>
</div>

<div class="info-section">
    <h2>The training labels</h2>
    <p>In 2020, planetary scientist <strong>Rosaly Lopes and colleagues</strong> published the first global geomorphological map of Titan in <em>Nature Astronomy</em> (<a href="https://doi.org/10.1038/s41550-019-0917-6">Lopes et al. 2020</a>). Through years of expert analysis, they manually classified Titan's surface into six terrain types:</p>
    <p><strong>Plains</strong> (65% of mapped surface) — low-relief, radar-dark expanses dominating the mid-latitudes. Likely organic sediment deposits. <strong>Dunes</strong> (12%) — linear features concentrated in equatorial regions, analogous to Earth's longitudinal sand dunes but composed of organic particles. <strong>Hummocky/mountainous terrain</strong> (12%) — radar-bright, rough topography, possibly the oldest exposed terrain on Titan. <strong>Lakes and seas</strong> (4%) — liquid methane and ethane bodies clustered near the north pole, appearing radar-dark due to specular reflection. <strong>Labyrinth terrain</strong> (4%) — dissected, canyon-like networks possibly carved by methane rainfall. <strong>Craters</strong> (&lt;1%) — remarkably few impact craters, suggesting a young, geologically active surface.</p>
    <p>The published shapefiles from this map are available on <a href="https://doi.org/10.17632/f6jrtyfp66.1">Mendeley Data</a>. We rasterised these polygons to match the SAR mosaic's pixel grid and used them as training labels for the neural network.</p>
</div>

<div class="info-section">
    <h2>The pipeline</h2>
    <p>The full workflow from raw Cassini data to the map you see above:</p>

    <div class="pipeline-step">
        <div class="step-num">1</div>
        <div class="step-content">
            <strong>Data acquisition</strong>
            <p>Downloaded the USGS HiSAR Global Mosaic (1 GB GeoTIFF, 46,080 x 23,040 pixels) and the Lopes 2020 geomorphological shapefiles from Mendeley Data.</p>
        </div>
    </div>

    <div class="pipeline-step">
        <div class="step-num">2</div>
        <div class="step-content">
            <strong>Preprocessing and tiling</strong>
            <p>Divided the mosaic into 10,711 tiles of 256x256 pixels. Each tile's SAR values were normalised using 2nd/98th percentile clipping. The Lopes shapefiles were rasterised (reprojected from Titan geographic CRS to the mosaic's equirectangular grid) to create matching label tiles.</p>
        </div>
    </div>

    <div class="pipeline-step">
        <div class="step-num">3</div>
        <div class="step-content">
            <strong>Geographic train/val/test split</strong>
            <p>Tiles were grouped into 10-degree spatial blocks and randomly assigned to train (70%), validation (15%), and test (15%) splits. This geographic blocking prevents spatial autocorrelation from leaking between splits — adjacent tiles tend to look similar, so a naive random split would overestimate performance.</p>
        </div>
    </div>

    <div class="pipeline-step">
        <div class="step-num">4</div>
        <div class="step-content">
            <strong>Model architecture</strong>
            <p>U-Net with an EfficientNet-B4 encoder pretrained on ImageNet. The single-channel SAR input is replicated to 3 channels to utilise the pretrained weights. The decoder outputs 6-class probability maps at full input resolution. Trained with Dice loss, AdamW optimiser (lr=5e-4), cosine annealing schedule, and augmentations (flip, rotate, Gaussian noise).</p>
        </div>
    </div>

    <div class="pipeline-step">
        <div class="step-num">5</div>
        <div class="step-content">
            <strong>GPU training</strong>
            <p>150 epochs on an RTX 3090 via RunPod (~5 hours, ~$2). The model converged to 0.455 mean Intersection-over-Union (mIoU) on the held-out test set. For context, perfect agreement with the labels would be 1.0, and a model predicting "plains" everywhere would score about 0.18.</p>
        </div>
    </div>

    <div class="pipeline-step">
        <div class="step-num">6</div>
        <div class="step-content">
            <strong>Overlapping inference</strong>
            <p>The full mosaic was classified using a sliding window with 50% overlap and cosine-weighted blending of softmax probabilities. This eliminates tile boundary artifacts — each pixel's classification is informed by multiple overlapping spatial contexts, and the model's most confident predictions (from tile centres) are weighted highest.</p>
        </div>
    </div>
</div>

<div class="info-section">
    <h2>Why this matters</h2>
    <p>Titan is the primary target for NASA's upcoming <strong>Dragonfly mission</strong> (launching 2028), which will send a rotorcraft lander to explore Titan's surface. Understanding the global distribution of terrain types is critical for mission planning — identifying safe landing zones, predicting surface conditions, and selecting scientifically interesting targets.</p>
    <p>Manual geological mapping is slow, subjective, and doesn't scale. Different experts can disagree on boundaries. An automated model produces <strong>consistent, reproducible</strong> classifications and can be instantly re-run when new data arrives. While Dragonfly carries cameras and spectrometers rather than SAR, the terrain classification framework demonstrated here — training on expert labels and generalising at pixel level — could be adapted to whatever imagery the mission returns.</p>
    <p>The pixel-level resolution of this map also reveals structure that polygon-based maps obscure. Terrain types on Titan don't have clean boundaries — they intergrade, with patches of one type embedded within another. The model captures this complexity in a way that hand-drawn polygons cannot.</p>
</div>

<div class="info-section">
    <h2>Limitations and caveats</h2>
    <p><strong>The model is only as good as its labels.</strong> It was trained on the Lopes 2020 map, which is itself an interpretation — expert, peer-reviewed, and the best available, but still a human judgement call in ambiguous areas. The 0.455 mIoU reflects both model error and label noise.</p>
    <p><strong>The "craters" class is essentially unlearnable</strong> at 0.3% of the training data. The model cannot reliably identify impact craters. This is a fundamental data limitation, not an architecture problem.</p>
    <p><strong>Coverage is incomplete.</strong> Cassini only imaged ~24% of Titan's surface at SAR resolution. The black regions are unknown. Some flyby swaths have different imaging geometries and incidence angles, which can affect radar backscatter independent of terrain type.</p>
    <p><strong>ImageNet pretraining contributes almost nothing.</strong> A randomly initialised encoder achieved 0.348 mIoU vs 0.350 with ImageNet weights — the domain gap between photographs of Earth objects and radar imagery of an alien moon is too large for transfer learning to help meaningfully.</p>
    <p><strong>Code:</strong> <a href="https://github.com/Volcanex/titan-sar">github.com/Volcanex/titan-sar</a></p>
</div>

</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function() {
    const loading = document.getElementById('loading');
    const bounds = [[-256, 0], [0, 512]];

    const map = L.map('titan-map', {
        crs: L.CRS.Simple,
        minZoom: 1,
        maxZoom: 11,
        zoomSnap: 1,
        zoomDelta: 1,
        attributionControl: false,
        maxBounds: [[-280, -20], [20, 532]],
        maxBoundsViscosity: 0.8,
    });

    const tileOpts = {
        tileSize: 256,
        zoomOffset: -1,
        minZoom: 1,
        maxNativeZoom: 8,
        maxZoom: 11,
        noWrap: true,
        bounds: bounds,
    };

    const segLayer = L.tileLayer('/assets/titan-terrain-map/tiles/seg/{z}/{x}/{y}.jpg', tileOpts);
    const lopesLayer = L.tileLayer('/assets/titan-terrain-map/tiles/lopes/{z}/{x}/{y}.jpg', tileOpts);
    const diffLayer = L.tileLayer('/assets/titan-terrain-map/tiles/diff/{z}/{x}/{y}.jpg', tileOpts);

    let currentLayer = segLayer;
    segLayer.addTo(map);

    segLayer.on('load', function() { loading.style.display = 'none'; });
    setTimeout(function() { loading.style.display = 'none'; }, 3000);

    map.fitBounds(bounds);

    window.setLayer = function(type) {
        map.removeLayer(currentLayer);
        document.querySelectorAll('.map-controls button').forEach(b => b.classList.remove('active'));
        if (type === 'seg') {
            currentLayer = segLayer;
            document.getElementById('btn-seg').classList.add('active');
        } else if (type === 'lopes') {
            currentLayer = lopesLayer;
            document.getElementById('btn-lopes').classList.add('active');
        } else {
            currentLayer = diffLayer;
            document.getElementById('btn-diff').classList.add('active');
        }
        currentLayer.addTo(map);
    };

    window.resetView = function() {
        map.fitBounds(bounds);
    };
})();
</script>
