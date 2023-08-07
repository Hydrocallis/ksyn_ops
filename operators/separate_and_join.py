import bpy
from bpy.types import Operator, Panel
from bpy.props import IntProperty

# 分離と結合を行うオペレータ
class SeparateAndJoinOperator(Operator):
    bl_idname = "object.separate_and_join_operator"
    bl_label = "Separate and Join"
    bl_description = "Separate the selected object and join it back"
    bl_options = {'REGISTER', 'UNDO'}


    subdivision_level: IntProperty(
        name="Subdivision Level",
        description="Level of subdivision",
        default=1,
        min=0,
        max=6
        )

    def execute(self, context):
        # 選択したオブジェクトを取得
        selected_object = bpy.context.active_object

        # 選択したオブジェクトのメッシュを分離
        bpy.ops.mesh.separate(type='SELECTED')

        # 分離したオブジェクトのモディファイアを削除
        separated_objects = bpy.context.selected_objects[-1]
        separated_objects.modifiers.clear()

        # 分離先のオブジェクトにサブディビジョンモディファイアを追加
        separated_object = separated_objects
        bpy.context.view_layer.objects.active = separated_object
        subsurf_modifier = separated_object.modifiers.new(name='Subdivision', type='SUBSURF')
        subsurf_modifier.levels = self.subdivision_level

        # サブディビジョンモディファイアを適応
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.modifier_apply(modifier=subsurf_modifier.name)

        # 分離したオブジェクトを統合
        selected_object.select_set(True)
        separated_objects.select_set(True)
        bpy.context.view_layer.objects.active = selected_object
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.join()
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}