import bpy, sys, os
from pathlib import Path


from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

class UVGRIDMATAdd():
    
    def __init__(self,obj):
        props = bpy.context.scene.myedit_property_group
        self.matname = "UVGRID"
        self.active_obj = obj
        filepath = Path(__file__).parent
        # print("###filepath", filepath)
        filepath /= '../tectures'
        # print("###filepath2", filepath)
        if props.uv_grid_material_image_bool == False:
            self.grid_tex_path = os.path.join(filepath, "uv_grid.png")
        else:
            self.grid_tex_path = os.path.join(filepath, "color_grid.png")
        # print('###',self.grid_tex_path)


    def material_nodes_set(self):
            # Create a material
        material = bpy.data.materials.new(name= self.matname ) 
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        # Reuse the material output node that is created by default
        material_output = nodes.get("Material Output")
        bsdf = nodes.get("Principled BSDF") 


        # Create Image Texture node and load the displacement texture.
        # You need to add the actual path to the texture.
#       # https://docs.blender.org/api/current/bpy.types.Node.html#bpy.types.Node..
        grid_tex = nodes.new("ShaderNodeTexImage")
        grid_tex.image = bpy.data.images.load(self.grid_tex_path)
        grid_tex.image.colorspace_settings.name = "Non-Color"
        grid_tex.location = (-300, 300)
        # print('###0-0###', grid_tex)

       # Create the Texture mapping node
        tex_mapping = nodes.new("ShaderNodeMapping")
        tex_mapping.location = (-500, 300)
        tex_mapping.name = "cus-Mapping"

        # print('###',tex_mapping.inputs[3].default_value)

        # Create the Texture Coordinate node
        tex_coordinate = nodes.new("ShaderNodeTexCoord")
        tex_coordinate.location = (-700, 300)


        # Connect the Texture Coordinate node to the displacement texture.
        # This uses the active UV map of the object.
        links.new(grid_tex.inputs["Vector"], tex_mapping.outputs["Vector"])
        
        links.new(tex_mapping.inputs["Vector"], tex_coordinate.outputs["UV"])

        # Connect the displacement texture to the Displacement node
        links.new(bsdf.inputs["Base Color"], grid_tex.outputs["Color"])
        self.grid_tex =grid_tex
        
        
        return (nodes, bsdf, grid_tex, tex_mapping, tex_coordinate, material, tex_mapping.inputs[3].default_value)
    

    def material_make(self):   
        
        materialset = self.material_nodes_set()     
        # parent を設定すればフレームの中にノードを入れられる。
        # https://dskjal.com/blender/process-node-from-python.html
        frame = materialset[0].new(type='NodeFrame')
        frame.name = "GRIDTEXFRAME"
        frame.label = "GRIDTEXFRAME"
        
        materialset[1].parent = frame
        materialset[2].parent = frame
        materialset[3].parent = frame
        materialset[4].parent = frame
        
        # Pythonを介してノードエディタでノードを選択します
        # https://blenderartists.org/t/select-node-in-node-editor-via-python/1210423
        materialset[0].active = frame

        return materialset[5]
    
    
    
    def act_obj_addmat(self):
        # Get the active object
        # print('###0-2###', material)
        # Check if the active object has a material slot, create one if it doesn't. 
        # Assign the material to the first slot for the active object.
        
        material = self.material_make()
        
        if self.active_obj.material_slots:
            self.active_obj.material_slots[0].material = material
        else:
            self.active_obj.data.materials.append(material)
            # print('###',material.name)
        return material.name


    def check_materialdata(self):
        matname_list =[mat.name for mat in bpy.data.materials]
        #print('###0-0###', matname_list)
        #print(matname_list)

        matbool = self.matname in matname_list
        #print('###0-0###', matbool)
     
        return matbool


    def girid_material_get(self,context):
        props = bpy.context.scene.myedit_property_group

        matbool = self.check_materialdata()

        if matbool == False:
            self.act_obj_addmat()
            mat = bpy.data.materials.get(self.matname)

        elif props.uv_grid_material_duplicate_bool == True:
            mat = self.act_obj_addmat()
            # print('###0-1###', mat)
            mat = bpy.data.materials.get(mat)
        elif matbool == True and props.uv_grid_material_duplicate_bool == False:
             mat = bpy.data.materials.get(self.matname)
             
        if self.active_obj.material_slots:
            self.active_obj.material_slots[0].material = mat
        else:
            self.active_obj.data.materials.append(mat)
        if context.space_data.shading.color_type != 'TEXTURE':
            context.space_data.shading.color_type = 'TEXTURE'



        
        
class UvGridMat(Operator):
    bl_idname = 'object.uvgridmat'
    bl_label = 'uvgridmat'
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            uv = UVGRIDMATAdd(obj)
            uv.girid_material_get(context)

        return {'FINISHED'}