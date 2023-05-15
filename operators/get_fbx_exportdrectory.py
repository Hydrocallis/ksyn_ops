import bpy, os , sys
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )
class GetFbxInformation(Operator):
        bl_idname = 'object.getfbxinformation'
        bl_label = 'getfbxinformation'
        # 自身のクラスの呼び出しにはSYSモジュールが必要
        bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
        
        def execute(self, context):
            props = context.scene.myedit_property_group
            blend_file_path = bpy.data.filepath
            blend_directory = os.path.dirname(blend_file_path)
            

            home = os.getenv('USERPROFILE')
            desktop_dir = os.path.join(home, 'デスクトップ')
            # ワンドライブがあるかどうか念のためチェックする
            if os.path.exists(desktop_dir) != True:
                desktop_dir = os.path.join(home, "onedrive", 'デスクトップ')


            blender_fbxfilename = bpy.path.basename(bpy.context.blend_data.filepath).replace(".blend","")
                       

            if blend_directory != "":
                props.workspace_path = blend_directory
            else:
                props.workspace_path = desktop_dir

            props.fbx_filename = blender_fbxfilename

            print('###workspae path is ',props.workspace_path)
            print('###blender file name is ',blender_fbxfilename)


            return {'FINISHED'}