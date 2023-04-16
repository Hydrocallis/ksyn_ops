import bpy
    
def top_right_draw(self):
    layout = self.layout
    pie = layout.menu_pie()

    
    other = pie.column()
    gap = other.column()
    gap.separator()
    gap.scale_y = -20
    other_menu = other.box().column()


    
    if hasattr(bpy.types, "SIMPLEFBXECPORT_PT_SETTINGFBXEXPORT1"):
        other_menu.label(text="FBXEXPORT")
        other_menu.popover("SIMPLEFBXECPORT_PT_SETTINGFBXEXPORT1", text = "FBXEXPORT", icon='EXPORT')
    else:
        # print('###OBJECT_PT_piesetting_fbxexport','のクラスが見つかりませんのでパスします。', )
        pass
