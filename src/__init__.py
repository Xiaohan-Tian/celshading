import bpy
from bpy.types import * 
from mathutils import *
from math import *


bl_info = {
    "name": "Rasqui's Simple CelShading ${version}",
    "description": "A simple celshading add-on designed for Blender 3.4+",
    "author": "Rasqui",
    "version": (0, 2, 2),
    "blender": (3, 40, 0),
}


const = {
    "stage": "_dev"
}


def del_mat_node(mat, node_name):
    if node_name in mat.node_tree.nodes:
        node_to_delete =  mat.node_tree.nodes[node_name]
        if node_to_delete is not None:
            mat.node_tree.nodes.remove(node_to_delete)
    

def find_mat_node_by_type(mat, type):
    for node in mat.node_tree.nodes:
        if node.type == type:
            return node
    return None


def find_mat_node_by_name(mat, node_name):
    if node_name in mat.node_tree.nodes:
        node_target =  mat.node_tree.nodes[node_name]
        if node_target is not None:
            return node_target
    return None


def remove_until_last(list):
    while len(list) > 1:
        list.remove(list[0])


def find_bbox(vertices):
    vmin = Vector((vertices[0].x, vertices[0].y, vertices[0].z))
    vmax = Vector((vertices[0].x, vertices[0].y, vertices[0].z))
    for vert in vertices:
        if vert.x > vmax.x: 
            vmax.x = vert.x
        if vert.y > vmax.y: 
            vmax.y = vert.y
        if vert.z > vmax.z: 
            vmax.z = vert.z
        if vert.x < vmin.x: 
            vmin.x = vert.x
        if vert.y < vmin.y: 
            vmin.y = vert.y
        if vert.z < vmin.z: 
            vmin.z = vert.z  
    return [vmin, vmax]


def find_available_name(prefix):
    i = 1
    while prefix + "." + str(i).zfill(3) in bpy.context.scene.objects:
        i = i + 1
    return prefix + "." + str(i).zfill(3)


def select_object_by_name(name):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[name]


def convert_to_cel_shading_mat(so):
    mat_target = so.data.materials[0]
    # print(mat_target.name)
    mat_nodes = mat_target.node_tree.nodes
    mat_links = mat_target.node_tree.links

    base_color = (1.0, 1.0, 1.0, 1.0)
    node_img = find_mat_node_by_type(mat_target, "TEX_IMAGE")
    simple_color = False
    if node_img is None:
        simple_color = True

        node_bsdf_principled = find_mat_node_by_type(mat_target, "BSDF_PRINCIPLED")
        base_color = node_bsdf_principled.inputs['Base Color'].default_value

        node_img = mat_nodes.new(type='ShaderNodeRGB')
        node_img.outputs[0].default_value = base_color

    del_mat_node(mat_target, "Principled BSDF")

    # Create Nodes
    node_diffuse = mat_nodes.new(type="ShaderNodeBsdfDiffuse")
    node_diffuse.location = Vector((-501, 1595))

    node_shaderToColor = mat_nodes.new(type="ShaderNodeShaderToRGB")
    node_shaderToColor.location = Vector((-275, 1595))

    node_colorRamp = mat_nodes.new(type="ShaderNodeValToRGB")
    node_colorRamp.location = Vector((-50, 1595))
    remove_until_last(node_colorRamp.color_ramp.elements)
    node_colorRamp.color_ramp.interpolation = "CONSTANT"
    node_colorRamp.color_ramp.elements.new(0.0)
    node_colorRamp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    node_colorRamp.color_ramp.elements[1].position = 0.205
    node_colorRamp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 0.0)

    node_hsv = mat_nodes.new(type="ShaderNodeHueSaturation")
    node_hsv.location = Vector((-501, 1385))
    node_hsv.inputs[0].default_value = 0.5 # Hue
    node_hsv.inputs[1].default_value = 1.2 # Saturation
    node_hsv.inputs[2].default_value = 1.0 # Value
    node_hsv.inputs[3].default_value = 1.0 # Fac

    node_trans_cel = mat_nodes.new(type="ShaderNodeBsdfTransparent")
    node_trans_cel.location = Vector((-275, 1299))
    node_trans_cel.name = "Transparent BSDF.Cel"

    node_mixs_cel = mat_nodes.new(type="ShaderNodeMixShader")
    node_mixs_cel.location = Vector((275, 1430))
    node_mixs_cel.name = "Mix Shader.Cel"

    node_mixs_tex = mat_nodes.new(type="ShaderNodeMixShader")
    node_mixs_tex.location = Vector((505, 1280))
    node_mixs_tex.name = "Mix Shader.Tex"
    node_mixs_tex.inputs[0].default_value = 0.9

    node_trans_main = mat_nodes.new(type="ShaderNodeBsdfTransparent")
    node_trans_main.location = Vector((-50, 1152))
    node_trans_main.name = "Transparent BSDF.Main"

    node_mixs_main = mat_nodes.new(type="ShaderNodeMixShader")
    node_mixs_main.location = Vector((700, 1152))
    node_mixs_main.name = "Mix Shader.Main"

    node_out = find_mat_node_by_type(mat_target, "OUTPUT_MATERIAL")
    node_out.location = Vector((900, 1152))

    # node_img = find_mat_node_by_type(mat_target, "TEX_IMAGE")
    node_img.location = Vector((-860, 1280))

    # Connect Nodes
    mat_links.new(node_diffuse.outputs[0], node_shaderToColor.inputs[0])
    mat_links.new(node_shaderToColor.outputs[0], node_colorRamp.inputs[0])
    mat_links.new(node_colorRamp.outputs[0], node_mixs_cel.inputs[2])
    mat_links.new(node_colorRamp.outputs[1], node_mixs_cel.inputs[0])
    mat_links.new(node_trans_cel.outputs[0], node_mixs_cel.inputs[1])
    mat_links.new(node_img.outputs[0], node_hsv.inputs[4])
    mat_links.new(node_hsv.outputs[0], node_mixs_tex.inputs[2])
    mat_links.new(node_mixs_cel.outputs[0], node_mixs_tex.inputs[1])
    mat_links.new(node_img.outputs[0 if simple_color else 1], node_mixs_main.inputs[0])
    mat_links.new(node_trans_main.outputs[0], node_mixs_main.inputs[1])
    mat_links.new(node_mixs_tex.outputs[0], node_mixs_main.inputs[2])
    mat_links.new(node_mixs_main.outputs[0], node_out.inputs[0])


