import bpy
from mathutils import Vector


def new_GeometryNodes_group(obj):
    ''' Create a new empty node group that can be used
        in a GeometryNodes modifier.
    '''
    node_group = bpy.data.node_groups.new('GeometryNodes', 'GeometryNodeTree')
    
    inNode = node_group.nodes.new('NodeGroupInput')
    GeometryNodeObjectInfo = node_group.nodes.new('GeometryNodeObjectInfo')
    GeometryNodeJoinGeometry = node_group.nodes.new('GeometryNodeJoinGeometry')
    GeometryNodeTransform = node_group.nodes.new('GeometryNodeTransform')
    GeometryNodeSetPosition = node_group.nodes.new('GeometryNodeSetPosition')
    
    node_group.outputs.new('NodeSocketGeometry', 'Geometry')
    outNode = node_group.nodes.new('NodeGroupOutput')
    node_group.inputs.new('NodeSocketGeometry', 'Geometry')
    
    node_group.inputs.new('NodeSocketObject', 'JOINOBJ')

    # LINK
    node_group.links.new(inNode.outputs['Geometry'], GeometryNodeJoinGeometry.inputs['Geometry'])
    node_group.links.new(GeometryNodeJoinGeometry.outputs['Geometry'], GeometryNodeSetPosition.inputs['Geometry'])
    node_group.links.new(GeometryNodeSetPosition.outputs['Geometry'], outNode.inputs['Geometry'])

    # LINK JONGT OBJECT
    node_group.links.new(inNode.outputs['JOINOBJ'], GeometryNodeObjectInfo.inputs['Object'])
    node_group.links.new(GeometryNodeObjectInfo.outputs['Geometry'], GeometryNodeTransform.inputs['Geometry'])
    node_group.links.new(GeometryNodeObjectInfo.outputs['Geometry'], GeometryNodeTransform.inputs['Geometry'])
    node_group.links.new(GeometryNodeObjectInfo.outputs['Location'], GeometryNodeTransform.inputs['Translation'])
    node_group.links.new(GeometryNodeObjectInfo.outputs['Scale'], GeometryNodeTransform.inputs['Scale'])
    node_group.links.new(GeometryNodeObjectInfo.outputs['Rotation'], GeometryNodeTransform.inputs['Rotation'])
    node_group.links.new(GeometryNodeTransform.outputs['Geometry'], GeometryNodeJoinGeometry.inputs['Geometry'])
    
    inNode.location = Vector((-1.5*inNode.width, 0))
    outNode.location = Vector((3.5*outNode.width, 0))
    GeometryNodeSetPosition.location = Vector((1.5*outNode.width, 0))
    GeometryNodeObjectInfo.location = Vector((0.1*inNode.width, -400))
    GeometryNodeTransform.location = Vector((1.5*GeometryNodeObjectInfo.width, -400))
    
    return node_group


