
# フォルダ読み込みに必要なこと。　
# インポートするだけではだめで、
# フォルダの場合はレジスターに登録してあげないと、
# 中のININTファイルが読み込まれない仕様である。

bl_info = {
    "name": "custum_3d_view_pie",
    "description": "Viewport custum",
    "author": "kk",
    "version": (0, 1, 1),
    "blender": (2, 93, 0),
    "location": "shift ctrl Q key",
    "warning": "",
    "doc_url": "",
    "category": "MY"
    }

if "bpy" in locals():
    import importlib
    reloadable_modules = [ # リストに読み込むものをまとめる
    # フォルダを再登録
    "panel",
    "properties",
    "operators",
    "menu",


    ]
    for module in reloadable_modules: # リスト内のものがすでにあれば、reloadを発動する
        if module in locals():
            importlib.reload(locals()[module])

import bpy, sys, os, subprocess

from . import operators
from . import properties
from . import panel
from . import menu




from math import radians
from mathutils import Matrix
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )

class PIE3D_OT_PiePropsSetting(Operator):
        bl_idname = 'object.pie_props_setting'
        bl_label = 'piepropssetting'
        # 自身のクラスの呼び出しにはSYSモジュールが必要
        bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
        
        
        def execute(self, context):
            return context.window_manager.invoke_popup(self)


        def draw(self, context):
            layout = self.layout
            props = context.scene.myedit_property_group

            row = layout.row()
            row.prop(props, "edit_int")
            row = layout.row()
            row.prop(props, "color_pic")
            row = layout.row()
            row.prop(props, "target_armature")
            row = layout.row()
            row.operator("object.amaturerestbool")
            row = layout.row()
            row.prop(props, "workspace_path")
            row = layout.row()
            row.prop(props, "fbx_selectbool")
            row = layout.row()
            row.prop(props, "fbx_act_collection_bool")
            row = layout.row()
            row.operator("object.fbxexortsupport")
            row = layout.row()

class PIE3D_OT_ColorPickupObject(Operator):
    """Tooltip"""
    bl_idname = "object.colorpickup_object"
    bl_label = "ColorPickupObject"

  
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj_color = context.scene.myedit_property_group.color_pic
            obj.color = obj_color

            
        return {'FINISHED'}

class PIE3D_OT_SubdivisionShow(Operator):
    """Tooltip"""
    bl_idname = "object.subdivision_show"
    bl_label = "subdivision_show"

    @classmethod
    def poll(cls, context):
        sub_mod = False
        for mod in bpy.context.object.modifiers:
            if mod.name == "Subdivision":
                sub_mod = True
                # print(sub_mod)
            else:
                pass
        return sub_mod
   
    def execute(self, context):
        if context.object.modifiers["Subdivision"].show_on_cage == False:
            context.object.modifiers["Subdivision"].show_on_cage = True
        
        elif context.object.modifiers["Subdivision"].show_on_cage == True:
            context.object.modifiers["Subdivision"].show_on_cage = False
            
        return {'FINISHED'}

class PIE3D_OT_AmatureRestBool(Operator):
    """Tooltip"""
    bl_idname = "object.amaturerestbool"
    bl_label = "amaturerestbool"

    @classmethod
    def poll(cls, context):
        props = context.scene.myedit_property_group
        return props.target_armature is not None
   

    def execute(self, context):
        props = context.scene.myedit_property_group
        print('###',props.target_armature)
        print('###',props.target_armature.name)
        amaturtur = props.target_armature
        print('###',amaturtur.data.pose_position)
        amr_pose = amaturtur.data.pose_position

        if amr_pose == "POSE":
            bpy.data.armatures[amaturtur.name].pose_position = "REST"
        
        elif amr_pose == "REST":
            bpy.data.armatures[amaturtur.name].pose_position = "POSE"

     
            
        return {'FINISHED'}
# Lock Camera Transforms
class PIE_OT_LockTransforms(Operator):
    bl_idname = "object.locktransforms"
    bl_label = "Lock Object Transforms"
    bl_description = ("Enable or disable the editing of objects transforms in the 3D View\n"
                     "Needs an existing Active Object")
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        if obj.lock_rotation[0] is False:
            obj.lock_rotation[0] = True
            obj.lock_rotation[1] = True
            obj.lock_rotation[2] = True
            obj.lock_scale[0] = True
            obj.lock_scale[1] = True
            obj.lock_scale[2] = True

        elif context.object.lock_rotation[0] is True:
            obj.lock_rotation[0] = False
            obj.lock_rotation[1] = False
            obj.lock_rotation[2] = False
            obj.lock_scale[0] = False
            obj.lock_scale[1] = False
            obj.lock_scale[2] = False

        return {'FINISHED'}

