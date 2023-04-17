from this import d
import bpy, sys
import bpy,bmesh

def get_select_verts():

    context = bpy.context
    obj = context.edit_object
    try:
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

    # メッシュをオブジェクト編集状態で選択した時
    except AttributeError:
        return None
    


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


def main(
    depth,
    fill_caps_bool,
    bevel_resolution,
    duplicate_move_bool,
    offset,
    extrude,
    get_object_bool,
    ):
    props = bpy.context.scene.simple_object_propertygroup
    # カーブの場合はセパレートをパスする
    if bpy.context.object.type == "CURVE":
        pass
    # メッシュ場合はセパレートを実行する
    elif bpy.context.object.type =="MESH":

        try:
            if duplicate_move_bool== True:
                bpy.ops.mesh.duplicate_move()
             
            # フェイスは除外して線だけ選択してやる。
            select_verts = get_select_verts()

            bpy.ops.mesh.delete(type='ONLY_FACE')

            set_select_verts(select_verts)

            bpy.ops.mesh.separate(type='SELECTED')
        # 選択したオブジェクトの中にメッシュ以外が混ざっていた場合の想定
        except RuntimeError:
            pass


    # セパレータ後のオブジェクトたち
    sele_objs= bpy.context.selected_objects
   
    if len(sele_objs) <= 2:

        try:
            sele_objs[0].select_set(False)
        # カーブを編集状態で選択した時
        except IndexError:
            pass
        bpy.context.view_layer.objects.active = sele_objs[-1]
        bpy.ops.object.mode_set(mode='OBJECT')
        # カーブオンリーの場合はコンバートをパスする
        try:
            bpy.ops.object.convert(target='CURVE')
        except RuntimeError:
            pass
        #　メッシュがクローズしてる場合はコンバートが聞かないので、全てパスする。
        if sele_objs[-1].type =='CURVE':
            sele_objs= bpy.context.selected_objects
            try:
                sele_objs[-1].data.bevel_depth = depth
                sele_objs[-1].data.use_fill_caps = fill_caps_bool
                sele_objs[-1].data.bevel_resolution = bevel_resolution
                sele_objs[-1].data.offset = offset
                sele_objs[-1].data.extrude = extrude
                if get_object_bool == True and props.target_curve != None:
                    
                    if props.target_curve.data.bevel_depth != 0.00:
                        props.target_curve.data.bevel_depth = 0.00

                    sele_objs[-1].data.bevel_mode = 'OBJECT'
                    sele_objs[-1].data.bevel_object = props.target_curve
                else:
                    sele_objs[-1].data.bevel_mode = 'ROUND'


            # カーブオンリーの場合はここに取り付くはず
            except IndexError:
                bpy.context.object.data.bevel_depth = depth
                bpy.context.object.data.use_fill_caps = fill_caps_bool
                bpy.context.object.data.bevel_resolution = bevel_resolution
                bpy.context.object.data.offset = offset
                bpy.context.object.data.extrude = extrude
                if get_object_bool == True and props.target_curve != None:
                    if props.target_curve.data.bevel_depth != 0.00:
                        props.target_curve.data.bevel_depth = 0.00
                    bpy.context.object.data.bevel_mode = 'OBJECT'
                    bpy.context.object.data.bevel_object = props.target_curve
                else:
                    bpy.context.object.data.bevel_mode = 'ROUND'



            return (True,"finished")

        else:
            return (False,"please select open mesh　or curve")



class SIMPLE_OT_easy_curve_to_mesh(bpy.types.Operator):
    bl_idname = 'object.easy_curve_to_mesh'
    bl_label = 'easy　curve　to　mesh'
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n '
    bl_options = {'REGISTER', 'UNDO','PRESET'}
    
    # testプロパティ

    cmd :  bpy.props.StringProperty(
        default="", 
        options={'HIDDEN'})

    depth:bpy.props.FloatProperty(
        name='depth', 
        description='', 
        default=(0.05),
        )
    offset:bpy.props.FloatProperty(
        name='offset', 
        description='', 
        default=(0.00),
        )
    extrude:bpy.props.FloatProperty(
        name='extrude', 
        description='', 
        default=(0.00),
        )

        
    fill_caps_bool : bpy.props.BoolProperty(
        name= "fill caps",
        default=0
        )

    bevel_resolution : bpy.props.IntProperty(
        name= "bevel resolution",
        default=4
        )

    duplicate_move_bool : bpy.props.BoolProperty(
        name= "duplicate move",
        default=False
        )

    get_object_bool:bpy.props.BoolProperty(
        name='object', 
        description='', 
        # default=(0.00),
        )

    @classmethod
    
    def poll(self, context):

        return True


    def execute(self, context):
        try:
            bool,messeage = main(
                self.depth,
                self.fill_caps_bool,
                self.bevel_resolution,
                self.duplicate_move_bool,
                self.offset,
                self.extrude,
                self.get_object_bool,
                )
            result = "INFO" if bool ==True else 'WARNING'
            self.report( {result, },messeage)

        except TypeError:
            pass
            self.report( {'WARNING', },"plese select one object.")


        return {'FINISHED'}


    