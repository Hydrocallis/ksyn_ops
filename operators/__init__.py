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
    # UV関係	
    "uvgridmat_add",	
    "uv_unwrap",	
    "uv_map_deletechange",	
    "meshuv_uvsetting",
    "uv_selmirseam",

    "weightpaint_value_change",	
    "material_delete",	
    "get_fbx_exportdrectory",	
    "cleanupinstans",	
    "shadingchange",	
    "copyasset",	
    "boolobject",	
    "meshbicect_mirror",	
    "mesh_emptyverdel",	
    "look_for_no_geometry",	
    "lastselectobject_addempty",	
    "select_mesh_separate_operator",	
    "simplerotate",	
    "mesh_mirror",	
    "simple_object_bake",	
    "material_append",	


 # ot
    "edge_fr_vertex_op",
    "easy_mirror",
    "object_easy_array",
    "easy_knife_project",
    "easy_curve_to_mesh",
    "ciercle_dupulicate_ot",
    "wordlorijin_move_ot",
    "curve_mirror_op",
    "objectinstans",
    "objectinstansmirror",
    "orijin_seting"

	]
	
	for module in reloadable_modules:
		if module in locals():
			importlib.reload(locals()[module])


# ※２
from .PiePropsSetting import *
#uv 関係
from .uvgridmat_add import *
from .uv_unwrap import *
from .uv_map_deletechange import *
from .meshuv_uvsetting import MESHUV_OT_uvsetting
from .uv_selmirseam import MESHUV_OT_uvsettingselmirseam

from .weightpaint_value_change import *
from .material_delete import *
from .get_fbx_exportdrectory import *

from .cleanupinstans import *

from .shadingchange import *
from .copyasset import *
from .boolobject import *


from .mesh_emptyverdel import *
from .look_for_no_geometry import *
from .lastselectobject_addempty import KSYN_OT_lastselectaddempty
from .select_mesh_separate_operator import MESH_OT_select_mesh_separate_operator
from .simplerotate import MESH_OT_simplerotate
from .mesh_mirror import MESH_OT_Meshmirror_operator
from .orijin_seting import PIE3D_OT_originset
from .meshbicect_mirror import MESH_OT_bicect_mirror
from .meshbicect_mirror import MESH_OT_bicect_mirror
from .material_append import MATERIAL_OT_matterialappend

from .edge_fr_vertex_op import SIMPLE_OT_edgefrvertex
from .object_easy_array import OBJECTEASYARRAY_OT_objarray
from .easy_knife_project import SIMPLE_OT_easy_knife_project
from .easy_curve_to_mesh import SIMPLE_OT_easy_curve_to_mesh
from .ciercle_dupulicate_ot import SIMPLEARRAY_OP_ciercle_dupulicate
from .wordlorijin_move_ot import WORDORIJINMOVE_OT_MAIN
from .curve_mirror_op import SIMPLE_OT_curve_mirror
from .easy_mirror import OBJECTEASYMIRROR_OT_MAIN
from .objectinstans import PIE3D_OT_objectinstans
from .objectinstansmirror import PIE3D_OT_objectinstansmirror





# ※３
classes = (
PIE3D_OT_GetFbxInformation,
PIE3D_OT_PiePropsSetting,
#　uv　関係
PIE3D_OT_UvGridMat,
PIE3D_OT_uv_Unwrap,
PIE3D_OT_UvMapDeleteChange,
PIE3D_OT_weightpaint_value_chnage,
PIE3D_OT_MaterialDelete,
MESHUV_OT_uvsetting,
MESHUV_OT_uvsettingselmirseam,


PIE3D_OT_cleanupinstans,

PIE3D_OT_ViewShading,
PIE3D_OT_ViewShadingShowFace,
PIE3D_OT_CopyAsset,
PIE3D_OT_SelectObjectBool,
PIE3D_OT_BoolOnOff,

MESH_OT_bicect_mirror,
PIE3D_OT_mesh_emptyverdel,
PIE3D_OT_look_for_no_geometry,
KSYN_OT_lastselectaddempty,
MESH_OT_select_mesh_separate_operator,
MESH_OT_simplerotate,
MESH_OT_Meshmirror_operator,
PIE3D_OT_originset,
MATERIAL_OT_matterialappend,


SIMPLE_OT_edgefrvertex,
SIMPLEARRAY_OP_ciercle_dupulicate,
OBJECTEASYARRAY_OT_objarray,
SIMPLE_OT_easy_knife_project,
SIMPLE_OT_easy_curve_to_mesh,
WORDORIJINMOVE_OT_MAIN,
SIMPLE_OT_curve_mirror,
OBJECTEASYMIRROR_OT_MAIN,
PIE3D_OT_objectinstans,
PIE3D_OT_objectinstansmirror,

)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
		

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
		

		

if __name__ == "__main__":
	register()
