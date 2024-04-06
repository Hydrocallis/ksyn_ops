import bpy,sys,inspect

from bpy.types import (
        Operator,
        )
# これはVSCODE上ではアドオン単体で開いているので通るが、ブレンダー上だと通らない。
# つまり、VSCODD上でリンクするためのダミー
try:
    from utils.operators_utils import description 
    from utils.operators_utils import description 
    from utils.get_translang import get_translang 

# ブレンダー上ではaddonフォルダがSYSにアペンドされてるため、
# 上位に潜る際はこのパス（ADDONが基準でその配下のフォルダは認識される）が通る
    
except ImportError:
    from ksyn_ops.utils.get_translang import get_translang # type: ignore
    from ksyn_ops.utils.operators_utils import description # type: ignore
    from ksyn_ops.utils.get_translang import get_translang # type: ignore


from mathutils import Matrix
from math import radians
import pathlib
from bpy.props import FloatProperty

import bpy
try:
    import win32clipboard
except ModuleNotFoundError:
    pass
    # print('### please install python module win32')
import os




class ImportFBXFromClipboardOperator(bpy.types.Operator):
    bl_idname = "wm.import_3dfile_from_clipboard"
    bl_label = get_translang("Import FBX GLB from Clipboard","クリップボードからFBX GLBインポート")
    
    def execute(self, context):
        # # クリップボードを開く
        # win32clipboard.OpenClipboard()

        # # FileName形式のクリップボードデータを取得
        # filename_format = win32clipboard.RegisterClipboardFormat('FileNameW')
        # if win32clipboard.IsClipboardFormatAvailable(filename_format):
        #     input_filenames = win32clipboard.GetClipboardData(filename_format)
        #     print("###input_filenames",input_filenames)

        #     # バイト列をUTF-16でデコード
        #     input_filenames = input_filenames.decode('utf-16', errors='ignore')

        #     # ファイル名はNULL文字で区切られているので、それを基に分割
        #     filenames = input_filenames.split('\x00')

        #     for filename in filenames:
        #         if filename:  # ファイル名が空でない場合のみ処理
        #             # ファイル拡張子を正しく表示
        #             # ファイル名から拡張子を取得
        #             base_filename, file_extension = os.path.splitext(filename)

        #             # FBXファイルをインポート
        #             if file_extension.lower() == '.fbx':
        #                 bpy.ops.import_scene.fbx(filepath=filename)

        #             # GLBファイルをインポート
        #             elif file_extension.lower() == '.glb':
        #                 bpy.ops.import_scene.gltf(filepath=filename)

        # # クリップボードを閉じる
        # win32clipboard.CloseClipboard()
        
        import ctypes
        import struct

        from io import BytesIO

        from ctypes.wintypes import BOOL, HWND, HANDLE, HGLOBAL, UINT, LPVOID
        from ctypes import c_size_t as SIZE_T

        OpenClipboard = ctypes.windll.user32.OpenClipboard
        OpenClipboard.argtypes = HWND,
        OpenClipboard.restype = BOOL
        EmptyClipboard = ctypes.windll.user32.EmptyClipboard
        EmptyClipboard.restype = BOOL
        GetClipboardData = ctypes.windll.user32.GetClipboardData
        GetClipboardData.argtypes = UINT,
        GetClipboardData.restype = HANDLE
        SetClipboardData = ctypes.windll.user32.SetClipboardData
        SetClipboardData.argtypes = UINT, HANDLE
        SetClipboardData.restype = HANDLE
        CloseClipboard = ctypes.windll.user32.CloseClipboard
        CloseClipboard.restype = BOOL
        IsClipboardFormatAvailable = ctypes.windll.user32.IsClipboardFormatAvailable
        IsClipboardFormatAvailable.argtypes = UINT,
        IsClipboardFormatAvailable.restype = BOOL
        CF_UNICODETEXT = 13
        CF_DIB = 8
        CF_HDROP = 15

        GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
        GlobalAlloc.argtypes = UINT, SIZE_T
        GlobalAlloc.restype = HGLOBAL
        GlobalLock = ctypes.windll.kernel32.GlobalLock
        GlobalLock.argtypes = HGLOBAL,
        GlobalLock.restype = LPVOID
        GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
        GlobalUnlock.argtypes = HGLOBAL,
        GlobalSize = ctypes.windll.kernel32.GlobalSize
        GlobalSize.argtypes = HGLOBAL,
        GlobalSize.restype = SIZE_T
        GMEM_MOVEABLE = 0x0002
        GMEM_ZEROINIT = 0x0040
        GMEM_SHARE    = 0x2000
        GHND = GMEM_MOVEABLE | GMEM_ZEROINIT

        unicode_type = type(u'')

        def read_raw(fmt):
            handle = GetClipboardData(fmt)
            pcontents = GlobalLock(handle)
            size = GlobalSize(handle)
            raw_string = None
            if pcontents and size:
                raw_data = ctypes.create_string_buffer(size)
                ctypes.memmove(raw_data, pcontents, size)
                raw_string = raw_data.raw
            GlobalUnlock(handle)
            return raw_string
            
        def get():
            text = None
            OpenClipboard(None)
            if IsClipboardFormatAvailable(CF_DIB):
                CloseClipboard()
                # from http://stackoverflow.com/a/7045677
                from PIL import ImageGrab
                return ImageGrab.grabclipboard()
            if IsClipboardFormatAvailable(CF_HDROP):
                raw_string = read_raw(CF_HDROP)
                CloseClipboard()
                pFiles, pt_x, pt_y, fNC, fWide = struct.unpack('IIIII', raw_string[:20])
                cooked = raw_string[pFiles:].decode('utf-16' if fWide else 'mbcs')
                return [name for name in cooked.split(u'\0') if name]
            handle = GetClipboardData(CF_UNICODETEXT)
            pcontents = GlobalLock(handle)
            size = GlobalSize(handle)
            if pcontents and size:
                raw_data = ctypes.create_string_buffer(size)
                ctypes.memmove(raw_data, pcontents, size)
                text = raw_data.raw.decode('utf-16le').rstrip(u'\0')
            GlobalUnlock(handle)
            CloseClipboard()
            return text


        def create_collection(collection_name):
            # ルートコレクションを取得
            root_collection = bpy.context.scene.collection

            # すでに同じ名前のコレクションが存在する場合は作成しない
            # if collection_name in bpy.data.collections:
            #     print(f"コレクション '{collection_name}' はすでに存在します。")
            #     return

            # 新しいコレクションを作成
            new_collection = bpy.data.collections.new(collection_name)

            # ルートコレクションに追加
            root_collection.children.link(new_collection)
            

            print(f"コレクション '{new_collection.name}' を作成しました。")
            return new_collection.name


        def move_obj(collection_name,objs):
            target_col = bpy.data.collections[collection_name]
            for obj in objs:
                for col in obj.users_collection:
                    # print(col)
                    # Unlink the object
                    col.objects.unlink(obj)

                target_col.objects.link(obj)

 

        file_paths = get()
        # if file_paths:
        #     print("Copied file paths:")
        #     for path in file_paths:
        #         print(path)
        # else:
        #     print("No file paths found on the clipboard.")

        for filename in file_paths:
            if filename:  # ファイル名が空でない場合のみ処理
                # ファイル拡張子を正しく表示
                # ファイル名から拡張子を取得

                base_filename, file_extension = os.path.splitext(filename)
                filename_bace = os.path.basename(filename)
                name_without_extension = os.path.splitext(filename_bace)[0]

                # FBXファイルをインポート
                if file_extension.lower() == '.fbx':
                    # コレクションを作成

                    bpy.ops.import_scene.fbx(filepath=filename)
                    collection_name=create_collection(name_without_extension)
                    move_obj(collection_name,bpy.context.selected_objects)
                    

                # GLBファイルをインポート
                elif file_extension.lower() == '.glb':
                    collection_name=create_collection(name_without_extension)
                    bpy.ops.import_scene.gltf(filepath=filename)
                    move_obj(collection_name,bpy.context.selected_objects)

                # OBJファイルをインポート
                elif file_extension.lower() == '.obj':
                    collection_name=create_collection(name_without_extension)
                    bpy.ops.import_scene.obj(filepath=filename)
                    move_obj(collection_name,bpy.context.selected_objects)


        return {'FINISHED'}



