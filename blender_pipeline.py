import bpy
import sys
import os

# Configuration
input_file = "C:/path/to/raw_splat2mesh.obj"
output_file = "C:/path/to/game_ready_room.glb"
decimation_ratio = 0.1  # Reduces polycount by 90%
texture_size = 4096     # 4K texture for environment detail

# 1. Clear default scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 2. Enable RTX GPU Compute for fast baking
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'OPTIX'
prefs.get_devices()
for d in prefs.devices:
    d.use = (d.type == 'OPTIX' and 'RTX' in d.name)

# 3. Import High-Poly Splat Mesh
bpy.ops.wm.obj_import(filepath=input_file)
high_poly = bpy.context.selected_objects[0]
high_poly.name = "Room_HighPoly"

# 4. Duplicate for Low-Poly target
bpy.ops.object.duplicate()
low_poly = bpy.context.active_object
low_poly.name = "Room_LowPoly"

# 5. Decimate the Low-Poly mesh
decimate_mod = low_poly.modifiers.new(name="Decimate", type='DECIMATE')
decimate_mod.ratio = decimation_ratio
bpy.ops.object.modifier_apply(modifier="Decimate")

# 6. Smart UV Project the Low-Poly mesh
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=1.15, margin_method='SCALED', island_margin=0.01)
bpy.ops.object.mode_set(mode='OBJECT')

# 7. Setup Material and Texture Node for Baking
mat = bpy.data.materials.new(name="Baked_Mat")
mat.use_nodes = True
low_poly.data.materials.append(mat)
nodes = mat.node_tree.nodes

# Create a new image for the bake
img = bpy.data.images.new("Room_Baked_Tex", width=texture_size, height=texture_size)
tex_node = nodes.new('ShaderNodeTexImage')
tex_node.image = img
tex_node.select = True
mat.node_tree.nodes.active = tex_node

# 8. Bake High to Low (Diffuse / Vertex Colors)
bpy.context.view_layer.objects.active = low_poly
high_poly.select_set(True)
low_poly.select_set(True)

bpy.context.scene.cycles.bake_type = 'DIFFUSE'
bpy.context.scene.render.bake.use_pass_direct = False
bpy.context.scene.render.bake.use_pass_indirect = False
bpy.context.scene.render.bake.use_selected_to_active = True
bpy.context.scene.render.bake.margin = 16

print("Starting OptiX Bake. This may take a moment...")
bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')

# 9. Pack texture and export to Game Engine format (.glb)
img.pack()
bpy.ops.object.select_all(action='DESELECT')
low_poly.select_set(True)

bpy.ops.export_scene.gltf(
    filepath=output_file,
    use_selection=True,
    export_format='GLB',
    export_materials='EXPORT',
    export_colors=False
)
print(f"Exported game-ready environment to {output_file}")
