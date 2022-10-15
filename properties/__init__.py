# プロパティをシーンに登録する場合は、
# クラスをレジスターの項目も登録してあげる。	bpy.types.Scene.####使用したシーンの名前 = bpy.props.PointerProperty(type=クラス名)
# 削除も忘れずに	del bpy.types.Scene.####使用したシーンの名前



import bpy

if "bpy" in locals():
	import importlib
	reloadable_modules = [

    "pieeditpropertyGroup",

	]
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])




from .pieeditpropertyGroup import *


classes = (

MyEDITPIEPropertyGroup,

)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
	bpy.types.Scene.myedit_property_group = bpy.props.PointerProperty(type=MyEDITPIEPropertyGroup)



def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.myedit_property_group



if __name__ == "__main__":
	register()
