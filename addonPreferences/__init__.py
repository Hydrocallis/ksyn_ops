# menu init

import bpy



if "bpy" in locals():
	import importlib
	reloadable_modules = [
    "piemenuaddonpreferences",	

	]
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])	

from .piemenuaddonpreferences import *
















classes = (
ExampleAddonPreferences,
)



def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	



def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)




if __name__ == "__main__":
	register()
