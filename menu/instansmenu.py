import bpy, sys

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

class PIE_MT_InstansMenu(Menu):
    bl_idname = "PIE_MT_InstansMenu"
    bl_label = "PIE_MT_InstansMenu"
    bl_description = "オブジェクトを並進移動します"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "



    def draw(self, context):
        layout = self.layout
        props = context.scene.myedit_property_group

        # サブメニューの登録
        layout.operator("object.objectinstansmirror_operator", text="オブジェクトのミラー化", icon="MOD_MIRROR")
        layout.operator("object.objectinstans_operator", text="インスタンス化", icon="OUTLINER_OB_GROUP_INSTANCE")
        layout.separator()
        layout.operator("object.cleanupinstans_operator", text="クリーンアップ", icon="FILE_REFRESH")
        layout.separator()
        layout.popover("PIE3D_PT_PIESettiongOp", text = "セッティング", icon='TOOL_SETTINGS')
        # layout.prop(props, "transform_axis")


