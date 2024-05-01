
import bpy,sys

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

from bpy.props import FloatProperty, IntProperty

try:
    from ..utils.get_translang import get_translang
except:
    from ksyn_ops.utils.get_translang import get_translang# type: ignore

class BevelProps:
         
    width: FloatProperty(
        name="Width",
        default=0.1,
        min=0.0,
        description="Width of the bevel"
    ) # type: ignore
    segments: IntProperty(
        name="Segments",
        default=3,
        min=1,
        description="Number of segments in the bevel"
    ) # type: ignore
        
# bpy.context.object.modifiers["Bevel"].width = 0.11 bpy.ops.object.modifier_add(type='BEVEL')
# bpy.context.object.modifiers["Bevel"].segments = 2
   
class Bevel(Operator,BevelProps):
    bl_idname = "object.selectobjectbevel_operator"
    bl_label = "Simple Boolean"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def add_or_modify_bevel_modifier(self, obj_name, width, segments):
        # 指定した名前のオブジェクトを取得する
        obj = bpy.data.objects.get(obj_name)
        if obj is None:
            print("指定された名前のオブジェクトが見つかりません。")
            return
        
        else:
            # Bevel モディファイアが既に存在するか確認する
            bevel_modifier = obj.modifiers.get("ksyn_Bevel")
            if bevel_modifier is None:
                # Bevel モディファイアを追加する
                bevel_modifier = obj.modifiers.new(name="ksyn_Bevel", type='BEVEL')
            else:
                # 既存の Bevel モディファイアの設定を変更する
                bevel_modifier.show_viewport = True

            # Bevel モディファイアの値を変更する
            bevel_modifier.width = width
            bevel_modifier.segments = segments


    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj_name = obj.name
            self.add_or_modify_bevel_modifier(obj_name, self.width, self.segments)


        return {'FINISHED'}


import bpy

# カスタムプロパティを保持するクラスを定義
class MyObjectProperties(bpy.types.PropertyGroup):
    # プロパティのゲット関数
    def get_bevel_width(self):
        obj = bpy.context.object
        if obj and obj.type == 'MESH':
            if obj.modifiers.get("ksyn_Bevel"):
                return obj.modifiers["ksyn_Bevel"].width
        return 0.0

    def get_bevel_segments(self):
        obj = bpy.context.object
        if obj and obj.type == 'MESH':
            if obj.modifiers.get("ksyn_Bevel"):
                return obj.modifiers["ksyn_Bevel"].segments
        return 0

    # プロパティのセット関数
    def set_bevel_width(self, value):
        obj = bpy.context.object
        if obj and obj.type == 'MESH':
            if obj.modifiers.get("ksyn_Bevel"):
                obj.modifiers["ksyn_Bevel"].width = value

    def set_bevel_segments(self, value):
        obj = bpy.context.object
        if obj and obj.type == 'MESH':
            if obj.modifiers.get("ksyn_Bevel"):
                obj.modifiers["ksyn_Bevel"].segments = value

    bevel_width: bpy.props.FloatProperty(
        name="Bevel Width",
        description="Width of the bevel modifier",
        default=0.0,
        min=0.0,
        max=1.0,
        get=get_bevel_width, # ゲット関数を指定
        set=set_bevel_width  # セット関数を指定
    ) # type: ignore
    bevel_segments: bpy.props.IntProperty(
        name="Bevel Segments",
        description="Segments of the bevel modifier",
        default=0,
        min=0,
        max=10,
        get=get_bevel_segments, # ゲット関数を指定
        set=set_bevel_segments  # セット関数を指定
    ) # type: ignore

# パネルを定義
# パネルを定義する
class BevelSettingsPanel(bpy.types.Panel):
    bl_label = "Bevel Settings"
    bl_idname = "OBJECT_PT_bevel_settings_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'KSYN'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.selectobjectbevel_operator", text="Add/Modify Bevel Modifier")

        obj = bpy.context.object
        obj_props = obj.my_object_properties

        if obj is not None and obj.type == 'MESH':
            if obj.modifiers.get("ksyn_Bevel"):
                layout.prop(obj_props, "bevel_width")
                layout.prop(obj_props, "bevel_segments")

# クラスを登録
classes = (
    MyObjectProperties,
)

def mod_status_register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.my_object_properties = bpy.props.PointerProperty(type=MyObjectProperties)

def mod_status_unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.my_object_properties