class pie1(Operator):
    bl_idname = "object.pie1_operator"
    bl_label = "オブジェクトにワイヤー表示"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        ob = bpy.context.object
        # 選択したオブジェクト
        # https://blenderartists.org/t/first-python-coding-toggle-wire-display-for-entire-scene/634793

        obs = bpy.context.selected_objects

        if ob is None:
            for o in obs:
                if o.type == 'MESH':
                    ob = o
                    break

        if ob is not None:
            show_wire = not ob.show_wire
            for ob in obs:
                if ob.type == 'MESH':
                    ob.show_wire = show_wire

        return {'FINISHED'}

class pie2(Operator):
    bl_idname = "object.pie2_operator"
    bl_label = "メッシュ全選択"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        ob = bpy.context.object
        # 選択したオブジェクト
        # https://blenderartists.org/t/first-python-coding-toggle-wire-display-for-entire-scene/634793

        bpy.ops.mesh.select_all(action='SELECT')
        return {'FINISHED'}

class pie3(Operator):
    bl_idname = "object.pie3_operator"
    bl_label = "隠していた選択面を表示"

    def execute(self, context):
        bpy.ops.mesh.reveal()
        return {'FINISHED'}

class pie4(Operator):
    bl_idname = "object.pie4_operator"
    bl_label = "選択面以外を非表示"

    def execute(self, context):
        bpy.ops.mesh.hide(unselected=True)
        return {'FINISHED'}

class pie7(Operator):
    bl_idname = "object.pie7_operator"
    bl_label = "subdivide"

    def execute(self, context):
        bpy.ops.mesh.subdivide()
        return {'FINISHED'}

class pie8(Operator):
    bl_idname = "object.pie8_operator"
    bl_label = "X軸90回転"

    def execute(self, context):
        obj = bpy.context.active_object
        obj.matrix_world @= Matrix.Rotation(radians(90), 4, 'X')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

class pie9(Operator):
    bl_idname = "object.pie9_operator"
    bl_label = "Y軸90回転"

    def execute(self, context):
        obj = bpy.context.active_object
        obj.matrix_world @= Matrix.Rotation(radians(90), 4, 'Y')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

class pie10(Operator):
    bl_idname = "object.pie10_operator"
    bl_label = "スムーズ"

    def execute(self, context):
        bpy.ops.object.shade_smooth()
        bpy.context.object.data.use_auto_smooth = True

        return {'FINISHED'}

class pie11(Operator):
    bl_idname = "object.pie11_operator"
    bl_label = "Z軸90回転"

    def execute(self, context):
        obj = bpy.context.active_object
        obj.matrix_world @= Matrix.Rotation(radians(90), 4, 'Z')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

class pie15(Operator):
    bl_idname = "object.pie15_operator"
    bl_label = "mesh-x-mirror"

    def execute(self, context):
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(-1, 0, 0), clear_inner=False, clear_outer=True, xstart=376, xend=376, ystart=225, yend=224, flip=False)
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.context.object.modifiers["Mirror"].use_clip = True
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

class pie18(Operator):
    bl_idname = "object.pie18_operator"
    bl_label = "フラット面を選択"

    def execute(self, context):
        bpy.ops.mesh.faces_select_linked_flat()
        return {'FINISHED'}

class pie19(Operator):
    bl_idname = "object.pie19_operator"
    bl_label = "シームをクリア"

    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=True)
        return {'FINISHED'}

class pie20(Operator):
    bl_idname = "object.pie20_operator"
    bl_label = "シームをつける"

    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=False)
        return {'FINISHED'}

class pie21(Operator):
    bl_idname = "object.pie21_operator"
    bl_label = "面オブジェクト分離"

    def execute(self, context):
        def obj_copy():
