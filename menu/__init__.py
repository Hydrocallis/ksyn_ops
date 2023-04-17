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
		"bottom_left_draw",	
		"right_draw",	
		#メニュー
		"pieviewmenu",	
    	"instansmenu",

	


	]
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])




from .pieviewmenu import PIE_MT_ViewNumpad
from .instansmenu import PIE_MT_InstansMenu,PIE_MT_InstansMenu2



classes = (
	PIE_MT_ViewNumpad,
    PIE_MT_InstansMenu,
    PIE_MT_InstansMenu2,

		)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()
