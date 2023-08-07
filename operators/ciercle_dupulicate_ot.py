import bpy, sys, math


def set_cursor_loc(self):
    context = bpy.context
    save_pivot_point = context.scene.tool_settings.transform_pivot_point
    get_cursor_loc = context.scene.cursor.location.xyz


    if self.pivot_type !=  "CURSOR":
        get_object_point = context.object.location.xyz
    else:
        get_object_point = get_cursor_loc
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

def add_prefix_to_object_names(object_dict, prefix):
    for obj in object_dict:
        obj.name = prefix + obj.name


def duplicate_and_rotate_objects(self, counted, link, radians, orient_axis, get_nameliset):
    object_dict = {}
    # オブジェクトを辞書に格納する
    object_dict["orij_obj"] = bpy.context.selected_objects

    for i in range(counted-1):
        # 複製する

        bpy.ops.object.duplicate_move(
            OBJECT_OT_duplicate={"linked":link, "mode":'TRANSLATION'}, 
        )
        # オブジェクトを辞書に格納する
        object_dict[i] = bpy.context.selected_objects

        # 中心軸を変えて回転する
        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

        bpy.ops.transform.rotate(
            value = math.radians(radians), 
            center_override=bpy.context.scene.cursor.location,
            orient_axis=orient_axis, 
        )


        nameset(self,i,get_nameliset)


    prefix= "000_"
    add_prefix_to_object_names(object_dict["orij_obj"], prefix)

    return object_dict

def select_all_objects_in_dict(object_dict):
    for obj_list in object_dict.values():
        print('###obj_list',obj_list)
        for obj in obj_list:

            obj.select_set(True)

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
        orient_axis=orient_axis, 
        )

    # last range pass
    # ここで各オブジェクトを複製して回転する。
    get_nameliset = bpy.context.selected_objects

    object_dict = duplicate_and_rotate_objects(self, counted, link, radians, orient_axis, get_nameliset)

    #　もとに戻す
    context.scene.cursor.location = get_cursor_loc
    context.scene.tool_settings.transform_pivot_point = save_pivot_point

    select_all_objects_in_dict(object_dict)

def main(self):
    save_pivot_point,get_cursor_loc, get_object_point = set_cursor_loc(self)

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
        default=(0.0, 0.0, 0),
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

    # ピボットタイプの列挙型を定義
    enum_items = [
        ("ACTIVE", "Active Pivot", "Use the active object as the pivot point"),
        ("CURSOR", "Cursor Pivot", "Use the 3D cursor as the pivot point")
    ]

    # ピボットタイプのプロパティを作成
    pivot_type : bpy.props.EnumProperty(
        name="Pivot Type",
        description="Select the pivot type to use",
        items=enum_items,
        default="ACTIVE")

                    
    def execute(self, context):
        main(self)


        return {'FINISHED'}


 