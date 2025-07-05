import bpy
import os

# Export and texture base paths
export_dir = r"C:\Users\maxim\Documents\coding\skinscreenshots\test\export"
texture_base_dir = r"C:\Users\maxim\Documents\textures"
os.makedirs(export_dir, exist_ok=True)

# Weapons to process
target_weapons = [
    "Bayonet", "Bowie", "Butterfly", "Survival", "Classic", "Falchion", "Flip", "Gut", "Karambit",
    "Kukri", "M9", "Navaja", "Nomad", "Paracord", "Shadowdaggers", "Skeleton", "Stiletto", "Huntsman",
    "Talon", "Ursus", "AK-47", "Five-Seven"
]

# Normalize name to folder key
def weapon_to_folder_key(name):
    return name.lower().replace(" ", "")

# Main knife collection
knife_collection = bpy.data.collections.get("CS2 Knives")
if not knife_collection:
    raise Exception("Collection 'CS2 Knives' not found!")

# Keep light/camera collection active
static_col = bpy.data.collections.get("light")
if static_col:
    static_col.hide_render = False
    static_col.hide_viewport = False

def ensure_in_view_layer(collection):
    if collection.name not in [c.name for c in bpy.context.view_layer.layer_collection.children]:
        bpy.context.scene.collection.children.link(collection)

# Load and assign image to a specific shader node
def apply_texture_to_shader(image_path):
    if not os.path.exists(image_path):
        print(f"❌ Texture not found: {image_path}")
        return False

    loaded_image = bpy.data.images.load(image_path, check_existing=True)
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
        return False

    return True

# Loop through weapons
for weapon_name in target_weapons:
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

    for texture_file in texture_files:
        texture_path = os.path.join(texture_folder, texture_file)
        texture_name = os.path.splitext(texture_file)[0]

        print(f"🔧 Processing: {weapon_name} with texture {texture_name}")

        # Hide all weapons
        for col in knife_collection.children:
            col.hide_render = True
            col.hide_viewport = True

        # Unhide current weapon
        ensure_in_view_layer(knife_col)
        knife_col.hide_render = False
        knife_col.hide_viewport = False
        bpy.context.view_layer.update()

        # Select only visible mesh objects
        bpy.ops.object.select_all(action='DESELECT')
        objects_to_export = [
            obj for obj in knife_col.all_objects
            if obj.type == 'MESH' and obj.visible_get()
        ]
        for obj in objects_to_export:
            obj.select_set(True)

        if not objects_to_export:
            print(f"⚠️ No mesh objects for {weapon_name}, skipping.")
            continue

        bpy.context.view_layer.objects.active = objects_to_export[0]

        if not apply_texture_to_shader(texture_path):
            continue

        export_filename = f"{folder_key}_{texture_name.split('_')[-1]}.glb"
        export_path = os.path.join(export_dir, export_filename)

        bpy.ops.export_scene.gltf(
            filepath=export_path,
            export_format='GLB',
            use_selection=True,
            export_apply=True,
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=6
        )

        print(f"✅ Exported {weapon_name} with {texture_name} to {export_path}")

print("🎉 All weapons and textures exported.")
