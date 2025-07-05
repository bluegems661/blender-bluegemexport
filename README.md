# Blender Weapon Texture Render Pipeline

A comprehensive Blender automation script for batch rendering weapon textures with multiple lighting setups and material configurations. Designed for CS2/Counter-Strike weapon skin rendering workflows.

## Features

- 🎨 **Multi-texture Processing**: Automatically processes all textures for each weapon
- 💡 **Dual Lighting Systems**: Supports both fancy and flat lighting setups
- 🔄 **Multiple Render Types**: Generates blade_fancy, blade_flat, and mask renders
- 📐 **Precise Orientation Control**: XYZ Euler rotation system for consistent viewpoints
- 🧠 **Memory Management**: Built-in cleanup and optimization for large batch jobs
- 🛡️ **Error Handling**: Robust error recovery and detailed logging
- ⚡ **Performance Optimized**: Skips already rendered files, efficient GPU utilization

## Output Examples

For each texture, the script generates 6 renders:
- `weapon_blade_fancy_playside_103.png` - Normal material with fancy lighting (front view)
- `weapon_blade_fancy_backside_103.png` - Normal material with fancy lighting (180° rotated)
- `weapon_blade_flat_playside_103.png` - Normal material with flat lighting (front view)
- `weapon_blade_flat_backside_103.png` - Normal material with flat lighting (180° rotated)
- `weapon_mask_playside_103.png` - Mask material with flat lighting (front view)
- `weapon_mask_backside_103.png` - Mask material with flat lighting (180° rotated)

## Project Structure

```
blender-export/
├── pngandmask_export.py      # Main render script
├── export/                   # Output directory for rendered images
├── debug_collections.py      # Collection debugging utilities
├── debug_flip_knife.py       # Knife orientation debugging
├── glb_export.py            # GLB export functionality
├── png_export.py            # Basic PNG export
├── README.md                # This file
├── .gitignore              # Git ignore rules
└── LICENSE                 # License information
```

## Prerequisites

### Software Requirements
- **Blender 4.1.1+** (tested with 4.1.1)
- **Python 3.11** (included with Blender)
- **NVIDIA GPU** with OptiX support (recommended)

### Blender Scene Setup
Your Blender file must contain:

1. **Weapon Collections**: 
   - Main collection: `"CS2 Knives"`
   - Sub-collections for each weapon: `"Karambit"`, `"Bayonet"`, `"Bowie"`, etc.

2. **Lighting Collections**:
   - `"lighting_fancy"` - Complex lighting setup for hero renders
   - `"lighting_flat"` - Flat/uniform lighting for technical renders

3. **Materials**:
   - Shader node `"Image Texture.003"` in materials for texture assignment
   - Mask material: `"weapon_knife_karambit_blade_mask"`

4. **Texture Directory Structure**:
   ```
   C:\Users\[username]\Documents\textures\
   ├── weapon_karambit\
   │   ├── texture_001.png
   │   ├── texture_002.png
   │   └── ...
   ├── weapon_bayonet\
   │   ├── texture_001.png
   │   └── ...
   └── [other weapons]
   ```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/blender-export.git
   cd blender-export
   ```

2. **Update paths** in `pngandmask_export.py`:
   ```python
   # Line 7-8: Update these paths to match your setup
   render_dir = r"C:\Users\[username]\Documents\coding\blender-export\export"
   texture_base_dir = r"C:\Users\[username]\Documents\textures"
   ```

3. **Configure weapon list** (optional):
   ```python
   # Line 11-15: Add or remove weapons as needed
   target_weapons = [
       "Karambit", "Bayonet", "Bowie", "Butterfly", 
       # ... add your weapons here
   ]
   ```

## Usage

### Basic Usage
1. Open your prepared Blender file
2. Open the script in Blender's Text Editor or run via command line:
   ```bash
   blender your_scene.blend --background --python pngandmask_export.py
   ```
3. Monitor console output for progress and any issues

### Command Line Usage
```bash
# Render in background (faster, no GUI)
blender scene.blend --background --python pngandmask_export.py

# Render with GUI (for debugging)
blender scene.blend --python pngandmask_export.py
```

### Configuration Options

#### Render Settings
```python
# Lines 22-31: Render quality settings
scene.render.resolution_x = 1024        # Output width
scene.render.resolution_y = 1024        # Output height
scene.cycles.samples = 256             # Render quality
scene.cycles.denoiser = 'OPTIX'        # Denoising method
```

#### Memory Management
```python
# Line 42: Adjust based on your GPU memory
cprefs.texture_cache_size = 2048  # 2GB cache (adjust as needed)
```

## Supported Weapons

The script supports these weapon types by default:
- Karambit, Bayonet, Bowie, Butterfly, Survival, Classic
- Falchion, Flip, Gut, Kukri, M9, Navaja, Nomad
- Paracord, Shadowdaggers, Skeleton, Stiletto
- Huntsman, Talon, Ursus

*Add more weapons by editing the `target_weapons` list in the script.*

## Performance Tips

- **GPU Memory**: Reduce `texture_cache_size` if you encounter out-of-memory errors
- **Batch Size**: The script processes weapons sequentially to manage memory
- **SSD Storage**: Use SSD for texture and output directories for faster I/O
- **Background Rendering**: Use `--background` flag for faster processing

## Troubleshooting

### Common Issues

**Black Renders (blade_flat)**
- Ensure `lighting_flat` collection exists and contains lights
- Check console output for lighting status messages
- Verify lights are not hidden or disabled

**Missing Textures**
- Verify texture directory structure matches expected format
- Check file extensions (supports .png, .jpg, .jpeg)
- Ensure texture folders are named `weapon_[weaponname]` (lowercase)

**Memory Crashes**
- Reduce `texture_cache_size` in the script
- Close other applications to free RAM
- Process weapons in smaller batches

**Material Errors**
- Verify `Image Texture.003` node exists in materials
- Check mask material `weapon_knife_karambit_blade_mask` is available
- Ensure blade objects have materials assigned

### Debug Output

The script provides detailed console output:
```
🔧 Processing: Karambit - Found 3 texture(s)
   📁 Texture 1/3: weapon_karambit_damascus_103
      💡 Switching to fancy lighting for blade_fancy renders...
         ✅ Enabled lighting_fancy collection
         🔦 Active lights: 5
         🎬 Rendering blade_fancy playside: karambit_blade_fancy_playside_103.png
      ✅ Completed texture: weapon_karambit_damascus_103 - 6 renders generated
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test with multiple weapon types and texture counts
- Update documentation for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for Blender 4.1.1 with Cycles rendering engine
- Optimized for NVIDIA OptiX denoising
- Designed for CS2/Counter-Strike weapon rendering workflows

## Support

For issues and questions:
1. Check the [troubleshooting section](#troubleshooting)
2. Review console output for error messages  
3. Open an issue with detailed error logs and setup information

---

**Note**: This script is designed for educational and personal use. Ensure you have proper rights to any textures and 3D models used with this pipeline. 