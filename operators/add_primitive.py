import bpy
from bpy.props import FloatVectorProperty, EnumProperty
from mathutils import Vector
import bmesh
from math import degrees
from mathutils import Vector,Euler
import mathutils
def calculate_average_euler(euler_list):
    # x, y, zの平均値を計算
    avg_x = sum(euler.x for euler in euler_list) / len(euler_list)
    avg_y = sum(euler.y for euler in euler_list) / len(euler_list)
    avg_z = sum(euler.z for euler in euler_list) / len(euler_list)

    # 平均値のEulerオブジェクトを作成
    avg_euler = mathutils.Euler((avg_x, avg_y, avg_z), 'XYZ')

    return avg_euler



def calculate_average_position():
    # アクティブオブジェクトの取得
    obj = bpy.context.object

    # メッシュを更新
    bpy.context.edit_object.update_from_editmode()

    # 選択された頂点のみを対象とする
    selected_verts = [v.co for v in obj.data.vertices if v.select]

    # 頂点の平均位置を計算
    average_pos = mathutils.Vector(sum(selected_verts, mathutils.Vector()) / len(selected_verts))

    return average_pos


def calculate_max_width():
    # メッシュを更新
    bpy.context.edit_object.update_from_editmode()
    # アクティブなオブジェクトを取得
    obj = bpy.context.active_object

    # 選択された頂点の位置を取得
    selected_verts = [v.co for v in obj.data.vertices if v.select]

    # 選択された頂点の最大の幅を算出
    max_width = 0.0
    for i in range(len(selected_verts)):
        for j in range(i+1, len(selected_verts)):
            width = (selected_verts[i] - selected_verts[j]).length
            if width > max_width:
                max_width = width

    # 最大の幅を出力
    # print("Max Width:", max_width)
    return max_width




