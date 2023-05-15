import bpy, os , sys ,bmesh
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )
        




class look_for_no_geometry(Operator):
        bl_idname = 'object.look_for_no_geometry_operator'
        bl_label = 'Get empty geometry'
        # 自身のクラスの呼び出しにはSYSモジュールが必要
        bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
        bl_options = {'REGISTER', 'UNDO'}


        def main(self):
            def meshver(obj):
                mever =None
                if obj.type =="MESH":
                    # Get the active mesh
                    objmesh = obj.data

                    # Get a BMesh representation
                    bm = bmesh.new()   # create an empty BMesh
                    bm.from_mesh(objmesh)   # fill it in from a Mesh

                    # Modify the BMesh, can do anything here...
                    mever = len(bm.verts)
                    
                return mever

            def meshfaces(obj):
                mever =None
                if obj.type =="MESH":
                    # Get the active mesh
                    objmesh = obj.data

                    # Get a BMesh representation
                    bm = bmesh.new()   # create an empty BMesh
                    bm.from_mesh(objmesh)   # fill it in from a Mesh

                    # Modify the BMesh, can do anything here...
                    mever = len(bm.faces)
                
                return mever



            def selset_del_vers(obj):
                obj.select_set(True)
                print("###ver_select", obj.name, "delete")
                return obj.name
                
            def selset_del_face(obj):
                obj.select_set(True)
                print("###face_select", obj.name)
                return obj.name


            seleobj = bpy.context.selected_objects
            bpy.ops.object.select_all(action='DESELECT')
            [print("###", i.name, meshver(i)) for i in seleobj]
            [print("###meshfaces", i.name, meshfaces(i)) for i in seleobj]

            select_del_verslist = [selset_del_vers(i) for i in seleobj if meshver(i) == 0]
            select_del_facelist = [selset_del_face(i) for i in seleobj if meshfaces(i) == 0 and meshver(i) != 0]

            return select_del_facelist,select_del_verslist


        @classmethod
        def poll(self, context):

            return  True

                           
        def execute(self, context):
            list = self.main()
            messeage = "novert="+str(list[0])+"noface="+str(list[1])
            
            self.report({'INFO'},messeage) 
            return {'FINISHED'}