class GetFacebySide(bpy.types.Operator):
    bl_idname = "ksyn.get_face_by_side"
    bl_label = "Get Face By_side"
    bl_options = {'REGISTER', 'UNDO'}
    
    # name: bpy.props.StringProperty(name="New Name") # type: ignore
    # label: bpy.props.StringProperty(name="New Label") # type: ignore # type: ignore
    # same_name_label: bpy.props.BoolProperty(name="Same as Name", default=True) # type: ignore
    number :bpy.props.IntProperty(name="Face Number", default=3) # type: ignore
    # def invoke(self, context, event):
    #     return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        bpy.ops.mesh.select_face_by_sides(number=self.number)
    
        return {'FINISHED'}
    
class RenameActiveNodeOperator(bpy.types.Operator):
    bl_idname = "object.rename_active_node"
    bl_label = "Rename Active Node"
    bl_options = {'REGISTER', 'UNDO'}
    
    name: bpy.props.StringProperty(name="New Name") # type: ignore
    label: bpy.props.StringProperty(name="New Label") # type: ignore # type: ignore
    same_name_label: bpy.props.BoolProperty(name="Same as Name", default=True) # type: ignore
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'NODE_EDITOR':
                node_area = area
        
        active_node = node_area.spaces.active.node_tree.nodes.active
        
        active_node.name = self.name
        if self.same_name_label:
            active_node.label = self.name
        else:
            active_node.label = self.label
        
        return {'FINISHED'}
    
    def draw(self,context):
        self.layout.prop(self,"name")
        self.layout.prop(self,"same_name_label")
    
        if not self.same_name_label:
            self.layout.prop(self,"label")