# 選択した面をセパレートして別オブジェクト化するスクリプト
            obj_name = bpy.context.active_object.name
            print(obj_name)

            bpy.ops.mesh.duplicate_move()
            #obj_copy()
            bpy.ops.mesh.separate(type='SELECTED')
            bpy.ops.object.mode_set(mode='OBJECT')
            obj2_name = bpy.context.selected_objects[1].name
            print(obj2_name)
            ## オブジェクトのアクティブ化
            ob = bpy.context.scene.objects[obj2_name]   # maeno object wo sentaku# ここに指定したオブジェクトの名前をついかする
            bpy.context.view_layer.objects.active = ob
            
            bpy.context.scene.objects[obj_name].select_set(False)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
        obj_copy()
        return {'FINISHED'}

# 廃止予定
class pie22(Operator):
    bl_idname = "object.pie22_operator"
    bl_label = "言語の切り替え"# 言語の切り替え
    bl_options = {'REGISTER', 'UNDO'}
# 入力の数値を登録

    # myCheckField: bpy.props.BoolProperty(
    #     name="InterFac",
    #     default=False
    # )
    # myCheckField2: bpy.props.BoolProperty(
    #     name="ToolTips",
    #     default=False
    # )
    
# 実際の実行関数
    def execute(self, context):
        pass
        # bpy.context.preferences.view.use_translate_interface = self.myCheckField
        # bpy.context.preferences.view.use_translate_tooltips = self.myCheckField2
        return {'FINISHED'}

def draw(self, context, layout):
    prefs = context.preferences
    view = prefs.view

    layout.prop(view, "language")

    col = layout.column(heading="Affect")
    col.active = (bpy.app.translations.locale != 'en_US')
    col.prop(view, "use_translate_tooltips", text="Tooltips")
    col.prop(view, "use_translate_interface", text="Interface")
    col.prop(view, "use_translate_new_dataname", text="New Data")

class CUSPIE23_OT_pie_operator(Operator):
    bl_idname = "object.cuspie23_pie_operator"
    bl_label = "OB＿MESH＿NAME"# 言語の切り替え
    bl_description = '"object.pie23_operator\nオブジェクト名にメッシュ名前を入れ替え'

# 実際の実行関数
    def execute(self, context):
        for ob in bpy.context.selected_objects:
            ob.data.name = ob.name
        return {'FINISHED'}
# アドオンの項目の設定項目
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

addon_keymapscuspie = []

class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")
        layout.prop(self, "number")
        layout.prop(self, "boolean")

        import rna_keymap_ui 
        layout = self.layout
        wm = context.window_manager
        kc = wm.keyconfigs.user
        old_km_name = "" 
        old_id_l = [] 
        for km_add, kmi_add in addon_keymapscuspie: 
            km = kc.keymaps[km_add.name] 
            for kmi_con in km.keymap_items: 
                if kmi_add.idname == kmi_con.idname: 
                    if not kmi_con.id in old_id_l:
                        kmi = kmi_con 
                        old_id_l.append(kmi_con.id) 
                        break 
            if kmi:
                if not km.name == old_km_name: 
                    layout.label(text=km.name,icon="DOT") 
                layout.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)
                layout.separator()
                old_km_name = km.name
                kmi = None
# クラスの登録
classes = (
            ExampleAddonPreferences,
            PIE_OT_LockTransforms,
            PIE3D_OT_ColorPickupObject,
            PIE3D_OT_SubdivisionShow,
            PIE3D_OT_AmatureRestBool,
            pie1,
            pie2,
            pie3,
            pie4,
            pie7,
            pie8,
            pie9,
            pie10,
            pie11,
            pie15,
            pie18,
            pie19,
            pie20,
            pie21,
            pie22,
            CUSPIE23_OT_pie_operator,
            )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    operators.register()
    panel.register()
    menu.register()
    properties.register()



    # 通常の３Dモードの（オブジェクトモードでしか何故か登録できない）キーマップ登録
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True, ctrl=True)
        kmi.properties.name = "PIE_MT_viewnumpad"
        addon_keymapscuspie.append((km, kmi))

    wm = bpy.context.window_manager
    
    # メッシュモードでのキーマップ登録
    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True, ctrl=True)
        kmi.properties.name = "PIE_MT_viewnumpad"
        addon_keymapscuspie.append((km, kmi))

    wm = bpy.context.window_manager
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    operators.unregister()
    panel.unregister()
    menu.unregister()
    properties.unregister()


    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymapscuspie:
            km.keymap_items.remove(kmi)
    addon_keymapscuspie.clear()

if __name__ == "__main__":
    register()
