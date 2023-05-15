from itertools import combinations
import bpy, sys, random


def objecttransform(
    trans,
    resize,

    ):
    bpy.ops.transform.translate(
        value=(trans)
            )

    bpy.ops.transform.resize(
        value=(resize),
            )

def raddamtransform(
    resize,
    ramdommin,
    ramdommax,

    ):
    rmdamusizefactorx = random.uniform(ramdommin[0], ramdommax[0])
    rmdamusizefactory = random.uniform(ramdommin[1], ramdommax[1])
    rmdamusizefactorz = random.uniform(ramdommin[2], ramdommax[2])
    rmdamusizefactorxyz =(rmdamusizefactorx,rmdamusizefactory,rmdamusizefactorz)

    combinedsizeliset = []

    for (x, y) in zip(resize, rmdamusizefactorxyz):
        combinedsizeliset.append(x*y)
    # print('###',combinedsizeliset[0],combinedsizeliset[1],combinedsizeliset[2])

    bpy.context.object.scale=combinedsizeliset
    # bpy.ops.transform.resize(
    #     value=(combinedsizeliset),
    #         )
    bpy.ops.object.transform_apply(
        location=False, 
        rotation=False, 
        scale=True
        )
    cobj= bpy.context.object
    return cobj.dimensions
       

def object_applyscale(aplly_bool):
    try:
        bpy.ops.object.transform_apply(
            location=False, 
            rotation=False, 
            scale=True
            )
    # link してる場合はアプライできんのよね
    except RuntimeError:
        pass

def object_duplicate_array(
    ro,
    co,
    dimensionss,
    link_bool,
    range,
    # parent_set_bool
    ):
    cobj = bpy.context.object
    selectedobjenamelist =  [i.name for i  in bpy.context.selected_objects]
    
    # if range ==0:
    x_dimension,y_dimension,z_dimension=cobj.dimensions
    # else:
    #     x_dimension,y_dimension,z_dimension=dimensionss

    bpy.ops.object.duplicate_move(
        OBJECT_OT_duplicate={
            "linked":link_bool,
            "mode":'TRANSLATION'},
        TRANSFORM_OT_translate={
            "value":(
                # inputdistans
                x_dimension*ro[0]+co[0], 
                y_dimension*ro[1]+co[1], 
                z_dimension*ro[2]+co[2], 
                 ), 
                }
                )


    # if parent_set_bool == True:
    #     bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    return selectedobjenamelist


def rename_sub(
   selectedobjenamelist,
   prefix,
   suffix,
   countnames_bool,
   range,
   ):
    newnamelist = []
    countnumber = range+1
    for oldname in selectedobjenamelist:
        newname = oldname
        if range ==0:

            if prefix !="":
                newname = prefix + "_"+newname
                
            if suffix !="":
                newname = newname+"_"+suffix
        
            if countnames_bool ==1 :
                newname = str(countnumber).zfill(3)+"_"+newname
                
            if countnames_bool == 0 and prefix =="" and suffix =="":
                newname = newname +"_copy"
        else:
            if countnames_bool ==1 :
                newname = str(countnumber).zfill(3) +newname[3:] 
     
            
        newnamelist.append(newname)
       

    return newnamelist


def rename(newnamelist):

    for (i,j) in zip(bpy.context.selected_objects,newnamelist):
        i.name =j
                

class objarray(bpy.types.Operator):
    bl_idname = 'object.obuect_easy_array'
    bl_label = 'SimpleArray'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
    # 3Dで用のプロパティ
    bl_options = {'REGISTER', 'UNDO','PRESET'}
    
    count : bpy.props.IntProperty(
    name= "count",
    default=1
    )

    ro:bpy.props.FloatVectorProperty(
        name='Relative Offset', 
        description='', 
        default=(1.0, 0.0, 0),
        subtype="XYZ"
        )
        
    co:bpy.props.FloatVectorProperty(
        name='Constant Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        )    
            
    prefix:bpy.props.StringProperty(
        name='prefix set name', 
        description='prefix', 
        default='',
        )  
              
    suffix:bpy.props.StringProperty(
        name='suffix set name', 
        description='suffix', 
        default='',
        )  

    countnames_bool : bpy.props.BoolProperty(
        name="Toggle Option"
        )

        
    trans:bpy.props.FloatVectorProperty(
        name='move object', 
        description='', 
        default=(0.0, 0.0, 0.0),
        subtype="XYZ_LENGTH"
        )   

    resize:bpy.props.FloatVectorProperty(
        name='scale change', 
        description='', 
        default=(1.0, 1.0, 1.0),
        subtype="XYZ"
        )   

    aplly_bool : bpy.props.BoolProperty(
        name=" apply_scale"
        )
    link_bool : bpy.props.BoolProperty(
        name="link"
        )

    # parent_set_bool : bpy.props.BoolProperty(
    #     name="parent set"
    #     )


    # ramdommin:bpy.props.FloatVectorProperty(
    #     name='ramdom min', 
    #     description='', 
    #     default=(1.0, 1.0, 1.0),
    #     subtype="XYZ"
    #     )   

    # ramdommax:bpy.props.FloatVectorProperty(
    #     name='ramdom max', 
    #     description='', 
    #     default=(1.0, 1.0, 1.0),
    #     subtype="XYZ"
    #     )   



    @classmethod
    def poll(self, context):
        
        return  bpy.context.object
        
    
    def execute(self, context):
        objecttransform(
                self.trans,
                self.resize,

                )

        object_applyscale(
            self.aplly_bool
            )
        dimensions =(1,1,1)
        for i in range(self.count):

            # dimensions = raddamtransform(
            #     self.resize,
            #     self.ramdommin,
            #     self.ramdommax,
            #     )   

            selectedobjenamelist = object_duplicate_array(
                self.ro,
                self.co,
                dimensions,
                self.link_bool,
                i,
                # self.parent_set_bool

                  )
                
            newnamelist = rename_sub(
                selectedobjenamelist,
                self.prefix,
                self.suffix,
                self.countnames_bool,
                i,
                )

                
            rename(newnamelist)



        return {'FINISHED'}
