import bpy
from mathutils import Vector
from bpy.props import IntProperty
from bpy.props import StringProperty
from bpy.props import BoolProperty
from bpy.props import FloatVectorProperty
from bpy.props import FloatProperty
from bpy.props import EnumProperty
from ksyn_ops.utils.get_translang import get_translang

import mathutils

def get_selected_objects_bottom_vertex_world_pos(seleobj):
    """
    選択したオブジェクト群の一番底辺の頂点のワールド座標を取得する関数。

    Returns:
        mathutils.Vector: 選択したオブジェクト群の一番底辺の頂点のワールド座標
    """
    bottom_vertex_world_pos = None

    # 選択したオブジェクト群の中で一番底辺の頂点のワールド座標を探索
    for obj in seleobj:
        if obj.type == 'MESH':  # メッシュオブジェクトのみ対象とする
            mesh = obj.data
            min_z = min([v.co.z for v in mesh.vertices])
            bottom_vertex_index = [v.index for v in mesh.vertices if v.co.z == min_z][0]
            bottom_vertex_world_pos_obj = obj.matrix_world @ mesh.vertices[bottom_vertex_index].co
            if bottom_vertex_world_pos is None or bottom_vertex_world_pos_obj.z < bottom_vertex_world_pos.z:
                bottom_vertex_world_pos = bottom_vertex_world_pos_obj

    return bottom_vertex_world_pos

def get_selected_objects_bounding_box_center(selected_objects):
    if not isinstance(selected_objects, list):
        selected_objects = [selected_objects]
    
    bb_center = mathutils.Vector()
    
    for obj in selected_objects:
        obj_bb_min = obj.matrix_world @ mathutils.Vector(obj.bound_box[0])
        obj_bb_max = obj.matrix_world @ mathutils.Vector(obj.bound_box[6])
        bb_center += (obj_bb_min + obj_bb_max) / 2
    bb_center /= len(selected_objects)
    return bb_center

def get_bottom_vertex_world_pos(obj):
    if obj.type == 'MESH':
        # メッシュデータを取得
        mesh = obj.data

        # メッシュの底辺の頂点のインデックスを検索
        min_z = min([v.co.z for v in mesh.vertices])
        bottom_vertex_index = [v.index for v in mesh.vertices if v.co.z == min_z][0]

        # ワールド座標を取得
        bottom_vertex_world_pos = obj.matrix_world @ mesh.vertices[bottom_vertex_index].co

        return bottom_vertex_world_pos
    else:
        # オブジェクトがメッシュでない場合は、オブジェクト自体のワールド座標を返す
        return obj.location

def set_parent_with_transform(seleobj,parent_obj, maintain_transform=True):
    """
    選択されたオブジェクトに親オブジェクトを設定し、子のトランスフォームを維持する関数。
    :param parent_obj: 親に設定するオブジェクト
    :param maintain_transform: 子のトランスフォームを維持するかどうかのブール値。Trueの場合は維持し、Falseの場合は初期状態に戻す。デフォルトはTrue。
    """
    # アクティブなオブジェクトのトランスフォームを保存
    parent_matrix = parent_obj.matrix_world.copy()

    # 選択されたオブジェクトのペアレントを設定
    for obj in seleobj:
        if obj != parent_obj and obj.parent is None:  # 既に親を持っていないオブジェクトに対してのみペアレントを設定
            # オブジェクトのペアレント関係を設定する前に、トランスフォームを保持しておく
            obj_matrix = obj.matrix_world.copy()

            # ペアレント関係を設定
            obj.parent = parent_obj

            # トランスフォームを維持する場合は、保持しておいたトランスフォームを適用
            if maintain_transform:
                obj.matrix_world = obj_matrix

    # アクティブなオブジェクトのトランスフォームを復元
    parent_obj.matrix_world = parent_matrix

    # # アクティブなオブジェクトを取得
    # parent_obj = bpy.context.active_object

    # # メソッドを呼び出し（トランスフォームを維持する場合）
    # set_parent_with_transform(parent_obj, True)

    # # メソッドを呼び出し（トランスフォームを維持しない場合）
    # set_parent_with_transform(parent_obj, False)


display_type_items = [
    ("PLAIN_AXES", "Plain Axes", "", 1),
    ("ARROWS", "Arrows", "", 2),
    ("SINGLE_ARROW", "Single Arrow", "", 3),
    ("CIRCLE", "Circle", "", 4),
    ("CUBE", "Cube", "", 5),
    ("SPHERE", "Sphere", "", 6),
    ("CONE", "Cone", "", 7),
        ]

