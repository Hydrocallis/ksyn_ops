
import bpy, sys, os, subprocess

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


class PIE3D_OT_uv_seleobjsmartuv(Operator):
    bl_idname = 'object.uv_seleobjsmartuv'
    bl_label = 'uv_seleobjsmartuv'
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        selobj = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')

        for obj in selobj:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.smart_project()
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.select_set(False)

        return {'FINISHED'}

    @classmethod
    def poll(self, context):
        return True
      
