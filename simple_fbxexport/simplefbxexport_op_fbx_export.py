import bpy, sys, os, subprocess

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )



# パネルの出力設定項目のチェック
def bool_check(context):
    props = context.scene.simplefbxecport_propertygroup
    blend_fbx_save_dir=props.workspace_path

    # ブレンダーファイルの拡張子なしの名前
    blender_fbxfilename = bpy.path.basename(bpy.context.blend_data.filepath).replace(".blend","")
 
    # アクティブ中のコレクションの名前
    get_collection_name=bpy.context.view_layer.active_layer_collection.name
    obj = bpy.context.object

    # チェック箇所によってのファイルネームの変更イフ文

    # オブジェクト選択系のいふ分
    if obj != None:
        obj_name = obj.name

    else:

        obj_name = "no_active_select_objct"

    if props.fbx_children_recursive == True:
        bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
        bpy.context.object.select_set(True)
    else:
        pass

    # ここからファイル名をデコレーションしていく

    # 選択したオブジェクトの名前と入力したファイル名を入れる
    if props.fbx_blenderfilename__bool == True:
        fbx_exportsavefile = blender_fbxfilename +"_" + props.fbx_filename
    elif props.fbx_blenderfilename__bool == False:
        fbx_exportsavefile = props.fbx_filename

    # 選択したオブジェクトの名前を仕様
    if props.fbx_selectfilename_bool == True:
        fbx_exportsavefile = fbx_exportsavefile + "_" + obj_name

    # コレクション名にチェックが入っていたら
    if props.fbx_get_col_name_bool == True:
        # print('###',get_collection_name)
        fbx_exportsavefile = fbx_exportsavefile + "_" + get_collection_name
    
    # デコレーションの終わり。下記に拡張子とディレクトリをジョインする
    fbx_exportsavefile = os.path.join(blend_fbx_save_dir,fbx_exportsavefile+".fbx")
 
    return fbx_exportsavefile
    

def make_filename(context,fbx_exportsavefile):
    props = context.scene.simplefbxecport_propertygroup
    
    # サブフォルダを追加する
    filepath = os.path.dirname(bpy.data.filepath)
    print(filepath)
    if props.workspace_fbxfolder_path_Collection != None:
    
        mkdirefilepath =  os.path.join(filepath, props.workspace_fbxfolder_path, props.workspace_fbxfolder_path_Collection.name)
    else:
        mkdirefilepath = os.path.join(filepath, props.workspace_fbxfolder_path, "")
        

    # コレクションを選択してない場合
    if not os.path.exists(mkdirefilepath):
        os.makedirs(mkdirefilepath)
        print("make dirfile")
    else:
        print("already file")

    # サブフォルダをファイルパスに組み込む
    direpath = os.path.dirname(fbx_exportsavefile)
    direfilename = os.path.basename(fbx_exportsavefile)


    # コレクションを選択してない場合
    if props.workspace_fbxfolder_path_Collection != None:
        finalfbx_exportsavefile = os.path.join(direpath,props.workspace_fbxfolder_path, props.workspace_fbxfolder_path_Collection.name, direfilename)
    else:
        finalfbx_exportsavefile = os.path.join(direpath,props.workspace_fbxfolder_path, "", direfilename)

    # fbxの名前が.fbxの場合は自動連番機能がバグるため、リネームする。
    if os.path.basename(fbx_exportsavefile) == ".fbx":
        fbx_exportsavefilename = "export_fbx.fbx"
        finalfbx_exportsavefile = os.path.join(mkdirefilepath, fbx_exportsavefilename)
    print('###final file name is ',finalfbx_exportsavefile)

    # 重複してるかどうかチェックする関数を実行
    if props.fbx_name_replace_bool == False:
        finalfbx_exportsavefile = filename_check(finalfbx_exportsavefile)

    return finalfbx_exportsavefile

# フォルダ名のリプレイス回避
def filename_check(fbx_exportsavefile):
    if os.path.exists(fbx_exportsavefile) == True:

        print('###found same file name. ',fbx_exportsavefile)

        (filepath, fileex) = os.path.splitext(fbx_exportsavefile) 
        # 該当なしないファイルネームが見つかるまでフォアを回す
        for i in range(100):
            newname = '{}_{}{}'.format(filepath, i, fileex)
            newpath = os.path.join(filepath, newname)
            if not os.path.exists(newpath):
                fbx_exportsavefile = newpath
                break  # 名前が空いている場合
    else:
        print('###not same file name',)
    return fbx_exportsavefile


# メインの出力関係
def fbx_export_oprator(
    fbx_exportsavefile, 
    fbx_selectbool, 
    fbx_act_collection_bool, 
    fbxexportpath
    ):
    props = bpy.context.scene.simplefbxecport_propertygroup
    blend_fbx_save_dir=props.workspace_path

    if blend_fbx_save_dir==".":
        return False

    else:
        bpy.ops.export_scene.fbx(
        # FBXの設定項目
        filepath=fbx_exportsavefile,
        #選択状態
        use_selection=fbx_selectbool,
        #アクティブなコレクション
        use_active_collection=fbx_act_collection_bool,
        #reference paths (enum in ['AUTO', 'ABSOLUTE', 'RELATIVE', 'MATCH', 'STRIP'(KANZENNI WAKARERU), 'COPY'], 
        path_mode='COPY',
        # テクスチャをFBXにはめ込むか
        embed_textures=True,
        )        
    
        subprocess.run('explorer /select,{}'.format(fbxexportpath))
        
        return fbxexportpath


class SIMPLEFBXECPORT_OT_FbxExort(Operator):
    bl_idname = 'object.fbxexortsupport'
    bl_label = 'fbxexortsupport'
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "

    # 実際の実行文
    def execute(self, context):
        props = context.scene.simplefbxecport_propertygroup

        # フォルダを参照して重複してるファイルネームをチェックする
        fbx_exportsavefile = bool_check(context)

        finalfbx_exportsavefile = make_filename(context,fbx_exportsavefile)
             
        fbxexportpath = fbx_export_oprator(
            finalfbx_exportsavefile, 
            props.fbx_selectbool,
            props.fbx_act_collection_bool,
            finalfbx_exportsavefile,
                        )

        if fbxexportpath == False:
            self.report({'INFO'}, 'ファイルを保存して下さい。')
        else:
            self.report({'INFO'}, str(fbxexportpath))
    
        return {'FINISHED'}