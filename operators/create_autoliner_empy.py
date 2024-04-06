import bpy,sys,os
import mathutils
from bpy.types import Operator

import subprocess
 
try:
    from ksyn_ops.utils.get_translang import get_translang   # type: ignore
except ImportError:
    from ..utils.get_translang import get_translang 



# エンプティを設置
def move_object_to_collection(obj, target_collection):
    for col in obj.users_collection:
        col.objects.unlink(obj)
    target_collection.objects.link(obj)


class CreateEmptyOperator(bpy.types.Operator):
    bl_idname = "object.create_empty"
    bl_label = "Create Empty(CURSOR)"


    @classmethod
    def poll(cls, context):

        if bpy.context.object != None:
            return True
        else:
            return False


    def execute(self, context):
        # アクティブなオブジェクトを取得
        active_object = bpy.context.object


        # エンプティを作成
        bpy.ops.object.empty_add()

        # 作成したエンプティをアクティブにする
        empty_object = bpy.context.object

        # エンプティの位置を移動する

        empty_object.location = bpy.context.scene.cursor.location

        collection = active_object.users_collection[0]

        move_object_to_collection(empty_object, active_object.users_collection[0])

        # エンプティの名前をコレクションの名前に設定
        empty_object.name = collection.name

        return {'FINISHED'}

class activeCreateEmptyOperator(bpy.types.Operator):
    bl_idname = "object.active_create_empty"
    bl_label = "Create Empty Active Object"

    def execute(self, context):
        # アクティブなオブジェクトを取得
        active_object = bpy.context.object


        # エンプティを作成
        bpy.ops.object.empty_add()

        # 作成したエンプティをアクティブにする
        empty_object = bpy.context.object

        # エンプティの位置を移動する

        empty_object.location = active_object.location

        # アクティブなオブジェクトのあるコレクションを取得
        collection = active_object.users_collection[0]

        move_object_to_collection(empty_object, collection)

        # エンプティの名前をコレクションの名前に設定
        empty_object.name = collection.name

        return {'FINISHED'}


class PlaceEmptyOperator(Operator):
    bl_idname = "object.place_empty"
    bl_label = "Place Empty"
    bl_description = "Place an empty at the average location of selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_object = bpy.context.object

        # 選択したオブジェクトの原点位置の平均値を計算
        selected_objects = bpy.context.selected_objects
        origin_sum = mathutils.Vector((0, 0, 0))
        for obj in selected_objects:
            origin_sum += obj.location
        origin_avg = origin_sum / len(selected_objects)

        # エンプティを作成
        bpy.ops.object.empty_add()

        # 作成したエンプティをアクティブにする
        empty_object = bpy.context.object

        # エンプティの位置を移動する
        empty_object.location = origin_avg

        # アクティブなオブジェクトのあるコレクションを取得
        collection = active_object.users_collection[0]
        move_object_to_collection(empty_object, collection)

        # エンプティの名前をコレクションの名前に設定
        empty_object.name = collection.name

        return {'FINISHED'}




# リネーム
class RenameSelectedObjects_collection_Operator(bpy.types.Operator):
    bl_description2= """
                        There is an object with the same name to be renamed 
                        based on the active object(Collection). 
                        Rename it to avoid it if it is an.
                        
                        アクティブなオブジェクト(コレクション)を基準にリネームする同じ名前の
                        オブジェクトが存在する場合はそれを避けてリネームする"""
    
    bl_idname = "object.rename_selected_objects_collection"
    bl_label = "Rename Selected Objects Collection Name"
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n \n{bl_description2}'

    bl_options = {'REGISTER', 'UNDO'}

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore


    def execute(self, context):


        # アクティブなオブジェクトを取得
        active_object = bpy.context.object
        collection = active_object.users_collection[0]
        # 選択したオブジェクトの名前を変更する
            # アクティブなオブジェクトの名前を基準にする
        if self.cmd == "COLLECTION":
            base_name = collection.name

        elif self.cmd == "SELECT":
            base_name = active_object.name
        else:
            base_name = collection.name

        for index, obj in enumerate(bpy.context.selected_objects,start=1):


            # アクティブなオブジェクトはリネーム対象から外す
            if self.cmd == "SELECT":
                if obj == bpy.context.active_object:
                    continue
            # オブジェクトの名前に_をつけて数字のカウントをする
            count = 1
            new_name = base_name + "_" + str(count).zfill(3)
            while bpy.data.objects.get(new_name) is not None:
                new_name = base_name + "_" +  str(count).zfill(3)
                count += 1


            # オブジェクトの名前を変更する
            obj.name = new_name

        return {'FINISHED'}

# class RenameSelectedObjectsOperator(bpy.types.Operator):
#     bl_idname = "object.rename_selected_objects"
#     bl_label = "Rename Selected Objects"
#     bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
#     bl_options = {'REGISTER', 'UNDO'}



    
#     def select_all_children_of_selected_objects(self):
#         # 選択したオブジェクトを取得
#         selected_objects = bpy.context.selected_objects

#         # 選択したオブジェクトの子オブジェクトを選択
#         for obj in selected_objects:
#             for child in obj.children:
#                 child.select_set(True)
                

#     def execute(self, context):
#         # アクティブなオブジェクトを取得
#         active_object = bpy.context.active_object

#         self.select_all_children_of_selected_objects()

#         # 選択したオブジェクトの名前を変更する
#         for obj in bpy.context.selected_objects:
#             # アクティブなオブジェクトの名前を基準にする
#             base_name = active_object.name

