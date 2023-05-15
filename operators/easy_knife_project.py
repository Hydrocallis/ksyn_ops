import bpy, sys,bmesh


def get_select_verts():

    context = bpy.context
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.select_mode |= {'EDGE'}
    select_verts=[]
    for e in bm.edges:

        # print(e.index,e.select)
        select_verts.append((e.index, e.select))
                        
    bm.select_flush_mode()   
    me.update()
    
    return select_verts


def set_select_verts(select_verts):

    context = bpy.context
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bm.select_mode |= {'EDGE'}
    for (e,s)  in zip(bm.edges,select_verts):

        if s[1] == 1:
            e.select = True
                
    bm.select_flush_mode()   
    me.update()

# point リストはオブジェクトの名前順で並ぶ
def separate_obje():

    # フェイスは除外して線だけ選択してやる。
    select_verts = get_select_verts()

    bpy.ops.mesh.delete(type='ONLY_FACE')

    set_select_verts(select_verts)
    try:
    # 線のみのコピー
        bpy.ops.mesh.separate(type='SELECTED')
        # 選択したオブジェクトの中にメッシュ以外が混ざっていた場合の想定
    except RuntimeError:
        print('###',"mesh dont select plese selsect mesh or select object and mesh same")


    # セパレータ後のオブジェクトたち
    # オブジェクトモードに変更した際に再選択用のオブジェクトを習得しておく
    sele_objs= bpy.context.selected_objects
    #　カットされるオブジェクト
    cuted_obj = sele_objs[0].name
    #　カットするオブジェクト
    sele_objs[-1].name = "separate_object_012345"
    cut_obj = sele_objs[-1].name
    sele_obj_name_list = [i.name for i in sele_objs]
    
    return sele_obj_name_list,cuted_obj, cut_obj


def obj_scalechange(

    cut_obj,
    objectlocation,
    objectscale,
    ):

    # モディファアをクリアしておく。
    bpy.data.objects[cut_obj].modifiers.clear()
             
    #location setting
    loc_combined = [x + y for (x, y) in zip(
        bpy.data.objects[cut_obj].location, 
        objectlocation
        )]
    # 重要　セパレーターされたオブジェクトは最後に配列されたオブジェクトになる
    bpy.data.objects[cut_obj].location = loc_combined


    ### size setting

    bpy.ops.object.mode_set(mode='OBJECT')
    # カットオブジェクトのみを選択したいので一度全選択解除する
    bpy.ops.object.select_all(action='DESELECT')
    #　カット用のオブジェクトをエディットモードでリサイズする必要があるので、一度アクティブにする。
    bpy.context.view_layer.objects.active = bpy.data.objects[cut_obj]
    # クラッシュ防止のためセレクテッドオブジェクトの変数は使わない
    bpy.data.objects[cut_obj].select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.resize(
    value=objectscale, 
    )


def cut_obj_set(
    cut_obj,
    cuted_obj, 
    ):
    bpy.ops.object.mode_set(mode='OBJECT')
    # ここで一度オブジェクトを全選択解除しておかないとカットした際に選択が損なわれる
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = bpy.data.objects[cuted_obj]
    
    #　複雑怪奇だが、一度カット用のオブジェクトを非選択にする必要がある
    # カット用オブジェクトはオブジェクトモード状態でないとだめなのだ
    bpy.data.objects[cuted_obj].select_set(True)
    # 細かいことだが、先にセパレートオブジェクトを優先しないと
    # キャッシュで残っていた際に前のカットオブジェクトが優先される
    try:
        bpy.data.objects["separate_object_012345"].select_set(False)
    except KeyError:
        bpy.data.objects["cut_mesh"].select_set(False)

    bpy.ops.object.mode_set(mode='EDIT')

    # エディットモードになってから再選択する
    # 細かいことだが、先にセパレートオブジェクトを優先しない
    # とキャッシュで残っていた際に前のカットオブジェクトが優先される
    try:
        bpy.data.objects["separate_object_012345"].select_set(True)
    except KeyError:
        bpy.data.objects["cut_mesh"].select_set(True)