def convert_to_emission_shading(so):
    mat_target = so.data.materials[0]
    # print(mat_target.name)
    mat_nodes = mat_target.node_tree.nodes
    mat_links = mat_target.node_tree.links

    del_mat_node(mat_target, "Principled BSDF")

    # Create Nodes
    node_trans_main = mat_nodes.new(type="ShaderNodeBsdfTransparent")
    node_trans_main.location = Vector((-50, 1152))
    node_trans_main.name = "Transparent BSDF.Main"

    node_mixs_main = mat_nodes.new(type="ShaderNodeMixShader")
    node_mixs_main.location = Vector((700, 1152))
    node_mixs_main.name = "Mix Shader.Main"

    node_out = find_mat_node_by_type(mat_target, "OUTPUT_MATERIAL")
    node_out.location = Vector((900, 1152))

    node_img = find_mat_node_by_type(mat_target, "TEX_IMAGE")
    node_img.location = Vector((-860, 1280))

    # Connect Nodes
    mat_links.new(node_img.outputs[0], node_mixs_main.inputs[2])
    mat_links.new(node_img.outputs[1], node_mixs_main.inputs[0])
    mat_links.new(node_trans_main.outputs[0], node_mixs_main.inputs[1])
    mat_links.new(node_mixs_main.outputs[0], node_out.inputs[0])


def create_outline(so, thickness=-0.005, clamp=1.9, welded=False):
    mat_target = so.data.materials[0]
    # print(mat_target.name)
    mat_nodes = mat_target.node_tree.nodes
    mat_links = mat_target.node_tree.links

    # create material if needed
    mat_outline = None

    if "_RASQUIRef.Mat.Outline" in bpy.data.materials:
        mat_outline = bpy.data.materials["_RASQUIRef.Mat.Outline"]
    else:
        # create nodes
        mat_outline = bpy.data.materials.new(name="_RASQUIRef.Mat.Outline")
        mat_outline.use_nodes = True # use nodes material
        mat_outline.use_backface_culling = True
        mat_outline.shadow_method = 'NONE'
        mat_nodes = mat_outline.node_tree.nodes

        del_mat_node(mat_outline, "Principled BSDF")

        node_color = mat_nodes.new(type="ShaderNodeRGB")
        node_color.location = Vector((39.0, 293.0))
        node_color.outputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

        node_out = find_mat_node_by_type(mat_outline, "OUTPUT_MATERIAL")
        node_out.location = Vector((263.0, 293.0))

        # create link
        mat_outline.node_tree.links.new(node_color.outputs[0], node_out.inputs[0])

    # append outline material to 2nd slot
    so.data.materials.append(mat_outline)
    
    # add modifier "weld"
    mod_weld = None
    if welded:
        mod_weld = so.modifiers.new(name="Weld", type="WELD")
        bpy.ops.mesh.customdata_custom_splitnormals_clear()

    # add modifier "solidify"
    mod_solid = so.modifiers.new(name="Outline", type="SOLIDIFY") 
    mod_solid.thickness = thickness
    mod_solid.use_rim = False
    mod_solid.use_flip_normals = True
    mod_solid.material_offset = 1
    mod_solid.thickness_clamp = clamp


