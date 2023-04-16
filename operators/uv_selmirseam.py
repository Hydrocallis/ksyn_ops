
import bpy, sys, os, subprocess

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


class MESHUV_OT_uvsettingselmirseam(Operator):
    bl_idname = 'object.uv_selmirseam'
    bl_label = 'uv_selmirseam'
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    # 3Dで用のプロパティ
    enum_prop : bpy.props.EnumProperty(items=[('X', "X", "One",1), ('Y', "Y", "Two",2), ('Z', "Z", "Two",3)])
  
    def execute(self, context):
        props = context.scene.myedit_property_group
        bpy.ops.mesh.select_mirror(axis={self.enum_prop}, extend=True)
        bpy.ops.mesh.mark_seam(clear=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap()
        return {'FINISHED'}

    @classmethod
    def poll(self, context):
        return True
      