# これは純粋にカットするための関数あとは結果を返すのみ
def knife_cut_set(
    cut_through_bool,
    delete_objbool,
    sele_obj_name_list,
        ):

    bpy.ops.mesh.knife_project(
        cut_through=cut_through_bool
        )
          
    # sepalate object proces
    # to leave object
    if delete_objbool == True:
        try:
            bpy.data.objects[sele_obj_name_list[-1]].hide_render = True
            bpy.data.objects[sele_obj_name_list[-1]].display_type = 'WIRE'
            bpy.data.objects[sele_obj_name_list[-1]].name = "cut_mesh"
        except:
            bpy.data.objects["cut_mesh"].hide_render = True
            bpy.data.objects["cut_mesh"].display_type = 'WIRE'
            bpy.data.objects["cut_mesh"].name = "cut_mesh"

        return (True,"finished",sele_obj_name_list)

    
    # delete object
    else:
        # bpy.data.objects.remove(bpy.data.objects[sele_obj_name_list[-1]], do_unlink=True)

        return (True,"finished",sele_obj_name_list)


def knife_cut(
    sele_obj_name_list,
    cut_through_bool,
    delete_objbool,
    ):
    # クラッシュ防止のため再選択
    # sele_objs= bpy.context.selected_objects
    cut_obj = sele_obj_name_list[-1]
    cutedlist=sele_obj_name_list[0:-1]
    # print('###',cutedlist)
    
    # 選択したオブジェクトが二個以上の場合は実行しない（最初に一個選択の縛りを入れたいから）
     # kife_project
     # アクティブオブジェクトがカットの対象となるのでそれぞれにフォアを回し絵アクティブにしてやる
    for i in cutedlist:
        # 連続でカットした時にカットメッシュが入っていたら次のカットでバグるので、削除
        if "cut_mesh" in cutedlist:
            cutedlist.remove("cut_mesh")

        cut_obj_set(
            cut_obj,
            i, 
            )

        bool = knife_cut_set(
        cut_through_bool,
        delete_objbool,
        sele_obj_name_list,
            )

        # print('###',i)

    # 最後にワイヤーオフの際はカットメッシュを削除　残す場合は選択を解除
    if delete_objbool == False:

        bpy.data.objects.remove(bpy.data.objects[sele_obj_name_list[-1]], do_unlink=True)
    else:
        bpy.data.objects["cut_mesh"].select_set(False)

    # 最後結果を確かめるために全選択してからエディットモードに戻る
    bpy.ops.object.mode_set(mode='OBJECT')
    for i in cutedlist:
         bpy.data.objects[i].select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    
             
    return bool


class easy_knife_project(bpy.types.Operator):
    bl_idname = 'object.easy_knife_project'
    bl_label = 'EasyKnifeProject'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
    bl_options = {'REGISTER', 'UNDO','PRESET'}
    
    # testプロパティ

    objectlocation:bpy.props.FloatVectorProperty(
        name='move', 
        description='', 
        default=(0.0, 0.0, 0.0),
        subtype="XYZ_LENGTH"
        )
    objectscale:bpy.props.FloatVectorProperty(
        name='resize', 
        description='', 
        default=(1.0, 1.0, 1.0),
        subtype="XYZ"
        )        

        
    delete_objbool : bpy.props.BoolProperty(
        name= "wire on",
        default=0
        )

    cut_through_bool : bpy.props.BoolProperty(
        name= "cut through",
        default=0
        )

    @classmethod
    
    def poll(self, context):
        try:
            if bpy.context.object.type == "MESH":
                return True
        except AttributeError:
            pass

    def execute(self, context):
        # cut_objの関数でフォアを回せば複数オブジェクトをカットできるはず・・・・

        sele_obj_name_list, cuted_obj, cut_obj, = separate_obje()

        obj_scalechange(
            cut_obj,
            self.objectlocation,
            self.objectscale,
            )


        bool,messeage,sele_obj_name_list =knife_cut(
            sele_obj_name_list,
            self.cut_through_bool,
            self.delete_objbool,
            )

        result = "INFO" if bool ==True else 'WARNING'
        self.report( {result, },messeage)

        return {'FINISHED'}


            