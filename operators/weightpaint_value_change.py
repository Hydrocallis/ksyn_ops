
import bpy, sys, os, subprocess

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


class PIE3D_OT_weightpaint_value_chnage(Operator):
    """Tooltip"""
    bl_idname = "object.weightpaint_value_chnage"
    bl_label = "weightpaint_value_chnage"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}
    
    def uvtex_items():
        a=0
        items = []
        weight_list = [1, 0.8, 0.5, 0.25, 0.2, 0]
        for t in weight_list:
            # When adding an icon, it is necessary to add the item number name as well.
            items.append((str(t), str(t), "description","WPAINT_HLT",a)) 
            a+=1
        return items
    ietms=uvtex_items()
    #　なぜかしらないが、ストレッチからウェイトに値が切り替わった。？？？
    def update(self, context):
        print('###0-0###UPDATE', self.uvtex)
        cst_s=context.scene.tool_settings
        cst_s.unified_paint_settings.weight = float(self.uvtex)
    
    uvtex:bpy.props.EnumProperty(name="test", items=ietms, update=update)

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH' and
                len(context.object.data.uv_layers) > 0)

    def invoke(self, context, event):

            


        return context.window_manager.invoke_props_dialog(self)
    

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self,"uvtex", expand=True)
        
    def execute(self, context):
        print("###CHange weight value", self.uvtex)
        cst_s=context.scene.tool_settings
        cst_s.unified_paint_settings.weight = float(self.uvtex)



        
        
   
        self.report({'INFO'}, self.uvtex)
        return {'FINISHED'}


