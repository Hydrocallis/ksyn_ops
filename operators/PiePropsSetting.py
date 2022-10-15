
import bpy, sys, os, subprocess

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )



class PIE3D_OT_PiePropsSetting(Operator):
        bl_idname = 'object.pie_props_setting'
        bl_label = 'piepropssetting'
        # 自身のクラスの呼び出しにはSYSモジュールが必要
        bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
        
        # @classmethod
        # def poll(self, context):
        #     jsonlistdictsave=JsonListDictSave()
        #     mes=jsonlistdictsave.check_list()

        #     if "listok_dictng" == mes or mes == "nolist":
        #         return False
        #     else:
        #         return True
        
        
        def execute(self, context):
            return context.window_manager.invoke_popup(self)


        # def invoke(self, context, event):
        #     return context.window_manager.invoke_props_dialog(self)
            
        def draw(self, context):
            layout = self.layout
            props = context.scene.myedit_property_group

            row = layout.row()
            row.prop(props, "edit_int")
            row = layout.row()
            row.prop(props, "color_pic")
            row = layout.row()
            row.prop(props, "target_armature")
            row = layout.row()
            row.operator("object.amaturerestbool")
            row = layout.row()
            row.prop(props, "workspace_path")
            row = layout.row()
            row.prop(props, "fbx_selectbool")
            row = layout.row()
            row.prop(props, "fbx_act_collection_bool")
            row = layout.row()
            row.operator("object.fbxexortsupport")
            row = layout.row()
            row.popover("OBJECT_PT_piesetting")
