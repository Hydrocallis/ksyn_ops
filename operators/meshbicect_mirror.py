

import bpy,sys

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng

class SelectionMemory:
    def __init__(self, vg_name="SelectionMemory"):
        self.vg_name = vg_name
    
    def store_selected_verts(self):
        # 選択中のメッシュオブジェクトを取得
        obj = bpy.context.object

        # 頂点グループを作成もしくは取得
        if self.vg_name not in obj.vertex_groups:
            obj.vertex_groups.new(name=self.vg_name)

        # 選択中の頂点を頂点グループに割り当てる
        bpy.ops.object.vertex_group_assign()

    def select_from_memory(self):
        if self.is_memory_exists():
            # 頂点グループに属する頂点を再選択する
            obj = bpy.context.object
            obj.vertex_groups.active = obj.vertex_groups[self.vg_name]
            bpy.ops.object.vertex_group_select()

    def delete_selection_memory_group(self):
        # 選択記憶用の頂点グループ名
        if self.is_memory_exists():
            # 頂点グループを削除する
            obj = bpy.context.object
            vg_index = obj.vertex_groups[self.vg_name].index
            obj.vertex_groups.remove(obj.vertex_groups[vg_index])
    
    def is_memory_exists(self):
        # 選択記憶用の頂点グループが存在するかどうかを返す
        return self.vg_name in bpy.context.object.vertex_groups
   
class option:
   # testプロパティ
    
    myfloatvector:bpy.props.FloatVectorProperty(
        name='Constant Offset', 
        description='', 
        default=(0.0, 0.0, 0),
        subtype="XYZ_LENGTH"
        )
        
    myboolvector : bpy.props.BoolVectorProperty(
        name= get_translang('Execution','実行'),
        default=(1, 0, 0),

        )
#      

    Fill : bpy.props.BoolProperty(
        name= "Fill",
        default=0
        )
       
class MeshEditingTools(option):
     
    def bisect(self, plane_co, plane_no):
        loc = bpy.context.object.location
        
        bpy.ops.mesh.select_all(action='SELECT')

        bpy.ops.mesh.bisect(
            plane_co=(
                plane_co[0] + loc[0],
                plane_co[1] + loc[1],
                plane_co[2] + loc[2]),
                
            plane_no=(
                int(plane_no[0]),
                int(plane_no[1]),
                int(plane_no[2])),
                
            clear_inner=False, 
            clear_outer=True
        )
        
        if self.Fill:
            bpy.ops.mesh.edge_face_add()

    def side_bicect(self):
        
        self.bisect(self.myfloatvector, self.myboolvector)

    def mirror(self):
        self.bisect(
            (
                -self.myfloatvector[0],
                -self.myfloatvector[1],
                -self.myfloatvector[2]
            ),
            (
                -int(self.myboolvector[0]),
                -int(self.myboolvector[1]),
                -int(self.myboolvector[2])
            )
        )
        
        if self.Fill:
            bpy.ops.mesh.edge_face_add()

class bicect_mirror(bpy.types.Operator,SelectionMemory,MeshEditingTools):
    bl_idname = 'mesh.mesh_ot_bicect_mirror'
    bl_label = get_translang('Mesh bicect mirror','二等分ミラー')
    bl_description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}/n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n ' 
    bl_options = {'REGISTER', 'UNDO','PRESET'}

    mirror_option : bpy.props.BoolProperty(
        name= "Mirror",
        default=False
        )
    
    sidebicect : bpy.props.BoolProperty(
        name= get_translang('Side Bicect','二等分'),
        default=True
        )
        
        
    def execute(self, context):

        if self.sidebicect ==True:
            self.side_bicect()
        if self.mirror_option== True:
            self.store_selected_verts()
            self.mirror()
            self.select_from_memory()
            self.delete_selection_memory_group()

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None


    def draw(self,context):
        layout = self.layout
        layout.prop(self, "sidebicect" )
        grifl=layout.grid_flow(row_major=True, columns=3, even_columns=False, even_rows=False, align=True)
        grifl.prop(self, "myfloatvector")
        grifl.prop(self, "myboolvector" ,)
        layout.prop(self, "Fill" )
        layout.prop(self, "mirror_option")
        


    
        