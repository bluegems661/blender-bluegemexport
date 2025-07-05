import bpy

print("=== DEBUG: Flip Knife Objects ===")

# Check for CS2 Knives collection
knife_collection = bpy.data.collections.get("CS2 Knives")
if knife_collection:
    flip_col = knife_collection.children.get("Flip")
    if flip_col:
        print(f"\n🔪 Flip knife collection objects:")
        for obj in flip_col.all_objects:
            if obj.type == 'MESH':
                print(f"  - {obj.name} (type: {obj.type})")
                print(f"    Materials: {[mat.name if mat else 'None' for mat in obj.data.materials]}")
                print(f"    Visible: {obj.visible_get()}")
        
        # Check which object would be selected as "blade"
        blade_obj = next((obj for obj in flip_col.all_objects if "blade" in obj.name.lower()), None)
        if blade_obj:
            print(f"\n✅ Found blade object: {blade_obj.name}")
        else:
            print(f"\n❌ No object with 'blade' in name found!")
            print("Available objects:")
            for obj in flip_col.all_objects:
                if obj.type == 'MESH':
                    print(f"  - {obj.name}")
    else:
        print("❌ Flip collection not found!")
else:
    print("❌ CS2 Knives collection not found!") 