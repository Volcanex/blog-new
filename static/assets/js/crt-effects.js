/**
 * Hybrid glitchGL Architecture
 * Layer 1: Original HTML content (source)
 * Layer 2: Canvas with glitchGL effects
 * Layer 3: Transparent HTML overlay for interactions
 */

class CRTEffectsController {
    constructor() {
        this.config = {
            enabled: false,
            intensity: 'full'
        };
        this.glitchInstance = null;
        this.canvas = null;
        this.ctx = null;
        this.sourceSnapshot = null;
        this.overlayContainer = null;
        this.updateInterval = null;
        this.currentSettings = null;
    }

    init(pageConfig = {}) {
        this.config.intensity = pageConfig.crt_effects || 'none';
        this.config.enabled = this.config.intensity !== 'none';

        if (!this.config.enabled) {
            console.log('[CRT] Effects disabled');
            return;
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.apply());
        } else {
            this.apply();
        }
    }

    async apply() {
        console.log('[CRT] Applying hybrid glitchGL architecture');

        // Wait for status to load before taking snapshot
        await this.waitForStatusLoad();

        // Load dependencies
        await this.loadDependencies();

        // Setup 3-layer architecture
        await this.setupLayers();

        // Initialize glitchGL
        this.initGlitchGL();

        // Setup periodic updates
        this.startUpdateLoop();

        console.log('[CRT] Hybrid architecture initialized');

        // Hide loading screen
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
            // Remove it completely after CRT power-on animation
            setTimeout(() => {
                loadingScreen.remove();
            }, 1100);
        }
    }

    async waitForStatusLoad() {
        console.log('[CRT] Waiting for status to load...');

        // Wait up to 5 seconds for status elements to update
        const timeout = 5000;
        const startTime = Date.now();

        while (Date.now() - startTime < timeout) {
            const minecraftStatus = document.getElementById('minecraft-status');
            const apiStatus = document.getElementById('api-status');

            if (minecraftStatus && apiStatus) {
                const minecraftText = minecraftStatus.textContent;
                const apiText = apiStatus.textContent;

                // Check if status has loaded (not "Loading..." anymore)
                if (minecraftText !== 'Loading...' && apiText !== 'Loading...') {
                    console.log('[CRT] Status loaded successfully');
                    return;
                }
            }

            // Wait 100ms before checking again
            await new Promise(resolve => setTimeout(resolve, 100));
        }

        console.log('[CRT] Status load timeout, proceeding anyway');
    }

    async loadDependencies() {
        // Load html2canvas if not available
        if (!window.html2canvas) {
            await new Promise((resolve, reject) => {
                const script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
                script.onload = resolve;
                script.onerror = reject;
                document.head.appendChild(script);
            });
        }
    }

    async setupLayers() {
        const content = document.getElementById('page-content');
        if (!content) {
            console.error('[CRT] #page-content not found');
            return;
        }

        // Layer 1: Original content stays visible and clickable
        content.style.position = 'relative';
        content.style.zIndex = '1';
        content.style.opacity = '0';  // Hide but keep rendered

        // Layer 2: Create canvas for glitchGL
        this.canvas = document.createElement('canvas');
        this.canvas.id = 'glitch-canvas';
        this.canvas.className = 'glitchGL';
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 2;
            pointer-events: none;
        `;
        document.body.appendChild(this.canvas);

        // Set canvas size
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.ctx = this.canvas.getContext('2d');

        // Take initial snapshot
        await this.captureSnapshot();

        // Layer 3: Create clickable overlay above canvas
        this.createClickableOverlay();
    }

    async captureSnapshot() {
        const content = document.getElementById('page-content');
        if (!content) return;

        try {
            // Make content visible temporarily for snapshot
            const originalOpacity = content.style.opacity;
            content.style.opacity = '1';

            // Capture using html2canvas
            this.sourceSnapshot = await html2canvas(content, {
                backgroundColor: '#000000',
                scale: 1,
                logging: false,
                useCORS: true
            });

            // Restore opacity
            content.style.opacity = originalOpacity;

            // Draw snapshot to canvas
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.drawImage(this.sourceSnapshot, 0, 0, this.canvas.width, this.canvas.height);

        } catch (error) {
            console.error('[CRT] Snapshot error:', error);
        }
    }

    createInteractionOverlay() {
        // Create overlay container
        this.overlayContainer = document.createElement('div');
        this.overlayContainer.id = 'interaction-overlay';
        this.overlayContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 3;
            pointer-events: none;
        `;
        document.body.appendChild(this.overlayContainer);

        // Extract links from original content
        this.extractInteractiveElements();
    }

    createClickableOverlay() {
        // Create overlay container above canvas
        this.overlayContainer = document.createElement('div');
        this.overlayContainer.id = 'clickable-overlay';
        this.overlayContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 3;
            pointer-events: none;
        `;
        document.body.appendChild(this.overlayContainer);

        // Find all grid items and create overlays
        const gridItems = document.querySelectorAll('.grid-item.blog-post');
        gridItems.forEach(item => {
            const rect = item.getBoundingClientRect();
            const url = item.getAttribute('data-url');

            if (url) {
                const overlay = document.createElement('div');
                overlay.style.cssText = `
                    position: absolute;
                    top: ${rect.top}px;
                    left: ${rect.left}px;
                    width: ${rect.width}px;
                    height: ${rect.height}px;
                    pointer-events: auto;
                    cursor: pointer;
                    z-index: 3;
                `;
                overlay.addEventListener('click', () => {
                    window.location.href = url;
                });

                this.overlayContainer.appendChild(overlay);
            }
        });

        // Also add overlays for links within grid items
        const links = document.querySelectorAll('.grid-item a');
        links.forEach(link => {
            const rect = link.getBoundingClientRect();
            const overlay = document.createElement('a');
            overlay.href = link.href;
            overlay.style.cssText = `
                position: absolute;
                top: ${rect.top}px;
                left: ${rect.left}px;
                width: ${rect.width}px;
                height: ${rect.height}px;
                pointer-events: auto;
                cursor: pointer;
                z-index: 3;
                color: transparent;
                text-decoration: none;
            `;
            this.overlayContainer.appendChild(overlay);
        });

        // Update overlay positions on window resize
        window.addEventListener('resize', () => {
            this.updateClickableOverlay();
        });
    }

    updateClickableOverlay() {
        if (!this.overlayContainer) return;
        this.overlayContainer.innerHTML = '';

        // Recreate overlays
        const gridItems = document.querySelectorAll('.grid-item.blog-post');
        gridItems.forEach(item => {
            const rect = item.getBoundingClientRect();
            const url = item.getAttribute('data-url');

            if (url && rect.width > 0) {  // Only if visible
                const overlay = document.createElement('div');
                overlay.style.cssText = `
                    position: absolute;
                    top: ${rect.top}px;
                    left: ${rect.left}px;
                    width: ${rect.width}px;
                    height: ${rect.height}px;
                    pointer-events: auto;
                    cursor: pointer;
                    z-index: 3;
                `;
                overlay.addEventListener('click', () => {
                    window.location.href = url;
                });

                this.overlayContainer.appendChild(overlay);
            }
        });

        // Also update link overlays
        const links = document.querySelectorAll('.grid-item a');
        links.forEach(link => {
            const rect = link.getBoundingClientRect();
            if (rect.width > 0) {
                const overlay = document.createElement('a');
                overlay.href = link.href;
                overlay.style.cssText = `
                    position: absolute;
                    top: ${rect.top}px;
                    left: ${rect.left}px;
                    width: ${rect.width}px;
                    height: ${rect.height}px;
                    pointer-events: auto;
                    cursor: pointer;
                    z-index: 3;
                    color: transparent;
                    text-decoration: none;
                `;
                this.overlayContainer.appendChild(overlay);
            }
        });
    }

    initGlitchGL() {
        if (!window.glitchGL) {
            console.error('[CRT] glitchGL library not loaded');
            return;
        }

        try {
            // Use current settings or get new ones
            if (!this.currentSettings) {
                this.currentSettings = this.getSettingsForIntensity(this.config.intensity);
            }

            const settings = this.currentSettings;

            this.glitchInstance = glitchGL({
                target: '.glitchGL',
                intensity: settings.intensity,
                aspectCorrection: true,
                interaction: {
                    enabled: true,
                    shape: 'circle',
                    radius: 200
                },
                effects: {
                    pixelation: {
                        enabled: settings.pixelation.enabled,
                        pixelSize: settings.pixelation.pixelSize,
                        pixelShape: 'square',
                        bitDepth: 'none',
                        dithering: 'none'
                    },
                    crt: {
                        enabled: settings.crt.enabled,
                        preset: settings.crt.preset,
                        scanlineIntensity: settings.crt.scanlineIntensity,
                        scanlineThickness: settings.crt.scanlineThickness,
                        scanlineCount: settings.crt.scanlineCount,
                        brightness: settings.crt.brightness,
                        phosphorGlow: settings.crt.phosphorGlow,
                        curvature: settings.crt.curvature,
                        chromaticAberration: settings.crt.chromaticAberration,
                        flicker: settings.crt.flicker,
                        flickerIntensity: settings.crt.flickerIntensity
                    },
                    glitch: {
                        enabled: settings.glitch.enabled,
                        rgbShift: settings.glitch.rgbShift,
                        digitalNoise: settings.glitch.digitalNoise,
                        lineDisplacement: settings.glitch.lineDisplacement
                    }
                },
                on: {
                    init: (instance) => {
                        console.log('[CRT] glitchGL initialized!');
                        this.glitchInstance = instance;
                    }
                }
            });
        } catch (error) {
            console.error('[CRT] glitchGL initialization error:', error);
        }
    }

    startUpdateLoop() {
        // Update snapshot more frequently for dynamic content
        this.updateInterval = setInterval(() => {
            this.captureSnapshot();
        }, 500); // Update every 500ms for real-time feel

        // Also update on window resize (updateClickableOverlay has its own resize handler)
        window.addEventListener('resize', () => {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
            this.captureSnapshot();
        });
    }

    getSettingsForIntensity(intensity) {
        // Moderate settings - noticeable but not overwhelming
        const settings = {
            intensity: 0.3,
            pixelation: {
                enabled: false,
                pixelSize: 1
            },
            crt: {
                enabled: true,
                preset: 'vga-monitor',
                scanlineIntensity: 0.15,
                scanlineThickness: 0.6,
                scanlineCount: 400,
                brightness: 1.0,
                phosphorGlow: 0,
                curvature: 0,
                chromaticAberration: 0,
                flicker: false,
                flickerIntensity: 0
            },
            glitch: {
                enabled: false,
                rgbShift: 0,
                digitalNoise: 0,
                lineDisplacement: 0
            }
        };

        return settings;
    }

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        if (this.glitchInstance && this.glitchInstance.destroy) {
            this.glitchInstance.destroy();
        }
        if (this.canvas) {
            this.canvas.remove();
        }
        if (this.overlayContainer) {
            this.overlayContainer.remove();
        }
        // Restore original content
        const content = document.getElementById('page-content');
        if (content) {
            content.style.opacity = '1';
            content.style.pointerEvents = 'auto';
        }
    }
}

window.crtEffects = new CRTEffectsController();

if (window.pageConfig) {
    window.crtEffects.init(window.pageConfig);
}