def create_normal_ref(so):
    target_obj = so
    vertices = so.data.vertices
    vertices_computed = [so.matrix_world @ vert.co for vert in vertices]

    bbox = find_bbox(vertices_computed)
    center = (bbox[0] + bbox[1]) / 2.0
    bbox_delta = bbox[0] - bbox[1]
    max_delta = max([abs(bbox_delta.x), abs(bbox_delta.y), abs(bbox_delta.z)])

    # set cursor to center
    bpy.context.scene.cursor.location = center

    # create ref normal sphere
    bpy.ops.mesh.primitive_uv_sphere_add()
    so = bpy.context.active_object
    ref_obj = bpy.context.active_object
    so.name = find_available_name("_RASQUIRef.Obj.Ref.Normal")
    so.scale = (max_delta / 2.0, max_delta / 2.0, max_delta / 2.0)

    # shade smooth
    for face in so.data.polygons:
        face.use_smooth = True

    bpy.data.meshes[so.data.name].use_auto_smooth = True
    bpy.data.meshes[so.data.name].auto_smooth_angle = radians(30)

    # apply subdivision modifier
    so.modifiers.new(name="Subdivision", type="SUBSURF")
    so.modifiers["Subdivision"].levels = 4
    so.modifiers["Subdivision"].render_levels = 4

    # hide viewport and render
    so.hide_viewport = True
    so.hide_render = True

    # normal transfer
    select_object_by_name(target_obj.name)
    so = bpy.context.active_object
    so.modifiers.new(name="Normal Transfer", type="DATA_TRANSFER")
    so.modifiers["Normal Transfer"].object = ref_obj
    so.modifiers["Normal Transfer"].use_loop_data = True
    so.modifiers["Normal Transfer"].data_types_loops = {"CUSTOM_NORMAL"}


def auto_shading_for_vroid_created_model(welded=False):
    parent_obj = bpy.context.active_object 
    for child in parent_obj.children:
        select_object_by_name(child.name)
        so = bpy.context.active_object
        
        # ignore if current object is hidden
        if so is None:
            continue
        
        print(so.name)
        
        if so.name.find("_Body_") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
            print("...apply outline")
            create_outline(so, welded=welded)
        elif so.name.find("_EyeWhite_") > 0:
            print("...apply emissionshading")
            convert_to_emission_shading(so)
            print("...apply outline")
            create_outline(so, welded=welded)
        elif so.name.find("_Face_") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
            print("...apply outline, thickness=-0.015, clamp=1.3")
            create_outline(so, thickness=-0.015, clamp=1.3, welded=welded)
            print("...apply face normal transfer")
            create_normal_ref(so)
        elif so.name.find("_FaceMouth_") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
        elif so.name.find("_HairBack_") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
        elif so.name.find("_Hair_") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
            print("...apply outline")
            create_outline(so, welded=welded)
        elif so.name.find("_Accessory_") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
            print("...apply outline")
            create_outline(so, welded=welded)
        elif so.name.find("_Tops_") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
            print("...apply outline")
            create_outline(so, welded=welded)
        elif so.name.find("_Shoes_") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
            print("...apply outline")
            create_outline(so, welded=welded)
        elif so.name.find("_EyeIris_") > 0:
            print("...apply emissionshading")
            convert_to_emission_shading(so)
        elif so.name.find("_FaceEyeline_") > 0:
            print("...apply emissionshading")
            convert_to_emission_shading(so)
        elif so.name.find("_FaceBrow_") > 0:
            print("...apply emissionshading")
            convert_to_emission_shading(so)
        elif so.name.find("Cleaned") > 0:
            print("...apply celshading")
            convert_to_cel_shading_mat(so)
            print("...apply outline")
            create_outline(so, welded=welded)


# === ===  === ===  === ===  REGISTER BLENDER UI  === ===  === ===  === ===
class ConvertToCelShadingOp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "rasqui.convert_to_celshading" + const["stage"]
    bl_label = "Convert to CelShading Material"
    bl_options = {'REGISTER', 'UNDO'} # register Undo support

    @classmethod
    def poll(cls, context): # validate if we can perform current operation
        return context.active_object is not None

    def execute(self, context):
        # logic you want to execute
        convert_to_cel_shading_mat(bpy.context.active_object)
        return {'FINISHED'}
    
    
class ConvertToEmissionShadingOp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "rasqui.convert_to_emissionshading" + const["stage"]
    bl_label = "Convert to Emission Material"
    bl_options = {'REGISTER', 'UNDO'} # register Undo support

    @classmethod
    def poll(cls, context): # validate if we can perform current operation
        return context.active_object is not None

    def execute(self, context):
        # logic you want to execute
        convert_to_emission_shading(bpy.context.active_object)
        return {'FINISHED'}
    
    
