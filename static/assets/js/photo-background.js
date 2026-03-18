/**
 * Photo Background with glitchGL Effects
 * Fetches a random background photo from photography collection
 * and applies CRT effects using glitchGL
 */

class PhotoBackgroundController {
    constructor() {
        this.config = {
            enabled: false,
            intensity: 'subtle'
        };
        this.glitchInstance = null;
        this.titleGlitchInstance = null;
        this.backgroundImage = null;
        this.glitchedTitle = null;

        // Admin mode
        this.adminMode = false;
        this.adminPassword = null;
        this.gui = null;
        this.savedSettings = null;

        // Setup admin mode toggle (Ctrl+Shift+G)
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'G') {
                e.preventDefault();
                this.toggleAdminMode();
            }
        });
    }

    async init(pageConfig = {}) {
        this.config.intensity = pageConfig.crt_effects || this.config.intensity;
        this.config.enabled = pageConfig.photo_background !== false;

        if (!this.config.enabled) {
            console.log('[PhotoBG] Photo background disabled');
            this.hideLoadingScreen();
            return;
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.apply());
        } else {
            this.apply();
        }
    }

    async apply() {
        console.log('[PhotoBG] Initializing photo background with glitchGL');

        // Load saved settings
        await this.loadSettings();

        // Fetch random background photo from API
        const photo = await this.fetchRandomBackgroundPhoto();

        if (!photo) {
            console.log('[PhotoBG] No background photo available');
            this.hideLoadingScreen();
            return;
        }

        console.log(`[PhotoBG] Selected photo: ${photo}`);

        // Setup background layer
        await this.setupBackgroundLayer();

        // Load and display photo
        await this.loadPhoto(photo);

        // Initialize glitchGL on the photo
        this.initGlitchGL();

        // Initialize glitchGL on the title
        this.initTitleGlitch();

        // Hide loading screen
        this.hideLoadingScreen();

        console.log('[PhotoBG] Photo background initialized');
    }

    async fetchRandomBackgroundPhoto() {
        try {
            const response = await fetch('/api/photography/random-background');
            const data = await response.json();
            return data.photo || null;
        } catch (error) {
            console.error('[PhotoBG] Failed to fetch random background:', error);
            return null;
        }
    }

    async setupBackgroundLayer() {
        // Create background image element (glitchGL will process this)
        this.backgroundImage = document.createElement('img');
        this.backgroundImage.id = 'photo-background-image';
        this.backgroundImage.className = 'glitchGL';
        this.backgroundImage.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            object-fit: cover;
            object-position: center;
        `;
        document.body.insertBefore(this.backgroundImage, document.body.firstChild);

        // Create glitched title overlay
        this.glitchedTitle = document.createElement('h1');
        this.glitchedTitle.id = 'glitched-title';
        this.glitchedTitle.className = 'glitchGL-title';
        this.glitchedTitle.textContent = 'GABRIELPENMAN.COM';
        this.glitchedTitle.style.cssText = `
            position: fixed;
            top: 1ch;
            left: 0;
            right: 0;
            width: 100%;
            text-align: center;
            font-size: 2.5em;
            color: #00FFFF;
            font-family: 'VT323', monospace;
            font-weight: normal;
            letter-spacing: 0.2ch;
            z-index: 0.5;
            margin: 0;
            padding: 0 1ch;
            text-shadow: 2px 2px 0 #000000;
        `;

        // Make title responsive on mobile
        if (window.innerWidth <= 768) {
            this.glitchedTitle.style.fontSize = '1.5em';
        }

        // Update on resize
        window.addEventListener('resize', () => {
            if (window.innerWidth <= 768) {
                this.glitchedTitle.style.fontSize = '1.5em';
            } else {
                this.glitchedTitle.style.fontSize = '2.5em';
            }
        });
        document.body.appendChild(this.glitchedTitle);

        // Hide the original title (we'll keep it for structure but make it invisible)
        const originalTitle = document.querySelector('#page-content h1');
        if (originalTitle) {
            originalTitle.style.opacity = '0';
        }

        // Make sure page content is above background but below glitched title
        const pageContent = document.getElementById('page-content');
        if (pageContent) {
            pageContent.style.position = 'relative';
            pageContent.style.zIndex = '1';
        }
    }

    async loadPhoto(filename) {
        return new Promise((resolve, reject) => {
            // Use thumbnail API for faster loading (1920px is good for backgrounds)
            const imageUrl = `/api/photography/thumbnail/${encodeURIComponent(filename)}?size=1920`;

            this.backgroundImage.onload = () => {
                console.log(`[PhotoBG] ✅ Photo loaded: ${filename}`);
                console.log(`[PhotoBG] Image dimensions: ${this.backgroundImage.naturalWidth}x${this.backgroundImage.naturalHeight}`);
                resolve();
            };

            this.backgroundImage.onerror = (error) => {
                console.error(`[PhotoBG] ❌ Failed to load photo: ${filename}`, error);
                reject(error);
            };

            // Set crossOrigin before src (required for glitchGL)
            this.backgroundImage.crossOrigin = 'anonymous';
            this.backgroundImage.src = imageUrl;
        });
    }

    initGlitchGL() {
        console.log('[PhotoBG] ========== initGlitchGL called ==========');
        console.log('[PhotoBG] window.glitchGL exists?', !!window.glitchGL);
        console.log('[PhotoBG] Background image element:', this.backgroundImage);
        console.log('[PhotoBG] Image loaded?', this.backgroundImage.complete);
        console.log('[PhotoBG] Image dimensions:', this.backgroundImage.naturalWidth, 'x', this.backgroundImage.naturalHeight);

        if (!window.glitchGL) {
            console.error('[PhotoBG] ❌ glitchGL library not loaded - check if script is included');
            return;
        }

        // Check if image exists in DOM
        const imageInDom = document.querySelector('.glitchGL');
        console.log('[PhotoBG] Image found in DOM?', !!imageInDom);
        console.log('[PhotoBG] Image src:', imageInDom ? imageInDom.src : 'N/A');

        try {
            // Use saved settings if available, otherwise use defaults
            const defaultSettings = this.getSettingsForIntensity(this.config.intensity);
            const settings = this.savedSettings?.background || defaultSettings;
            console.log('[PhotoBG] Settings:', settings);

            console.log('[PhotoBG] Calling glitchGL() with target:', '.glitchGL');
            this.glitchInstance = glitchGL({
                target: '.glitchGL',
                intensity: settings.intensity,
                aspectCorrection: true,
                interaction: {
                    enabled: true,      // Enable mouse interaction!
                    shape: 'circle',    // Circular distortion area
                    radius: 300         // Large radius for dramatic effect
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
                        console.log('[PhotoBG] ✅ glitchGL initialized successfully!');
                        console.log('[PhotoBG] glitchGL instance:', instance);
                        this.glitchInstance = instance;
                    },
                    error: (error) => {
                        console.error('[PhotoBG] ❌ glitchGL error callback:', error);
                    }
                }
            });

            console.log('[PhotoBG] glitchGL() returned:', this.glitchInstance);

            if (!this.glitchInstance) {
                console.error('[PhotoBG] ❌ glitchGL returned null/undefined!');
            }

        } catch (error) {
            console.error('[PhotoBG] ❌ glitchGL initialization error:', error);
            console.error('[PhotoBG] Error stack:', error.stack);
        }
    }

    initTitleGlitch() {
        console.log('[PhotoBG] ========== initTitleGlitch called ==========');

        if (!window.glitchGL) {
            console.error('[PhotoBG] ❌ glitchGL library not loaded for title');
            return;
        }

        if (!this.glitchedTitle) {
            console.error('[PhotoBG] ❌ Glitched title element not found');
            return;
        }

        try {
            // Use saved settings if available, otherwise use defaults with multipliers
            let titleSettings;
            if (this.savedSettings?.title) {
                titleSettings = this.savedSettings.title;
            } else {
                const baseSettings = this.getSettingsForIntensity(this.config.intensity);
                titleSettings = {
                    intensity: baseSettings.intensity,
                    pixelation: { ...baseSettings.pixelation },
                    crt: {
                        enabled: baseSettings.crt.enabled,
                        preset: baseSettings.crt.preset,
                        scanlineIntensity: baseSettings.crt.scanlineIntensity * 0.4,
                        scanlineThickness: baseSettings.crt.scanlineThickness * 0.7,
                        scanlineCount: baseSettings.crt.scanlineCount,
                        brightness: baseSettings.crt.brightness * 1.1,
                        phosphorGlow: baseSettings.crt.phosphorGlow * 0.8,
                        curvature: 0,
                        chromaticAberration: baseSettings.crt.chromaticAberration * 0.5,
                        flicker: baseSettings.crt.flicker,
                        flickerIntensity: baseSettings.crt.flickerIntensity * 0.3
                    },
                    glitch: {
                        enabled: baseSettings.glitch.enabled,
                        rgbShift: baseSettings.glitch.rgbShift * 0.3,
                        digitalNoise: baseSettings.glitch.digitalNoise * 0.2,
                        lineDisplacement: baseSettings.glitch.lineDisplacement * 0.3
                    }
                };
            }

            console.log('[PhotoBG] Initializing glitchGL on title...');
            this.titleGlitchInstance = glitchGL({
                target: '.glitchGL-title',
                intensity: titleSettings.intensity,
                aspectCorrection: false,  // Don't need aspect correction for text
                interaction: {
                    enabled: false  // Don't need mouse interaction on title
                },
                effects: {
                    pixelation: {
                        enabled: titleSettings.pixelation.enabled,
                        pixelSize: titleSettings.pixelation.pixelSize,
                        pixelShape: 'square',
                        bitDepth: 'none',
                        dithering: 'none'
                    },
                    crt: {
                        enabled: titleSettings.crt.enabled,
                        preset: titleSettings.crt.preset,
                        scanlineIntensity: titleSettings.crt.scanlineIntensity,
                        scanlineThickness: titleSettings.crt.scanlineThickness,
                        scanlineCount: titleSettings.crt.scanlineCount,
                        brightness: titleSettings.crt.brightness,
                        phosphorGlow: titleSettings.crt.phosphorGlow,
                        curvature: titleSettings.crt.curvature,
                        chromaticAberration: titleSettings.crt.chromaticAberration,
                        flicker: titleSettings.crt.flicker,
                        flickerIntensity: titleSettings.crt.flickerIntensity
                    },
                    glitch: {
                        enabled: titleSettings.glitch.enabled,
                        rgbShift: titleSettings.glitch.rgbShift,
                        digitalNoise: titleSettings.glitch.digitalNoise,
                        lineDisplacement: titleSettings.glitch.lineDisplacement
                    }
                },
                on: {
                    init: (instance) => {
                        console.log('[PhotoBG] ✅ glitchGL initialized on TITLE!');
                        this.titleGlitchInstance = instance;
                    },
                    error: (error) => {
                        console.error('[PhotoBG] ❌ glitchGL title error:', error);
                    }
                }
            });

            console.log('[PhotoBG] Title glitchGL() returned:', this.titleGlitchInstance);

        } catch (error) {
            console.error('[PhotoBG] ❌ Title glitchGL initialization error:', error);
            console.error('[PhotoBG] Error stack:', error.stack);
        }
    }

    getSettingsForIntensity(intensity) {
        const presets = {
            subtle: {
                intensity: 0.6,
                pixelation: { enabled: true, pixelSize: 3 },
                crt: {
                    enabled: true,
                    preset: 'vga-monitor',
                    scanlineIntensity: 0.4,
                    scanlineThickness: 1.0,
                    scanlineCount: 300,
                    brightness: 0.8,
                    phosphorGlow: 0.4,
                    curvature: 2,
                    chromaticAberration: 0.3,
                    flicker: true,
                    flickerIntensity: 0.05
                },
                glitch: {
                    enabled: true,
                    rgbShift: 0.15,
                    digitalNoise: 0.08,
                    lineDisplacement: 0.05
                }
            },
            full: {
                intensity: 0.9,
                pixelation: { enabled: true, pixelSize: 4 },
                crt: {
                    enabled: true,
                    preset: 'vga-monitor',
                    scanlineIntensity: 0.6,
                    scanlineThickness: 1.2,
                    scanlineCount: 250,
                    brightness: 0.7,
                    phosphorGlow: 0.6,
                    curvature: 5,
                    chromaticAberration: 0.8,
                    flicker: true,
                    flickerIntensity: 0.15
                },
                glitch: {
                    enabled: true,
                    rgbShift: 0.4,
                    digitalNoise: 0.2,
                    lineDisplacement: 0.2
                }
            }
        };

        return presets[intensity] || presets.subtle;
    }

    hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
            setTimeout(() => loadingScreen.remove(), 500);
        }
    }

    // ── Admin Mode ────────────────────────────────────────────────────────────

    toggleAdminMode() {
        if (!this.adminMode) {
            this.enterAdminMode();
        } else {
            this.exitAdminMode();
        }
    }

    enterAdminMode() {
        // Check if password is stored
        this.adminPassword = localStorage.getItem('adminPassword');

        if (!this.adminPassword) {
            this.adminPassword = prompt('Enter admin password:');
            if (!this.adminPassword) return;
            localStorage.setItem('adminPassword', this.adminPassword);
        }

        this.adminMode = true;
        console.log('[PhotoBG] 🔧 Admin mode enabled');
        this.createGUI();
    }

    exitAdminMode() {
        this.adminMode = false;
        console.log('[PhotoBG] Admin mode disabled');

        if (this.gui) {
            this.gui.destroy();
            this.gui = null;
        }
    }

    async loadSettings() {
        try {
            const response = await fetch('/api/photography/glitch-settings');
            const data = await response.json();
            this.savedSettings = data.settings;
            console.log('[PhotoBG] Loaded saved settings:', this.savedSettings);
            return this.savedSettings;
        } catch (error) {
            console.error('[PhotoBG] Failed to load settings:', error);
            return null;
        }
    }

    async saveSettings(settings) {
        try {
            const response = await fetch('/api/photography/glitch-settings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Admin-Password': this.adminPassword
                },
                body: JSON.stringify({ settings })
            });

            const data = await response.json();

            if (response.status === 401) {
                alert('Invalid admin password');
                localStorage.removeItem('adminPassword');
                this.adminPassword = null;
                this.exitAdminMode();
                return false;
            }

            console.log('[PhotoBG] ✅ Settings saved!', data);
            this.savedSettings = settings;
            return true;
        } catch (error) {
            console.error('[PhotoBG] Failed to save settings:', error);
            return false;
        }
    }

    createGUI() {
        if (!window.lil) {
            console.error('[PhotoBG] lil-gui not loaded');
            return;
        }

        // Destroy existing GUI if any
        if (this.gui) {
            this.gui.destroy();
        }

        this.gui = new lil.GUI({ title: 'glitchGL Settings', width: 320 });

        // Get current settings from instances and store them as instance variables
        this.currentBgSettings = this.getCurrentBackgroundSettings();
        this.currentTitleSettings = this.getCurrentTitleSettings();

        // Background folder
        const bgFolder = this.gui.addFolder('Background Photo');
        this.addEffectControls(bgFolder, this.currentBgSettings, 'background');
        bgFolder.open();

        // Title folder
        const titleFolder = this.gui.addFolder('Title Text');
        this.addEffectControls(titleFolder, this.currentTitleSettings, 'title');
        titleFolder.open();

        // Save button
        this.gui.add({ save: () => this.handleSave() }, 'save').name('💾 Save Settings');

        // Reset button
        this.gui.add({ reset: () => this.handleReset() }, 'reset').name('🔄 Reset to Defaults');
    }

    addEffectControls(folder, settings, target) {
        // Intensity
        folder.add(settings, 'intensity', 0, 1, 0.1)
            .name('Intensity')
            .onChange(v => this.updateEffect(target, { intensity: v }));

        // Pixelation folder
        const pixFolder = folder.addFolder('Pixelation');
        pixFolder.add(settings.pixelation, 'enabled').name('Enabled')
            .onChange(v => this.updateEffect(target, { effects: { pixelation: { enabled: v } } }));
        pixFolder.add(settings.pixelation, 'pixelSize', 1, 10, 1).name('Pixel Size')
            .onChange(v => this.updateEffect(target, { effects: { pixelation: { pixelSize: v } } }));

        // CRT folder
        const crtFolder = folder.addFolder('CRT');
        crtFolder.add(settings.crt, 'enabled').name('Enabled')
            .onChange(v => this.updateEffect(target, { effects: { crt: { enabled: v } } }));
        crtFolder.add(settings.crt, 'scanlineIntensity', 0, 1, 0.1).name('Scanlines')
            .onChange(v => this.updateEffect(target, { effects: { crt: { scanlineIntensity: v } } }));
        crtFolder.add(settings.crt, 'curvature', 0, 10, 1).name('Curvature')
            .onChange(v => this.updateEffect(target, { effects: { crt: { curvature: v } } }));
        crtFolder.add(settings.crt, 'chromaticAberration', 0, 2, 0.1).name('Chromatic Aberration')
            .onChange(v => this.updateEffect(target, { effects: { crt: { chromaticAberration: v } } }));
        crtFolder.add(settings.crt, 'phosphorGlow', 0, 1, 0.1).name('Phosphor Glow')
            .onChange(v => this.updateEffect(target, { effects: { crt: { phosphorGlow: v } } }));

        // Glitch folder
        const glitchFolder = folder.addFolder('Glitch');
        glitchFolder.add(settings.glitch, 'enabled').name('Enabled')
            .onChange(v => this.updateEffect(target, { effects: { glitch: { enabled: v } } }));
        glitchFolder.add(settings.glitch, 'rgbShift', 0, 1, 0.1).name('RGB Shift')
            .onChange(v => this.updateEffect(target, { effects: { glitch: { rgbShift: v } } }));
        glitchFolder.add(settings.glitch, 'digitalNoise', 0, 1, 0.1).name('Digital Noise')
            .onChange(v => this.updateEffect(target, { effects: { glitch: { digitalNoise: v } } }));
    }

    getCurrentBackgroundSettings() {
        const settings = this.getSettingsForIntensity(this.config.intensity);
        return {
            intensity: settings.intensity,
            pixelation: { ...settings.pixelation },
            crt: { ...settings.crt },
            glitch: { ...settings.glitch }
        };
    }

    getCurrentTitleSettings() {
        const settings = this.getSettingsForIntensity(this.config.intensity);
        return {
            intensity: settings.intensity,
            pixelation: { ...settings.pixelation },
            crt: {
                enabled: settings.crt.enabled,
                scanlineIntensity: settings.crt.scanlineIntensity * 0.4,
                curvature: 0,
                chromaticAberration: settings.crt.chromaticAberration * 0.5,
                phosphorGlow: settings.crt.phosphorGlow * 0.8
            },
            glitch: {
                enabled: settings.glitch.enabled,
                rgbShift: settings.glitch.rgbShift * 0.3,
                digitalNoise: settings.glitch.digitalNoise * 0.2
            }
        };
    }

    updateEffect(target, options) {
        if (target === 'background' && this.glitchInstance) {
            this.glitchInstance.updateOptions(options);
            console.log('[PhotoBG] Updated background:', options);
        } else if (target === 'title' && this.titleGlitchInstance) {
            this.titleGlitchInstance.updateOptions(options);
            console.log('[PhotoBG] Updated title:', options);
        }
    }

    async handleSave() {
        // Use the settings objects that the GUI is modifying
        const settings = {
            background: this.currentBgSettings,
            title: this.currentTitleSettings
        };

        console.log('[PhotoBG] Saving settings:', settings);

        const success = await this.saveSettings(settings);
        if (success) {
            alert('✅ Settings saved successfully!');
        } else {
            alert('❌ Failed to save settings');
        }
    }

    handleReset() {
        if (confirm('Reset to default settings?')) {
            // Reload page to reset
            window.location.reload();
        }
    }

    destroy() {
        if (this.glitchInstance && this.glitchInstance.destroy) {
            this.glitchInstance.destroy();
        }
        if (this.titleGlitchInstance && this.titleGlitchInstance.destroy) {
            this.titleGlitchInstance.destroy();
        }
        if (this.backgroundImage) {
            this.backgroundImage.remove();
        }
        if (this.glitchedTitle) {
            this.glitchedTitle.remove();
        }
    }
}

// Initialize global instance
window.photoBackground = new PhotoBackgroundController();

// Auto-init if pageConfig exists
if (window.pageConfig) {
    window.photoBackground.init(window.pageConfig);
}
