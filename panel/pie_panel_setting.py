import bpy,sys

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

from ..utils.get_translang import get_translang

class PIE3D_PT_PIESETTINGARM_main:
    """Creates a Panel in the Object properties window"""
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"
    
class PIE3D_PT_PIESETTING1(PIE3D_PT_PIESETTINGARM_main,Panel):
    bl_label = get_translang("Pie Panel","パイパネル")
    bl_idname = "PIE3D_PT_PIESETTING"
        # アドオンのバージョンを取得する関数
    def get_addon_version(self,addon_name):
        return sys.modules[addon_name].bl_info.get("version", (-1,-1,-1))



    def draw(self, context):
         
        addon_version = self.get_addon_version(__package__.split(".")[0])
        self.layout.label(text=f"Addon Version: {addon_version[0]}.{addon_version[1]}.{addon_version[2]}")

        pass

class PIE3D_PT_PIESETTING2(PIE3D_PT_PIESETTINGARM_main,Panel):
    bl_label = "pie Setting Armture"
    bl_parent_id = "PIE3D_PT_PIESETTING"

    def draw(self, context):
        layout = self.layout
        props = context.scene.myedit_property_group


        row = layout.row()
        row.prop(props, "target_armature")
        row = layout.row()
        row.operator("object.amaturerestbool")

class PIE3D_PT_PIESETTING3(PIE3D_PT_PIESETTINGARM_main,Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "pie Setting Colorpic"
    bl_parent_id ="PIE3D_PT_PIESETTING"


    def draw(self, context):
        layout = self.layout
        props = context.scene.myedit_property_group


        row = layout.row()
        row.prop(props, "edit_int")
        row = layout.row()
        row.prop(props, "color_pic")


        row = layout.row()
        row.operator("object.uvgridmat")

        matname_list =[mat.name for mat in bpy.data.materials]
        matbool = "UVGRID" in matname_list
        row = layout.row()
        row.prop(props, "uv_grid_material_image_bool")
        if  matbool == True:
            row = layout.row()
            row.prop(props, "uv_grid_scail_size")
            row = layout.row()
            row.prop(props, "uv_grid_material_duplicate_bool")

        row = layout.row()
        row = layout.row()
        row.prop(props, "crease_themas_bool")
        row = layout.row()
        row.operator("object.uv_map_delete_change")     

        sel_objs = bpy.context.selected_objects
        for  sele_ob in sel_objs:
            obj_data = sele_ob.data
            row = layout.row()
            if sele_ob.type == "MESH": 
                row.label(text=sele_ob.name)
                row = layout.row()
                row.template_list("MESH_UL_uvmaps", "uvmaps", obj_data, "uv_layers", obj_data.uv_layers, "active_index", rows=2)


class SIMPLEOBJECT_PT_PANEL(PIE3D_PT_PIESETTINGARM_main,Panel):
    bl_label = "Simple Object"
    # bl_idname = "SIMPLEOBJECT_PT_PANEL"
    # bl_space_type = 'VIEW_3D'
    # bl_region_type = 'UI'
    # bl_category = "KSYN"
    bl_parent_id = "PIE3D_PT_PIESETTING"

   


    def draw(self, context):

        layout = self.layout
        props = bpy.context.scene.simple_object_propertygroup

        if bpy.context.mode == "EDIT_MESH":
            if bpy.context.object != None and len (bpy.context.selected_objects) > 0 :
                layout.operator("object.easy_knife_project",
                text="Easy Knife Project"
                )


        if bpy.context.mode == "OBJECT":

            if bpy.context.object != None:

                objarraybox = layout.box()  
                
                objarraybox.operator(
                    "object.obuect_easy_array",
                    text="Object Easy Array"
                    )

                objarraybox.operator(
                    "object.ciercle_dupulicate",
                    text="Circle Dupulicate"
                    )
        
        curvebox = layout.box()

        if bpy.context.object != None and len (bpy.context.selected_objects) > 0 :
            curvebox.operator(
                "object.easy_curve_to_mesh",
                text="Easy Curve To Mesh"
                )
            # curvebox.operator(
            #     "object.edge_fr_vertex",
            #     )

            curvebox.operator(
                "object.curve_mirror",
                )
                
        curvebox.label(text="Curve object to change the shape of a curve")                                                                        
        curvebox.prop(props, "target_curve",text="Target Curve")

        # その他アシスト機能
        otherbox = layout.box()
        if bpy.context.mode == "OBJECT":
            if bpy.context.object != None:
                otherbox.operator(
                    "object.wordlorijn_move",
                    text="World Origin Move"
                    )
                
                otherbox.operator(
                    "object.object_easy_mirror",
                    text="Easy Object Mirror"
                    )
                otherbox.menu('PIE_MT_InstansMenu', icon='RIGHTARROW_THIN', text = "オブジェクトコピー")
                
        layout.separator()

        layout.operator(
            "object.visual_transform_apply",
            text="Visual Transform",
        )
        layout.operator(
            "object.convert",
            text="Visual Geometry to Mesh",
        ).target = 'MESH'
        layout.operator("object.link_objects_to_new_scene_operator", text=get_translang('New Scene','オブジェクトをシーンへ'))
        layout.operator("object.duplicates_make_real")
        layout.operator("object.join_hierarchy_objects",text=get_translang("Join Hierarchy Objects","階層オブジェクトの結合"))
        layout.operator("object.square_empty_layout_operator",text=get_translang("Square Empty Layout Operator","正方形の空のレイアウト"))

        layout.label(text=get_translang('Instans Object','インスタンス化'))
                # サブメニューの登録
        # layout.operator("object.objectinstansmirror_operator", text="オブジェクトのミラー化", icon="MOD_MIRROR")
        layout.operator("object.objectinstans_operator", text="インスタンス化", icon="OUTLINER_OB_GROUP_INSTANCE")
        layout.separator()
        layout.operator("object.cleanupinstans_operator", text="クリーンアップ", icon="FILE_REFRESH")







        