

import bpy,sys
from bpy.props import IntProperty
import math

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng
def main_draw(self):
    layout = self.layout
    layout.prop(self, "sidebicect" )
    grifl=layout.grid_flow(row_major=True, columns=3, even_columns=False, even_rows=False, align=True)
    grifl.prop(self, "myfloatvector")
    grifl.prop(self, "myboolvector" ,)
    layout.prop(self, "Fill" )
    layout.prop(self, "mirror")
    


def sidebicect(self,context):
    loc=bpy.context.object.location
    
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.bisect(
        plane_co=(
            self.myfloatvector[0]+loc[0],
            self.myfloatvector[1]+loc[1],
            self.myfloatvector[2]+loc[2]),
            
        plane_no=(
            int(self.myboolvector[0]),
            int(self.myboolvector[1]),
            int(self.myboolvector[2]))
            ,
        clear_inner=False, 
        clear_outer=True, 
        # xstart=420, 
        # xend=1090, ystart=599, yend=599, flip=False
        )
    if self.Fill == True:
        bpy.ops.mesh.edge_face_add()
    

def main(self, context):

    if self.sidebicect ==True:
        sidebicect(self,context)

    if self.mirror== True:
        mirror(self,context)

def mirror(self, context):   
    loc=bpy.context.object.location

    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(
        plane_co=(
            -self.myfloatvector[0]+loc[0],
            -self.myfloatvector[1]+loc[1],
            -self.myfloatvector[2]+loc[2])
            ,
        plane_no=(
            -int(self.myboolvector[0]),
            -int(self.myboolvector[1]),
            -int(self.myboolvector[2]))
            ,
        clear_inner=False, 
        clear_outer=True, 
        # xstart=420, 
        # xend=1090, ystart=599, yend=599, flip=False
        ) 
    if self.Fill == True:
        bpy.ops.mesh.edge_face_add()
       


class bicect_mirror(bpy.types.Operator):
    bl_idname = 'mesh.mesh_ot_bicect_mirror'
    bl_label = get_translang('Mesh bicect mirror','二等分ミラー')
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n ' 
    bl_options = {'REGISTER', 'UNDO'}
    
    # testプロパティ
    
    myfloatvector:bpy.props.FloatVectorProperty(
        name='Constant Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        )
        
    myboolvector : bpy.props.BoolVectorProperty(
        name= get_translang('Execution','実行'),
#        default=0
        )
#      

    mirror : bpy.props.BoolProperty(
        name= "Mirror",
        default=0
        )
    Fill : bpy.props.BoolProperty(
        name= "Fill",
        default=0
        )
    sidebicect : bpy.props.BoolProperty(
        name= get_translang('Side Bicect','二等分'),
        default=True
        )
        


        
    def execute(self, context):
        main(self, context)


        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None




    def draw(self,context):
        main_draw(self)


    
        