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
                        StringProperty)

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng
    
def ShowMessageBox(message:list = [], title = "Message Box", icon = 'INFO'):

    def draw(self, context):

        for mes in message:
            self.layout.label(text=mes)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

# パネル用のオペレーター
class OBJECT_OT_boolean_targets_enum(bpy.types.Operator):
    bl_idname = "object.boolean_targets_enum"
    bl_label = get_translang("Boolean Targets","ブーリアン・ターゲット")
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore

    def collection_exculude_hide(self, colename="BOOL"):
        # #Recursivly transverse layer_collection for a particular name
        def recurLayerCollection(layerColl, collName):
            found = None
            if (layerColl.name == collName):
                return layerColl
            for layer in layerColl.children:
                found = recurLayerCollection(layer, collName)
                if found:
                    return found

        #Change the Active LayerCollection to 'My Collection'
        layer_collection = bpy.context.view_layer.layer_collection
        layerColl = recurLayerCollection(layer_collection, colename)
        if not layerColl==None:

            bpy.context.view_layer.active_layer_collection = layerColl
            layerColl.exclude = False
            layerColl.hide_viewport = False
            return layerColl
        else:
            return None

    def draw(self, context):
        layout = self.layout

    def execute(self, context):
        tuple_from_str = tuple(eval(self.cmd))
        if tuple_from_str[0] =="apply":
            active_object=bpy.context.object
            # print("###bpy.data.objects[tuple_from_str[2]]",bpy.data.objects[tuple_from_str[2]])
            bpy.context.view_layer.objects.active = bpy.data.objects[tuple_from_str[2]]
            bpy.context.object.select_set(True)
            bpy.ops.object.modifier_apply(modifier=tuple_from_str[1])
            # bpy.context.object.select_set(False)
            bpy.context.view_layer.objects.active = active_object


        elif tuple_from_str[0] =="bool_viewport":
            if bpy.data.objects[tuple_from_str[2]].modifiers[tuple_from_str[1]].show_viewport:
                bpy.data.objects[tuple_from_str[2]].modifiers[tuple_from_str[1]].show_viewport = False
            else:
                bpy.data.objects[tuple_from_str[2]].modifiers[tuple_from_str[1]].show_viewport = True

        else:
            
            # print("Selected Boolean Target:", self.cmd)
            try:
                bpy.data.objects[tuple_from_str[0]].hide_set(tuple_from_str[1])
            except RuntimeError:
                layerColl = self.collection_exculude_hide(colename="BOOL")
                if not layerColl==None:
                    bpy.data.objects[tuple_from_str[0]].hide_set(tuple_from_str[1])
                else:
                    ShowMessageBox(message=["Not found BOOl collection"], title = "Message Box", icon = 'INFO')
                    pass

        return {'FINISHED'}

