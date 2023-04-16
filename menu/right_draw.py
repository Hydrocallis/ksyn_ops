import bpy
from ..utils.get_translang import get_translang

def right_draw(self):
    layout = self.layout
    pie = layout.menu_pie()


    box = pie.split().column()
    row = box.row(align=True)
    row.label(text=get_translang("display-related","表示関係"))
    row = box.row(align=True)
    row.operator("object.wiredisplay_operator")
    row = box.row(align=True)
    row.operator("object.viewshadingshowface_operator")
    row = box.row(align=True)
    row.operator("object.pie10_operator")
    row = box.row(align=True)
    row.operator("object.viewshading")
    row = box.row(align=True)
    row.popover(panel="VIEW3D_PT_shading", text="")
    row = box.row(align=True)
    row.operator("object.subdivision_show", icon='TRIA_UP')
    row = box.row(align=True)
    row.label(text=get_translang("asset-related","アセット関係"))
    row = box.row(align=True)
    row.operator("object.copyasset_operator")
    row.operator("object.material_append",text=get_translang("Matarial Append","マテリアル適応"))

