import bpy,sys,inspect

from bpy.types import (
        Operator,
        )

from ..utils.get_translang import get_translang
from ..utils.operators_utils import description
from mathutils import Matrix
from math import radians

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
    bl_idname = "ksyn_ops.setting_operator"
    bl_label = get_translang("Setting","設定")
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        # obj = bpy.context.active_object
        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers["WinMan"].addon_search = sys.modules['ksyn_ops'].bl_info.get("name")
        # print('###',sys.modules[__package__].bl_info.get("version", (-1,-1,-1)))
        return {'FINISHED'}

class pie4(Operator):
    bl_idname = "object.pie4_operator"
    bl_label = "選択面以外非表示"
    bl_description = description(bl_idname)

    def execute(self, context):
        bpy.ops.mesh.hide(unselected=True)
        return {'FINISHED'}

class pie8(Operator):
    bl_idname = "object.pie8_operator"
    bl_label = "X軸90回転"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        obj = bpy.context.active_object
        obj.matrix_world @= Matrix.Rotation(radians(90), 4, 'X')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

class pie9(Operator):
    bl_idname = "object.pie9_operator"
    bl_label = "Y軸90回転"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        obj = bpy.context.active_object
        obj.matrix_world @= Matrix.Rotation(radians(90), 4, 'Y')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

class pie18(Operator):
    bl_idname = "object.pie18_operator"
    bl_label = "フラット面を選択"

    def execute(self, context):
        bpy.ops.mesh.faces_select_linked_flat()
        return {'FINISHED'}

class pie19(Operator):
    bl_idname = "object.pie19_operator"
    bl_label = "シームをクリア"

    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=True)
        return {'FINISHED'}

class pie20(Operator):
    bl_idname = "object.pie20_operator"
    bl_label = "シームをつける"

    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=False)
        return {'FINISHED'}

