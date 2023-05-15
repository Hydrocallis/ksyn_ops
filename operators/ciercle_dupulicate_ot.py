import bpy, sys, math


def set_cursor_loc():
    context = bpy.context
    save_pivot_point = context.scene.tool_settings.transform_pivot_point
    get_cursor_loc = context.scene.cursor.location.xyz

    get_object_point = context.object.location.xyz
    context.scene.cursor.location = get_object_point

    return (
        save_pivot_point, 
        get_cursor_loc, 
        get_object_point
        )


def nameset(self,countrange,get_nameliset):
    if self.nameset_bool == True:
        for (i,oldobj) in zip(bpy.context.selected_objects,get_nameliset):
            i.name = str(countrange+1).zfill(3)+ "_"+oldobj.name 

    
def rot_dup(
    self,
    save_pivot_point,
    get_cursor_loc,
    move_value,
    # move_axis,
    counted,
    radians,
    orient_axis,
    link
    ):
    
    context = bpy.context
        

    bpy.ops.transform.translate(
        value=move_value, 
        # orient_axis_ortho=move_axis,
        ) 
        # 回転位置の微調整
    context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
    bpy.ops.transform.rotate(
        value = self.after_adjustment, 
        # center_override=context.scene.cursor.location,
        orient_axis=orient_axis, 
        )

    # last range pass
    # ここで各オブジェクトを複製して回転する。
    get_nameliset = bpy.context.selected_objects
    for i in range(counted-1):
        # 顔の向きを合わせる
        # context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
        # bpy.ops.transform.rotate(
        #     value = math.radians(radians), 
        #     # center_override=context.scene.cursor.location,
        #     orient_axis=orient_axis, 
        #     )
        
        #　複製する
        
        bpy.ops.object.duplicate_move(
            OBJECT_OT_duplicate={"linked":link, "mode":'TRANSLATION'}, 
        )

        # 中心軸を変えて回転する
        context.scene.tool_settings.transform_pivot_point = 'CURSOR'

        bpy.ops.transform.rotate(
            value = math.radians(radians), 
            center_override=context.scene.cursor.location,
            orient_axis=orient_axis, 
            )
        
        
        nameset(self,i,get_nameliset)




    #　もとに戻す
    context.scene.cursor.location = get_cursor_loc
    context.scene.tool_settings.transform_pivot_point = save_pivot_point


def main(self):
    save_pivot_point,get_cursor_loc,get_object_point = set_cursor_loc()

    rot_dup(self,
        save_pivot_point,
        get_cursor_loc,
        self.myfloatvector,
        self.countedint,
        360/self.countedint,
        self.transform_axis,
        self.link_bool
        )


class ciercle_dupulicate(bpy.types.Operator):
    bl_idname = 'object.ciercle_dupulicate'
    bl_label = 'circle dupulicate'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    
    # testプロパティ
    
    myfloatvector:bpy.props.FloatVectorProperty(
        name='Relative Offset', 
        description='', 
        default=(1.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        )

    after_adjustment:bpy.props.FloatProperty(
        name='After Adjustment', 
        description='', 
        # default=(0.0, 0.0, 0),
        unit ="ROTATION"
        )     

    transform_axis: bpy.props.EnumProperty(items= [
                                    ('X', "X", "", 1),
                                    ("Y", "Y", "", 2),
                                    ("Z", "Z", "", 3),
                            
                
                                ],
                                default="Z",
                                )
                                
    countedint : bpy.props.IntProperty(
        name= "count",
        default=3,
        soft_min=1
        )

    link_bool : bpy.props.BoolProperty(
        name= "link",
        default=False
        )

    nameset_bool : bpy.props.BoolProperty(
        name= "name set",
        default=False
        )



                    
    def execute(self, context):
        main(self)


        return {'FINISHED'}


 