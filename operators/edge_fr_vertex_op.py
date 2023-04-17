import bpy, sys
import bpy,bmesh


def getselevertex_makeedge():
    ob   = bpy.context.object
    mesh = bmesh.from_edit_mesh(ob.data)
    selectedvertex= []
    if mesh.select_mode == {'VERT'}:
        for v in mesh.verts:
            if v.select == True:
                selectedvertex.append(v)
        bpy.ops.mesh.select_all(action='DESELECT')

    if len(selectedvertex) < 1000 and len(selectedvertex) >1:

        for i,j in enumerate(selectedvertex):
            if i <len(selectedvertex)-2:
                j.select = True
                selectedvertex[i+1].select = True
                bpy.ops.mesh. edge_face_add()

                j.select =False
                selectedvertex[i+1].select = False

                
                selectedvertex[i+1].select = True
                selectedvertex[i+2].select = True
                bpy.ops.mesh. edge_face_add()

                selectedvertex[i+1].select = False
                selectedvertex[i+2].select = False
            else:
                
                selectedvertex[-1].select = True
                selectedvertex[-2].select = True
                bpy.ops.mesh. edge_face_add()
                
    elif selectedvertex ==[] :
        pass
        
    for i,j in enumerate(selectedvertex):
        j.select =True
        

class SIMPLE_OT_edgefrvertex(bpy.types.Operator):
    bl_idname = 'object.edge_fr_vertex'
    bl_label = 'Edge from Vertex'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
  
    @classmethod
    
    def poll(self, context):

        return True


    def execute(self, context):
       
        getselevertex_makeedge()


        return {'FINISHED'}


    