import bpy


def top_left_draw(self):
    layout = self.layout
    pie = layout.menu_pie()
    box = pie.split().column()
    gap = box.column()
    gap.separator()
    gap.scale_y = -10

    box.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
    box.operator("wm.save_as_mainfile", text="Save As...")
    box.operator("ksyn_ops.setting_operator")
