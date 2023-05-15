import bpy, sys


def makediff(a, b):
    import numpy as np
    arr=np.array([a,b])
    diff = np.diff(arr)
    return diff
# print(makediff(-5,2))

def axislocget(self,axis,location,seleobjloc):

    if self.axis[axis] == True:
        if self.axis[axis] == True and self.lastselected== True:
            locationabs = makediff(seleobjloc[axis],location[axis])
            if location[axis]<0 ==True:
                movelocation=  location[axis]+(locationabs*2)
            else:
                movelocation=  location[axis]-(locationabs*2)
        else:   
            movelocation= -location[axis]


    return movelocation


def duplicate_mirrormove(self,seleobjloc):

    location = bpy.context.object.location


    if self.axis[0] == True:
        axis =0
        x_location =axislocget(self,axis,location,seleobjloc)
    else:
        x_location = location[0]


    if self.axis[1] == True:
        axis =1
        y_location =axislocget(self,axis,location,seleobjloc)

    else:
        y_location = location[1]

    if self.axis[2] == True:
        axis =2
        z_location =axislocget(self,axis,location,seleobjloc)
    
    else:
        z_location = location[2]

    object_locationmoveaxis = (x_location,y_location,z_location)

    
    actobjname = bpy.context.object.name
    bpy.context.object.name = actobjname+"_R"
    bpy.ops.object.duplicate_move()
    bpy.context.object.name = actobjname+"_L"
    bpy.ops.transform.mirror(
        orient_type='GLOBAL', 
        constraint_axis=self.axis
        )
    bpy.context.object.location = object_locationmoveaxis


def aplly_meshfilip(self):

    if bpy.context.object.type != "MESH":
        pass

    else:
        bpy.ops.object.transform_apply(
            location=False, rotation=False, scale=True)
        # xountaxis = [axis[0],axis[1],axis[2]]
        xountaxis = list(self.axis)
        # print('###',xountaxis.count)
        if xountaxis.count(True) == 2 or xountaxis.count(True) ==0:
            pass
        else:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.flip_normals()
            bpy.ops.object.mode_set(mode='OBJECT')


def main_function(self,seleobjloc):
    duplicate_mirrormove(self,seleobjloc)
    aplly_meshfilip(self)

def main(self,context,):
        seleobjloc=bpy.context.object.location

        if self.lastselected == True:
            bpy.context.object.select_set(False)
                    
       
        
        sele_obj = context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        for setobj in sele_obj:
            #self.lastselected　がオンの場合はパスして基準値のみの習得とする

            if setobj.type =='CURVE':
                pass

            else:
                context.view_layer.objects.active = setobj
                setobj.select_set(True)
                main_function(self,seleobjloc)
                bpy.ops.object.select_all(action='DESELECT')





class OBJECTEASYMIRROR(bpy.types.Operator):
    bl_idname = 'object.object_easy_mirror'
    bl_label = 'Easy Object Mirror'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
    bl_options = {'REGISTER', 'UNDO'}

    lastselected: bpy.props.BoolProperty(
        name="Last Selection Basis",
        default=False,
        )
    

    axis:bpy.props.BoolVectorProperty(
        name='Axis', 
        description='', 
        default=(True, False, False),
        subtype="XYZ"
        )
    

    def draw(self, context):

        layout = self.layout
        # array setting
        row = layout.row()
        box1 = row.box()
        box1.label(text="axis bool")
        box1.prop(self, 'axis')
        box1.prop(self, 'lastselected')
        
    def execute(self, context):
        main(self,context)
        

            
 
        return {'FINISHED'}

