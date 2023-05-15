import bpy,sys
from bpy.props import IntProperty
import math



def main(self, context):
    if self.mybool == True:
        minus = -1
    else:
        minus = 1

    if self.mybool2 == True:
        angle = 45
    else:
        angle = 90
        
    bpy.ops.transform.rotate(
        value=math.radians(minus*angle*self.myint), orient_axis=self.my_enum
        
        )


class simplerotate(bpy.types.Operator):
    bl_idname = 'object.simplerotate'
    bl_label = 'Simple Rotate'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n ' 
    bl_options = {'REGISTER', 'UNDO'}
    
    # testプロパティ
    
    myint : bpy.props.IntProperty(
        name= "count",
        default=1
        )

    mybool : bpy.props.BoolProperty(
        name= "Reverse",
        default=0
        )
    mybool2 : bpy.props.BoolProperty(
        name= "45",
        default=0
        )

    my_enum: bpy.props.EnumProperty(items= [
                                ('X', "X", "", 1),
                                ("Y", "Y", "", 2),
                                ("Z", "Z", "", 3),
                                    
                            ],
                            name="Axis",
                            default='X',
                            )


        
    def execute(self, context):
        main(self, context)


        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None



    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)


    
        