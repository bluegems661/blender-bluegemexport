#!/usr/bin/env python3
"""
Blender Weapon Texture Render Pipeline

A comprehensive Blender automation script for batch rendering weapon textures 
with multiple lighting setups and material configurations. Designed for 
CS2/Counter-Strike weapon skin rendering workflows.

Features:
- Multi-texture processing for each weapon
- Dual lighting systems (fancy/flat)
- Multiple render types (blade_fancy, blade_flat, mask)
- Precise XYZ Euler rotation control
- Memory management and error handling
- Performance optimization with skip logic

Author: Blender Export Pipeline
License: MIT
Version: 1.0.0
Blender: 4.1.1+
"""

import bpy
import os
import math
import gc

# ========================================
# CONFIGURATION SECTION
# ========================================

# === Output paths ===
# TODO: Update these paths to match your local setup
render_dir = r"C:\Users\maxim\Documents\coding\blender-export\export"
texture_base_dir = r"C:\Users\maxim\Documents\textures"
os.makedirs(render_dir, exist_ok=True)

# === Weapon Configuration ===
# List of weapons to process. Add or remove weapons as needed.
# Each weapon must have a corresponding collection in "CS2 Knives" and 
# a texture folder named "weapon_[weaponname]" (lowercase) in texture_base_dir
target_weapons = [
    "Karambit", "Bayonet", "Bowie", "Butterfly", "Survival", "Classic", "Falchion", "Flip", "Gut", "Kukri", "M9", 
    "Navaja", "Nomad", "Paracord", "Shadowdaggers", "Skeleton", "Stiletto", 
    "Huntsman", "Talon", "Ursus","AK-47", "Five-Seven"
]

# ========================================
# RENDER CONFIGURATION
# ========================================

# === Render settings ===
# Configure Cycles render engine with optimized settings
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100

scene.cycles.device = 'GPU'
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.001
scene.cycles.samples = 1024
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX'
scene.cycles.tile_x = 256
scene.cycles.tile_y = 256

prefs = bpy.context.preferences
cprefs = prefs.addons['cycles'].preferences
cprefs.compute_device_type = 'OPTIX'
for device in cprefs.devices:
    device.use = True
    
# ✅ Reduce texture cache size to prevent memory issues
cprefs.texture_cache_size = 2048  # Reduced from 4GB to 2GB

# ========================================
# MEMORY MANAGEMENT
# ========================================

def cleanup_memory():
    """
    Force garbage collection and cleanup unused images to prevent memory crashes.
    
    This function:
    1. Removes unused images from bpy.data.images
    2. Forces Python garbage collection
    3. Updates the view layer to refresh the scene
    
    Should be called periodically during batch processing.
    """
    # Remove unused images
    for img in bpy.data.images:
        if img.users == 0:
            try:
                bpy.data.images.remove(img, do_unlink=True)
            except:
                pass
    
    # Force garbage collection
    gc.collect()
    
    # Update view layer
    bpy.context.view_layer.update()

# ========================================
# HELPER FUNCTIONS
# ========================================
def weapon_to_folder_key(name):
    """
    Convert weapon name to folder key format.
    
    Args:
        name (str): Weapon name (e.g., "Karambit", "M9 Bayonet")
        
    Returns:
        str: Lowercase folder key (e.g., "karambit", "m9bayonet")
    """
    return name.lower().replace(" ", "")

def ensure_in_view_layer(collection):
    """
    Ensure a collection is linked to the scene collection.
    
    Args:
        collection: Blender collection object
    """
    # Simple approach: just link to scene collection if not already linked
    if collection.name not in [c.name for c in bpy.context.scene.collection.children]:
        bpy.context.scene.collection.children.link(collection)

def ensure_lighting_in_view_layer(collection):
    """
    Ensure lighting collection is properly linked to view layer and visible.
    
    This function handles the complex logic of making sure lighting collections
    are properly linked to the scene and enabled in the view layer.
    
    Args:
        collection: Blender collection object containing lights
    """
    if not collection:
        return
    
    # Link to scene collection if not already linked
    if collection.name not in [c.name for c in bpy.context.scene.collection.children]:
        bpy.context.scene.collection.children.link(collection)
        print(f"   Linked {collection.name} to scene collection")
    
    # Make sure it's in the view layer
    layer_collection = bpy.context.view_layer.layer_collection
    if collection.name not in [lc.name for lc in layer_collection.children]:
        # Try to find it in nested collections
        for child in layer_collection.children:
            if child.collection == collection:
                child.exclude = False
                print(f"   Enabled {collection.name} in view layer")
                break

