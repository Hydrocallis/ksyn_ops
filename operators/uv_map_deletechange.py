import bpy, sys, os
from pathlib import Path


from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

class UvMapDeleteChange(Operator):
    bl_idname = 'object.uv_map_delete_change'
    bl_label = 'uv_map_delete_change'
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "

    def execute(self, context):
        seleobj = bpy.context.selected_objects
        for obj in seleobj:

            lay = obj.data.uv_layers
            actlay = obj.data.uv_layers.active
            # print('###1-0###', actlay)
            layname = obj.data.uv_layers.active.name
            # print('###0-0###', layname)
            lay.new(name="copynewuvlayer")
            lay.remove(actlay)
            obj.data.uv_layers["copynewuvlayer"].name = layname

        return {'FINISHED'}