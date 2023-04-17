
import bpy, sys, pathlib

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


from bpy.props import (
                        StringProperty, 
                        IntProperty, 
                        FloatProperty, 
                        EnumProperty, 
                        BoolProperty,
                        PointerProperty,
                        FloatVectorProperty,
                        StringProperty
                        )


class PropertyGroup(PropertyGroup):
  
    # レストとポーズの入れ替え用のプロパティ
    def update_func(self, context):
        pass
        # print("my test function", self)

    def empty_poll(self, object):

        return object.type == 'EMPTY'

    def empty_curve(self, object):

        return object.type == 'CURVE'


    target_empty : PointerProperty(
                type = bpy.types.Object, name = "EMPTY", 
                update = update_func, 
                poll=empty_poll
                                                )

    array_curve : PointerProperty(
                type = bpy.types.Object, name = "Array curve", 
                # update = update_func, 
                poll=empty_curve
                                                )

    target_curve : PointerProperty(
                type = bpy.types.Object, name = "Curve", 
                # update = update_func, 
                poll=empty_curve
                                                )

    counted : IntProperty(
                name = "array count1", 
                default=1
                                                )
    counted_second : IntProperty(
                name = "array count1", 
                default=1

                                                )
    counted_third : IntProperty(
                name = "array count1", 
                default=1

                                                )