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
from .bottom_left_draw import bottom_left_draw
from .right_draw import right_draw

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng
    
def get_addon_version(addon_name):
    return sys.modules[addon_name].bl_info.get("version", (-1,-1,-1))



class KSN_MT_node_editerpiemenu(Menu):
    addon_version = get_addon_version(__package__.split(".")[0])

    bl_idname = "KSN_MT_node_editerpiemenu_menu"
    bl_label = f"KSYN OPS Pie Node Menu v{addon_version[0]}.{addon_version[1]}.{addon_version[2]}"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
 
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.separator() # Skip West position
        pie.separator() # Skip East position
        pie.operator("object.rename_active_node",icon = "FONT_DATA")
        pie.operator("node.detach",icon = "CON_TRANSLIKE")
        prefs = bpy.context.preferences
        view = prefs.view
        other = pie.column()
        other_menu = other.box().column()

        other_menu.prop(view, "language")
        # other_menu = layout.column(heading="Affect")
        # other_menu.active = (bpy.app.translations.locale != 'en_US')
        if bpy.app.translations.locale != 'en_US':
            other_menu.prop(view, "use_translate_tooltips", text="Tooltips")
            other_menu.prop(view, "use_translate_interface", text="Interface")
            other_menu.prop(view, "use_translate_new_dataname", text="New Data")


class PIE_MT_ViewNumpad(Menu):
    addon_version = get_addon_version(__package__.split(".")[0])

    bl_idname = "PIE_MT_viewnumpad_mypanel"
    bl_label = f"KSYN OPS Pie Menu v{addon_version[0]}.{addon_version[1]}.{addon_version[2]}"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
 
    def draw(self, context):
        # 4 - LEFT
        left_draw(self)

        # 6 - RIGHT
        right_draw(self)

        # 2 - BOTTOM
        bottom_draw(self)
       
        # 8 - TOP
        top_draw(self)

        # 7 - TOP - LEFT
        top_left_draw(self)

        # 9 - TOP - RIGHT
        top_right_draw(self)

        # 1 - BOTTOM - LEFT
        bottom_left_draw(self)

        # 1 - BOTTOM - RIGHT
        botom_right_draw(self)
