import bpy, sys

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


class PIE_MT_InstansMenu2(Menu):
    bl_idname = "PIE_MT_InstansMenu2"
    bl_label = "PIE_MT_InstansMenu2"
    bl_description = ""
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "



    def draw(self, context):
        layout = self.layout
        props = context.scene.myedit_property_group

        layout.prop(props, "target_armature",text="")

        layout.operator("object.amaturerestbool",text="text")

        
        layout.prop(props, "edit_int")
        
        layout.prop(props, "color_pic")
       
        layout.operator("object.uvgridmat")

        matname_list =[mat.name for mat in bpy.data.materials]
        matbool = "UVGRID" in matname_list
        
        layout.prop(props, "uv_grid_material_image_bool")
        if  matbool == True:
            
            layout.prop(props, "uv_grid_scail_size")
            
            layout.prop(props, "uv_grid_material_duplicate_bool")
        
        
        layout.prop(props, "crease_themas_bool")
        
        layout.operator("object.uv_map_delete_change")     

        # sel_objs = bpy.context.selected_objects
        # for  sele_ob in sel_objs:
        #     obj_data = sele_ob.data
            
        #     if sele_ob.type == "MESH": 
        #         layout.label(text=sele_ob.name)
                
        #         layout.template_list("MESH_UL_uvmaps", "uvmaps", obj_data, "uv_layers", obj_data.uv_layers, "active_index", rows=2)





        




class PIE_MT_InstansMenu(Menu):
    bl_idname = "PIE_MT_InstansMenu"
    bl_label = "PIE_MT_InstansMenu"
    bl_description = "オブジェクトを並進移動します"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "



    def draw(self, context):
        layout = self.layout
        props = context.scene.myedit_property_group



