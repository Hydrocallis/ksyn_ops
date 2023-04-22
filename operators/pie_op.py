import bpy,sys

from bpy.types import (
        Operator,
        )

from ..utils.get_translang import get_translang

class AutoSommth(Operator):
    bl_idname = "object.pie10_operator"
    bl_label = "スムーズ"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    sommth : bpy.props.BoolProperty(name=get_translang('Sommth','スムース'),default=True)
    auto_sommth_bool : bpy.props.BoolProperty(name=get_translang('Auto Smooth','Auto Smooth'),default=True)
    auto_smooth_angle : bpy.props.FloatProperty(name=get_translang('Angle','Angle'),
                                                subtype='ANGLE',
                                                default=0.523599)

    def execute(self, context):
        if self.sommth ==True:
            bpy.ops.object.shade_smooth()
        else:
            bpy.ops.object.shade_flat()

        for obj in bpy.context.selected_objects:
            if obj.type =="MESH":
                if self.auto_sommth_bool ==True:
                    obj.data.use_auto_smooth = True
                else:
                    obj.data.use_auto_smooth = False
                obj.data.auto_smooth_angle = self.auto_smooth_angle



        


        return {'FINISHED'}

class Setting(Operator):
    bl_idname = "object.pie11_operator"
    bl_label = get_translang("Setting","設定")
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        # obj = bpy.context.active_object
        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers["WinMan"].addon_search = sys.modules['ksyn_ops'].bl_info.get("name")
        # print('###',sys.modules[__package__].bl_info.get("version", (-1,-1,-1)))
        return {'FINISHED'}