def apply_texture_to_shader(image_path):
    """
    Load and apply a texture to all materials with "Image Texture.003" node.
    
    This function:
    1. Loads the image from the given path
    2. Finds all materials with "Image Texture.003" shader node
    3. Applies the texture to those nodes
    
    Args:
        image_path (str): Path to the texture image file
        
    Returns:
        bpy.types.Image: Loaded image object, or None if failed
    """
    if not os.path.exists(image_path):
        print(f"❌ Texture not found: {image_path}")
        return None
    try:
        loaded_image = bpy.data.images.load(image_path, check_existing=True)
    except RuntimeError as e:
        print(f"❌ Failed to load image: {image_path} — {e}")
        return None

    found_node = False
    for material in bpy.data.materials:
        if not material.use_nodes or not material.node_tree:
            continue
        node = material.node_tree.nodes.get("Image Texture.003")
        if node and isinstance(node, bpy.types.ShaderNodeTexImage):
            node.image = loaded_image
            found_node = True

    if not found_node:
        print("⚠️ Shader node 'Image Texture.003' not found.")
        return None
    return loaded_image

def get_collection_objects_safely(collection):
    """
    Safely get mesh objects from a collection with comprehensive error handling.
    
    This function prevents crashes by:
    1. Converting iterators to lists to avoid reference issues
    2. Filtering only valid mesh objects
    3. Checking object visibility
    4. Handling ReferenceError and AttributeError exceptions
    
    Args:
        collection: Blender collection object
        
    Returns:
        list: List of valid mesh objects
    """
    try:
        # Convert to list to avoid iterator issues
        objects = list(collection.all_objects)
        # Filter for mesh objects that are valid
        valid_objects = []
        for obj in objects:
            try:
                if obj and obj.type == 'MESH' and hasattr(obj, 'visible_get'):
                    if obj.visible_get():
                        valid_objects.append(obj)
            except (AttributeError, ReferenceError):
                # Skip invalid objects
                continue
        return valid_objects
    except Exception as e:
        print(f"❌ Error getting objects from collection: {e}")
        return []

def debug_active_lights():
    """
    Debug function to check what lights are active in the scene.
    
    Prints information about active lights to the console for troubleshooting
    lighting issues, especially useful when diagnosing black renders.
    """
    active_lights = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'LIGHT' and obj.visible_get():
            active_lights.append(f"{obj.name} (in {obj.users_collection[0].name if obj.users_collection else 'No Collection'})")
    
    print(f"   🔦 Active lights: {len(active_lights)}")
    for light in active_lights[:5]:  # Show first 5 lights
        print(f"      - {light}")
    if len(active_lights) > 5:
        print(f"      ... and {len(active_lights) - 5} more")

def render_and_save(output_path):
    """
    Render the current scene and save to the specified path.
    
    This function combines the lighting debug output with the actual render operation.
    
    Args:
        output_path (str): Full path where the render should be saved
    """
    debug_active_lights()
    scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

# ========================================
# MAIN PROCESSING LOOP
# ========================================

# === Collections ===
knife_collection = bpy.data.collections.get("CS2 Knives")
if not knife_collection:
    raise Exception("Collection 'CS2 Knives' not found!")

