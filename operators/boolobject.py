import bpy, os , sys
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )

from bpy.props import (
                        StringProperty, 
                        IntProperty, 
                        FloatProperty, 
                        EnumProperty, 
                        BoolProperty,
                        PointerProperty,
                        FloatVectorProperty,
                        StringProperty
                        )

class BoolOnOff(Operator):
    bl_idname = "object.boolonoff_operator"
    bl_label = "ブール用ワイヤーON/OFF"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}




    def execute(self, context):
        
        ob = bpy.context.object
        obs = bpy.context.selected_objects
        # ※選択したオブジェクトのテクスチャーとワイヤーとレンダー表示のオンオフ
        for obj in obs:
            if obj.display_type == 'TEXTURED':
                obj.display_type = 'WIRE'
                bpy.context.object.hide_render = True
            elif obj.display_type == 'WIRE':
                obj.display_type = 'TEXTURED'
                bpy.context.object.hide_render = False

        return {'FINISHED'}
booleanname='ksynbooly'
def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng


def applyboolean(obj):
    togle = None

    if bpy.context.mode == 'EDIT_MESH':
        togle = "EDIT_MESH"
        bpy.ops.object.editmode_toggle()


    for mod in obj.modifiers:
        if mod.type == 'BOOLEAN':
            
            if mod.object != None:
                bpy.ops.object.modifier_apply(modifier=mod.name)
                
            elif mod.object == None:
                bpy.ops.object.modifier_remove(modifier=mod.name)



    if togle == 'EDIT_MESH':
        bpy.ops.object.editmode_toggle()


def wireon(sel_obj):
    sel_obj.display_type = 'WIRE'
    sel_obj.hide_render = True


# 対象のオブジェクトを指定したコレクションに入れる
def linkcolobject(sel_obj):
    col="BOOL"

    # ブールがすでにあるとき
    try:
        bpy.data.collections[col].objects.link(sel_obj)
    # 選択したオブジェクトがすでにブールフォルダにあるとき。
    except RuntimeError:
        pass
    # ブールフォルダが無い時
    except KeyError:
        right_collection = bpy.data.collections.new("BOOL")
        bpy.context.scene.collection.children.link(right_collection)
        right_collection.color_tag = 'COLOR_01'
        bpy.data.collections[col].objects.link(sel_obj)


# 指定のオブジェクトを指定のコレクション以外アンリンクする
def checkunlinkcol(selectobj, selcolname):
    for checkcol in bpy.data.collections:
        
        if checkcol.name== selcolname:
            pass
        
        else:
            
            for colobj in checkcol.objects:
                
                if colobj.name == selectobj.name:
                    # print(colobj.name)
                    bpy.data.collections[checkcol.name].objects.unlink(colobj)
                    
# 最後のオブジェクトをブールコレクションに移動
def collectionmove(activeob):
    wireon(activeob)
    if bpy.context.view_layer.objects.active == activeob:
        linkcolobject(activeob)
        checkunlinkcol(activeob, "BOOL")


def add_triangul(add_tryi, obj):
    if add_tryi:
        if obj.modifiers.get("Bool Triangulate"):
            act_obj=bpy.context.view_layer.objects.active 
            bpy.context.view_layer.objects.active = obj
            obj_mod_count=len(obj.modifiers)-1
            # トライアングルモディファイをもとに戻す
            bpy.ops.object.modifier_move_to_index(modifier="Bool Triangulate", index=obj_mod_count)
            #　return to the point (of a discussion)
            bpy.context.view_layer.objects.active = act_obj

        else:
            tri_modi = obj.modifiers.new(name='Bool Triangulate', type='TRIANGULATE')

# アクティブなオブジェクトにブールをかける
def selected_mulch(self, obs,activeob,parent_bool,operation_enum,add_tryi):

    for sel_obj in obs:
        # アクティブなオブジェクトにブールモディファイアを適応
        bool = activeob.modifiers.new(name=booleanname, type='BOOLEAN')
        # 選択したオブジェクトを適応
        bool.object = sel_obj
        if operation_enum=="SLICE":
            bool.operation = "DIFFERENCE"
        else:
            bool.operation = operation_enum
        bool.solver = 'FAST'


        
        # アクティブオブジェクト以外をブールフォルダに移動する。（既存のコレクションはアンリンク）
        if bpy.context.view_layer.objects.active != sel_obj:
            wireon(sel_obj)
            if self.move_colection_bool == True:
                linkcolobject(sel_obj)
                checkunlinkcol(sel_obj, "BOOL")

    add_triangul(add_tryi, activeob)

    #　最後に選択したオブジェクトにペアレントするかどうか。
    if parent_bool == True:
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
    else:
        pass



