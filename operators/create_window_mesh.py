import bpy,bmesh,math

from bpy.types import Context

def create_arch(radius, height, segments, arch,  depth,location_z):
    bpy.ops.object.select_all(action='DESELECT')
    # 新しいメッシュを作成
    mesh = bpy.data.meshes.new(name="ArchMesh")

    # メッシュのオブジェクトを作成
    obj = bpy.data.objects.new("Arch", mesh)
    scene = bpy.context.scene
    scene.collection.objects.link(obj)

    # メッシュをアクティブに設定
    obj.select_set(True)

    # メッシュを編集モードに変更
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')

    # bmeshを作成
    bm = bmesh.from_edit_mesh(mesh)

    # アーチの頂点とエッジを作成
    vertices = []
    edges = []

    for i in range(segments):
        angle = (math.pi / (segments - 1)) * i
        x = radius * math.cos(angle)
        y = 0
        z = radius * math.sin(angle)+location_z
        vertices.append(bm.verts.new((x, y, z)))

    for i in range(segments - 1):
        edges.append(bm.edges.new([vertices[i], vertices[i + 1]]))

    # アーチの側面の頂点とエッジを作成
    for i in range(segments):
        angle = (math.pi / (segments - 1)) * i
        x = radius * math.cos(angle) * arch
        y = 0
        z = radius * math.sin(angle) * arch+location_z
        vertices.append(bm.verts.new((x, y, z)))

    for i in range(segments - 1):
        edges.append(bm.edges.new([vertices[i + segments], vertices[i + segments + 1]]))

    # メッシュのフェースを作成
    faces = []

    for i in range(segments - 1):
        face = bm.faces.new([vertices[i], vertices[i + 1], vertices[i + segments + 1], vertices[i + segments]])
        faces.append(face)

    ## フェースを押し出す
    # メッシュのフェースを押し出す
    # フェースを押し出す
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip": False, "use_dissolve_ortho_edges": False, "mirror": False}, TRANSFORM_OT_translate={"value": (0, 0, -depth), "orient_type": 'NORMAL', "orient_matrix": ((-1, 0, 1.5114e-08), (-1.5114e-08, -0, -1), (0, -1, 0)), "orient_matrix_type": 'NORMAL', "constraint_axis": (False, False, True), "mirror": False, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_elements": {'INCREMENT'}, "use_snap_project": False, "snap_target": 'CLOSEST', "use_snap_self": True, "use_snap_edit": True, "use_snap_nonedit": True, "use_snap_selectable": False, "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "view2d_edge_pan": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})

    # bmeshを更新
    bmesh.update_edit_mesh(mesh)

    # メッシュをオブジェクトモードに変更
    bpy.ops.object.mode_set(mode='OBJECT')

    return obj

class WINDOW_CREATE_objectPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_hello"
    bl_label = "Create Bars"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "KSYN"

    def draw(self, context):
        self.layout.operator("object.create_bars")

class ArchPropaty:

    create_arch : bpy.props.BoolProperty(name="Create Arch")

    segments: bpy.props.IntProperty(
        name="Segments",
        default=32,
        min=4,
        max=64,
        description="The number of segments to divide the object"
    )

    arch: bpy.props.FloatProperty(
        name="Arch",
        default=0.8,
        min=0.0,
        max=1.0,
        description="The degree of arch of the object"
    )

    depth: bpy.props.FloatProperty(
        name="Depth",
        default=0.025,
        description="The depth of the object"
    )

