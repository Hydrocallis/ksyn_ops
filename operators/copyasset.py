import bpy, os , sys, pathlib
from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )

from bpy.props import (
                        StringProperty, 
                        IntProperty, 
                        FloatProperty, 
                        EnumProperty, 
                        BoolProperty,
                        PointerProperty,
                        FloatVectorProperty,
                        StringProperty
                        )

class PIE3D_OT_CopyAsset(Operator):
    bl_idname = "object.copyasset_operator"
    bl_label = "人ものさし"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    test_items = [
    ("1", "座り158ｃｍ女性", "", 1),
    ("2", "立ち158ｃｍ女性", "", 2),
        ]

    asset_enum : EnumProperty(
        items=test_items,
        name='タイプ',

        )

    def execute(self, context):
        p_file = pathlib.Path(__file__)
        filepath=  p_file.parents[1].joinpath("asset", 'asset_001.blend')

        if self.asset_enum == "1":
            coll_name = "monosashi_suwari_158"
        elif self.asset_enum == "2":
            coll_name = "monosashi_tachi_158"

        link = False

        print('###0-0###file full path', __file__)
        print('###0-1###scriptname', p_file.name)
        print('###0-2###asset filepath',filepath)
        print('###0-3###asset exists', filepath.exists())
        print('###0-0###', filepath)
        # link all collections starting with 'MyCollection'
        with bpy.data.libraries.load(str(filepath), link=link) as (data_from, data_to):
            data_to.collections = [c for c in data_from.collections if c.startswith(coll_name)]
        # link collection to scene collection
        for coll in data_to.collections:
            if coll is not None:
                # bpy.context.scene.collection.children.link(coll)
                bpy.ops.object.collection_instance_add(collection=coll.name, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
  
        return {'FINISHED'}
