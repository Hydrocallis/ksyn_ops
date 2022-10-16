
import bpy, sys, os, subprocess, bmesh

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


class PIE3D_OT_mesh_emptyverdel(Operator):
    bl_idname = 'object.mesh_emptyverdel'
    bl_label = 'mesh_emptyverdel'
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    # 3Dで用のプロパティ
  
    def meshver(self, obj):
        # Get the active mesh
        objmesh = obj.data

        # Get a BMesh representation
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(objmesh)   # fill it in from a Mesh

        mever = len(bm.verts)
        
        return mever

    def meshfaces(self, obj):
        # Get the active mesh
        objmesh = obj.data

        # Get a BMesh representation
        bm = bmesh.new()   # create an empty BMesh
        bm.from_mesh(objmesh)   # fill it in from a Mesh

        # Modify the BMesh, can do anything here...
        mever = len(bm.faces)
        return mever
        
    def selset_del_ver(self, obj):
        obj.select_set(True)
        print("###ver_selct", obj.name, "delete")

    def selset_del_face(self, obj):
        obj.select_set(True)
        print("###face_select", obj.name)

    def execute(self, context):
 
        seleobj = bpy.context.selected_objects

        bpy.ops.object.select_all(action='DESELECT')

        [print("###", i.name, self.meshver(i)) for i in seleobj]

        [self.selset_del_ver(i) for i in seleobj if self.meshver(i) == 0]
        [self.selset_del_face(i) for i in seleobj if self.meshfaces(i) == 0 and self.meshver(i) != 0]


        bpy.ops.object.delete(use_global=False) 
        
        return {'FINISHED'}

    @classmethod
    def poll(self, context):
        return True
      
