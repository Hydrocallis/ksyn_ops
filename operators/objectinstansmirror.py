import bpy, os , sys
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )
class PIE3D_OT_objectinstansmirror(Operator):
        bl_idname = 'object.objectinstansmirror_operator'
        bl_label = 'objectinstansmirror_operator'
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
   
        transform_axis: bpy.props.EnumProperty(items= [
                                        ('X', "X", "", 1),
                                        ("Y", "Y", "", 2),
                                        ("Z", "Z", "", 3),
                  
                                    ])

        colname: bpy.props.StringProperty(
                                name='colname',
                                default="",
                                )

       
        @classmethod
        def poll(self, context):
            # 選択したオブジェクトの中にメッシュとカーブ以外があるかどうか調べてる
            # objtypelist = []
            # for obj in context.selected_objects:
            #     if obj.type =="MESH" or obj.type== 'CURVE':
            #         objtypelist.append(True)
            #     else:
            #         objtypelist.append(False)

            # if  all(objtypelist) == True:
                return True


        def copy_miror(self):

     
            self.sele_obj = bpy.context.selected_objects 

            self.right_select_objectlist = []

            self.right_collection = bpy.data.collections.new(self.colname + "MIRROR_RIGHT_OB")
            bpy.context.scene.collection.children.link(self.right_collection)

            self.left_obj_list = []

            self.left_collection = bpy.data.collections.new(self.colname + "MIRROR_LEFT_OB")
            bpy.context.scene.collection.children.link(self.left_collection)

            bpy.ops.object.select_all(action='DESELECT')

        def copy_obj(self):

            # 右用のオブジェクトを複製して選択する
            for obj in self.sele_obj:

                right_copyobj=obj.copy()
                right_copyobj.name = obj.name + "_right_of_mirror"
                
                # オブジェクトを先程作成したコレクションにリンクする
                bpy.data.collections[self.right_collection.name].objects.link(right_copyobj)
                right_copyobj.select_set(True)
                self.right_select_objectlist.append(right_copyobj)
                bpy.context.view_layer.objects.active = right_copyobj

            # 選択したオブジェクトをシングルユーザー化してメッシュ化する
            bpy.ops.object.make_single_user(object=True, obdata=True, material=True, animation=False)
            bpy.ops.object.convert(target='MESH')   
            bpy.ops.object.select_all(action='DESELECT')
            scene = bpy.context.scene
        
        def copy_right_ofj(self):
            # 次に、右用のオブジェクトから左を複製して同じくメッシュ化する
            # 最後に二等分して左右に分離する
            for obj in self.right_select_objectlist:

                copyobj=obj.copy()
                
                scene = bpy.context.scene
                # オブジェクトを先程作成したコレクションにリンクする
                bpy.data.collections[self.left_collection.name].objects.link(copyobj)
                bpy.context.view_layer.objects.active = copyobj
                copyobj.select_set(True)
                bpy.ops.object.make_single_user(object=True, obdata=True, material=True, animation=False, obdata_animation=False)
                copyobj.select_set(False)
                
                
                copyobj.name =copyobj.name.replace("_right_of_mirror.001", "_left_of_mirror")
                self.left_obj_list.append(copyobj)
            bpy.ops.object.select_all(action='DESELECT')

        def left_slice_obj(self):

            if self.transform_axis == "Y":
                plano=(0,1,0)
            elif self.transform_axis =="X":
                plano=(1,0,0)
            elif self.transform_axis =="Z":
                plano=(0,0,1)

            
            for obj in self.left_obj_list:
             
                # 左を切断する
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                # https://docs.blender.org/api/current/bpy.ops.mesh.html#bpy.ops.mesh.bisect
                bpy.ops.mesh.bisect(
                plane_co=(0, 0, 0), 
                plane_no=plano, 
                clear_inner=False, 
                clear_outer=True, 
                xstart=280, 
                xend=279, 
                ystart=247, 
                yend=422, 
                flip=False
                )

                bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
                
        def right_slice_obj(self,):

            for rightogj in self.right_select_objectlist:
                             
                # 右を切断する
                bpy.context.view_layer.objects.active = rightogj
                rightogj.select_set(True)

                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                # https://docs.blender.org/api/current/bpy.ops.mesh.html#bpy.ops.mesh.bisect
                if self.transform_axis == "Y":
                    plano=(0,1,0)
                elif self.transform_axis =="X":
                    plano=(1,0,0)
                elif self.transform_axis =="Z":
                    plano=(0,0,1)

                bpy.ops.mesh.bisect(
                plane_co=(0, 0, 0), 
                plane_no=plano, 
                clear_inner=True, 
                clear_outer=False, 
                xstart=280, 
                xend=279, 
                ystart=247, 
                yend=422, 
                flip=False
                )

                bpy.ops.object.mode_set(mode='OBJECT')
                rightogj.select_set(False)
        ### ミラーコピー完了
        # 作業が上記で終わったので、移動したコレクションをインスタンス化して最後にコレクションのチェックを外す。
        def check_obj(self,colar):

            scenename = bpy.context.scene.name
            self.instansname = scenename + "_INSTANS"


            # インスタンスコレクションがあるかどうか確かめる
            try:
                def recurLayerCollection(layerColl, collName):
                    found = None
                    if (layerColl.name == collName):
                        return layerColl
                    for layer in layerColl.children:
                        found = recurLayerCollection(layer, self.instansname)
                        if found:
                            return found

                #Change the Active LayerCollection to 'My Collection'
                layer_collection = bpy.context.view_layer.layer_collection
                layerColl = recurLayerCollection(layer_collection, self.instansname)
                bpy.context.view_layer.active_layer_collection = layerColl
        #        # サブコレクションを追加
                # 右をインスタンス化
                # bpy.ops.object.collection_instance_add(collection=self.right_collection.name, align='WORLD')
                # どういうわけかわからないが、二度目は消してもすでにインスタンスにコレクションがリンクしてあるので、エラーチェックする
                # try:
                #     bpy.data.collections[self.instansname].objects.link(bpy.context.object)
                # except RuntimeError:

                #     pass
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
                #Change the Active LayerCollection to 'My Collection'
                layer_collection = bpy.context.view_layer.layer_collection
                layerColl = recurLayerCollection(layer_collection, self.instansname)
                bpy.context.view_layer.active_layer_collection = layerColl
                
                bpy.context.collection.color_tag = colar
                # 右をインスタンス化
            #     bpy.ops.object.collection_instance_add(collection=self.right_collection.name, align='WORLD')
            # # 左をインスタンス化
            # bpy.ops.object.collection_instance_add(collection=self.left_collection.name, align='WORLD')
         #    bpy.context.object.name = "left"
        def instans(self):
            # 右をインスタンス化
            bpy.ops.object.collection_instance_add(collection=self.right_collection.name, align='WORLD')
            # 左をインスタンス化
            bpy.ops.object.collection_instance_add(collection=self.left_collection.name, align='WORLD')
         #    bpy.context.object.name = "left"

        def hide_col(self):
            # インスタンス化が終わったので、コレクションを非表示にしていく
            try:
                layer_collection = bpy.context.view_layer.layer_collection.children[self.right_collection.name]
            except NameError:
                layer_collection = bpy.context.view_layer.layer_collection.children[self.right_collection.name]
            bpy.context.view_layer.active_layer_collection = layer_collection
            bpy.context.view_layer.active_layer_collection.exclude = True
            try:
                layer_collection = bpy.context.view_layer.layer_collection.children[self.left_collection.name]
            except NameError:
                layer_collection = bpy.context.view_layer.layer_collection.children[self.left_collection.name]

            bpy.context.view_layer.active_layer_collection = layer_collection
            bpy.context.view_layer.active_layer_collection.exclude =True
            # コレクション非表示完了
        def hide_obj(self):

            # 複製元のオブジェクトを隠す
            for obj in self.sele_obj:
                obj.hide_set(True)
                print('###hide object is ',obj)
                           
        def execute(self, context):

            # オブジェクトを選択してるかどうか確かめる
            objtypelist = []
            for obj in context.selected_objects:
                if obj.type =="MESH" or obj.type== 'CURVE':
                    objtypelist.append(True)
                else:
                    objtypelist.append(False)

            # if  all(objtypelist) == True:
            if bpy.context.selected_objects != [] and all(objtypelist) == True:
  
                self.copy_miror()
                self.copy_obj()
                self.copy_right_ofj()
                self.left_slice_obj()
                self.right_slice_obj()
                self.check_obj(self.col_color)

                if self.make_instans_bool == True:
                    self.instans()

                if self.hide_ins_col_bool == True:
                    self.hide_col()
                    
                if self.hide_bool == True:
                    self.hide_obj()

            elif all(objtypelist) == False:
                self.report({'INFO'}, "Do not select objects other than meshes and curves.")
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
            col.prop(self,"col_color", expand=True)
            col.prop(self,"colname")
            col.prop(self,"transform_axis")