import bpy,sys,inspect

from bpy.types import (
        Operator,
        )

from ksyn_ops.utils.get_translang import get_translang
from ksyn_ops.utils.operators_utils import description
from mathutils import Matrix
from math import radians
import pathlib
from bpy.props import FloatProperty

class ChangeLightEnergyOperator(bpy.types.Operator):
    bl_idname = "object.change_light_energy"
    bl_label = "Change Light Energy"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}
    
    
    energy : FloatProperty(name="Energy", default=1.0, min=0.0)
    

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        
        for obj in selected_objects:
            if obj.type == 'LIGHT':
                obj.data.energy = self.energy
        
        return {'FINISHED'}




class ImportNodeGroupsOperator(Operator):
    bl_idname = "object.import_node_groups"
    bl_label = "Import Node Groups"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO' }
  
    operation : bpy.props.EnumProperty(
        name="Operation",
        description="Choose an operation",
        items=[
            ('CURVE_TO_MESH', 'Curve to Mesh', 'Convert curve to mesh'),
            ('NOIZE_TRANSFORM', 'Noize Transform', 'Apply noize transform'),
        ]
        )
    def execute(self, context):
        p_file = pathlib.Path(__file__)
        filepath=  str(p_file.parents[1].joinpath("asset", 'ksyn_nodes.blend'))
        if self.operation =="CURVE_TO_MESH":
            node_name = "curve_to_mesh"
        elif self.operation =="NOIZE_TRANSFORM":
            node_name = "Noize Transform"
        
        # Open the file
        with bpy.data.libraries.load(filepath) as (data_from, data_to):
            print(data_from.node_groups)
            # Import node groups
            data_to.node_groups = [m for m in data_from.node_groups if m == node_name]
        
        # Get the imported node group
        node_group = data_to.node_groups[0] if data_to.node_groups else None
        
        # Apply the geometry node to the object
        obj = bpy.context.object
        modifier = obj.modifiers.new(name=f"KSYN {node_name} Node", type="NODES")
        modifier.node_group = node_group
        
        return {'FINISHED'}


class ReName(Operator):
    bl_idname = "ksyn.renameop"
    bl_label = "Rename Object"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    name : bpy.props.StringProperty(name="Name",default="Object")
        # モードの選択肢
    mode_items = [
        ("ACTIVE_OBJECT", "アクティブなオブジェクト", "アクティブなオブジェクトをベースにする"),
        ("COLLECTION_NAME", "コレクションの名前", "コレクションの名前を使用する"),
    ]
    
    use_Custom : bpy.props.BoolProperty(name="Use Custom Name")
    
    # モードのプロパティ
    mode: bpy.props.EnumProperty(
        items=mode_items,
        name="モード",
        description="オブジェクトのベースとなる要素を選択します",
        default="ACTIVE_OBJECT"
    )

    
    def Based_on_the_name_of_the_active_object(self,active_object,seleobj):
        for obj in seleobj:
                            
            # 名前を基準
            if self.mode == "ACTIVE_OBJECT":
                base_name = active_object.name
            else:
                base_name = obj.users_collection[0].name

            # アクティブなオブジェクトはリネーム対象から外す
            if self.mode == "COLLECTION_NAME":
                pass
            else:
                if obj == bpy.context.active_object:
                    continue  

            # オブジェクトの名前に_をつけて数字のカウントをする
            count = 1
            new_name = base_name + "_" + str(count)
            while bpy.data.objects.get(new_name) is not None:
                count += 1
                new_name = base_name + "_" + str(count)

            # オブジェクトの名前を変更する
            obj.name = new_name

    def execute(self, context):
        seleobj = bpy.context.selected_objects
        if self.use_Custom:
            self.Based_on_the_name_of_the_active_object(bpy.context.object, seleobj)
        else:
            count = 1

            for obj in bpy.context.selected_objects:

                    obj.name = "{}_{:03d}".format(self.name, count)
                    count += 1

        return {'FINISHED'}


