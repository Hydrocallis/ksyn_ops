
import bpy, sys, os, subprocess

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

from ..utils.orijin_set import orijinset



class PIE3D_OT_originset(Operator):
    """Tooltip"""
    bl_idname = "object.originset_oparetor"
    bl_label = "Select area set origin"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH')


    def draw(self, context):
        layout = self.layout
        
    def execute(self, context):
        orijinset()

        
   
        return {'FINISHED'}


