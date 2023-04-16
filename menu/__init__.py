import bpy



if "bpy" in locals():
	import importlib
	# ※１	
	reloadable_modules = [
		"botom_right_draw",	
		"left_draw",	
		"top_draw",	
		"top_left_draw",	
		"top_right_draw",	
		"bottom_draw",	
		#メニュー
		"pieviewmenu",	
	


	]
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])




from .pieviewmenu import PIE_MT_ViewNumpad



classes = (
	PIE_MT_ViewNumpad,
		)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