class AutoSommth(Operator):
    bl_idname = "object.pie10_operator"
    bl_label = "スムーズ"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    sommth : bpy.props.BoolProperty(name=get_translang('Sommth','スムース'),default=True)
    auto_sommth_bool : bpy.props.BoolProperty(name=get_translang('Auto Smooth','Auto Smooth'),default=True)
    auto_smooth_angle : bpy.props.FloatProperty(name=get_translang('Angle','Angle'),
                                                subtype='ANGLE',
                                                default=0.523599)

    def execute(self, context):
        if self.sommth ==True:
            bpy.ops.object.shade_smooth()
        else:
            bpy.ops.object.shade_flat()

        for obj in bpy.context.selected_objects:
            if obj.type =="MESH":
                if self.auto_sommth_bool ==True:
                    obj.data.use_auto_smooth = True
                else:
                    obj.data.use_auto_smooth = False
                obj.data.auto_smooth_angle = self.auto_smooth_angle
     

        return {'FINISHED'}

class Setting(Operator):
    bl_idname = "ksyn_ops.setting_operator"
    bl_label = get_translang("Setting","設定")
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):


        addon_name = "ksyn_ops"
        preferences = bpy.context.preferences
        addon_prefs = preferences.addons[addon_name].preferences

        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        addon_prefs.active_section = 'ADDONS'
        bpy.ops.preferences.addon_expand(module = addon_name)
        bpy.ops.preferences.addon_show(module = addon_name)

        return {'FINISHED'}

class mesh_hide(Operator):
    bl_idname = "object.pie4_operator"
    bl_label = "選択面以外非表示"
    bl_description = description(bl_idname)

    def execute(self, context):
        bpy.ops.mesh.hide(unselected=True)
        return {'FINISHED'}

class toggle_mode(Operator):
    bl_idname = "object.toggle_mode"
    bl_label = "Toggle Mode"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    
    mode_options = [
        ("OBJECT", "Object", "Object Mode"),
        ("EDIT", "Edit", "Edit Mode"),
        ("SCULPT", "Sculpt", "Sculpt Mode")
    ]
    
    mode: bpy.props.EnumProperty(
        items=mode_options,
        name="Mode",
        description="Select the mode to toggle"
    )
    
    def execute(self, context):
        if self.mode == "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")
        elif self.mode == "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
        elif self.mode == "SCULPT":
            bpy.ops.object.mode_set(mode="SCULPT")
        
        return {'FINISHED'}


class rotationx(Operator):
    bl_idname = "object.pie8_operator"
    bl_label = "X軸90回転"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        obj = bpy.context.active_object
        obj.matrix_world @= Matrix.Rotation(radians(90), 4, 'X')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

class rotationy(Operator):
    bl_idname = "object.pie9_operator"
    bl_label = "Y軸90回転"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        obj = bpy.context.active_object
        obj.matrix_world @= Matrix.Rotation(radians(90), 4, 'Y')
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

class flatselect(Operator):
    bl_idname = "object.pie18_operator"
    bl_label = "フラット面を選択"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        bpy.ops.mesh.faces_select_linked_flat()
        return {'FINISHED'}

class seamclear(Operator):
    bl_idname = "object.pie19_operator"
    bl_label = "シームをクリア"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=True)
        return {'FINISHED'}

class seamadd(Operator):
    bl_idname = "object.pie20_operator"
    bl_label = "シームをつける"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "


    def execute(self, context):
        bpy.ops.mesh.mark_seam(clear=False)
        return {'FINISHED'}

class ColorPickupObject(Operator):
    """Tooltip"""
    bl_idname = "object.colorpickup_object"
    bl_label = "ColorPickupObject"

  
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj_color = context.scene.myedit_property_group.color_pic
            obj.color = obj_color

            
        return {'FINISHED'}

class SubdivisionShow(Operator):
    """Tooltip"""
    bl_idname = "object.subdivision_show"
    bl_label = "subdivision_show"

    @classmethod
    def poll(cls, context):
        sub_mod = False
        try:
            if bpy.context.object.type == 'MESH':
                for mod in bpy.context.object.modifiers:
                    if mod.name == "Subdivision":
                        sub_mod = True
                        return sub_mod

                    else:
                        pass
        except AttributeError:
            pass
    
    def execute(self, context):
        if context.object.modifiers["Subdivision"].show_on_cage == False:
            context.object.modifiers["Subdivision"].show_on_cage = True
        
        elif context.object.modifiers["Subdivision"].show_on_cage == True:
            context.object.modifiers["Subdivision"].show_on_cage = False
            
        return {'FINISHED'}

class AmatureRestBool(Operator):
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
class PLockTransforms(Operator):
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

class wiredisplay(Operator):
    bl_idname = "object.wiredisplay_operator"
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
