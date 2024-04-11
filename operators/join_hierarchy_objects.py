import bpy

class OBJECT_OT_JoinHierarchyObjects(bpy.types.Operator):
    bl_idname = "object.join_hierarchy_objects"
    bl_label = "Join Hierarchy Objects"
    bl_description = "Joins selected objects and their hierarchy"
    bl_options = {'REGISTER', 'UNDO'}


    hide_original_objects: bpy.props.BoolProperty(
        name="Hide Original Objects",
        description="Hide the original objects after joining",
        default=True
    )
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects
    
    def execute(self, context):
        seleobj = context.selected_objects
        hierarchy = GetHierarchyChildren()
        hierarchy.join_hierarchy_objects(seleobj, self.hide_original_objects)
        return {'FINISHED'}

class GetHierarchyChildren:
    
    def get_hierarchy_children(self, obj):
        children = []
        for child in obj.children:
            children.append(child)
            children.extend(self.get_hierarchy_children(child))
        return children
    
    def make_hierarchy_dict(self):
        selected_objs = bpy.context.selected_objects
        hierarchy_dict = {}
        parent_objs = set()
        
        for obj in selected_objs:
            parent_obj = obj
            while parent_obj.parent:
                parent_obj = parent_obj.parent
            parent_objs.add(parent_obj)
        
        for parent_obj in parent_objs:
            children = []
            for obj in selected_objs:
                if obj.parent == parent_obj:
                    children.append(obj)
                    children.extend(self.get_hierarchy_children(obj))
            hierarchy_dict[parent_obj] = children
        return hierarchy_dict
    
    def make_hierarchy_obj_lists(self):
        hierarchy_dict = self.make_hierarchy_dict()
        hierarchy_obj_lists = []
        for parent_obj, children in hierarchy_dict.items():
            obj_list = [parent_obj]
            for child in children:
                if child not in hierarchy_dict:
                    obj_list.append(child)
            hierarchy_obj_lists.append(obj_list)
        return hierarchy_obj_lists
    
    def join_hierarchy_objects(self, seleobj, hide_original_objects):
        hierarchy_obj_lists = self.make_hierarchy_obj_lists()
        copy_list = []
        
        for index, obj_list in enumerate(hierarchy_obj_lists, start=1):
            key_name = obj_list[0]
            
            bpy.ops.object.select_all(action='DESELECT')
            
            for obj in obj_list:
                if obj in seleobj:
                    copy_obj = obj.copy()
                    copy_obj.name = key_name.name + f"_join_obj"
                    copy_obj.data.name = key_name.name + f"_join_obj"
                    
                    bpy.context.collection.objects.link(copy_obj)
                    copy_obj.select_set(True)
                    obj.select_set(False)
                    bpy.context.view_layer.objects.active = copy_obj
                    bpy.ops.object.convert(target='MESH')
            
            bpy.ops.object.join()
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            
            for obj in bpy.context.selected_objects:
                copy_list.append(obj)
        
        for obj in copy_list:
            obj.select_set(True)
        
        if hide_original_objects:
            for obj in seleobj:
                obj.hide_set(True)
        
        return copy_list
