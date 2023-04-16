import bpy

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


class MESH_OT_select_mesh_separate_operator(Operator):
    bl_idname = "object.select_mesh_separate_operator"
    bl_label = "Mesh Separate"
    bl_options = {'REGISTER', 'UNDO'}

    floatvector : bpy.props.FloatVectorProperty(
    name = "Length",
    default=(0, 0, 0),
    subtype='XYZ_LENGTH',
    )

    duplicate_move: bpy.props.BoolProperty(
                                name='Duplicate',
                                default=True,
                                )

    def execute(self, context):
        obj_name = bpy.context.active_object.name
        if self.duplicate_move == True:
            bpy.ops.mesh.duplicate_move()
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')
        obj2_name = bpy.context.selected_objects[-1].name

        bpy.ops.object.select_all(action='DESELECT')
        #　セパレートのオブジェクトのアクティブ化
        sepaob = bpy.context.scene.objects[obj2_name]  
        bpy.context.view_layer.objects.active = sepaob
        sepaob.select_set(True)

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.transform.translate(value= self.floatvector)


        return {'FINISHED'}
