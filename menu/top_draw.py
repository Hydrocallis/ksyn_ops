import bpy

def modeset(self,col):

    obj = bpy.context.active_object

    object_mode = 'OBJECT' if obj is None else obj.mode
    has_pose_mode = (
        (object_mode == 'POSE') or
        (object_mode == 'WEIGHT_PAINT' and bpy.context.pose_object is not None)
    )

    act_mode_item = bpy.types.Object.bl_rna.properties["mode"].enum_items[object_mode]
    act_mode_i18n_context = bpy.types.Object.bl_rna.properties["mode"].translation_context
    # row = layout.row(align=True)
    # sub = row.row(align=True)
    col.ui_units_x = 5.5
    col.operator("object.toggle_mode",text="Object").mode ="OBJECT"
    col.operator("object.toggle_mode",text="Edit").mode ="EDIT"
    col.operator("object.toggle_mode",text="Sculpt").mode ="SCULPT"

def top_draw(self):
    layout = self.layout
    pie = layout.menu_pie()
    col = pie.column(align=True)
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[__name__.split(".")[0]].preferences

    modeset(self,col)
    col.popover('OBJECT_PT_transform', icon='RIGHTARROW_THIN',  text='TRANSFORM')

    if addon_prefs.adminmode ==True:
        col.scale_x = 0.5 # メニューの幅を半分に制限する
        # col.popover("OBJECT_PT_piesetting_arm", text = "AMATURE", icon='ARMATURE_DATA')
        row = col.row(align=True)
        row = col.row(align=True)
        row.popover("PIE3D_PT_PIESETTING", icon='TRIA_UP')
        # row = col.row(align=True)
        # row.operator("object.uvgridmat", icon='EVENT_U')
        # # row = col.row(align=True)
        # # row.operator("object.subdivision_show", icon='TRIA_UP')
        # row = col.row(align=True)
        # row.operator("object.colorpickup_object", icon='EYEDROPPER',text="Obj Color")
        # row = col.row(align=True)

        # # row.menu("PIE_MT_InstansMenu2", icon='EYEDROPPER')

