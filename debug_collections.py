import bpy

print("=== DEBUG: Collections and Objects ===")

# List all collections
print("\n📁 All Collections:")
for collection in bpy.data.collections:
    print(f"  - {collection.name}")

# Check for CS2 Knives collection
knife_collection = bpy.data.collections.get("CS2 Knives")
if knife_collection:
    print(f"\n✅ Found 'CS2 Knives' collection")
    print(f"   Children: {[c.name for c in knife_collection.children]}")
    
    # Check each weapon collection
    for weapon_name in ["Karambit", "Bayonet"]:
        weapon_col = knife_collection.children.get(weapon_name)
        if weapon_col:
            print(f"\n🔪 {weapon_name} collection:")
            print(f"   Objects: {[obj.name for obj in weapon_col.all_objects]}")
            print(f"   Mesh objects: {[obj.name for obj in weapon_col.all_objects if obj.type == 'MESH']}")
            print(f"   Visible mesh objects: {[obj.name for obj in weapon_col.all_objects if obj.type == 'MESH' and obj.visible_get()]}")
            
            # Check individual object visibility
            for obj in weapon_col.all_objects:
                if obj.type == 'MESH':
                    print(f"   Object '{obj.name}': visible_get()={obj.visible_get()}, hide_viewport={obj.hide_viewport}, hide_render={obj.hide_render}")
            
            # Check view layer visibility
            print(f"   View layer children: {[c.name for c in bpy.context.view_layer.layer_collection.children]}")
            
            # Check if collection is in view layer
            for layer_col in bpy.context.view_layer.layer_collection.children:
                if layer_col.name == "CS2 Knives":
                    print(f"   CS2 Knives in view layer: {layer_col.name}")
                    for child in layer_col.children:
                        if child.name == weapon_name:
                            print(f"   {weapon_name} in view layer: {child.name}")
                            print(f"   {weapon_name} hide_viewport: {child.hide_viewport}")
        else:
            print(f"\n❌ {weapon_name} collection not found")
else:
    print("\n❌ 'CS2 Knives' collection not found")

# Check view layer structure
print(f"\n👁️ View Layer Structure:")
for layer_col in bpy.context.view_layer.layer_collection.children:
    print(f"  - {layer_col.name}")
    for child in layer_col.children:
        print(f"    - {child.name}")

# Check scene collection
print(f"\n🎬 Scene Collection:")
for collection in bpy.context.scene.collection.children:
    print(f"  - {collection.name}")

print("\n=== END DEBUG ===") 