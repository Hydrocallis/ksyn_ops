import bpy



class SIMPLEFBXECPORT_OT_Add_Operator(bpy.types.Operator):

    bl_idname = "simplefbxexport.add"
    bl_label = "Add"
    
    fbxfilenameset_date : bpy.props.StringProperty(
        name="file name"
    )


    def execute(self, context):
        
        filenameset = context.scene.fbxfilenameset_collection.add()
        filenameset.fbxfilenameset_text = self.fbxfilenameset_date


        return {'FINISHED'}
 
    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)   


class SIMPLEFBXECPORT_OT_Remove_Operator(bpy.types.Operator):

    bl_idname = "simplefbxexport.remove"
    bl_label = "Remove"


    def execute(self, context):
        
        if len(context.scene.fbxfilenameset_collection) > 0:
            context.scene.fbxfilenameset_collection.remove(0)


        return {'FINISHED'}


class SIMPLEFBXECPORT_PG_filenameset(bpy.types.PropertyGroup):
    fbxfilenameset_text: bpy.props.StringProperty()
    

# class SIMPLEFBXECPORT_PT_Panel(bpy.types.Panel):

#     bl_label = "Panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = "simplefbxexport"

#     def draw(self, context):
#         layout = self.layout
        
#         row = layout.row(align=True)
#         row.prop(context.scene, "filenameset", text="")
#         row.operator("simplefbxexport.add", text="", icon="ADD")
#         row.operator("simplefbxexport.remove", text="", icon="REMOVE")


