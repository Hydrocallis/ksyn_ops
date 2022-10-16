import bpy

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

# fbx出力関連
class SIMPLEFBXECPORT_PT_SETTINGFBXEXPORT(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "pie setting panel fbxexport"
    bl_idname = "SIMPLEFBXECPORT_PT_SETTINGFBXEXPORT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.simplefbxecport_propertygroup

        row = layout.row()
        # row.operator("object.getfbxinformation", text="ファイルの保存先を自動入力")
        row = layout.row()
        row.label(text = "save file path")
        row = layout.row()
        row.label(text = f" {props.workspace_path}")
        row = layout.row()
        row.label(text="※コレクショ名を優先")
        row = layout.row()
        
        row.prop(props, "fbx_blenderfilename__bool")
        row = layout.row()

        row.prop(props, "fbx_filename")
        row = layout.row()
        row.prop(props, "fbx_selectfilename_bool")
        row = layout.row()
        row.prop(props, "fbx_get_col_name_bool")

        row = layout.row()
        row.prop(props, "fbx_selectbool")
        row = layout.row()
        row.prop(props, "fbx_act_collection_bool")
        row = layout.row()
        
        row.prop(props, "fbx_name_replace_bool")
        row = layout.row()
        row.prop(props, "fbx_children_recursive")
        row = layout.row()
        row.prop(props, "clipstudio_body_modelset_bool")
        row = layout.row()
        row.prop(props, "workspace_fbxfolder_path")
        row = layout.row()
        row.prop(props, "workspace_fbxfolder_path_Collection")
        
        # FBXを出力する
        row = layout.row()
        row.operator("object.fbxexortsupport", text = "FBXを出力する")

        