class AddPrimitiveOperator(bpy.types.Operator):
    bl_idname = "object.add_primitive"
    bl_label = "Add Primitive"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    
    primitive_types = [
        ("CIRCLE", "Circle", "Add Circle"),
        ("CONE", "Cone", "Add Cone"),
        ("CUBE", "Cube", "Add Cube"),
#        ("CUBE_GIZMO", "Cube Gizmo", "Add Cube Gizmo"),
        ("CYLINDER", "Cylinder", "Add Cylinder"),
        ("GRID", "Grid", "Add Grid"),
        ("ICO_SPHERE", "Ico Sphere", "Add Ico Sphere"),
        ("POINT", "Add Point", "Add Point"),
        ("PLANE", "Plane", "Add Plane"),
        ("TORUS", "Torus", "Add Torus"),
        ("UV_SPHERE", "UV Sphere", "Add UV Sphere"),
    ]
    
    primitive_type : EnumProperty(
        name="Primitive Type",
        items=primitive_types,
        default="CIRCLE"
    ) # type: ignore
    
    location : FloatVectorProperty(
        name="Location",
        default=(0, 0, 0),
        subtype='TRANSLATION',
        size=3
    ) # type: ignore
    
    rotation : FloatVectorProperty(
        name="Rotation",
        default=(0, 0, 0),
        subtype='EULER',
    ) # type: ignore
    
    scale : FloatVectorProperty(
        name="Scale",
        default=(1, 1, 1),
        subtype='XYZ',
    ) # type: ignore
        
    use_average_pos: bpy.props.BoolProperty(
        name="Use Average Position",
        description="Place the average position",
        default=True
    ) # type: ignore
    use_select_rot: bpy.props.BoolProperty(
        name="Use select rotation",
        description="Use select rotation",
        default=True
    ) # type: ignore

    remember_and_reselect_faces: bpy.props.BoolProperty(
        name="remember and reselect faces",
        description="remember and reselect faces",
        default=False
    ) # type: ignore


    width: bpy.props.BoolProperty(
        name="Auto Scale",
        description="Desired width for the selected vertices",
        default=True,

    ) # type: ignore
    
    @classmethod
    def get_face_rotation(cls):
        # Select the active object
        obj = bpy.context.object

        # Switch to edit mode while maintaining the mesh data
        bpy.ops.object.mode_set(mode='EDIT')

        # Update the mesh data
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.data.update()

        # Switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Create a new bmesh object from the object's mesh data
        cls.bm = bmesh.new()
        cls.bm.from_mesh(obj.data)
        cls.me = obj.data

        # Get a list of selected faces in the bmesh
        selected_faces = [f for f in cls.bm.faces if f.select]

        if len(selected_faces) > 0:
            # Get the first selected face
            vectors = []
            for face in selected_faces:


                # Calculate the center location of the face
                face_location = face.calc_center_median()

                # Convert the face location to world space
                loc_world_space = obj.matrix_world @ Vector(face_location)

                # Define a vector pointing in the positive Z direction
                z = Vector((0, 0, 1))

                # Calculate the rotation difference between the face normal and the positive Z direction
                rot = z.rotation_difference(face.normal).to_euler()
                vectors.append(rot)

                # print("Face location:", loc_world_space)
                # print(rot)
                # face.select = True	 
        
            average_vector = calculate_average_euler(vectors)
    

        return average_vector,selected_faces
            
    def remember_and_reselect_face(self,selected_faces):
        face_index = []
        for face in selected_faces:
            print(face.index)
            face_index.append(face.index)
            face.select = True
            self.bm.verts.index_update()

        mesh = bpy.context.object.data
        bm = bmesh.from_edit_mesh(mesh)

        for face in bm.faces:
            if face.index in face_index:
                face.select = True

        bmesh.update_edit_mesh(mesh)

    def execute(self, context):
        # オブジェクトの位置を取得
        obj = context.object
        if self.use_average_pos !=True:
            current_location = obj.location
        else:
            average_position = calculate_average_position()
            current_location = average_position

        if self.width ==True:
            max_width =calculate_max_width()
            # scaleベクターにmax_widthの値を反映
            scale_factor =  max_width/2
            self.scale = (scale_factor, scale_factor, scale_factor)

        if self.use_select_rot:
            self.rotation,selected_faces = self.get_face_rotation()


        # プロパティのベクターをベクターに変換
        
        # オブジェクトのグローバルマトリックスを取得する
        matrix = obj.matrix_world

        # オブジェクトのベクター位置をグローバルマトリックスの位置に合わせる
        # vector = obj.location
        new_vector = matrix @ current_location
        location_vector = Vector(self.location)
        
        # 新しい位置を計算
        new_location = new_vector + location_vector
        # bpy.ops.mesh.primitive_circle_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

        # 選択されたプリミティブの種類に応じて追加するメッシュを決定
        if self.primitive_type == "CIRCLE":
            bpy.ops.mesh.primitive_circle_add(
                vertices=32, 
                radius=self.scale[0], 
                fill_type='NOTHING', 
                calc_uvs=True,
                enter_editmode=False, 
                align='WORLD', 
                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                # scale=self.scale
            )
        elif self.primitive_type == "CONE":
            bpy.ops.mesh.primitive_cone_add(
                vertices=32, 
                radius1=1, 
                radius2=0, 
                depth=2, 
                end_fill_type='NOTHING', 
                calc_uvs=True,
                enter_editmode=False, 
                align='WORLD', 
                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                scale=self.scale
            )
        elif self.primitive_type == "CUBE":
            bpy.ops.mesh.primitive_cube_add(

                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                scale=self.scale
                )
        elif self.primitive_type == "POINT":
            bpy.ops.mesh.primitive_cube_add(

                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                scale=self.scale
                )
            bpy.ops.mesh.merge(type='CENTER', uvs=False)
            
        elif self.primitive_type == "PLANE":
            bpy.ops.mesh.primitive_plane_add(

                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                size=self.scale[0]*2
            )
        elif self.primitive_type == "CYLINDER":
            bpy.ops.mesh.primitive_cylinder_add(

                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                scale=self.scale
            )

        elif self.primitive_type == "UV_SPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(

                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                scale=self.scale
            )
            
        elif self.primitive_type == "ICO_SPHERE":
            bpy.ops.mesh.primitive_ico_sphere_add(

                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                scale=self.scale
            )
            
        elif self.primitive_type == "GRID":
            bpy.ops.mesh.primitive_grid_add(

                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
                size=self.scale[0]
            )

            
        elif self.primitive_type == "TORUS":
            bpy.ops.mesh.primitive_torus_add(
                major_radius=self.scale[0],

                location=new_location, 
                rotation=(self.rotation[0], self.rotation[1], self.rotation[2]), 
#                scale=self.scale
            )


        # 他のプリミティブの追加処理も同様に追加
        if self.remember_and_reselect_faces:
            self.remember_and_reselect_face(selected_faces)

             
        return {'FINISHED'}