class OBJECT_PT_BooleanObjectsPanel(bpy.types.Panel):
    bl_label = "KSYN Boolean Objects Status"
    bl_idname = "OBJECT_PT_boolean_objects"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "

    def get_boolean_modifier_targets(self,obj):
        boolean_modifiers = [modifier for modifier in obj.modifiers if modifier.type == 'BOOLEAN']
        target_objects = [(modifier.object,modifier.name) for modifier in boolean_modifiers]

        return target_objects
    
    def load_panle_boolean_object(self,layout,obj):
        try:
            from .. import ksynops_preview_collections
        except:
            from ksyn_ops import ksynops_preview_collections # type: ignore

        pcoll = ksynops_preview_collections["main"]
        layout.label(text="Boolean Objects for " + obj.name)
        target_objects = self.get_boolean_modifier_targets(obj)

        for boolean_obj,modifier_name in target_objects:
            if  boolean_obj:
                if boolean_obj.hide_get():
                    obj_hide_reslut = False
                else:
                    obj_hide_reslut = True
                # print("###b",bpy.context.object)
            
                if obj.modifiers[modifier_name].show_viewport:
                    bool_modifire_viewport_reslut=True
                else:
                    bool_modifire_viewport_reslut=False

                grid = layout.grid_flow(row_major=True, columns=5, even_columns=True, even_rows=True, align=True)
        
                grid.label(text="- " + boolean_obj.name)

                if "ksynbooly_slice_dif" in modifier_name:
                    operation_name = "SLICE_DIFFERENCE"
                    ope_icon=pcoll["slice"].icon_id
                elif "ksynbooly_slice_int" in modifier_name:
                    operation_name = "SLICE_INTERSECT"
                    ope_icon=pcoll["slice_int"].icon_id
                elif "ksynbooly_slice_gapint" in modifier_name:
                    operation_name = "SLICE_GAP_INTERSECT"
                    ope_icon=pcoll["slice_gap"].icon_id
                else:
                    operation_name = obj.modifiers[modifier_name].operation
                    if  obj.modifiers[modifier_name].operation=="DIFFERENCE":
                        ope_icon=pcoll["diff"].icon_id
                    elif  obj.modifiers[modifier_name].operation=="UNION":
                        ope_icon=pcoll["join"].icon_id
                    elif  obj.modifiers[modifier_name].operation=="INTERSECT":
                        ope_icon=pcoll["int"].icon_id
                    else:
                        ope_icon=pcoll["diff"].icon_id




                grid.label(text=operation_name, icon_value=ope_icon)
                grid.operator("object.boolean_targets_enum",depress = obj_hide_reslut, icon=f"HIDE_OFF" if obj_hide_reslut else f"HIDE_ON",text="").cmd =str((boolean_obj.name, obj_hide_reslut))
                # grid.operator("object.boolean_targets_enum",depress =reslut,text=f"Show" if reslut else f"Hide").cmd =str(("bool_viewport", modifier_name))
                grid.operator("object.boolean_targets_enum",text="", icon="RESTRICT_VIEW_OFF" ,depress =bool_modifire_viewport_reslut ).cmd =str(("bool_viewport", modifier_name,obj.name))
                grid.operator("object.boolean_targets_enum",text="",icon="CHECKMARK").cmd =str(("apply", modifier_name,obj.name))
        
    def load_panle_trimod_object(self,layout,obj):
    
        grid = layout.grid_flow(row_major=True, columns=5, even_columns=True, even_rows=True, align=True)
        for mod in obj.modifiers:
            if mod.type == 'TRIANGULATE':
                grid.label(text=f"")    
                grid.label(text=f"",icon="MOD_TRIANGULATE")

    def load_panle_mirror_object(self,layout,obj):
        grid = layout.grid_flow(row_major=True, columns=5, even_columns=True, even_rows=True, align=True)
        for mod in obj.modifiers:
            if mod.type == 'MIRROR':
                grid.label(text=f"")    
                grid.label(text=f"",icon="MOD_MIRROR")

    def draw(self, context):
        layout = self.layout
        layout.operator("object.selectobjectbool_operator").cmd = "simpleboolean"
        layout.operator("object.selectobjectbool_operator",text=get_translang('Appy Boolean','ブーリアン適応')).cmd = "applyboolean"
        layout.operator("object.boolonoff_operator")
        layout.operator("object.selectobjectbool_operator",text=get_translang('Triangle modifier remove','三角モディファイアを削除')).cmd = "remove_Triangle"
        layout.operator("object.selectobjectbool_operator",text=get_translang('Triangle modifier add','三角モディファイアを追加')).cmd = "add_Triangle"
        selected_objects = bpy.context.selected_objects
        
        for obj in selected_objects:
            self.load_panle_boolean_object(layout,obj)
            self.load_panle_trimod_object(layout, obj)
            self.load_panle_mirror_object(layout, obj)
    
class BoolOnOff(Operator):
    bl_idname = "object.boolonoff_operator"
    bl_label = get_translang("Wire for boule ON/OFF","ブール用ワイヤーON/OFF")
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

