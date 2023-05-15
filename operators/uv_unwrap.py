
import bpy, sys, os, subprocess

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


class uv_Unwrap(Operator):
    bl_idname = 'object.uv_unwrap'
    bl_label = 'uv_unwrap'
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
  
  
    def execute(self, context):
        props = context.scene.myedit_property_group
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap()
        bpy.ops.mesh.select_all(action='DESELECT')
      

        return {'FINISHED'}