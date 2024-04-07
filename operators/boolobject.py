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

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng

class OBJECT_OT_boolean_targets_enum(bpy.types.Operator):
    bl_idname = "object.boolean_targets_enum"
    bl_label = "Boolean Targets Enum"
#    bl_options = {'REGISTER', 'UNDO'}

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore

#    bool: bpy.props.BoolProperty(
#        name="show autocomplete Status",
#        default=True,
#        options={'HIDDEN'}
#    ) # type: ignore


    def draw(self, context):
        layout = self.layout
#        layout.prop(self, "cmd", expand=True, text="")
#        layout.prop(self, "bool")

    def execute(self, context):
        tuple_from_str = tuple(eval(self.cmd))
        if tuple_from_str[0] =="apply":
            bpy.ops.object.modifier_apply(modifier=tuple_from_str[1])
            print("hello")
        else:
            

            print("Selected Boolean Target:", self.cmd)
            bpy.data.objects[tuple_from_str[0]].hide_viewport =tuple_from_str[1]

        return {'FINISHED'}


class OBJECT_PT_BooleanObjectsPanel(bpy.types.Panel):
    bl_label = "Boolean Objects"
    bl_idname = "OBJECT_PT_boolean_objects"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"


    def get_boolean_modifier_targets(self,obj):
        boolean_modifiers = [modifier for modifier in obj.modifiers if modifier.type == 'BOOLEAN']
        target_objects = [(modifier.object,modifier.name) for modifier in boolean_modifiers]

        return target_objects
    
    def draw(self, context):
        layout = self.layout
        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            layout.label(text="Boolean Objects for " + obj.name)
            target_objects = self.get_boolean_modifier_targets(obj)
            for boolean_obj,modifier_name in target_objects:
                if  boolean_obj:
#                    print(modifier_name)
                    layout.label(text="- " + boolean_obj.name)
                    if boolean_obj.hide_viewport:
                        reslut=False
                    else:
                        reslut =True
                    grid = layout.grid_flow(row_major=True, columns=3, even_columns=True, even_rows=True, align=True)
               
                    grid.operator("object.boolean_targets_enum",depress =reslut,text="Show" if reslut else "Hide").cmd =str((boolean_obj.name, reslut))
                    grid.operator("object.boolean_targets_enum",text="",icon="CHECKMARK").cmd =str(("apply", modifier_name))

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


    booleanname='ksynbooly'

    def ShowMessageBox(self,message = "", title = "Message Box", icon = 'INFO'):

        def draw(self, context):

            for mes in message:
                self.layout.label(text=mes)

        bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


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

    def add_triangul(self,add_tryi, obj):
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
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        else:
            pass
    # 選択したオブジェクトにアクティブなオブジェクトのブールをかける
    def selected_single_bool(self, obs,activeob,operation_enum,add_tryi):

    
        for sel_obj in obs:
                    # アクティブなオブジェクトにブールモディファイアを適応
            bool = sel_obj.modifiers.new(name=self.booleanname, type='BOOLEAN')
            # 選択したオブジェクトアクティブオブジェクトを適応

            bool.object = activeob
            if operation_enum=="SLICE":
                bool.operation = "DIFFERENCE"
            else:
                bool.operation = operation_enum

            bool.solver = 'FAST'
            self.add_triangul(add_tryi, sel_obj)

            # 最後のオブジェクトをブールコレクションに移動
            if self.move_colection_bool == True:
                self.collectionmove(activeob)
            else:
                self.wireon(activeob)
            


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

            self.layout.prop(self,"add_tryi_bool")

    def execute(self, context):
        if self.cmd =="applyboolean":
            message_poplist=[]
            for obj in bpy.context.selected_objects:
                message_poplist=self.applyboolean(obj,message_poplist)
            
            if message_poplist==[]:
                message_poplist=["none object"]
            self.ShowMessageBox(message= message_poplist)
            bpy.context.scene["boolean_applay_list"]=message_poplist
            
        else:
            self.main(self.selected_mulch_bool, self.parent_bool,self.operation_enum,self.add_tryi_bool)
    
        return {'FINISHED'}
    def draw(self, context):
        
        self.draw_main()