# 選択したオブジェクトにアクティブなオブジェクトのブールをかける
def selected_single_bool(self, obs,activeob,operation_enum,add_tryi):

   
    for sel_obj in obs:
                # アクティブなオブジェクトにブールモディファイアを適応
        bool = sel_obj.modifiers.new(name=booleanname, type='BOOLEAN')
        # 選択したオブジェクトアクティブオブジェクトを適応

        bool.object = activeob
        if operation_enum=="SLICE":
            bool.operation = "DIFFERENCE"
        else:
            bool.operation = operation_enum

        bool.solver = 'FAST'
        add_triangul(add_tryi, sel_obj)

        # 最後のオブジェクトをブールコレクションに移動
        if self.move_colection_bool == True:
            collectionmove(activeob)
        else:
            wireon(activeob)
        


    if operation_enum=="SLICE":
        activeob.select_set(False)

        bpy.ops.object.duplicate_move()

        for sel_obj in bpy.context.selected_objects:
            obs.append(sel_obj)
            if add_tryi:
                bool = sel_obj.modifiers[-2]
            else:
                bool = sel_obj.modifiers[-1]

            bool.operation = "INTERSECT"

    # print("###list",obs)



def main(self, selected_mulch_bool, parent_bool,operation_enum,add_tryi):

    # 削りたい対象のオブジェクト（アクティブ）を定義
    activeob = bpy.context.active_object

    # アクティブが対象にならないように選択を解除
    activeob.select_set(False)

    # 削りのオブジェクトを定義
    obs = bpy.context.selected_objects

    # 一つのオブジェクトだけ削りたい時（アクティブオブジェクト以外は非ブール）
    if selected_mulch_bool == True:
        selected_mulch(self, obs,activeob,parent_bool,operation_enum,add_tryi)

    # 複数のオブジェクトだけ削りたい時（アクティブオブジェクトは非ブール）
    else:
        selected_single_bool(self, obs,activeob,operation_enum,add_tryi)


class SelectObjectBool(Operator):
    bl_idname = "object.selectobjectbool_operator"
    bl_label = "Simple Boolean"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    options = [
        ('DIFFERENCE', 'Difference', 'Difference'),
        ('UNION', 'Union', 'Union'),
        ('INTERSECT', 'Intersect', 'Intersect'),
        ('SLICE', 'slice', 'slice')
        ]
    
    operation_enum: bpy.props.EnumProperty(
        name="operation",
        items=options,
        description=""
        ) # type: ignore
    
    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore

    
    parent_bool: bpy.props.BoolProperty(
                                    name=get_translang('Parent','親子化'),
                                    default=True,
                                    ) # type: ignore
    selected_mulch_bool: bpy.props.BoolProperty(
                                    name=get_translang('selected_mulch_bool','複数でブール'),
                                    default=True,
                                    ) # type: ignore
    
    move_colection_bool: bpy.props.BoolProperty(
                                    name=get_translang('move colection','コレクション移動'),
                                    default=True,
                                    ) # type: ignore
    add_tryi_bool: bpy.props.BoolProperty(
                                    name=get_translang('Triangulation modifier added','三角化モディファイア追加'),
                                    default=True,
                                    ) # type: ignore




    def draw_main(self):
        if self.cmd =="applyboolean":
            pass
        elif self.cmd =="simpleboolean":

            self.layout.prop(self,"parent_bool")
            self.layout.prop(self,"selected_mulch_bool")
            self.layout.prop(self,"move_colection_bool")

            self.layout.prop_enum(self, "operation_enum", "DIFFERENCE")        
            self.layout.prop_enum(self, "operation_enum", "UNION")        
            self.layout.prop_enum(self, "operation_enum", "INTERSECT") 
            
            if not self.selected_mulch_bool:
                self.layout.prop_enum(self, "operation_enum", "SLICE")        

            self.layout.prop(self,"add_tryi_bool")

    def execute(self, context):
        if self.cmd =="applyboolean":
            applyboolean(context.object)
        else:
            main(self, self.selected_mulch_bool, self.parent_bool,self.operation_enum,self.add_tryi_bool)
    
        return {'FINISHED'}
    def draw(self, context):
        
        self.draw_main()