class BevelExtrudeOperator(bpy.types.Operator):
    bl_idname = "mesh.bevel_extrude"
    bl_label = "Bevel and Extrude"
    bl_options = {'REGISTER', 'UNDO'}
    
    bevel_amount: FloatProperty(
        name="Bevel Amount",
        default=0.005,
        min=0.0,
        description="Amount of bevel offset"
    ) # type: ignore
    
    extrude_amount: FloatProperty(
        name="Extrude Amount",
        default=-0.00475417,
        description="Amount of extrude offset"
    ) # type: ignore
    
    def execute(self, context):
        bpy.ops.mesh.bevel(offset=self.bevel_amount, offset_pct=0, affect='EDGES')
        
        bpy.ops.mesh.extrude_region_shrink_fatten(
            MESH_OT_extrude_region={
                "use_normal_flip": False,
                "use_dissolve_ortho_edges": False,
                "mirror": False
            },
            TRANSFORM_OT_shrink_fatten={
                "value": self.extrude_amount,
                "use_even_offset": False,
                "mirror": False,
                "use_proportional_edit": False,
                "proportional_edit_falloff": 'SMOOTH',
                "proportional_size": 2.743,
                "use_proportional_connected": False,
                "use_proportional_projected": False,
                "snap": False,
                "release_confirm": False,
                "use_accurate": False
            }
        )
        
        return {'FINISHED'}


class ChangeLightEnergyOperator(bpy.types.Operator):
    bl_idname = "object.change_light_energy"
    bl_label = "Change Light Energy"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}
    
    
    energy : FloatProperty(name="Energy", default=1.0, min=0.0) # type: ignore
    

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        
        for obj in selected_objects:
            if obj.type == 'LIGHT':
                obj.data.energy = self.energy
        
        return {'FINISHED'}


class MakeRealAndParentOperator(bpy.types.Operator):
    bl_idname = "object.make_real_and_parent"
    bl_label = "Make Real and Parent"
    bl_description = "Make selected objects real and parent them to an empty"
    bl_options = {'REGISTER', 'UNDO'}
    
    create_empty: bpy.props.BoolProperty(
        name="Create Empty",
        default=True,
        description="Create an empty object to parent the selected objects"
    ) # type: ignore
    select_empty: bpy.props.BoolProperty(
        name="Select Empty",
        default=True,
        description="Create an empty object Select"
    ) # type: ignore
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects
    
    def execute(self, context):
        # インスタンスからリアライズ
        bpy.ops.object.duplicates_make_real()
        
        # 選択したオブジェクトを取得
        selected_objects = context.selected_objects
        
        # 各オブジェクトのモディファイアをチェックして削除
        for obj in selected_objects:
            modifiers = obj.modifiers
            for modifier in modifiers:
                if modifier.type == 'NODES':
                    modifiers.remove(modifier)
        
        active_object = context.active_object
        
        if self.create_empty:
            # エンプティを作成
            empty = bpy.data.objects.new("Empty", None)
            context.collection.objects.link(empty)
            
            # エンプティの位置をアクティブなオブジェクトの位置に設定
            empty.name = active_object.name + "_empty"
            
            # 選択したオブジェクトをエンプティの子に設定
            for obj in selected_objects:
                obj.parent = empty
            if self.select_empty:
                empty.select_set(True)
                bpy.context.view_layer.objects.active = empty

            
        
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
            ('NOIZE_TRANSFORM', 'Noize Transform', 'Apply noize transform'),
            ('Rotation_Array', 'Rotation Array', 'Rotation Array '),
        ]
        ) # type: ignore

    
    def execute(self, context):
        p_file = pathlib.Path(__file__)
        filepath=  str(p_file.parents[1].joinpath("asset", 'ksyn_nodes.blend'))
        if self.operation =="CURVE_TO_MESH":
            node_name = "curve_to_mesh"
        elif self.operation =="NOIZE_TRANSFORM":
            node_name = "Noize Transform"
        
        elif self.operation =="Rotation_Array":
            node_name = "Rotation Array"
        
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

    name : bpy.props.StringProperty(name="Name",default="Object") # type: ignore
        # モードの選択肢
    mode_items = [
        ("ACTIVE_OBJECT", "アクティブなオブジェクト", "アクティブなオブジェクトをベースにする"),
        ("COLLECTION_NAME", "コレクションの名前", "コレクションの名前を使用する"),
    ]
    
    use_Custom : bpy.props.BoolProperty(name="Use Custom Name") # type: ignore
    
    # モードのプロパティ
    mode: bpy.props.EnumProperty(
        items=mode_items,
        name="モード",
        description="オブジェクトのベースとなる要素を選択します",
        default="ACTIVE_OBJECT"
    ) # type: ignore

    
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

    sommth : bpy.props.BoolProperty(name=get_translang('Sommth','スムース'),default=True) # type: ignore
    auto_sommth_bool : bpy.props.BoolProperty(name=get_translang('Auto Smooth','Auto Smooth'),default=True) # type: ignore
    auto_smooth_angle : bpy.props.FloatProperty(name=get_translang('Angle','Angle'),
                                                subtype='ANGLE',
                                                default=0.523599) # type: ignore

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
    ) # type: ignore
    
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
