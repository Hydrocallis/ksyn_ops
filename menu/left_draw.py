import bpy

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng
    
def left_draw_edit_mode(row,box):
        
        row.label(text = "Slect Menu")
        row = box.row(align=True)
        row.operator("mesh.select_all", text="All").action = 'SELECT'
        row.operator("mesh.select_mirror").extend = True

        row = box.row(align=True)
        row.operator("object.pie18_operator")
        row.operator("mesh.select_linked", text="Linked")
        row.operator("ksyn.get_face_by_side")
        row.menu("VIEW3D_MT_edit_mesh_select_similar")

        row = box.row(align=True)
        row.label(text = "Mesh Display")
        row = box.row(align=True)
        row.operator("mesh.reveal")
        row.operator("object.pie4_operator")
        row = box.row(align=True)
        row.label(text = "Mesh deformation")
        row = box.row(align=True)
        row.operator("object.meshmirror_operator")
        row.operator("mesh.convert_ngons_to_tris")
        row = box.row(align=True)
        row.operator("object.simplerotate")
        row.operator("mesh.bevel_extrude")
        row.operator("object.originset_oparetor")
        row = box.row(align=True)
        props= bpy.context.scene.myedit_property_group

        
        row = box.row(align=True)




        if hasattr(bpy.types, bpy.ops.object.simplearry_operator.idname()):
            row.label(text="MESH ARRAY")
            row = box.row(align=True)
            row.operator("object.simplearry_operator")
        else:
            pass
            # row.label(text="simplearry_operatorのオペレータークラスは登録されてません。")

        if hasattr(bpy.types, "MESHARRAY_PT_PANEL"):
            row = box.row(align=True)
            row.popover("MESHARRAY_PT_PANEL", text = "MESHARRAY_PANEL", icon='MOD_ARRAY')
        else:
            # print('###OBJECT_PT_piesetting_fbxexport','のクラスが見つかりませんのでパスします。', )
            pass



        row = box.row(align=True)
        # row.prop(props, "uv_pie_selct_bool", text = "UV_Menu")

        if props.uv_pie_selct_bool == True:
            row = box.row(align=True)
            row.operator("object.pie19_operator")
            row.operator("object.pie20_operator")
            row = box.row(align=True)
            row.operator("object.uv_unwrap")
            row = box.row(align=True)
            row.operator("object.uv_selmirseam")

        row = box.row(align=True)
        #　メッシュ操作関係
        row.label(text = "Mesh Oparator")
        row = box.row(align=True)
        row.operator("object.select_mesh_separate_operator",text=get_translang('Mesh Duplicate','選択メッシュ複製')).duplicate_move = True
        row.operator("object.select_mesh_separate_operator",text=get_translang('Mesh Separate','選択メッシュ分離')).duplicate_move = False
        row.operator("mesh.mesh_ot_bicect_mirror")
        row.operator("object.separate_and_join_operator")

        row.label(text = "            ")# ダミー

        # row.operator("object.pie7_operator")
        row = box.row(align=True)

def left_draw(self):
    layout = self.layout
    layout.column()
    
    pie = layout.menu_pie()
    box = pie.split().column()
    # y軸方向に空間を開けるための空白を用意
    separete = box.row(align=True)
    separete.separator()
    separete.scale_y = 5
    separete
    row = box.row(align=True)

    #     'VERTEX_GPENCIL']、デフォルト 'EDIT_MESH'、（読み取り専用）
    if bpy.context.mode == 'EDIT_MESH':
        left_draw_edit_mode(row,box)
      
    ### OBJECT MODE
    else:

        row.operator_menu_enum("object.modifier_add", "type")
        # row = box.row(align=True)
        # row.operator("object.pie8_operator")
        # row.operator("object.pie9_operator")
        row = box.row(align=True)
        row.operator("object.meshmirror_operator")
        row.operator("ksyn.select_children_recursive")
        # 削除クリーンアップ関係
        row = box.row(align=True)
        row.label(text = "CleanUp")

        row = box.row(align=True)
        row.operator("object.mesh_emptyverdel")
        row = box.row(align=True)
        row.operator("object.material_delete_operator")
        
        row = box.row(align=True)
        row.label(text = "Boolean")
        row = box.row(align=True)
        row.operator("object.boolonoff_operator")
        # row.operator("object.boolean_operator")
        row = box.row(align=True)

        row.operator("object.selectobjectbool_operator").cmd = "simpleboolean"
        # row.operator("object.geometry_nodes_operator")
        row.operator("object.selectobjectbool_operator",text=get_translang('Appy Boolean','ブーリアン適応')).cmd = "applyboolean"



        # row.operator("object.uv_seleobjsmartuv")
        row = box.row(align=True)
            
        if hasattr(bpy.types, "SIMPLEOBJECT_PT_PANEL"):
            row.label(text="SIMPLE OBJECT")
            row = box.row(align=True)
            row.popover("SIMPLEOBJECT_PT_PANEL", text = "SIMPLEOBJECT_PT_PANEL", icon='FILE_3D')
        else:
            # print('###OBJECT_PT_piesetting_fbxexport','のクラスが見つかりませんのでパスします。', )
            pass