class CreateOutlineOp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "rasqui.create_outline" + const["stage"]
    bl_label = "Create Outline"
    bl_options = {'REGISTER', 'UNDO'} # register Undo support

    @classmethod
    def poll(cls, context): # validate if we can perform current operation
        return context.active_object is not None

    def execute(self, context):
        # logic you want to execute
        create_outline(bpy.context.active_object)
        return {'FINISHED'}
    
    
class CreateWeldedOutlineOp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "rasqui.create_welded_outline" + const["stage"]
    bl_label = "Create Welded Outline"
    bl_options = {'REGISTER', 'UNDO'} # register Undo support

    @classmethod
    def poll(cls, context): # validate if we can perform current operation
        return context.active_object is not None

    def execute(self, context):
        # logic you want to execute
        create_outline(bpy.context.active_object, welded=True)
        return {'FINISHED'}
    
    
class CreateNormalRefOp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "rasqui.create_normal_ref" + const["stage"]
    bl_label = "Create Sphere Normal Reference"
    bl_options = {'REGISTER', 'UNDO'} # register Undo support

    @classmethod
    def poll(cls, context): # validate if we can perform current operation
        return context.active_object is not None

    def execute(self, context):
        # logic you want to execute
        create_normal_ref(bpy.context.active_object)
        return {'FINISHED'}
    
    
class AutoCelShadingForVRoidModel(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "rasqui.auto_celshading_for_vroid_model" + const["stage"]
    bl_label = "Auto Shading for VRoid Created Model"
    bl_options = {'REGISTER', 'UNDO'} # register Undo support

    @classmethod
    def poll(cls, context): # validate if we can perform current operation
        return True

    def execute(self, context):
        # logic you want to execute
        auto_shading_for_vroid_created_model(welded=False)
        return {'FINISHED'}
    
    
class AutoCelShadingForVRoidModelWithWeldedOutline(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "rasqui.auto_celshading_for_vroid_model_welded" + const["stage"]
    bl_label = "Auto Shading for VRoid Created Model w/Welded Outline"
    bl_options = {'REGISTER', 'UNDO'} # register Undo support

    @classmethod
    def poll(cls, context): # validate if we can perform current operation
        return True

    def execute(self, context):
        # logic you want to execute
        auto_shading_for_vroid_created_model(welded=True)
        return {'FINISHED'}
    
    
class RasquiCelShading(bpy.types.Panel):
    bl_label = "Rasqui's CelShading v${version}"
    bl_idname = "rasqui.cel_shading" + const["stage"]
    bl_space_type = "VIEW_3D" # will be in "3D Viewport" view
    bl_region_type = "UI"
    bl_category = "CelShading" # defines which tab on the right side will locate this panel. you can define a new name to set this panel to a new tab.
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("rasqui.convert_to_celshading" + const["stage"])
        
        row = layout.row()
        row.operator("rasqui.convert_to_emissionshading" + const["stage"])
        
        row = layout.row()
        row.operator("rasqui.create_outline" + const["stage"])
        
        row = layout.row()
        row.operator("rasqui.create_welded_outline" + const["stage"])
        
        row = layout.row()
        row.operator("rasqui.create_normal_ref" + const["stage"])
        
        row = layout.row()
        row.label(text="Experimental: ")
        
        row = layout.row()
        row.operator("rasqui.auto_celshading_for_vroid_model" + const["stage"])
        
        row = layout.row()
        row.operator("rasqui.auto_celshading_for_vroid_model_welded" + const["stage"])
        
        
def register():
    bpy.utils.register_class(ConvertToCelShadingOp)
    bpy.utils.register_class(ConvertToEmissionShadingOp)
    bpy.utils.register_class(CreateOutlineOp)
    bpy.utils.register_class(CreateWeldedOutlineOp)
    bpy.utils.register_class(CreateNormalRefOp)
    bpy.utils.register_class(AutoCelShadingForVRoidModel)
    bpy.utils.register_class(AutoCelShadingForVRoidModelWithWeldedOutline)
    bpy.utils.register_class(RasquiCelShading)
    
    
def unregister():
    bpy.utils.unregister_class(ConvertToCelShadingOp)
    bpy.utils.unregister_class(ConvertToEmissionShadingOp)
    bpy.utils.unregister_class(CreateOutlineOp)
    bpy.utils.unregister_class(CreateWeldedOutlineOp)
    bpy.utils.unregister_class(CreateNormalRefOp)
    bpy.utils.unregister_class(AutoCelShadingForVRoidModel)
    bpy.utils.unregister_class(AutoCelShadingForVRoidModelWithWeldedOutline)
    bpy.utils.unregister_class(RasquiCelShading)
    

if __name__ == "__main__":
    register()
    
    
# notes
# bpy.data.objects["_RASQUIRef.Obj.Ref.Normal.001"].hide_viewport = False
