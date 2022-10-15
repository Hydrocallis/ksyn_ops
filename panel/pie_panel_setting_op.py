import bpy

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

# fbx出力関連


class PIE3D_PT_PIESettiongOp(Panel):
    bl_label = "PIE3D_PT_PIESettiongOp"
    bl_idname = "PIE3D_PT_PIESettiongOp"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    


    def draw(self, context):
        layout = self.layout
        props = context.scene.myedit_property_group
        layout.prop(props, "transform_axis")






        