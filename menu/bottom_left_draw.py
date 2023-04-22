
import bpy

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
    # other_menu.operator("object.pie22_operator")

    prefs = bpy.context.preferences
    view = prefs.view
    other_menu.prop(view, "language")
    # other_menu = layout.column(heading="Affect")
    # other_menu.active = (bpy.app.translations.locale != 'en_US')
    if bpy.app.translations.locale != 'en_US':
        other_menu.prop(view, "use_translate_tooltips", text="Tooltips")
        other_menu.prop(view, "use_translate_interface", text="Interface")
        other_menu.prop(view, "use_translate_new_dataname", text="New Data")
