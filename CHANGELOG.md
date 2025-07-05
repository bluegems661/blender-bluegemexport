# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-19

### Added
- **Initial Release**: Complete Blender weapon texture rendering pipeline
- **Multi-texture Processing**: Automatic processing of all texture files per weapon
- **Dual Lighting System**: Support for both `lighting_fancy` and `lighting_flat` collections
- **Six Render Types**: 
  - `blade_fancy_playside/backside` - Normal materials with fancy lighting
  - `blade_flat_playside/backside` - Normal materials with flat lighting
  - `mask_playside/backside` - Mask materials with flat lighting
- **XYZ Euler Rotation System**: Simplified rotation control (0°/180°)
- **Memory Management**: Comprehensive cleanup system to prevent crashes
- **Error Handling**: Robust error recovery and detailed logging
- **Skip Logic**: Intelligent skipping of already rendered files
- **Progress Tracking**: Detailed console output with emojis and progress indicators
- **Safe Collection Iteration**: Prevents EXCEPTION_ACCESS_VIOLATION crashes
- **GPU Optimization**: OptiX denoising and optimized texture cache settings

### Technical Features
- **Supported Weapons**: 20 knife types including Karambit, Bayonet, Bowie, Butterfly, etc.
- **Render Settings**: 1024x1024 resolution, 256 samples, Cycles GPU rendering
- **Texture Formats**: Support for PNG, JPG, JPEG files
- **Output Naming**: Structured naming convention with weapon, type, side, and texture suffix
- **Lighting Management**: Dynamic lighting collection switching per render type
- **Memory Cleanup**: Automatic cleanup every 3 weapons to prevent memory issues

### Development History
- **Phase 1**: Basic rendering with quaternion rotations and crash issues
- **Phase 2**: Added base rotation system and improved error handling
- **Phase 3**: Simplified to XYZ Euler rotations and added dual lighting
- **Phase 4**: Expanded to 6 render types and multi-texture processing
- **Phase 5**: Added comprehensive debugging and memory management
- **Phase 6**: Documentation and GitHub preparation

### Known Issues
- Requires specific Blender scene setup with predefined collections
- GPU memory requirements may vary based on texture sizes
- Some lighting setups may result in black renders (diagnostic tools included)

### Dependencies
- Blender 4.1.1 or higher
- Python 3.11 (included with Blender)
- NVIDIA GPU with OptiX support (recommended)
- Properly structured texture directories and Blender collections

### Performance Notes
- Processes weapons sequentially to manage memory
- Texture cache limited to 2GB to prevent out-of-memory errors
- Background rendering recommended for production use
- SSD storage recommended for faster I/O operations

---

## Development Roadmap

### Future Enhancements (Not Yet Implemented)
- [ ] Configuration file support for paths and settings
- [ ] Multi-threading support for parallel processing
- [ ] Automatic Blender scene validation
- [ ] Additional render formats (EXR, TIFF)
- [ ] Batch processing UI within Blender
- [ ] Advanced material switching capabilities
- [ ] Custom lighting setup automation
- [ ] Render farm integration
- [ ] Quality presets (low/medium/high)
- [ ] Automatic texture format conversion

### Bug Fixes History
- **Fixed**: EXCEPTION_ACCESS_VIOLATION during collection iteration
- **Fixed**: Black renders in blade_flat mode due to lighting issues
- **Fixed**: Memory leaks during batch processing
- **Fixed**: Incorrect rotation handling with object hierarchies
- **Fixed**: Texture loading failures with certain file formats
- **Fixed**: Skip logic not working correctly for existing files

---

*Note: This project evolved through extensive testing and iteration to handle the complexities of automated Blender rendering workflows.* 