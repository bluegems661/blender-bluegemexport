# Contributing to Blender Weapon Texture Render Pipeline

Thank you for your interest in contributing to this project! This guide will help you get started with development and contributions.

## 🚀 Getting Started

### Prerequisites
- **Blender 4.1.1+** installed and working
- **NVIDIA GPU** with OptiX support (recommended for testing)
- **Git** for version control
- Basic knowledge of **Python** and **Blender Python API (bpy)**

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/blender-export.git
   cd blender-export
   ```

3. **Set up your local paths** in `pngandmask_export.py`:
   ```python
   # Update these paths to match your setup
   render_dir = r"C:\Users\[username]\Documents\coding\blender-export\export"
   texture_base_dir = r"C:\Users\[username]\Documents\textures"
   ```

4. **Prepare test data**:
   - Create a test Blender scene with required collections
   - Add sample texture files for testing
   - Ensure proper collection structure (`CS2 Knives`, lighting collections, etc.)

## 🛠️ Development Workflow

### Code Style Guidelines

- **Follow PEP 8** Python style guidelines
- **Use descriptive variable names** (e.g., `weapon_name` instead of `w`)
- **Add docstrings** to all functions with parameters and return values
- **Use type hints** where applicable
- **Add comments** for complex logic or Blender-specific operations

### Example Function Documentation:
```python
def apply_texture_to_shader(image_path):
    """
    Load and apply a texture to all materials with "Image Texture.003" node.
    
    Args:
        image_path (str): Path to the texture image file
        
    Returns:
        bpy.types.Image: Loaded image object, or None if failed
    """
    # Implementation here...
```

### Testing Your Changes

1. **Manual Testing**:
   - Test with multiple weapon types
   - Test with different texture counts
   - Test error conditions (missing files, invalid paths)
   - Test memory usage with large batch jobs

2. **Background Testing**:
   ```bash
   blender your_scene.blend --background --python pngandmask_export.py
   ```

3. **GUI Testing**:
   ```bash
   blender your_scene.blend --python pngandmask_export.py
   ```

### Common Areas for Contribution

#### 🎨 **Rendering Features**
- Additional render formats (EXR, TIFF)
- New lighting configurations
- Material switching capabilities
- Quality presets (low/medium/high)

#### 🔧 **Technical Improvements**
- Configuration file support
- Better error handling
- Performance optimizations
- Memory management improvements

#### 📚 **Documentation**
- Code comments and docstrings
- Usage examples
- Troubleshooting guides
- Video tutorials

#### 🐛 **Bug Fixes**
- Memory leaks
- Crash prevention
- Compatibility issues
- Edge case handling

## 📋 Contribution Process

### 1. Create an Issue
Before starting work, create an issue describing:
- **Problem**: What you're trying to solve
- **Solution**: How you plan to solve it
- **Testing**: How you'll test the changes

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 3. Make Changes
- Write clean, documented code
- Follow the existing code style
- Add comments for complex logic
- Test thoroughly

### 4. Update Documentation
- Update README.md if needed
- Add/update docstrings
- Update CHANGELOG.md with your changes

### 5. Submit Pull Request
- **Clear title**: Describe what the PR does
- **Detailed description**: Explain the changes and why they're needed
- **Testing notes**: How you tested the changes
- **Screenshots**: If applicable, especially for UI changes

## 🔍 Code Review Process

### What We Look For:
- **Functionality**: Does it work as expected?
- **Code Quality**: Is it clean, readable, and well-documented?
- **Performance**: Does it introduce any performance issues?
- **Compatibility**: Does it work with different Blender versions?
- **Error Handling**: Are edge cases handled gracefully?

### Review Timeline:
- Initial review within 3-7 days
- Follow-up reviews within 1-3 days
- Merge when approved by maintainers

## 🧪 Testing Guidelines

### Essential Test Cases:
1. **Single weapon, single texture**
2. **Multiple weapons, multiple textures**
3. **Missing texture files**
4. **Invalid collection structure**
5. **Memory stress test** (large batches)
6. **Background vs GUI rendering**

### Performance Testing:
- Monitor memory usage during batch processing
- Test with different texture sizes
- Measure render times for optimization

## 📚 Resources

### Blender Python API Documentation:
- [Blender Python API Reference](https://docs.blender.org/api/current/)
- [Blender Python Best Practices](https://docs.blender.org/api/current/info_best_practice.html)

### Useful Development Tools:
- **Blender Console**: For testing bpy commands
- **Blender Text Editor**: For script development
- **External IDE**: VS Code, PyCharm with Blender extensions

### Community Resources:
- [Blender Stack Exchange](https://blender.stackexchange.com/)
- [Blender Developer Forum](https://devtalk.blender.org/)
- [r/blender](https://www.reddit.com/r/blender/)

## 🆘 Getting Help

### Before Asking for Help:
1. Check the [README.md](README.md) troubleshooting section
2. Search existing issues on GitHub
3. Test with the latest version of Blender
4. Review the [CHANGELOG.md](CHANGELOG.md) for recent changes

### How to Ask for Help:
- **Clear problem description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **System information** (OS, Blender version, GPU)
- **Error messages** (full stack traces)
- **Screenshots** or console output

### Contact:
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For general questions and ideas
- **Pull Request Comments**: For code-specific questions

## 🏆 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- CHANGELOG.md contributor lists
- GitHub contributor graphs
- Release notes for significant contributions

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping improve this project! Every contribution, no matter how small, makes a difference.** 🙏 