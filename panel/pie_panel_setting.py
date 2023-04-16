import bpy

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

        
class PIE3D_PT_PIESETTINGARM(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "pie Setting Armture"
    bl_idname = "OBJECT_PT_piesetting_arm"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"
    


    def draw(self, context):
        layout = self.layout
        props = context.scene.myedit_property_group


        row = layout.row()
        row.prop(props, "target_armature")
        row = layout.row()
        row.operator("object.amaturerestbool")



class PIE3D_PT_PIESETTING(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "pie Setting Colorpic"
    bl_options = {'DEFAULT_CLOSED'}
    bl_idname = "OBJECT_PT_piesetting"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"
    


    def draw(self, context):
        layout = self.layout
        props = context.scene.myedit_property_group


        row = layout.row()
        row.prop(props, "edit_int")
        row = layout.row()
        row.prop(props, "color_pic")


        row = layout.row()
        row.operator("object.uvgridmat")

        matname_list =[mat.name for mat in bpy.data.materials]
        matbool = "UVGRID" in matname_list
        row = layout.row()
        row.prop(props, "uv_grid_material_image_bool")
        if  matbool == True:
            row = layout.row()
            row.prop(props, "uv_grid_scail_size")
            row = layout.row()
            row.prop(props, "uv_grid_material_duplicate_bool")

        row = layout.row()
        row = layout.row()
        row.prop(props, "crease_themas_bool")
        row = layout.row()
        row.operator("object.uv_map_delete_change")     

        sel_objs = bpy.context.selected_objects
        for  sele_ob in sel_objs:
            obj_data = sele_ob.data
            row = layout.row()
            if sele_ob.type == "MESH": 
                row.label(text=sele_ob.name)
                row = layout.row()
                row.template_list("MESH_UL_uvmaps", "uvmaps", obj_data, "uv_layers", obj_data.uv_layers, "active_index", rows=2)





        