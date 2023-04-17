import bpy, os , sys
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )
        

def curve_to_mesh(context, curve):
    deg = context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(curve.evaluated_get(deg), depsgraph=deg)

    new_obj = bpy.data.objects.new(curve.name + "_ins_ob", me)


    for o in context.selected_objects:
        o.select_set(False)

    new_obj.matrix_world = curve.matrix_world

    return new_obj


def mesh_eval_to_mesh(context, obj):
    deg = context.evaluated_depsgraph_get()
    eval_mesh = obj.evaluated_get(deg).data.copy()
    new_obj = bpy.data.objects.new(obj.name + "_ins_ob", eval_mesh)
    for o in context.selected_objects:
        o.select_set(False)

    new_obj.matrix_world = obj.matrix_world
    return new_obj


class PIE3D_OT_objectinstans(Operator):
        bl_idname = 'object.objectinstans_operator'
        bl_label = 'objectinstans_operator'
        # 自身のクラスの呼び出しにはSYSモジュールが必要
        bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
        bl_options = {'REGISTER', 'UNDO'}

        hide_bool: bpy.props.BoolProperty(
                                        name='sorce_obj_hide',
                                        default=True,
                                        )

        hide_ins_col_bool: bpy.props.BoolProperty(
                                        name='hide_ins_col_bool',
                                        default=True,
                                        )

        make_instans_bool: bpy.props.BoolProperty(
                                        name='make_instans_bool',
                                        default=True,
                                        )
     
        col_color: bpy.props.EnumProperty(items= [
                                        ('NONE', "NONE", "", 1),
                                        ("COLOR_01", "赤", "", 2),
                                        ("COLOR_02", "橙", "", 3),
                                        ("COLOR_03", "黄色", "", 4),
                                        ("COLOR_04", "緑", "", 5),
                                        ("COLOR_05", "水色", "", 6),
                                        ("COLOR_06", "紫", "", 7),
                                        ("COLOR_07", "桃色", "", 8),
                                        ("COLOR_08", "茶色", "", 9),
                                    ])

        colname: bpy.props.StringProperty(
                                name='colname',
                                default="",
                                )


        @classmethod
        def poll(self, context):

            return  True

        def copy_miror(self):
            self.sele_obj = bpy.context.selected_objects 
            self.right_select_objectlist = []
            self.instans_collection = bpy.data.collections.new(self.colname + "INSTANS_OB")
            bpy.context.scene.collection.children.link(self.instans_collection)
            self.instans_collection.color_tag = self.col_color


            self.left_obj_list = []
        
        def copy_obj(self):
            bpy.ops.object.select_all(action='DESELECT')


            # 複製して選択する
            for obj in self.sele_obj:

                right_copyobj=obj.copy()
                right_copyobj.name = obj.name + "_instans_ob"
                
                # オブジェクトを先程作成したコレクションにリンクする
                bpy.data.collections[self.instans_collection.name].objects.link(right_copyobj)
                right_copyobj.select_set(True)
                self.right_select_objectlist.append(right_copyobj)
                bpy.context.view_layer.objects.active = right_copyobj


            # 選択したオブジェクトをシングルユーザー化してメッシュ化する
            bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False)
            bpy.ops.object.select_all(action='DESELECT')


            for obj in self.right_select_objectlist:

                if obj.type != "EMPTY":

                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                else:
                    obj.select_set(False)

            try:
                bpy.ops.object.convert(target='MESH')
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
   
            except RuntimeError:
                pass
            bpy.ops.object.select_all(action='DESELECT')

        # 作業が上記で終わったので、移動したコレクションをインスタンス化して最後にコレクションのチェックを外す。
        def check_obj(self):

            scenename = bpy.context.scene.name
            self.instansname = scenename + "_INSTANS"


            # インスタンスコレクションがあるかどうか確かめる
            try:
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
                layerColl = recurLayerCollection(layer_collection, self.instansname)
                bpy.context.view_layer.active_layer_collection.exclude = False
                # コレクションを表示状態にしないと何故かアクティブ化できない
                bpy.context.view_layer.active_layer_collection = layerColl

                      
            # インスタンスコレクションが無いので、作成する
            except TypeError:
                obj_instans_col = bpy.data.collections.new(self.instansname)
                bpy.context.scene.collection.children.link(obj_instans_col)
                
                def recurLayerCollection(layerColl, collName):
                    found = None
                    if (layerColl.name == collName):
                        return layerColl
                    for layer in layerColl.children:
                        found = recurLayerCollection(layer, collName)
                        if found:
                            return found

                # インスタンスコレクションをアクティブ化
                layer_collection = bpy.context.view_layer.layer_collection
                layerColl = recurLayerCollection(layer_collection, self.instansname)
                bpy.context.view_layer.active_layer_collection = layerColl
                bpy.context.collection.color_tag = 'COLOR_04'

        def instans(self):
                # 右をインスタンス化
                
                bpy.ops.object.collection_instance_add(collection=self.instans_collection.name, align='WORLD')
        
        def hide_col(self):
            # インスタンス化が終わったので、コレクションを非表示にしていく
            actcolchil = bpy.context.view_layer.layer_collection.children
            layer_collection = actcolchil[self.instans_collection.name]
            bpy.context.view_layer.active_layer_collection = layer_collection
            bpy.context.view_layer.active_layer_collection.exclude = True

        def hide_obj(self):
                                
            # 複製元のオブジェクトを隠す
            for obj in self.sele_obj:
                obj.hide_set(True)
                           
        def execute(self, context):
            # オブジェクトを選択してるかどうか確かめる
            if bpy.context.selected_objects != []:
                self.copy_miror()
                self.copy_obj()
                self.check_obj()
                
                if self.make_instans_bool == True:
                    self.instans()

                if self.hide_ins_col_bool == True:
                    self.hide_col()
                    
                if self.hide_bool == True:
                    self.hide_obj()

            else:
                self.report({'INFO'}, "plese select object")
                pass
                
            
            return {'FINISHED'}

        def invoke(self, context, event):
            
            return context.window_manager.invoke_props_dialog(self)

        def draw(self, context):
            layout = self.layout
            col = layout.column()
            col.prop(self,"hide_bool")
            col.prop(self,"hide_ins_col_bool")
            col.prop(self,"make_instans_bool")
            col.prop(self,"col_color")
            col.prop(self,"colname")