import bpy,sys

from bpy.props import BoolProperty,FloatVectorProperty
from bpy.types import Operator

# 対象のオブジェクトを指定したコレクションに入れる
def linkcolobject(sel_obj,col="BOOL"):
    

    # ブールがすでにあるとき
    try:
        bpy.data.collections[col].objects.link(sel_obj)
    # 選択したオブジェクトがすでにブールフォルダにあるとき。
    except RuntimeError:
        pass
    # ブールフォルダが無い時
    except KeyError:
        right_collection = bpy.data.collections.new(col)
        bpy.context.scene.collection.children.link(right_collection)
        right_collection.color_tag = 'COLOR_01'
        bpy.data.collections[col].objects.link(sel_obj)
# 指定のオブジェクトを指定のコレクション以外アンリンクする
def checkunlinkcol(selectobj, selcolname):
    for checkcol in bpy.data.collections:
        
        if checkcol.name== selcolname:
            pass
        
        else:
            
            for colobj in checkcol.objects:
                
                if colobj.name == selectobj.name:
                    # print(colobj.name)
                    bpy.data.collections[checkcol.name].objects.unlink(colobj)
                    
class BooleanOperator(Operator):
    bl_idname = "object.boolean_operator"
    bl_label = "Boolean Operator"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    
    hide_selected : BoolProperty(
        name="Hide Selected",
        description="Hide selected objects",
        default=False
    ) # type: ignore


    location : FloatVectorProperty(
        name="Location",
        default=(0, 0, 0),
        subtype='TRANSLATION',
        size=3
    ) # type: ignore


    options = [
        ('UNION', 'Union', 'Union'),
        ('INTERSECT', 'Intersect', 'Intersect'),
        ('DIFFERENCE', 'Difference', 'Difference')
    ]
    
    operation_enum: bpy.props.EnumProperty(
        name="operation",
        items=options,
        description=""
        ) # type: ignore
    def execute(self, context):
        # アクティブなオブジェクトを取得
        active_obj = bpy.context.active_object

        # 選択中のオブジェクトを取得（アクティブを除く）
        selected_objs = bpy.context.selected_objects
        selected_objs.remove(active_obj)


        # アクティブなオブジェクトを親として、選択中のオブジェクトを子にする
        for obj in selected_objs:
            
            obj.display_type = 'WIRE'
            obj.location = obj.location + self.location

            # ブーリアンモディファイを追加
            bool_mod = active_obj.modifiers.new(name=f"KSYN_JOINT_Boolean_{obj.name}", type='BOOLEAN')
            bool_mod.operation = self.operation_enum
            bool_mod.solver = 'FAST'
            obj.name = obj.name + "_jont"


            # ブーリアンモディファイのオブジェクトを設定
            bool_mod.object = obj
            linkcolobject(obj,col="BOOL")
            checkunlinkcol(obj, "BOOL")



        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        for obj in selected_objs:
            if self.hide_selected:
                obj.hide_set(True)



        return {'FINISHED'}