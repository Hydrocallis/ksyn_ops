import re
import bpy, sys
from mathutils import Matrix
import math
import bmesh

from math import radians


class WORLDORIJINMOVE:

    def copy_applay_obje(self):
        bobj = bpy.context.object # main select object
        bpy.ops.object.select_all(action='DESELECT')
        bobj.select_set(True)
        
        bpy.ops.object.duplicate_move()
        bobj.select_set(False)
        
        bpy.ops.object.convert(target='MESH')
        bpy.ops.object.transform_apply(
            location=False, rotation=True, scale=False)
        bpy.context.object.name = bobj.name + "_cache"
        caheobj = bpy.context.object
        
        return bobj,caheobj
        

    def select_set_oldobje(self,bobj):
        bpy.context.view_layer.objects.active = bobj
        bobj.select_set(True)


    def get_min_axis(self,axis,bool):

        context=bpy.context
        
        dimensions= context.object.dimensions
        
        mobj = context.object.matrix_world
        obj = context.object
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.faces.ensure_lookup_table()# オブジェクト上でも動作

        list =[]

        for i in bm.verts:
            vector =mobj @ i.co
            list.append(vector[axis])

            
    #    print('###0-0###min(list)', min(list))
        plusloc = min(list)

        if bool ==True:
            plusloc += dimensions[axis]
        return plusloc


    def remove_oldcashe(self,caheobj):
        object_to_delete = caheobj
        bpy.data.objects.remove(object_to_delete, do_unlink=True)


    def set_wordorijin_z(self,obj,axis,plusloc):
        
        location =obj.location
        obj.location[axis] = location[axis]-plusloc


    def memory_selectedobjs(self,):
        objes=bpy.context.selected_objects
        return objes


    def memory_objsselecte_set(self,objes):
        for i in objes:
            i.select_set(True)

        


    # main
    def wordlorijin_move(self,axis,posinega):
        objes = self.memory_selectedobjs()
        obtype =bpy.context.object.type

        if obtype =='CURVE' or obtype =='MESH':
            bobj,caheobj=self.copy_applay_obje()

            plusloc=self.get_min_axis(axis,posinega)
            self.select_set_oldobje(bobj)
            self.remove_oldcashe(caheobj)
            
        else:
            
            plusloc=bpy.context.object.location[axis]
            bobj =bpy.context.object.type
            

        self.memory_objsselecte_set(objes)

        for obj in objes:
            
            self.set_wordorijin_z(obj, axis,plusloc)


class WORDORIJINMOVE_OT_MAIN(WORLDORIJINMOVE,bpy.types.Operator):
    bl_idname = 'object.wordlorijn_move'
    bl_label = 'world orijn_move'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
    bl_options = {'REGISTER', 'UNDO'}
    

    transform_axis: bpy.props.EnumProperty(items= [
                                    ('X', "X", "", 1),
                                    ("Y", "Y", "", 2),
                                    ("Z", "Z", "", 3),
                            
                
                                ],
                                default="Z",
                                )

    positive_axis: bpy.props.BoolProperty(name="positive axis")

    def draw(self, context):

        layout = self.layout
        # array setting
        row = layout.row()
        box1 = row.box()
        box1.label(text="axis")
        box1.prop(self, 'transform_axis')
        box1.prop(self, 'positive_axis')
        
    def execute(self, context):

        if self.transform_axis =="X":
            axis =0
        elif self.transform_axis =="Y":
            axis =1
        elif self.transform_axis =="Z":
            axis =2
        
        print(axis)
        self.wordlorijin_move(
            axis,
            self.positive_axis
            )
            
 
        return {'FINISHED'}
        
               