class WINDOW_CREATE_CreateBars(bpy.types.Operator,ArchPropaty):
    bl_idname = "object.create_bars"
    bl_label = "Create Bars"
    bl_description = "Create bar meshes"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    num_vertical_bars: bpy.props.IntProperty(name="Vertical Bars", default=5)
    num_horizontal_bars: bpy.props.IntProperty(name="Horizontal Bars", default=8)
    width: bpy.props.FloatProperty(name="Width", default=0.50)
    height: bpy.props.FloatProperty(name="Height", default=1.0)
    thickness: bpy.props.FloatProperty(name="Thickness", default=0.01)
    frame_thickness: bpy.props.FloatProperty(name="Frame Thickness", default=0.015)
    thickness_difference: bpy.props.FloatProperty(name="Frame Thickness difference", default=0.001)

    width_of_outer_frame: bpy.props.FloatProperty(name="Width of outer frame", default=0.025)
    depth_of_outer_frame: bpy.props.FloatProperty(name="Depth of outer frame", default=0.025)
    create_mesh_cylinder : bpy.props.BoolProperty(name="create_mesh_cylinder")
    look_edit_mode : bpy.props.BoolProperty(name="Edit Mode")

    def draw(self, context: Context):

        self.layout.label(text="Arch")
        arch_box=self.layout.box()
        arch_box.prop(self,"create_arch")
        arch_box.prop(self,"segments")
        arch_box.prop(self,"arch")
        arch_box.prop(self,"depth")

        self.layout.label(text="Windos")
        window_box=self.layout.box()
        window_box.prop(self,"num_vertical_bars")
        window_box.prop(self,"num_horizontal_bars")
        window_box.prop(self,"width")
        window_box.prop(self,"height")
        window_box.prop(self,"thickness")
        window_box.prop(self,"frame_thickness")

        self.layout.label(text="Frame")
        frame_box=self.layout.box()
        frame_box.prop(self,"width_of_outer_frame")
        frame_box.prop(self,"depth_of_outer_frame")
        frame_box.prop(self,"create_mesh_cylinder")
        frame_box.prop(self,"look_edit_mode")



    def execute(self, context):
        mesh_list = []

        # Function to create mesh
        def create_mesh(name, dimensions, location):
            bpy.ops.mesh.primitive_cube_add(size=1, location=location)
            mesh_list.append(context.object)
            mesh = context.object
            mesh.name = name
            mesh.scale = dimensions
            return mesh
        
                # Function to create mesh
        def create_mesh_cylinder(name, dimensions, location):
            bpy.ops.mesh.primitive_cylinder_add(location=location, rotation=(0.0, 1.5708, 0.0),scale=(0.5,0.5,0.5))
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            mesh_list.append(context.object)
            mesh = context.object
            mesh.name = name
            mesh.scale = dimensions
           
            
            return mesh
        def create_mesh_cylinder_horizontal(name, dimensions, location):
            bpy.ops.mesh.primitive_cylinder_add(location=location, rotation=(0.0, 0, 0.0),scale=(0.5,0.5,0.5))
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
            mesh_list.append(context.object)
            mesh = context.object
            mesh.name = name
            mesh.scale = dimensions
           
            
            return mesh


        # Create vertical bars
        
        for i in range(self.num_vertical_bars - 1):
            z = self.height / self.num_vertical_bars
            
            if self.create_mesh_cylinder:
                create_mesh_cylinder(f"Mesh_vertical_{i}", 
                    
                    (self.width , self.frame_thickness+self.thickness_difference, self.thickness), 
                    (self.width * 0.5, 0, i * z + z))

      
            else:
                create_mesh(f"Mesh_vertical_{i}", 
                            (self.width , self.frame_thickness+self.thickness_difference, self.thickness), 
                            (self.width * 0.5, 0, i * z + z))

        # Create horizontal bars
        for i in range(self.num_horizontal_bars - 1):
            if self.create_mesh_cylinder:
                x = self.width / self.num_horizontal_bars
                create_mesh_cylinder_horizontal(f"Mesh_horizontal_{i}", 
                            (self.thickness, self.frame_thickness, self.height), 
                            (i * x + x, 0, self.height * 0.5))
        

            else:

                x = self.width / self.num_horizontal_bars
                create_mesh(f"Mesh_horizontal_{i}", 
                            (self.thickness, self.frame_thickness, self.height), 
                            (i * x + x, 0, self.height * 0.5))
        
        # Create outer frame
  
        create_mesh("Outer_Mesh_Top", (self.width , self.depth_of_outer_frame, self.width_of_outer_frame), 
                   (self.width * 0.5, 0, self.height+self.width_of_outer_frame/2))  
        # Top
        create_mesh("Outer_Mesh_Left_Right", (self.width_of_outer_frame,  self.depth_of_outer_frame, 
                   self.height + self.width_of_outer_frame*2), 
                   (0-self.width_of_outer_frame/2, 0, self.height * 0.5))  
        # Left
        create_mesh("Outer_Mesh_Left_Right", (self.width_of_outer_frame,  self.depth_of_outer_frame,  
                   self.height +self.width_of_outer_frame*2), 
                   (self.width+self.width_of_outer_frame/2, 0, self.height * 0.5))  
        # Right
        
        create_mesh("Outer_Mesh_Bottom", (self.width , self.depth_of_outer_frame,self.width_of_outer_frame), 
                   (self.width * 0.5, 0, 0-self.width_of_outer_frame/2))  
        # Bottom
        
        
        
        if self.create_arch:
            # create arch
            radius = (self.width+self.width_of_outer_frame*2)/2
            height = 0
            segments = self.segments
            arch =self.arch
            depth = self.depth
            arch_obj = create_arch(radius, height, segments, arch,  depth,self.height+self.width_of_outer_frame)
            mesh_list.append(arch_obj)
            arch_obj.location[0]=self.width/2.0
            arch_obj.location[1]=0-depth/2
            
        
        
        # Join the meshes
        for obj in mesh_list:
            obj.select_set(True)

        bpy.ops.object.join()
        bpy.context.object.location.x=0
        
        if self.look_edit_mode:
            bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}