class SelectObjectBool_props():

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
    
    cmd: bpy.props.StringProperty(default="simpleboolean", options={'HIDDEN'}) # type: ignore

    
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
    
    sline_Intersect_bool: bpy.props.BoolProperty(
                                    name=get_translang('Gaps in sliced objects','スライスしたオブジェクトのギャップ'),
                                    default=True,
                                    ) # type: ignore

    sline_Intersect_vector: bpy.props.FloatVectorProperty(default =(0.99,0.99,0.99),
                                                          subtype="XYZ"

        )# type: ignore
    
    sline_Intersect_location_vector: bpy.props.FloatVectorProperty(default =(0,0,0),
                                                                   subtype="XYZ_LENGTH" 

        )# type: ignore

    booleanname='ksynbooly'

class SelectObjectBool(Operator,SelectObjectBool_props):
    bl_idname = "object.selectobjectbool_operator"
    bl_label = "Simple Boolean"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    def get_and_apply_mod(self,mod,obj,message_poplist,prev_name):
        if mod.type == 'BOOLEAN':
            act_obj = bpy.context.view_layer.objects.active 
            bpy.context.view_layer.objects.active = obj
            
            if mod.object is not None:
                bpy.ops.object.modifier_apply(modifier=mod.name)
                
                # 省略して同じ文字数のダッシュで表現
                current_name = obj.name
                if current_name == prev_name:
                    abbreviated_name = '-' * len(current_name)
                else:
                    abbreviated_name = current_name
                prev_name = current_name
                try:
                    message_poplist.append(f"Apply {abbreviated_name} : {mod.name}")
                except UnicodeDecodeError:
                    message_poplist.append(f"UnicodeDecodeError")



            bpy.context.view_layer.objects.active = act_obj

        return message_poplist,prev_name

    def applyboolean(self,obj,message_poplist):
        togle = None

        if bpy.context.mode == 'EDIT_MESH':
            togle = "EDIT_MESH"
            bpy.ops.object.editmode_toggle()

        prev_name = None
        for mod in obj.modifiers:
            message_poplist, prev_name = self.get_and_apply_mod(mod,obj,message_poplist,prev_name)
           
        if togle == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
        return message_poplist

    def wireon(self,sel_obj):
        sel_obj.display_type = 'WIRE'
        sel_obj.hide_render = True

    # 対象のオブジェクトを指定したコレクションに入れる
    def linkcolobject(self,sel_obj):
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
    def checkunlinkcol(self,selectobj, selcolname):
        for checkcol in bpy.data.collections:
            
            if checkcol.name== selcolname:
                pass
            
            else:
                
                for colobj in checkcol.objects:
                    
                    if colobj.name == selectobj.name:
                        # print(colobj.name)
                        bpy.data.collections[checkcol.name].objects.unlink(colobj)
                        
    # 最後のオブジェクトをブールコレクションに移動
    def collectionmove(self,activeob):
        self.wireon(activeob)
        if bpy.context.view_layer.objects.active == activeob:
            self.linkcolobject(activeob)
            self.checkunlinkcol(activeob, "BOOL")

    def add_triangul(self, add_tryi, obj, add_triy_dics={"move_trymod": [], "new_trymod": []}):

        if add_tryi:
            if obj.modifiers.get("Bool Triangulate"):
                act_obj = bpy.context.view_layer.objects.active 
                bpy.context.view_layer.objects.active = obj
                obj_mod_count = len(obj.modifiers) - 1
                # トライアングルモディファイをもとに戻す
                bpy.ops.object.modifier_move_to_index(modifier="Bool Triangulate", index=obj_mod_count)
                # return to the point (of a discussion)
                bpy.context.view_layer.objects.active = act_obj
                # Add the object to the move_trymod list in the dictionary
                add_triy_dics["move_trymod"].append(obj.name+" Move try mod")
            else:
                obj.modifiers.new(name='Bool Triangulate', type='TRIANGULATE')
                # Add the object to the new_trymod list in the dictionary
                add_triy_dics["new_trymod"].append(obj.name + " New Add try mod")

        return add_triy_dics

    def dict_to_list(self, dict_obj):
        result_list = []
        for key, value_list in dict_obj.items():
            for value in value_list:
                result_list.append(value)
        return result_list
    
    def remove_triangulate_modifier(self,obj_name,removelist):
        obj = bpy.data.objects[obj_name]
        for mod in obj.modifiers:
            if mod.type == 'TRIANGULATE':
                obj.modifiers.remove(mod)
                removelist.append(obj.name+" remove try mod")
        return removelist

    def select_triangul(self, cmd):
        add_triy_dics = {"move_trymod": [], "new_trymod": []}
        removelist=[]

        for obj in bpy.context.selected_objects:
            if cmd=="remove_Triangle":
                removelist=self.remove_triangulate_modifier(obj.name,removelist)
                result=removelist
            elif cmd=="add_Triangle":
                add_triy_dics=self.add_triangul(add_tryi=True,obj=obj,add_triy_dics=add_triy_dics)
                result=self.dict_to_list(add_triy_dics)

        ShowMessageBox(message = result , title = "Message Box", icon = 'INFO')

    # アクティブなオブジェクトにブールをかける
    def selected_mulch(self, obs,activeob,parent_bool,operation_enum,add_tryi):

        for sel_obj in obs:
            # アクティブなオブジェクトにブールモディファイアを適応
            bool = activeob.modifiers.new(name=self.booleanname, type='BOOLEAN')
            # 選択したオブジェクトを適応
            bool.object = sel_obj
            if operation_enum=="SLICE":
                bool.operation = "DIFFERENCE"
            else:
                bool.operation = operation_enum
            bool.solver = 'FAST'

            
            # アクティブオブジェクト以外をブールフォルダに移動する。（既存のコレクションはアンリンク）
            if bpy.context.view_layer.objects.active != sel_obj:
                self.wireon(sel_obj)
                if self.move_colection_bool == True:
                    self.linkcolobject(sel_obj)
                    self.checkunlinkcol(sel_obj, "BOOL")

        self.add_triangul(add_tryi, activeob)

        #　最後に選択したオブジェクトにペアレントするかどうか。
        if parent_bool == True:
            try:
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
            except RuntimeError:
                bpy.context.scene["boolean_Status"]="Roop"
                print("roop")
            
        else:
            pass

    def selected_single_bool_first(self,obs,activeob,operation_enum,add_tryi,slice_op=False):
        for sel_obj in obs:
                    # アクティブなオブジェクトにブールモディファイアを適応
            bool = sel_obj.modifiers.new(name=self.booleanname, type='BOOLEAN')
            # 選択したオブジェクトアクティブオブジェクトを適応

            bool.object = activeob
            if operation_enum=="SLICE":
                bool.operation = "DIFFERENCE"
                bool.name = "ksynbooly_slice_dif"
 
            else:
                bool.operation = operation_enum

            if slice_op==True:
                bool.operation = "INTERSECT"
                bool.name = "ksynbooly_slice_gapint"

            bool.solver = 'FAST'
            self.add_triangul(add_tryi, sel_obj)

            # 最後のオブジェクトをブールコレクションに移動
            if self.move_colection_bool == True:
                self.collectionmove(activeob)
            else:
                self.wireon(activeob)

    def slice_object_transform(self):
        bpy.context.object.scale = (
            bpy.context.object.scale[0]*self.sline_Intersect_vector[0],
            bpy.context.object.scale[1]*self.sline_Intersect_vector[1],
            bpy.context.object.scale[2]*self.sline_Intersect_vector[2],
            )
        bpy.context.object.location = (
            bpy.context.object.location[0]+self.sline_Intersect_location_vector[0],
            bpy.context.object.location[1]+self.sline_Intersect_location_vector[1],
            bpy.context.object.location[2]+self.sline_Intersect_location_vector[2],
            )
 
    def slile_obj(self,operation_enum,activeob,obs,add_tryi):
        if operation_enum=="SLICE":
            activeob.select_set(False)

            bpy.ops.object.duplicate_move()

            selfobj=bpy.context.selected_objects

            for sel_obj in selfobj:
                obs.append(sel_obj)
                if add_tryi:
                    bool = sel_obj.modifiers[-2]
                else:
                    bool = sel_obj.modifiers[-1]

                bool.operation = "INTERSECT"
                bool.name = "ksynbooly_slice_int"



            if self.sline_Intersect_bool:
                slice_op=True
                for obj in bpy.context.selected_objects:
                    obj.select_set(False)

                    
                activeob.select_set(True)

                bpy.ops.object.duplicate_move()

                self.selected_single_bool_first(selfobj,bpy.context.object,operation_enum,add_tryi,slice_op=slice_op)
                self.slice_object_transform()

                # ギャップをつけた際に非選択になったスライスしたオブジェクトを選択状態にする
                for obj in selfobj:
                    obj.select_set(True)
                
                slice_op=False
    # 選択したオブジェクトにアクティブなオブジェクトのブールをかける# slice機能の時はこの関数を使用
    def selected_single_bool(self, obs,activeob,operation_enum,add_tryi):

        self.selected_single_bool_first(obs,activeob,operation_enum,add_tryi)
        self.slile_obj(operation_enum,activeob,obs,add_tryi)
       
    def main(self, selected_mulch_bool, parent_bool,operation_enum,add_tryi):

        # 削りたい対象のオブジェクト（アクティブ）を定義
        activeob = bpy.context.active_object

        # アクティブが対象にならないように選択を解除
        activeob.select_set(False)

        # 削りのオブジェクトを定義
        obs = bpy.context.selected_objects

        # 一つのオブジェクトだけ削りたい時（アクティブオブジェクト以外は非ブール）
        if selected_mulch_bool == True:
            self.selected_mulch(obs,activeob,parent_bool,operation_enum,add_tryi)

        # 複数のオブジェクトだけ削りたい時（アクティブオブジェクトは非ブール）
        else:
            self.selected_single_bool(obs,activeob,operation_enum,add_tryi)

    def draw_main(self):
        if self.cmd =="applyboolean":
            if bpy.context.scene.get("boolean_applay_list"):
                for obj_list in enumerate(bpy.context.scene["boolean_applay_list"],start=1):
                    self.layout.label(text=f"{obj_list[0]}_{obj_list[1]}")
            pass
        elif self.cmd =="simpleboolean":

            if self.selected_mulch_bool:
                self.layout.prop(self,"parent_bool")

            self.layout.prop(self,"selected_mulch_bool")
            self.layout.prop(self,"move_colection_bool")

            self.layout.prop_enum(self, "operation_enum", "DIFFERENCE")        
            self.layout.prop_enum(self, "operation_enum", "UNION")        
            self.layout.prop_enum(self, "operation_enum", "INTERSECT") 
            
            if not self.selected_mulch_bool:
                self.layout.prop_enum(self, "operation_enum", "SLICE")        
                if self.operation_enum == "SLICE":
                    self.layout.prop(self,"sline_Intersect_bool")
                    if self.sline_Intersect_bool:
                        self.layout.prop(self,"sline_Intersect_vector")
                        self.layout.prop(self,"sline_Intersect_location_vector")
            self.layout.prop(self,"add_tryi_bool")

        elif self.cmd =="remove_Triangle" or self.cmd == "add_Triangle":
            pass

    def execute(self, context):
        save_act_obj = bpy.context.view_layer.objects.active 
        seleobj=bpy.context.selected_objects

        if self.cmd =="applyboolean":
            message_poplist=[]
            for obj in bpy.context.selected_objects:
                message_poplist=self.applyboolean(obj,message_poplist)
            
            if message_poplist==[]:
                message_poplist=["none object"]
            ShowMessageBox(message= message_poplist)
            bpy.context.scene["boolean_applay_list"]=message_poplist

        elif self.cmd =="remove_Triangle" or self.cmd == "add_Triangle":
            self.select_triangul(self.cmd)    
            
        else:
            self.main(self.selected_mulch_bool, self.parent_bool,self.operation_enum,self.add_tryi_bool)
        save_act_obj.select_set(True)

        for obj in seleobj:
            if not obj.select_get():
                obj.select_set(True)

        return {'FINISHED'}
    
    def draw(self, context):
        
        self.draw_main()