class GeometryNodesOperator(bpy.types.Operator):
    bl_idname = "object.geometry_nodes_operator"
    bl_label = "Geometry Nodes Operator"
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    scene_enum: bpy.props.EnumProperty(
        items=lambda self, context: [(s.name, s.name, s.name) for s in bpy.data.scenes],
        name="Scene",
        description="Select a scene"
    )

    hide_children: bpy.props.BoolProperty(
        name="Hide Children",
        default=False
    )

    wire_children: bpy.props.BoolProperty(
        name="Wire Children",
        default=False
    )
    
    use_collection: bpy.props.BoolProperty(
        name="Use Collection",
        default=False
    )

    location_cursor : bpy.props.BoolProperty(
        name="Location to the cursor",
        description="Location to the cursor",
        default=False
    )
    duplicate_to_collection : bpy.props.BoolProperty(
        name="Duplicate to Collection",
        description="Duplicate selected objects to a collection",
        default=True
    )
    scene_name: bpy.props.StringProperty(name="Scene Name", default="New Scene")

    use_custom_name: bpy.props.BoolProperty(name="Use Custom Scene(Object Copy)", default=False)

    select_scene: bpy.props.BoolProperty(name="Select Scene", default=True)

    def draw(self,context):
        self.layout.label(text="Scene Setting")
        self.layout.prop(self,"use_custom_name")
        if self.use_custom_name:
            self.layout.prop(self,"select_scene")

            if self.select_scene:
                self.layout.prop(self,"scene_enum")
            else:
                self.layout.prop(self,"scene_name")

        self.layout.label(text="Object Setting")
        self.layout.prop(self,"hide_children")
        self.layout.prop(self,"wire_children")
        self.layout.prop(self,"location_cursor")

        self.layout.label(text="Collection Setting")

        self.layout.prop(self,"use_collection")

        if self.use_collection:
            self.layout.prop(self,"duplicate_to_collection")

    # @classmethod
    # def poll(cls, context):
        # return context.object is not None and context.object.type == 'MESH'
    

    def new_scene_copyobj(self):
        if not self.select_scene:
            # 新しいシーンを作成
            new_scene = bpy.data.scenes.new(self.scene_name)
        else:
            new_scene = bpy.data.scenes[self.scene_enum]

        # # 新しいコレクションを作成
        new_collection = bpy.data.collections.new(self.activeobject.name)
        new_scene.collection.children.link(new_collection)

        # 選択したオブジェクトを取得
        selected_objects = bpy.context.selected_objects

        # 選択したオブジェクトを新しいコレクションにリンク
        for obj in selected_objects:
            new_obj = obj.copy()
            new_obj.name = obj.name + "_"
            new_obj.animation_data_clear()
            new_collection.objects.link(new_obj)
            #同じシーンにコピーする場合
            if new_scene == bpy.context.scene:
                obj.select_set(False)


        # オブジェクトをリンクするシーンを指定
        bpy.context.window.scene = new_scene

    def execute(self, context):
        
        active_object = context.object
        if self.location_cursor:
            active_location = bpy.context.scene.cursor.location
        else:
            active_location = active_object.location

        if self.use_custom_name:
            self.activeobject = active_object
            self.new_scene_copyobj()

        if self.use_collection:
            # make collection
            new_collection = bpy.data.collections.new(active_object.name + '_join')
            bpy.context.scene.collection.children.link(new_collection)
            new_collection.color_tag = 'COLOR_02'


        # Create new object and mesh
        vertices = [(0, 0, 0)]
        edges = []
        faces = []
        new_mesh = bpy.data.meshes.new('new_mesh')
        new_mesh.from_pydata(vertices, edges, faces)
        new_mesh.update()
        new_object = bpy.data.objects.new(active_object.name + '_join', new_mesh)
        
        # Add object to scene collection
        bpy.context.collection.objects.link(new_object)
        new_object.select_set(True)
        bpy.context.view_layer.objects.active = new_object
        
        # Create Geometry Nodes group for each selected object
        for obj in bpy.context.selected_objects:
            if obj == bpy.context.object:
                continue
            
            node_group = new_GeometryNodes_group(obj)
            mod = new_object.modifiers.new('GeometryNodes', 'NODES')
            mod.node_group = node_group
            new_object.modifiers[-1]['Input_2'] = obj
            if self.wire_children:
                obj.display_type = 'WIRE'

            if self.hide_children:
                obj.hide_set(True)
            
            if self.use_collection:
                # add object to scene collection
                if not self.duplicate_to_collection:
                    for collection in obj.users_collection:
                        collection.objects.unlink(obj)
                new_collection.objects.link(obj)
            
        # Set position offset for the last modifier
        bpy.context.object.modifiers[-1].node_group.nodes['Set Position'].inputs['Offset'].default_value = active_location * -1
        
        # Set active object's location
        bpy.context.object.location = active_location
        
        # Parent the new object to the active object
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        # self.scene_name = bpy.context.object.name
        return context.window_manager.invoke_props_dialog(self)