import bpy
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import FloatVectorProperty
from bpy.props import FloatProperty
from bpy.props import EnumProperty



def main(self, context):
    seleobj = bpy.context.selected_objects
    selelocation = bpy.context.object.location.xyz
    pulsloac = Vector(self.emlocation)
    totalloc =  selelocation + pulsloac

    # emptysetting
    bpy.ops.object.empty_add(
        type='PLAIN_AXES', align='WORLD', 
        location=totalloc, 
        scale=(1, 1, 1))

    emptyobj = bpy.context.object
    emptyobj.name = self.name
    emptyobj.empty_display_type = self.display_items
        
    bpy.context.object.empty_display_size = self.display_size

    

    for i in seleobj:
        i.select_set(state = True)
    if self.parent == True:
        bpy.ops.object.parent_set(
            type='OBJECT',
            keep_transform=self.parent_keep_transform
            )

display_type_items = [
    ("PLAIN_AXES", "PLAIN_AXES", "", 1),
    ("ARROWS", "ARROWS", "", 2),
    ("SINGLE_ARROW", "SINGLE_ARROW", "", 3),
    ("CIRCLE", "CIRCLE", "", 4),
    ("CUBE", "CUBE", "", 5),
    ("SPHERE'", "SPHERE'", "", 6),
    ("CONE", "CONE", "", 7),
]

class KSYN_OT_lastselectaddempty(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.lastselectaddempty"
    bl_label = "Last select add empty"
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    name : StringProperty(default = "Empty")
    parent : BoolProperty(default = True)
    # single_arrows : BoolProperty(default = True)
    display_items : EnumProperty(items=display_type_items, default="SINGLE_ARROW")
    parent_keep_transform : BoolProperty(default = True)
    emlocation : FloatVectorProperty(subtype="XYZ_LENGTH")
    display_size : FloatProperty(default= 1)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(self, context)
        return {'FINISHED'}

    # def invoke(self, context, event):
    #     wm = context.window_manager
    #     return wm.invoke_props_dialog(self)