bottom_types = [
    ("act_obj", "Active Object", "", 1),
    ("cursor", "Cursor", "", 2),
    # ("sele_center", get_translang("Select object Center","オブジェクト群の中心"), "", 3),
    ("sele_bottom", get_translang("Bottom of object group","オブジェクト群の一番下"), "", 4),

        ]

target_center = [
    ("act_obj", "Active Object", "", 1),
    ("sel_obj", "Select Objects", "", 2),
    ("cursor", "Cursor", "", 3),

        ]

class lastselectaddempty(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.lastselectaddempty"
    bl_label = "Last select add empty"
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    name : StringProperty(default = "Empty")

    parent : BoolProperty(default = True,name = "Parent")
    parent_keep_transform : BoolProperty(default = True,name=get_translang("Keep the transformation","変形をキープする"))
    parent_chid_keep : BoolProperty(default = True,name=get_translang("Keeping the hierarchy in place","階層のキープ"))
    name_change : BoolProperty(default = False,name=get_translang("Name Change","Name Change"))
    
    display_items : EnumProperty(items=display_type_items, default="SINGLE_ARROW")
    targe_centers : EnumProperty(items=target_center, default="act_obj",name ="Target Center")
    bottom_type : EnumProperty(items=bottom_types, default="act_obj",name ="Bottom Type")

    emlocation : FloatVectorProperty(subtype="XYZ_LENGTH")
    display_size : FloatProperty(default= 1)



    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.cursor_loc = bpy.context.scene.cursor.location
        self.actobj = bpy.context.active_object

        seleobj = context.selected_objects
        totalloc = self.getloacation(context, seleobj)
        self.add_empty(context, totalloc, seleobj)
        
        if self.name_change:
            self.name_changeadd(seleobj)

        return {'FINISHED'}

    def getloacation(self, context, seleobj):

        if self.targe_centers == "sel_obj":
            centerget = seleobj
            center =  get_selected_objects_bounding_box_center(centerget)
        elif self.targe_centers =="act_obj":
            centerget = self.actobj
            center =  get_selected_objects_bounding_box_center(centerget)
        if self.targe_centers =="cursor":
            center = tuple(self.cursor_loc)

        bb_center =  get_selected_objects_bounding_box_center(seleobj)

        if self.bottom_type == "act_obj":
            obj = self.actobj
            bottom_location = get_bottom_vertex_world_pos(obj)
            bb_center = Vector((bb_center[0],bb_center[1],bottom_location[2]))
        

        if self.bottom_type == "sele_bottom":
            obj = self.actobj
            bottom_vertex_world_pos = get_selected_objects_bottom_vertex_world_pos(seleobj)
            bb_center = Vector((bb_center[0],bb_center[1],bottom_vertex_world_pos[2]))

        
        elif self.bottom_type == "cursor":
            # カーソルの位置を取得
            cursor_location = self.cursor_loc
            bb_center = Vector((bb_center[0],bb_center[1],cursor_location[2]))

        totalloc = (center[0],center[1],0) 
        totalloc = (totalloc[0],totalloc[1],bb_center[2])
        totalloc = tuple(map(sum, zip(totalloc, self.emlocation)))

        return totalloc


    def add_empty(self,context, totalloc, seleobj):

        # emptysetting
        # print('###',totalloc)
        bpy.ops.object.empty_add(
            type='PLAIN_AXES', align='WORLD', 
            location=totalloc, 
            scale=(1, 1, 1))

        emptyobj = bpy.context.object
        emptyobj.name = self.name
        emptyobj.empty_display_type = self.display_items
            
        bpy.context.object.empty_display_size = self.display_size

        if self.parent == True:
            if self.parent_chid_keep != True:
                for i in seleobj:
                    i.select_set(state = True)
                
                    bpy.ops.object.parent_set(
                        type='OBJECT',
                        keep_transform=self.parent_keep_transform
                        )
            else:
                # アクティブなオブジェクトを取得
                parent_obj = self.actobj

                # メソッドを呼び出し
                set_parent_with_transform(seleobj,parent_obj,self.parent_keep_transform)

    def name_changeadd(self,seleobj):
        count = 1
        for obj in seleobj:
            obj.name = self.name +"_" + str(count)
            count += 1