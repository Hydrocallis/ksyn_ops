import bpy

class MoveSelectedToLastOperator(bpy.types.Operator):
    bl_idname = "object.move_selected_to_last"
    bl_label = "Move Selected to Last"
    bl_description = "Move selected objects to the position of the last selected object"

    def execute(self, context):
        # 最後に選択したオブジェクトを取得
        last_selected = context.object

        # 選択されたオブジェクトを移動する
        for obj in context.selected_objects:
            if obj != last_selected:
                obj.location = last_selected.location

        return {'FINISHED'}