import bpy, sys
# from .utils.curve_mirror import curve_mirror

# 0でｘ１でｙ２でｚの方向軸 filip はbool
def curve_mirror(
    axis,
    flip,
    ):
    axis = int(axis)
    
    mirror = bpy.context.object.modifiers.new(name='curveMIRROR', type='MIRROR')
    mirror.use_axis[0] = False
    mirror.use_axis[axis] = True
    mirror.use_bisect_axis[axis] = True
    mirror.use_bisect_flip_axis[axis] = flip


    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.convert(target='CURVE')

    bpy.ops.object.mode_set(mode='EDIT')

class CurveMirror(bpy.types.Operator):
    bl_idname = 'object.curve_mirror'
    bl_label = 'Curve Mirror'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    axis: bpy.props.EnumProperty(items= [
                                ('0', "X", "", 1),
                                ("1", "Y", "", 2),
                                ("2", "Z", "", 3),
                                                 
                            ],
                            name=" Axis",
                            default='0',
                            )

    flip : bpy.props.BoolProperty(
            name="filp"
            )


    @classmethod
    
    def poll(self, context):

        return True


    def execute(self, context):
       
        curve_mirror(
            self.axis,
            self.flip,
            )


        return {'FINISHED'}


    