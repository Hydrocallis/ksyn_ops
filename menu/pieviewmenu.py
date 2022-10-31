import bpy, sys

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

class PIE_MT_ViewNumpad(Menu):
    bl_idname = "PIE_MT_viewnumpad_mypanel"
    bl_label = "CUSYANG_Pie Views Menu_"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "

    def botom_right_draw(self):
        layout = self.layout
        pie = layout.menu_pie()

        
        if bpy.context.mode == 'EDIT_MESH':
            other = pie.column()
            gap = other.column()
            gap.separator()
            gap.scale_y = 30
            other_menu = other.box().column()
            other_menu.scale_y=1.3

            other_menu.menu('VIEW3D_MT_edit_mesh_merge', icon='RIGHTARROW_THIN',  text='marge_vertex')
            other_menu.popover('OBJECT_PT_transform', icon='RIGHTARROW_THIN',  text='TRANSFORM')



        else:
            other = pie.column()
            gap = other.column()
            gap.separator()
            gap.scale_y = 10
            other_menu = other.box().column()
            other_menu.scale_y=1.3
            if bpy.context.mode == 'PAINT_WEIGHT':
                   other_menu.operator("object.weightpaint_value_chnage")
            other_menu.popover('OBJECT_PT_transform', icon='RIGHTARROW_THIN',  text='TRANSFORM')
            other_menu.menu('PIE_MT_InstansMenu', icon='RIGHTARROW_THIN', text = "オブジェクトコピー")
            other_menu.operator("object.look_for_no_geometry_operator")

    def bottom_left_draw(self):
        ob = bpy.context.active_object
        scene = bpy.context.scene
        rd = scene.render

        layout = self.layout
        pie = layout.menu_pie()


        other = pie.column()
        gap = other.column()
        gap.separator()
        gap.scale_y = 35
        other_menu = other.box().column()
        other_menu.scale_y=1.3

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
            other_menu.operator("object.cuspie23_pie_operator")


    def left_draw(self):
        layout = self.layout
        pie = layout.menu_pie()

        box = pie.split().column()
       
        # y軸方向に空間を開けるための空白を用意
        separete = box.row(align=True)
        separete.separator()
        separete.scale_y = 5
  

        row = box.row(align=True)
        #エディットモードの場合はこれを表示する https://docs.blender.org/api/current/bpy.context.html#bpy.context.mode
        #         タイプ
        # ['EDIT_MESH'、 'EDIT_CURVE'、 'EDIT_SURFACE'、 'EDIT_TEXT'、 'EDIT_ARMATURE'、
        #  'EDIT_METABALL'、 'EDIT_LATTICE'、 'POSE'、 'SCULPT'、 'PAINT_WEIGHT'、
        #   'PAINT_VERTEX'、 'PAINT_TEXTURE'の列挙型、 'PARTICLE'、 'OBJECT'、
        #    'PAINT_GPENCIL'、 'EDIT_GPENCIL'、 'SCULPT_GPENCIL'、 'WEIGHT_GPENCIL'、
        #     'VERTEX_GPENCIL']、デフォルト 'EDIT_MESH'、（読み取り専用）
        if bpy.context.mode == 'EDIT_MESH':
            
            row.label(text = "Slect_Menu")
            row = box.row(align=True)
            row.operator("object.pie2_operator")
            row.operator("mesh.select_mirror").extend = True
  
            row = box.row(align=True)
            row.operator("object.pie3_operator")
            row.operator("object.pie4_operator")
            row = box.row(align=True)
            row.operator("object.pie18_operator")
            row = box.row(align=True)
            props= bpy.context.scene.myedit_property_group
    
            row.prop(props, "uv_pie_selct_bool", text = "UV_Menu")
            
            row = box.row(align=True)

            if hasattr(bpy.types, bpy.ops.object.simplearry_operator.idname()):
                row.operator("object.simplearry_operator")
            else:
                row.label(text="simplearry_operatorのオペレータークラスは登録されてません。")

            if props.uv_pie_selct_bool == True:
                row = box.row(align=True)
                row.operator("object.pie19_operator")
                row.operator("object.pie20_operator")
                row = box.row(align=True)
                row.operator("object.uv_unwrap")
                row = box.row(align=True)
                row.operator("object.uv_selmirseam")

            row = box.row(align=True)
            row.label(text = "Selct mesh")
            row = box.row(align=True)
            row.operator("object.pie21_operator")
            row.operator("object.pie7_operator")
            row = box.row(align=True)

        else:
            row.operator("object.pie8_operator")
            row.operator("object.pie9_operator")
            row = box.row(align=True)
            row.operator("object.pie11_operator")
            row = box.row(align=True)
            row.operator("object.material_delete_operator")
            row = box.row(align=True)
            row.operator("object.boolonoff_operator")
            row.operator("object.selectobjectbool_operator")
            row = box.row(align=True)
            row.operator("object.pie15_operator")
            row.operator("object.mesh_emptyverdel")
            row = box.row(align=True)
            row.operator("object.uv_seleobjsmartuv")


    def right_draw(self):
        layout = self.layout
        pie = layout.menu_pie()


        box = pie.split().column()
        row = box.row(align=True)
        row.operator("object.pie1_operator")
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
        other_menu.operator("script.reload")
        if hasattr(bpy.types, "TEXTEDITOR_PT_panel"):
            other_menu.popover("TEXTEDITOR_PT_panel", text = "TEST", icon='EXPORT')
        else:
            other_menu.label( text = "オペは見つかりません", icon='EXPORT')

            print('### 3D からテキストへの読み込みで、TEXT_PT_ImputComment2のクラスが見つかりませんのでパスします。', )


    
    def top_draw(self):
        layout = self.layout
        pie = layout.menu_pie()

        box = pie.split().column()
        row = box.row(align=True)
        row.popover("OBJECT_PT_piesetting", icon='TRIA_UP')
        row = box.row(align=True)
        row.operator("object.uvgridmat", icon='EVENT_U')
        row = box.row(align=True)
        row.operator("object.subdivision_show", icon='TRIA_UP')
        row.operator("object.colorpickup_object", icon='EYEDROPPER')

    def top_left_draw(self):
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.split().column()

        row =box.row()
        row.popover("OBJECT_PT_piesetting_arm", text = "AMATURE", icon='ARMATURE_DATA')
        row.operator("wm.save_mainfile", text="Save", icon='FILE_TICK')
        row.operator("wm.save_as_mainfile", text="Save As...")
        
            
    def top_right_draw(self):
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.split().column()

        row =box.row()
        
        if hasattr(bpy.types, "SIMPLEFBXECPORT_PT_SETTINGFBXEXPORT"):
            row.popover("SIMPLEFBXECPORT_PT_SETTINGFBXEXPORT", text = "FBXEXPORT", icon='EXPORT')
        else:
            # print('###OBJECT_PT_piesetting_fbxexport','のクラスが見つかりませんのでパスします。', )
            pass

        
    def draw(self, context):
        # 4 - LEFT
        self.left_draw()

        # 6 - RIGHT
        self.right_draw()

        # 2 - BOTTOM
        self.bottom_draw()
       
        # 8 - TOP
        self.top_draw()

        # 7 - TOP - LEFT
        self.top_left_draw()

        # 9 - TOP - RIGHT
        self.top_right_draw()

        # 1 - BOTTOM - LEFT
        self.bottom_left_draw()

        # 1 - BOTTOM - RIGHT
        self.botom_right_draw()