# === Main processing loop ===
# Process each weapon in the target list, generating multiple renders per texture
processed_count = 0
for weapon_name in target_weapons:
    try:
        print(f"🔍 Processing weapon: {weapon_name}")
        
        knife_col = knife_collection.children.get(weapon_name)
        if not knife_col:
            print(f"❌ Weapon '{weapon_name}' not found, skipping.")
            continue

        folder_key = weapon_to_folder_key(weapon_name)
        texture_folder = os.path.join(texture_base_dir, f"weapon_{folder_key}")
        if not os.path.exists(texture_folder):
            print(f"❌ Texture folder not found for {weapon_name}: {texture_folder}")
            continue

        texture_files = [f for f in os.listdir(texture_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not texture_files:
            print(f"⚠️ No textures found in {texture_folder}, skipping.")
            continue

        print(f"🔧 Processing: {weapon_name} - Found {len(texture_files)} texture(s)")
        
        # Process each texture file for this weapon
        for texture_index, texture_file in enumerate(texture_files):
            texture_path = os.path.join(texture_folder, texture_file)
            texture_name = os.path.splitext(texture_file)[0]
            
            print(f"   📁 Texture {texture_index + 1}/{len(texture_files)}: {texture_name}")
            
            # Check if all expected PNG files already exist
            texture_suffix = texture_name.split('_')[-1]
            blade_fancy_playside_path = os.path.join(render_dir, f"{folder_key}_blade_fancy_playside_{texture_suffix}.png")
            blade_fancy_backside_path = os.path.join(render_dir, f"{folder_key}_blade_fancy_backside_{texture_suffix}.png")
            blade_flat_playside_path = os.path.join(render_dir, f"{folder_key}_blade_flat_playside_{texture_suffix}.png")
            blade_flat_backside_path = os.path.join(render_dir, f"{folder_key}_blade_flat_backside_{texture_suffix}.png")
            mask_playside_path = os.path.join(render_dir, f"{folder_key}_mask_playside_{texture_suffix}.png")
            mask_backside_path = os.path.join(render_dir, f"{folder_key}_mask_backside_{texture_suffix}.png")
            
            if (os.path.exists(blade_fancy_playside_path) and os.path.exists(blade_fancy_backside_path) and 
                os.path.exists(blade_flat_playside_path) and os.path.exists(blade_flat_backside_path) and
                os.path.exists(mask_playside_path) and os.path.exists(mask_backside_path)):
                print(f"      ⏭️ All renders already exist for {texture_name}, skipping.")
                continue
            
            print(f"      🎨 Will generate 6 renders: blade_fancy (playside/backside), blade_flat (playside/backside), mask_flat (playside/backside)")

            # Hide all other collections
            for col in knife_collection.children:
                try:
                    col.hide_render = True
                    col.hide_viewport = True
                except:
                    pass

            # Ensure collection is in view layer and objects are visible
            ensure_in_view_layer(knife_col)
            knife_col.hide_render = False
            knife_col.hide_viewport = False
            
            # Safely get objects from collection
            print(f"      🔍 Getting objects from collection: {knife_col.name}")
            objects_to_render = get_collection_objects_safely(knife_col)
            
            if not objects_to_render:
                print(f"      ⚠️ No valid mesh objects found for {weapon_name}, skipping texture.")
                continue
            
            print(f"      ✅ Found {len(objects_to_render)} objects to render")
            
            # Unhide objects and prepare for rendering
            bpy.ops.object.select_all(action='DESELECT')
            for obj in objects_to_render:
                try:
                    obj.hide_set(False)
                    obj.hide_viewport = False
                    obj.hide_render = False
                    obj.select_set(True)
                except:
                    pass
            
            bpy.context.view_layer.update()
            
            if objects_to_render:
                bpy.context.view_layer.objects.active = objects_to_render[0]

            # Apply texture
            loaded_image = apply_texture_to_shader(texture_path)
            if not loaded_image:
                print(f"      ❌ Failed to apply texture {texture_name}, skipping.")
                continue

            # === Lighting setup ===
            # Get lighting collections
            lighting_fancy = bpy.data.collections.get("lighting_fancy")
            lighting_flat = bpy.data.collections.get("lighting_flat")
            
            if not lighting_fancy:
                print("      ⚠️ 'lighting_fancy' collection not found - normal renders will use default lighting")
            if not lighting_flat:
                print("      ⚠️ 'lighting_flat' collection not found - mask renders will use default lighting")
            
            # Store original lighting states
            lighting_states = {}
            if lighting_fancy:
                lighting_states['fancy'] = {
                    'hide_render': lighting_fancy.hide_render,
                    'hide_viewport': lighting_fancy.hide_viewport
                }
            if lighting_flat:
                lighting_states['flat'] = {
                    'hide_render': lighting_flat.hide_render,
                    'hide_viewport': lighting_flat.hide_viewport
                }

            # Store original rotations for topmost parent objects
            original_rotations = {}
            for obj in objects_to_render:
                try:
                    # Find topmost parent
                    target = obj
                    while target.parent:
                        target = target.parent
                    
                    # Store original rotation mode and euler (only once per parent)
                    if target not in original_rotations:
                        original_rotations[target] = {
                            'rotation_mode': target.rotation_mode,
                            'rotation_euler': target.rotation_euler.copy()
                        }
                except:
                    pass

            # === Render normal material with fancy lighting (blade_fancy) ===
            # Set lighting for normal renders (fancy lighting)
            print("      💡 Switching to fancy lighting for blade_fancy renders...")
            if lighting_fancy:
                ensure_lighting_in_view_layer(lighting_fancy)
                lighting_fancy.hide_render = False
                lighting_fancy.hide_viewport = False
                print(f"         ✅ Enabled lighting_fancy collection")
            if lighting_flat:
                lighting_flat.hide_render = True
                lighting_flat.hide_viewport = True
                print(f"         ❌ Disabled lighting_flat collection")
            
            # Force view layer update after lighting changes
            bpy.context.view_layer.update()
            
            # Set playside rotation on topmost parent (0,0,0)
            for obj in objects_to_render:
                try:
                    target = obj
                    while target.parent:
                        target = target.parent
                    target.rotation_mode = 'XYZ'
                    target.rotation_euler = (0, 0, 0)
                except:
                    pass
            
            bpy.context.view_layer.update()
            playside_path = os.path.join(render_dir, f"{folder_key}_blade_fancy_playside_{texture_name.split('_')[-1]}.png")
            print(f"         🎬 Rendering blade_fancy playside: {playside_path}")
            render_and_save(playside_path)

            # Set backside rotation on topmost parent (0,0,180)
            for obj in objects_to_render:
                try:
                    target = obj
                    while target.parent:
                        target = target.parent
                    target.rotation_mode = 'XYZ'
                    target.rotation_euler = (0, 0, math.radians(180))
                except:
                    pass
            
            bpy.context.view_layer.update()
            backside_path = os.path.join(render_dir, f"{folder_key}_blade_fancy_backside_{texture_name.split('_')[-1]}.png")
            print(f"         🎬 Rendering blade_fancy backside: {backside_path}")
            render_and_save(backside_path)

            # === Render normal material with flat lighting (blade_flat) ===
            # Set lighting for normal renders (flat lighting)
            print("      💡 Switching to flat lighting for blade_flat renders...")
            if lighting_flat:
                ensure_lighting_in_view_layer(lighting_flat)
                lighting_flat.hide_render = False
                lighting_flat.hide_viewport = False
                print(f"         ✅ Enabled lighting_flat collection")
            else:
                print("         ⚠️ lighting_flat collection not found!")
            if lighting_fancy:
                lighting_fancy.hide_render = True
                lighting_fancy.hide_viewport = True
                print(f"         ❌ Disabled lighting_fancy collection")
            
            # Force view layer update after lighting changes
            bpy.context.view_layer.update()
            
            # Set playside rotation on topmost parent (0,0,0)
            for obj in objects_to_render:
                try:
                    target = obj
                    while target.parent:
                        target = target.parent
                    target.rotation_mode = 'XYZ'
                    target.rotation_euler = (0, 0, 0)
                except:
                    pass
            
            bpy.context.view_layer.update()
            playside_path = os.path.join(render_dir, f"{folder_key}_blade_flat_playside_{texture_name.split('_')[-1]}.png")
            print(f"         🎬 Rendering blade_flat playside: {playside_path}")
            render_and_save(playside_path)

            # Set backside rotation on topmost parent (0,0,180)
            for obj in objects_to_render:
                try:
                    target = obj
                    while target.parent:
                        target = target.parent
                    target.rotation_mode = 'XYZ'
                    target.rotation_euler = (0, 0, math.radians(180))
                except:
                    pass
            
            bpy.context.view_layer.update()
            backside_path = os.path.join(render_dir, f"{folder_key}_blade_flat_backside_{texture_name.split('_')[-1]}.png")
            print(f"         🎬 Rendering blade_flat backside: {backside_path}")
            render_and_save(backside_path)

            # === Swap to *_blade_mask materials ===
            # Find object with blade material (not just "blade" in object name)
            blade_obj = None
            for obj in objects_to_render:
                try:
                    if obj.data and obj.data.materials:
                        for mat in obj.data.materials:
                            if mat and "blade" in mat.name.lower():
                                blade_obj = obj
                                break
                        if blade_obj:
                            break
                except:
                    continue
            
            # Fallback to old method if no blade material found
            if not blade_obj:
                for obj in objects_to_render:
                    try:
                        if "blade" in obj.name.lower():
                            blade_obj = obj
                            break
                    except:
                        continue
            
            if not blade_obj:
                print("      ⚠️ No blade object found for mask rendering.")
                continue

            # Store original materials
            original_materials = []
            try:
                original_materials = blade_obj.data.materials[:]
            except:
                print("      ⚠️ Could not access blade object materials")
                continue
                
            mask_mat = bpy.data.materials.get("weapon_knife_karambit_blade_mask")
            if not mask_mat:
                print("      ❌ 'weapon_knife_karambit_blade_mask' material not found, skipping mask render.")
                continue
                
            # Apply mask material
            try:
                for i in range(len(blade_obj.data.materials)):
                    blade_obj.data.materials[i] = mask_mat
            except:
                print("      ⚠️ Could not apply mask material")
                continue

            # === Render mask material with flat lighting (mask_flat) ===
            # Set lighting for mask renders (flat lighting)
            print("      💡 Switching to flat lighting for mask_flat renders...")
            if lighting_flat:
                ensure_lighting_in_view_layer(lighting_flat)
                lighting_flat.hide_render = False
                lighting_flat.hide_viewport = False
                print(f"         ✅ Enabled lighting_flat collection")
            if lighting_fancy:
                lighting_fancy.hide_render = True
                lighting_fancy.hide_viewport = True
                print(f"         ❌ Disabled lighting_fancy collection")
            
            # Force view layer update after lighting changes
            bpy.context.view_layer.update()
            
            # Set playside rotation on topmost parent (0,0,0)
            for obj in objects_to_render:
                try:
                    target = obj
                    while target.parent:
                        target = target.parent
                    target.rotation_mode = 'XYZ'
                    target.rotation_euler = (0, 0, 0)
                except:
                    pass
            
            bpy.context.view_layer.update()
            playside_path = os.path.join(render_dir, f"{folder_key}_mask_playside_{texture_name.split('_')[-1]}.png")
            print(f"         🎬 Rendering mask_flat playside: {playside_path}")
            render_and_save(playside_path)

            # Set backside rotation on topmost parent (0,0,180)
            for obj in objects_to_render:
                try:
                    target = obj
                    while target.parent:
                        target = target.parent
                    target.rotation_mode = 'XYZ'
                    target.rotation_euler = (0, 0, math.radians(180))
                except:
                    pass
            
            bpy.context.view_layer.update()
            backside_path = os.path.join(render_dir, f"{folder_key}_mask_backside_{texture_name.split('_')[-1]}.png")
            print(f"         🎬 Rendering mask_flat backside: {backside_path}")
            render_and_save(backside_path)

            # Restore original materials
            try:
                for i in range(len(original_materials)):
                    blade_obj.data.materials[i] = original_materials[i]
            except:
                print("      ⚠️ Could not restore original materials")

            # Restore original rotations for topmost parent objects
            for target in original_rotations:
                try:
                    target.rotation_mode = original_rotations[target]['rotation_mode']
                    target.rotation_euler = original_rotations[target]['rotation_euler']
                except:
                    pass
            
            # Restore original lighting states
            if lighting_fancy and 'fancy' in lighting_states:
                try:
                    lighting_fancy.hide_render = lighting_states['fancy']['hide_render']
                    lighting_fancy.hide_viewport = lighting_states['fancy']['hide_viewport']
                except:
                    pass
            if lighting_flat and 'flat' in lighting_states:
                try:
                    lighting_flat.hide_render = lighting_states['flat']['hide_render']
                    lighting_flat.hide_viewport = lighting_states['flat']['hide_viewport']
                except:
                    pass
            
            bpy.context.view_layer.update()

            # Clean up memory after each texture
            cleanup_memory()
            
            print(f"      ✅ Completed texture: {texture_name} - 6 renders generated")
        
        # End of texture loop
        processed_count += 1
        print(f"✅ Completed weapon: {weapon_name} - All {len(texture_files)} textures processed ({processed_count}/{len(target_weapons)})")
        
        # Force a brief pause to let memory settle
        if processed_count % 3 == 0:
            print("🧹 Performing additional cleanup...")
            bpy.context.view_layer.update()
            
    except Exception as e:
        print(f"❌ Error processing {weapon_name}: {str(e)}")
        print(f"   Continuing with next weapon...")
        
        # Clean up memory even on error
        cleanup_memory()
        continue

# Calculate total textures processed
total_textures_processed = 0
for weapon_name in target_weapons:
    folder_key = weapon_to_folder_key(weapon_name)
    texture_folder = os.path.join(texture_base_dir, f"weapon_{folder_key}")
    if os.path.exists(texture_folder):
        texture_files = [f for f in os.listdir(texture_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        total_textures_processed += len(texture_files)

print(f"✅ Done: Processed {processed_count} weapons with {total_textures_processed} total textures. Generated {total_textures_processed * 6} total renders (blade_fancy, blade_flat, mask_flat).")
