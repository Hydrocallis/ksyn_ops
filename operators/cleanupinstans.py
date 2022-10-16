import bpy, os , sys
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )
class PIE3D_OT_cleanupinstans(Operator):
        bl_idname = 'object.cleanupinstans_operator'
        bl_label = 'cleanupinstans_operator'
        # 自身のクラスの呼び出しにはSYSモジュールが必要
        bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
        
  
        @classmethod
        def poll(self, context):
            
            return True
                        
        
        def execute(self, context):

            # 全体のコレクションリスト
            allcollist = [i.name for i in bpy.data.collections]
            # 削除するコレクション一覧
            collist = [s for s in allcollist if '_INSTANS' in s]
            # MIRRORのみ抽出する
            filllist = [s for s in allcollist if 'MIRROR_' in s]
            instans_filllist = [s for s in allcollist if 'INSTANS_OB' in s]
            # インスタンスのリストと合体
            pulselist = collist + filllist + instans_filllist

            # コレクションインスタンスが入るリスト
            collists= []

            # コレクションのインスタンスリストを作成
            for get_col in pulselist:
                try:
                    collists.append(bpy.data.collections.get(get_col))
                except AttributeError:
                    pass

            # コレクション内のオブジェクトを削除していく
            for cols in collists:
                try:
                    for obj in cols.objects:
                        bpy.data.objects.remove(obj, do_unlink=True)
                except AttributeError:
                    pass
                    
            # コレクションを削除していく
            for i in collists:
                try:
                    bpy.data.collections.remove(i)
                except TypeError:
                    pass
            
            return {'FINISHED'}