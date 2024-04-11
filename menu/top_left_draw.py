import bpy


def top_left_draw(self):
    layout = self.layout
    pie = layout.menu_pie()
    box = pie.split().column()
    gap = box.column()
    gap.separator()
    gap.scale_y = -10
    row = box.row(align=True)   
    row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
    row.operator("wm.save_as_mainfile", text="Save As...")
    row = box.row(align=True)

    row.operator("ksyn_ops.setting_operator")
