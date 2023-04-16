import bpy, sys

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

# サブモジュール読み込み
from .botom_right_draw import botom_right_draw
from .left_draw import left_draw
from .top_draw import top_draw
from .top_left_draw import top_left_draw
from .top_right_draw import top_right_draw
from .bottom_draw import bottom_draw


def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng

class PIE_MT_ViewNumpad(Menu):
    bl_idname = "PIE_MT_viewnumpad_mypanel"
    bl_label = "CUSYANG_Pie Views Menu_"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "



    def bottom_left_draw(self):
        ob = bpy.context.active_object
        scene = bpy.context.scene
        rd = scene.render

        layout = self.layout
        pie = layout.menu_pie()


        other = pie.column()
        gap = other.column()
        gap.separator()
        gap.scale_y = 45
        other_menu = other.box().column()

        other_menu.operator("view3d.view_camera", text="View Cam", icon='HIDE_OFF')
        other_menu.operator("view3d.camera_to_view", text="Cam To View", icon='NONE')
  
        if bpy.context.space_data.lock_camera is False:
            other_menu.operator("wm.context_toggle", text="Lock Cam To View",
                            icon='UNLOCKED').data_path = "space_data.lock_camera"
        elif bpy.context.space_data.lock_camera is True:
            other_menu.operator("wm.context_toggle", text="Lock Cam to View",
                            icon='LOCKED').data_path = "space_data.lock_camera"

        icon_locked = 'LOCKED' if ob and ob.lock_rotation[0] is False else \
                        'UNLOCKED' if ob and ob.lock_rotation[0] is True else 'LOCKED'

        other_menu.prop(rd, "use_border", text="Border")

        # 言語の切り替え
        other_menu.operator("object.pie22_operator")

        prefs = bpy.context.preferences
        view = prefs.view
        other_menu.prop(view, "language")
        # other_menu = layout.column(heading="Affect")
        # other_menu.active = (bpy.app.translations.locale != 'en_US')
        if bpy.app.translations.locale != 'en_US':
            other_menu.prop(view, "use_translate_tooltips", text="Tooltips")
            other_menu.prop(view, "use_translate_interface", text="Interface")
            other_menu.prop(view, "use_translate_new_dataname", text="New Data")
 

    def right_draw(self):
        layout = self.layout
        pie = layout.menu_pie()


        box = pie.split().column()
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
        row.operator("object.copyasset_operator")
        row.operator("object.material_append",text=get_translang("Matarial Append","マテリアル適応"))


 
    def draw(self, context):
        # 4 - LEFT
        left_draw(self)

        # 6 - RIGHT
        self.right_draw()

        # 2 - BOTTOM
        bottom_draw(self)
       
        # 8 - TOP
        top_draw(self)

        # 7 - TOP - LEFT
        top_left_draw(self)

        # 9 - TOP - RIGHT
        top_right_draw(self)

        # 1 - BOTTOM - LEFT
        self.bottom_left_draw()

        # 1 - BOTTOM - RIGHT
        botom_right_draw(self)
