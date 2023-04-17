# panel init

import bpy

if "bpy" in locals():
	import importlib
	reloadable_modules = [
    "pie_panel_setting",
    "panel_simpleobject",


	]
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])


from .pie_panel_setting import PIE3D_PT_PIESETTING1,PIE3D_PT_PIESETTING2,PIE3D_PT_PIESETTING3,SIMPLEOBJECT_PT_PANEL




classes = (
PIE3D_PT_PIESETTING1,
SIMPLEOBJECT_PT_PANEL,
PIE3D_PT_PIESETTING2,
PIE3D_PT_PIESETTING3,

)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
