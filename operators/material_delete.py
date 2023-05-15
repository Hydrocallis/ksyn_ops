
import bpy, sys, os, subprocess

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )




class MaterialDelete(Operator):
    bl_idname = "object.material_delete_operator"
    bl_label = "Delete Material"

    def execute(self, context):

        sel = context.selected_objects
        select_object_liset = []

        for ob in sel:
            if len(ob.material_slots.values()) !=0:
                print('###object name is ',ob.name)
                ob.data.materials.clear()
                #https://blender.stackexchange.com/questions/76828/how-to-apply-a-specific-modifier-on-selected-objects
                #https://blender.stackexchange.com/questions/2362/how-to-unlink-material-from-a-mesh-with-python-script
                select_object_liset.append(ob.name)  

        self.report({'INFO'}, str(select_object_liset) + "のマテリアルを削除しました。")

        return {'FINISHED'}