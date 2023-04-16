import bpy

def get_translang(eng,trans):
    prev=bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
         return trans
    else:
         return eng

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

        other_menu.label(text=get_translang("UV","UV関係"))
        other_menu.operator("object.uv_setting",text=get_translang("Rotation uv","UVを回転")).cmd ="rotationuv"
        other_menu.operator("object.uv_setting",text=get_translang("Rotate UV 90","UVを90度回転")).cmd ="90rotation"
        other_menu.operator("object.uv_setting",text=get_translang("Selected UV Scale","選択面のみUVの縮尺変更")).cmd ="scalesize"
        other_menu.operator("object.uv_setting",text=get_translang("Scale of UVs of active material","アクティブなマテリアルのUVの縮尺")).cmd ="uvscalechange"
        other_menu.operator("object.uv_selmirseam",text=get_translang("Mirror Seam","シームをミラー"))
        other_menu.menu('VIEW3D_MT_edit_mesh_merge', icon='RIGHTARROW_THIN')



    else:
        other = pie.column()
        gap = other.column()
        gap.separator()
        gap.scale_y = 30
        other_menu = other.box().column()
        other_menu.scale_y=1.3
        if bpy.context.mode == 'PAINT_WEIGHT':
                other_menu.operator("object.weightpaint_value_chnage")
        # other_menu.menu('PIE_MT_InstansMenu', icon='RIGHTARROW_THIN', text = "オブジェクトコピー")
        other_menu.operator("object.look_for_no_geometry_operator")
        other_menu.operator("object.lastselectaddempty")
        # メニューにおけるオペレターの確認
        if hasattr(bpy.types, bpy.ops.bake.simpleobjectbake.idname()):
            other_menu.operator("bake.simpleobjectbake").cmd = "bake"
        else:
            pass
