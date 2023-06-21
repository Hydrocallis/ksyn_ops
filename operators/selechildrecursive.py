import bpy
from ksyn_ops.utils.get_translang import get_translang

class SelectChildrenRecursiveOperator(bpy.types.Operator):
    bl_idname = "ksyn.select_children_recursive"
    bl_label = get_translang("Select Children Recursive","再帰的に子供を選択")
    bl_description = "Selects all child objects recusively"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 選択されたオブジェクトを取得
        selected_objects = bpy.context.selected_objects

        # 前に選択されていたオブジェクトを保持する辞書を作成
        prev_selected_objects = {}
        for obj in selected_objects:
            prev_selected_objects[obj.name] = [ch.name for ch in obj.children_recursive]

        # 選択した各オブジェクトの下の階層にあるオブジェクトを選択
        for obj in selected_objects:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')

        # 前に選択されていたオブジェクトを再選択
        for prev_obj_name, prev_children_names in prev_selected_objects.items():
            prev_obj = bpy.data.objects.get(prev_obj_name)
            if prev_obj:
                prev_obj.select_set(True)
                for ch_name in prev_children_names:
                    ch_obj = bpy.data.objects.get(ch_name)
                    if ch_obj:
                        ch_obj.select_set(True)

        return {'FINISHED'}