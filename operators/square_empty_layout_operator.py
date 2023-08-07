import bpy,sys
import math
from bpy.props import FloatProperty, FloatVectorProperty
from mathutils import Euler

class SquareEmptyLayoutOperator(bpy.types.Operator):
    bl_idname = "object.square_empty_layout_operator"
    bl_label = "Square Empty Layout Operator"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    
    margin: FloatProperty(
        name="Margin",
        default=0.1,
        min=0,
        description="Margin between empty objects"
    )
    
    rotation: FloatVectorProperty(
        name="Rotation",
        default=(0, 0, 0),
        subtype='EULER',
        description="Rotation values for each object"
    )
    

    def execute(self, context):
        actobjloc = bpy.context.object.location
        # 選択されたオブジェクトを取得する
        selected_objects = bpy.context.selected_objects

        # 選択されたオブジェクトがエンプティでかつデータタイプが 'IMAGE' の場合にディスプレイサイズを統一する
        empty_display_sizes = []
        for obj in selected_objects:
            # print('###',obj)
            try:
                if obj.type == 'EMPTY' and obj.data.type == 'IMAGE':
                    empty_display_sizes.append(obj.empty_display_size)
                    obj.scale =(1,1,1)
                    obj.rotation_euler = (obj.rotation_euler[0] + self.rotation[1],obj.rotation_euler[1] + self.rotation[2],obj.rotation_euler[2] + self.rotation[2])
            except AttributeError:
                pass

        if empty_display_sizes:
            average_empty_display_size = sum(empty_display_sizes) / len(empty_display_sizes)
        else:
            average_empty_display_size = 0.0

        # エンプティでかつデータタイプが 'IMAGE' のオブジェクトの数を取得する
        filtered_objects = [obj for obj in selected_objects if obj.type == 'EMPTY' and obj.data.type == 'IMAGE']
        num_objects = len(filtered_objects)

        # エンプティを正方形状に配置する
        row_length = int(math.sqrt(num_objects))
        for i, obj in enumerate(filtered_objects):
            # エンプティの位置を計算する
            x = i % row_length
            z = i // row_length
            y = 0
            obj.empty_display_size = average_empty_display_size
            # if i == 0:
            #     obj.location = actobjloc
            # else:
            obj.location = ( x * (average_empty_display_size + self.margin),  y,  z * (average_empty_display_size + self.margin))

        bpy.ops.transform.translate(value=(actobjloc[0], actobjloc[1], actobjloc[2]), 
                                    # orient_axis_ortho='X', 
                                    orient_type='GLOBAL')


        return {'FINISHED'} 