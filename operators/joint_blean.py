import bpy

from bpy.props import BoolProperty,FloatVectorProperty
from bpy.types import Operator

class BooleanOperator(Operator):
    bl_idname = "object.boolean_operator"
    bl_label = "Boolean Operator"
    bl_options = {'REGISTER', 'UNDO'}

    
    hide_selected : BoolProperty(
        name="Hide Selected",
        description="Hide selected objects",
        default=False
    )


    location : FloatVectorProperty(
        name="Location",
        default=(0, 0, 0),
        subtype='TRANSLATION',
        size=3
    )
    def execute(self, context):
        # アクティブなオブジェクトを取得
        active_obj = bpy.context.active_object

        # 選択中のオブジェクトを取得（アクティブを除く）
        selected_objs = bpy.context.selected_objects
        selected_objs.remove(active_obj)

        # アクティブなオブジェクトを親として、選択中のオブジェクトを子にする
        for obj in selected_objs:
            
            obj.display_type = 'WIRE'
            obj.location = obj.location + self.location

            # ブーリアンモディファイを追加
            bool_mod = active_obj.modifiers.new(name=f"KSYN_JOINT_Boolean_{obj.name}", type='BOOLEAN')
            bool_mod.operation = 'UNION'
            bool_mod.solver = 'FAST'
            obj.name = obj.name + "_jont"


            # ブーリアンモディファイのオブジェクトを設定
            bool_mod.object = obj

        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        for obj in selected_objs:
            if self.hide_selected:
                obj.hide_set(True)

        return {'FINISHED'}