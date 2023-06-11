
import bpy
import bmesh
from ksyn_bpy_chat_gpt.utils.get_translang import get_translang

def ShowMessageBox(message=[""], title="Message Box", icon='INFO'):
    def draw(self, context):
        for mes in message:
            self.layout.label(text=mes)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def meshngoncheck(ob):
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    count = 0
    for f in bm.faces:
        if len(f.verts) >= 5:
            f.select = True
            count += 1
    bmesh.update_edit_mesh(me)
    obj_name = ob.name
    return count, obj_name

class ConvertNgonsToTrisOperator(bpy.types.Operator):
    bl_idname = "mesh.convert_ngons_to_tris"
    bl_label = get_translang("Convert Ngons to Tris","Nゴンを三角に変換する")
    bl_description = "Converts ngons to tris for all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    convert_tris : bpy.props.BoolProperty(name="Convert",default=True)

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        convert_list = {}
        bpy.ops.mesh.select_all(action='DESELECT')
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                count, obj_name = meshngoncheck(obj)
                convert_list[obj_name] = count
        if self.convert_tris == True:
            bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        message = ["{}: {}".format(k, v) for k, v in convert_list.items()]
        ShowMessageBox(message=message, title="Conversion Results")

        return {'FINISHED'}
