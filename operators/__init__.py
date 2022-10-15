# operators init

"""
❏❏❏手順❏❏❏
１、※１のlocasの中にリロード用のスクリプト名を入力
２，※２読み込むモジュールの中にスクリプト名を入力
３，※３読み込むクラスを入力

"""

import bpy

if "bpy" in locals():
	import importlib
	# ※１	
	reloadable_modules = [
    "PiePropsSetting",	
    "uvgridmat_add",	
    "uv_unwrap",	
    "uv_map_deletechange",	
    "weightpaint_value_change",	
    "material_delete",	
    "get_fbx_exportdrectory",	
    "objectinstans",	
    "cleanupinstans",	
    "objectinstansmirror",	
    "shadingchange",	
    "copyasset",	
    "boolobject",	
    "uv_selmirseam",	
    "mesh_emptyverdel",	
    "uv_seleobjsmartuv",	
    "look_for_no_geometry",	


	]
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])

# ※２
from .PiePropsSetting import *
from .uvgridmat_add import *
from .uv_unwrap import *
from .uv_map_deletechange import *
from .weightpaint_value_change import *
from .material_delete import *
from .get_fbx_exportdrectory import *
from .objectinstans import *
from .cleanupinstans import *
from .objectinstansmirror import *
from .shadingchange import *
from .copyasset import *
from .boolobject import *
from .uv_selmirseam import *
from .mesh_emptyverdel import *
from .uv_seleobjsmartuv import *
from .look_for_no_geometry import *


# ※３
classes = (
PIE3D_OT_GetFbxInformation,
PIE3D_OT_PiePropsSetting,
PIE3D_OT_UvGridMat,
PIE3D_OT_uv_Unwrap,
PIE3D_OT_UvMapDeleteChange,
PIE3D_OT_weightpaint_value_chnage,
PIE3D_OT_MaterialDelete,
PIE3D_OT_objectinstans,
PIE3D_OT_cleanupinstans,
PIE3D_OT_objectinstansmirror,
PIE3D_OT_ViewShading,
PIE3D_OT_ViewShadingShowFace,
PIE3D_OT_CopyAsset,
PIE3D_OT_SelectObjectBool,
PIE3D_OT_BoolOnOff,
PIE3D_OT_uv_selmirseam,
PIE3D_OT_mesh_emptyverdel,
PIE3D_OT_uv_seleobjsmartuv,
PIE3D_OT_look_for_no_geometry,

)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