#             # アクティブなオブジェクトはリネーム対象から外す
#             if obj == bpy.context.active_object:
#                 continue

#             # オブジェクトの名前に_をつけて数字のカウントをする
#             count = 1
#             new_name = base_name + "_" + str(count)
#             while bpy.data.objects.get(new_name) is not None:
#                 count += 1
#                 new_name = base_name + "_" + str(count)

#             # オブジェクトの名前を変更する
#             obj.name = new_name

#         return {'FINISHED'}

# その他

class OBJECT_OT_ParentActiveObject(bpy.types.Operator):
    bl_idname = "object.parent_active_object"
    bl_label = "Parent Active Object"

    def parent_active_object(self, context):
        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.active_object

        if active_object is None:
            self.report({'ERROR'}, "No active object found.")
            return

        for obj in selected_objects:
            if obj != active_object:
                obj.parent = active_object
                obj.matrix_parent_inverse = active_object.matrix_world.inverted()

    def execute(self,context):
        self.parent_active_object(context)
        return {'FINISHED'}

class ExportSelectedObjectsToFbx(Operator):
    bl_idname = "object.export_selected_to_fbx"
    bl_label = "Export Selected Objects to FBX"
    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore

    
    def get_file_size(self,filepath):
        size = os.path.getsize(filepath)
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{size / 1024:.2f} KB"
        else:
            return f"{size / (1024 * 1024):.2f} MB"

    def show_file_size(self,filepath):
        message = [f"File Size: {self.get_file_size(filepath)}"]
        title = "File Size"
        icon = 'INFO'

        def draw(self, context):
            for mes in message:
                self.layout.label(text=mes)

        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
    


    def execute(self, context):
        print('###cmd',self.cmd)
        # 選択したオブジェクトの位置を保存
        selected_objects = bpy.context.selected_objects
        object_locations = [(obj, obj.location.copy()) for obj in selected_objects]

        if self.cmd != "not_move":
            # 選択したオブジェクトのxとyのロケーションを0に設定
            for obj in selected_objects:
                obj.location.x = 0
                obj.location.y = 0

        # ブレンダーファイルの場所を取得
        blend_file_path = bpy.data.filepath
        blend_file_directory = os.path.dirname(blend_file_path)

        # アクティブなコレクションの名前を取得
        active_collection_name = bpy.context.collection.name

        # FBX出力先のパスを設定
        output_path = os.path.join(blend_file_directory, f"{active_collection_name}.fbx")

        # FBX出力
        bpy.ops.export_scene.fbx(
            filepath=output_path,
            use_selection=True,
            path_mode='COPY',
            embed_textures=True
        )

        # 元の位置に戻す
        for obj, location in object_locations:
            obj.location = location


        self.show_file_size(output_path)

        # 出力先のフォルダをエクスプローラーで開く
        subprocess.Popen(f'explorer /select,"{output_path}"')
        subprocess.Popen(["start", "", output_path], shell=True)


        return {'FINISHED'}
    
def renameop(layout):
    layout.operator("object.rename_selected_objects_collection",text=get_translang("Changed according to base name (based on collection)","ベース名に準じて変更(コレクションをベースに)")).cmd ="COLLECTION"
    layout.operator("object.rename_selected_objects_collection",text=get_translang("Changed according to base name (based on object)","ベース名に準じて変更(オブジェクトをベースに)")).cmd ="SELECT"

class ksyn_outliner_AssistMenu(bpy.types.Menu):
    bl_idname = "OUTLINER_MT_assist_menu"
    bl_label = "Assist Menu"

    def draw(self, context):
        layout = self.layout

        # 補助機能に関連するメニュー項目を追加
        renameop(layout)
        layout.separator()


def register():
    bpy.utils.register_class(ExportSelectedObjectsToFbx)
    bpy.utils.register_class(ksyn_outliner_AssistMenu)

def unregister():
    bpy.utils.unregister_class(ExportSelectedObjectsToFbx)
    bpy.utils.unregister_class(ksyn_outliner_AssistMenu)

# メニュードロー
def draw_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.label(text="OUTLINER PARENT")
    layout.separator()
    layout.operator("object.parent_active_object")
    # layout.operator_enum("object.parent_set", "type")
    layout.operator_enum("object.parent_clear", "type")
    layout.separator()
    renameop(layout)
    layout.separator()
    layout.operator("object.join")
    layout.menu("VIEW3D_MT_object_apply")
    layout.menu("VIEW3D_MT_object_convert")
    layout.separator()
    layout.operator("object.active_create_empty")
    layout.operator("object.create_empty")
    layout.operator("object.place_empty")

 
def draw_col_menu(self, context):
    layout = self.layout
    layout.operator("object.create_empty")
    layout.operator("object.active_create_empty")
    layout.operator("object.place_empty")

# 登録
def draw_header_menu(self, context):
    self.layout.menu(ksyn_outliner_AssistMenu.bl_idname)



def OUTLINER_MT_objectregister():
    register()
    bpy.types.OUTLINER_MT_object.append(draw_menu)
    bpy.types.OUTLINER_MT_collection.append(draw_col_menu)
    bpy.types.OUTLINER_HT_header.append(draw_header_menu)

def OUTLINER_MT_objectunregister():
    unregister()
    bpy.types.OUTLINER_MT_object.remove(draw_menu)
    bpy.types.OUTLINER_MT_collection.remove(draw_col_menu)
    bpy.types.OUTLINER_HT_header.remove(draw_header_menu)
