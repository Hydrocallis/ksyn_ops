import bpy, os , sys
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )

from bpy.props import (
                        StringProperty, 
                        IntProperty, 
                        FloatProperty, 
                        EnumProperty, 
                        BoolProperty,
                        PointerProperty,
                        FloatVectorProperty,
                        StringProperty
                        )

class PIE3D_OT_ViewShading(Operator):
    bl_idname = "object.viewshading"
    bl_label = "スタジのの表示設定"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    test_items = [
    ("1", "フラットテクスチャ", "", 1),
    ("2", "スタジオテクスチャ", "", 2),
    ("3", "テクスチャ無し", "", 3),
    ("4", "マテリアルビュー", "", 4),
    ("5", "オブジェクトビュー", "", 5),
        ]

    material_enum : bpy.props.EnumProperty(
        items=test_items,
        name='タイプ',

        )

    def execute(self, context):
        print('###',self.material_enum)
        if self.material_enum == "1":
            context.space_data.shading.type = 'SOLID'
            context.space_data.shading.light = 'FLAT'
            bpy.context.space_data.shading.color_type = 'TEXTURE'


        elif self.material_enum == "2":
            context.space_data.shading.type = 'SOLID'
            context.space_data.shading.light = 'STUDIO'
            bpy.context.space_data.shading.color_type = 'TEXTURE'


        elif self.material_enum == "3":
            context.space_data.shading.type = 'SOLID'
            context.space_data.shading.light = 'STUDIO'
            context.space_data.shading.color_type = 'MATERIAL'

        elif self.material_enum == "4":
            context.space_data.shading.type = 'MATERIAL'

        elif self.material_enum == "5":
            bpy.context.space_data.shading.type = 'SOLID'
            bpy.context.space_data.shading.light = 'STUDIO'
            bpy.context.space_data.shading.color_type = 'OBJECT'





        return {'FINISHED'}

    # def invoke(self, context, event):

    #     wm = context.window_manager
    #     return {'RUNNING_MODAL'}

class PIE3D_OT_ViewShadingShowFace(Operator):
    """Tooltip"""
    bl_idname = "object.viewshadingshowface_operator"
    bl_label = "フェイスの裏表切り替え"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "

    def execute(self, context):
        if  context.space_data.overlay.show_face_orientation == True:
            context.space_data.overlay.show_face_orientation = False
        else:
             context.space_data.overlay.show_face_orientation = True

        return {'FINISHED'}
