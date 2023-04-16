import bpy

def top_draw(self):
    layout = self.layout
    pie = layout.menu_pie()
    col = pie.column(align=True)
    col.scale_x = 0.5 # メニューの幅を半分に制限する
    col.popover("OBJECT_PT_piesetting_arm", text = "AMATURE", icon='ARMATURE_DATA')
    row = col.row(align=True)
    row.popover('OBJECT_PT_transform', icon='RIGHTARROW_THIN',  text='TRANSFORM')
    row = col.row(align=True)
    row.popover("OBJECT_PT_piesetting", icon='TRIA_UP')
    row = col.row(align=True)
    row.operator("object.uvgridmat", icon='EVENT_U')
    row = col.row(align=True)
    row.operator("object.subdivision_show", icon='TRIA_UP')
    row = col.row(align=True)
    row.operator("object.colorpickup_object", icon='EYEDROPPER',text="Obj Color")

