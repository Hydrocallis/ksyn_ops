
import bpy

def bottom_draw(self): 
        
    layout = self.layout
    pie = layout.menu_pie()


    other = pie.column()
    gap = other.column()
    gap.separator()
    gap.scale_y = 5
    other_menu = other.box().column()
    other_menu.scale_y=1.3
        
    other_menu.operator("view3d.view_axis", text="Bottom", icon='TRIA_DOWN').type = 'BOTTOM'
    other_menu.operator("view3d.view_axis", text="Top", icon='TRIA_UP').type = 'TOP'
    other_menu.operator("view3d.view_axis", text="Back", icon="AXIS_SIDE").type = 'BACK'
    other_menu.operator("view3d.view_axis", text="Front", icon = "AXIS_FRONT").type = 'FRONT'
    other_menu.operator("script.reload",text="リロード")
    if hasattr(bpy.types, bpy.ops.object.texttestop_1_operator.idname()):
        other_menu.operator("object.texttestop_1_operator")
    else:
        pass
    
    if hasattr(bpy.types, "TEXTEDITOR_PT_panel"):

        other_menu.popover("TEXTEDITOR_PT_panel", text = "TEST", icon='EXPORT')
    else:
        pass
        # other_menu.label( text = "オペは見つかりません", icon='EXPORT')

        # print('### 3D からテキストへの読み込みで、TEXT_PT_ImputComment2のクラスが見つかりませんのでパスします。', )
                