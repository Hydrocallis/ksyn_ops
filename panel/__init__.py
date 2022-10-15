# panel init

import bpy

if "bpy" in locals():
	import importlib
	reloadable_modules = [
    "pie_panel_setting",
    "pie_panel_setting_op",

	]
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])


from .pie_panel_setting import *
from .pie_panel_setting_op import *


classes = (
PIE3D_PT_PIESETTING,
PIE3D_PT_PIESETTINGARM,
PIE3D_PT_PIESettiongOp,


)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
