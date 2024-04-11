import bpy
from ..utils.get_translang import get_translang

def right_draw(self):
    layout = self.layout
    view = bpy.context.space_data
    overlay = view.overlay

    layout = self.layout
    pie = layout.menu_pie()
    box = pie.split().column()
    
    row.label(text=get_translang("display-related","表示関係"))
    row = box.row(align=True)
    row.operator("object.wiredisplay_operator")
    row.operator("object.change_light_energy",text=get_translang("Light Energy","ライトの強さ変更"))
    row = box.row(align=True)
    # row.operator("object.viewshadingshowface_operator")

    row.prop(overlay, "show_face_orientation")
    row.operator("object.ksynautosommth_operator")

    row = box.row(align=True)
    row = box.row(align=True)
    # row.operator("object.viewshading")
    row = box.row(align=True)
    row.popover(panel="VIEW3D_PT_shading", text="")
    row = box.row(align=True)
    row.operator("object.subdivision_show", icon='TRIA_UP')
    row = box.row(align=True)
    row.label(text=get_translang("asset-related","アセット関係"))
    row = box.row(align=True)
    row.operator("object.copyasset_operator")
    row.operator("object.material_append",text=get_translang("Matarial Append","マテリアル適応"))
    row = box.row(align=True)
    row.operator("wm.import_3dfile_from_clipboard")
    row.operator("object.add_primitive",text=get_translang("Add primitives","プリミティブを追加"))
    row = box.row(align=True)
    row.operator("object.import_node_groups",text=get_translang("Import Node Groups","ジオメトリーノードを追加"))
    row.operator("object.make_real_and_parent",text=get_translang("Realize geometry nodes","ジオメトリーノードをリアル化"))

