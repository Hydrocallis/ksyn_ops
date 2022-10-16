# プロパティをシーンに登録する場合は、
# クラスをレジスターの項目も登録してあげる。	bpy.types.Scene.####使用したシーンの名前 = bpy.props.PointerProperty(type=クラス名)
# 削除も忘れずに	del bpy.types.Scene.####使用したシーンの名前



import bpy

if "bpy" in locals():
	import importlib
	reloadable_modules = [

    "simplefbxexport_op_fbx_export",
    "simplefbxexport_panel",
    "simplefbxexoprt_propertyGroup",

	]
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])



from .simplefbxexport_op_fbx_export import *
from .simplefbxexport_panel import *
from .simplefbxexoprt_propertyGroup import *


classes = (

SIMPLEFBXECPORT_PropertyGroup,

SIMPLEFBXECPORT_OT_FbxExort,

SIMPLEFBXECPORT_PT_SETTINGFBXEXPORT,

)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
	bpy.types.Scene.simplefbxecport_propertygroup = bpy.props.PointerProperty(type=SIMPLEFBXECPORT_PropertyGroup)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.simplefbxecport_propertygroup


if __name__ == "__main__":
	register()
