# CRT Effects System Guide

## Overview
The blog now has a retro CRT-style visual effects system with 3-bit color compression, dithering, and authentic CRT monitor emulation.

## Homepage
The homepage has **full CRT effects enabled by default** with:
- CRT-era system fonts (Courier New, Courier, Lucida Console, Fixedsys, monospace)
- Inverted color scheme (black background, green text, cyan links)
- Full CRT effects: scanlines, phosphor glow, screen curvature, color compression, dithering

## Blog Post Configuration

### Adding CRT Effects to a Blog Post
In any page's `config.json`, add the `crt_effects` field:

```json
{
    "title": "Your Post Title",
    "slug": "your-post-slug",
    "date": "2025-02-26",
    "description": "Your description",
    "categories": ["category1", "category2"],
    "crt_effects": "full"
}
```

### Effect Intensity Levels

#### `"crt_effects": "none"` (default for blog posts)
- No CRT effects applied
- Normal rendering
- Best for readability-focused content

#### `"crt_effects": "subtle"`
- Light CRT effects
- Minimal pixelation (2px)
- 8-bit color depth
- Bayer dithering
- Light scanlines
- Small screen curvature (2.0)
- No glitch effects
- Good balance between retro aesthetic and readability

#### `"crt_effects": "full"` (homepage default)
- Maximum CRT effects
- Pixelation (3px)
- 4-bit color depth (closest to 3-bit / 8 colors)
- Floyd-Steinberg dithering
- Strong scanlines (0.8 intensity)
- VGA monitor preset
- Screen curvature (6.0)
- Phosphor glow (0.5)
- Chromatic aberration
- Flicker effect
- Glitch effects: RGB shift, digital noise, line displacement, etc.
- Full retro authenticity

## Technical Details

### Color Compression
- **3-bit color**: Reduces to approximately 8 colors (R/G/B on/off)
- Uses 4-bit mode (16 colors) as closest approximation
- Floyd-Steinberg dithering for smooth gradients

### CRT Emulation Features
- Scanlines with configurable intensity and thickness
- Phosphor glow simulation
- Screen curvature (barrel distortion)
- Chromatic aberration (RGB channel separation)
- Optional flicker effect (use with caution for accessibility)

### Glitch Effects (Full mode only)
- RGB color shift
- Digital noise
- Line displacement
- Bit crushing
- Signal dropout
- Sync errors
- Interference patterns
- Frame ghosting
- Stutter/freeze frames
- Datamoshing

## Files Modified

### Core Files
- `/home/gabriel/blog-new/compile.py` - Added CRT effects integration
- `/home/gabriel/blog-new/static/assets/js/crt-effects.js` - Main controller
- `/home/gabriel/blog-new/static/assets/js/glitchGL.min.js` - WebGL effects library

### How It Works
1. compile.py reads `crt_effects` from page config.json
2. If not "none", it includes Three.js, glitchGL, and crt-effects.js
3. The page initializes with the specified intensity level
4. WebGL shaders apply real-time effects to the entire page

## Recompiling After Config Changes

After modifying any config.json file:
```bash
cd /home/gabriel/blog-new
python3 compile.py
```

The Flask server will automatically serve the updated static files.

## Example Configurations

### Heavy Glitch Art Post
```json
{
    "title": "Glitch Art Showcase",
    "crt_effects": "full"
}
```

### Retro Computing Article
```json
{
    "title": "The History of VGA Monitors",
    "crt_effects": "subtle"
}
```

### Normal Blog Post
```json
{
    "title": "Regular Content",
    "crt_effects": "none"
}
```

## Performance Notes

- CRT effects use WebGL and can be GPU-intensive
- Effects are disabled by default for blog posts
- Mobile devices will experience the same effects (no automatic detection)
- Consider using "subtle" for better performance

## Accessibility Considerations

- **Flicker effect**: Only enabled in "full" mode, can trigger photosensitive epilepsy
- **Readability**: "subtle" mode maintains better text legibility
- Consider adding a user toggle in the future for accessibility

## Dependencies

- **Three.js r128**: WebGL rendering engine (loaded from CDN)
- **glitchGL v1.0.0**: CRT/glitch effects library (free for personal use)

## License Note

glitchGL uses a dual license model:
- **Free for personal use** (current usage)
- Requires commercial license for commercial applications
