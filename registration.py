
import bpy,importlib,os
import importlib.util
import sys
from bpy.utils import register_class, unregister_class


# 親ディレクトリのパスを取得
addon_path = os.path.dirname(os.path.realpath(__file__))
addon_keymapscuspie = []

class_paths = [
    ("operators", "pie_op", "ChangeLightEnergyOperator"),
    ("operators", "pie_op", "ImportNodeGroupsOperator"),
    ("operators", "pie_op", "ReName"),
    ("operators", "pie_op", "AutoSommth"),
    ("operators", "pie_op", "Setting"),
    ("operators", "pie_op", "mesh_hide"),
    ("operators", "pie_op", "toggle_mode"),
    ("operators", "pie_op", "rotationx"),
    ("operators", "pie_op", "rotationy"),
    ("operators", "pie_op", "flatselect"),
    ("operators", "pie_op", "seamclear"),
    ("operators", "pie_op", "seamadd"),
    ("operators", "pie_op", "ColorPickupObject"),
    ("operators", "pie_op", "SubdivisionShow"),
    ("operators", "pie_op", "AmatureRestBool"),
    ("operators", "pie_op", "PLockTransforms"),
    ("operators", "pie_op", "wiredisplay"),
    ("operators", "boolobject", "BoolOnOff"),
    ("operators", "boolobject", "SelectObjectBool"),
    ("operators", "ciercle_dupulicate_ot", "ciercle_dupulicate"),
    ("operators", "cleanupinstans", "cleanupinstans"),
    ("operators", "copyasset", "CopyAsset"),
    ("operators", "curve_mirror_op", "CurveMirror"),
    ("operators", "easy_curve_to_mesh", "easy_curve_to_mesh"),
    ("operators", "easy_knife_project", "easy_knife_project"),
    ("operators", "easy_mirror", "OBJECTEASYMIRROR"),
    ("operators", "edge_fr_vertex_op", "edgefrvertex"),
    ("operators", "get_fbx_exportdrectory", "GetFbxInformation"),
    ("operators", "lastselectobject_addempty", "lastselectaddempty"),
    ("operators", "look_for_no_geometry", "look_for_no_geometry"),
    ("operators", "material_append", "matterialappend"),
    ("operators", "material_delete", "MaterialDelete"),
    ("operators", "mesh_emptyverdel", "mesh_emptyverdel"),
    ("operators", "mesh_mirror", "Meshmirror_operator"),
    ("operators", "meshbicect_mirror", "bicect_mirror"),
    ("operators", "meshuv_uvsetting", "uvsetting"),
    ("operators", "object_easy_array", "objarray"),
    ("operators", "objectinstans", "objectinstans"),
    ("operators", "objectinstansmirror", "objectinstansmirror"),
    ("operators", "objectinstansmirror", "LinkObjectsToNewSceneOperator"),
    ("operators", "orijin_seting", "originset"),
    ("operators", "PiePropsSetting", "PiePropsSetting"),
    ("operators", "select_mesh_separate_operator", "select_mesh_separate_operator"),
    ("operators", "shadingchange", "ViewShading"),
    ("operators", "shadingchange", "ViewShadingShowFace"),
    ("operators", "simplerotate", "simplerotate"),
    ("operators", "uv_map_deletechange", "UvMapDeleteChange"),
    ("operators", "uv_selmirseam", "uvsettingselmirseam"),
    ("operators", "uv_unwrap", "uv_Unwrap"),
    ("operators", "uvgridmat_add", "UvGridMat"),
    ("operators", "weightpaint_value_change", "weightpaint_value_chnage"),
    ("operators", "wordlorijin_move_ot", "WORDORIJINMOVE"),
    ("operators", "ConvertNgonsToTris", "ConvertNgonsToTrisOperator"),
    ("operators", "selechildrecursive", "SelectChildrenRecursiveOperator"),
    ("operators", "separate_and_join", "SeparateAndJoinOperator"),
    ("operators", "mode_actobje_loc", "MoveSelectedToLastOperator"),
    ("operators", "add_primitive", "AddPrimitiveOperator"),
    ("operators", "join_hierarchy_objects", "OBJECT_OT_JoinHierarchyObjects"),
    ("operators", "square_empty_layout_operator", "SquareEmptyLayoutOperator"),
    ("operators", "create_autoliner_empy", "OBJECT_OT_ParentActiveObject"),
    ("operators", "create_autoliner_empy", "CreateEmptyOperator"),
    ("operators", "create_autoliner_empy", "activeCreateEmptyOperator"),
    ("operators", "create_autoliner_empy", "PlaceEmptyOperator"),
    ("operators", "create_autoliner_empy", "RenameSelectedObjectsOperator"),
    ("operators", "create_autoliner_empy", "RenameSelectedObjects_collection_Operator"),
    ("operators", "translate_property", "TranslatePropertyOperator"),
    ("operators", "translate_property", "TranslatePropertyPanel"),
    ("operators", "joint_blean", "BooleanOperator"),
    ("operators", "geometry_nodes_operator", "GeometryNodesOperator"),
    ("operators", "create_window_mesh", "WINDOW_CREATE_objectPanel"),
    ("operators", "create_window_mesh", "WINDOW_CREATE_CreateBars"),

    ("ohters", "preference", "ExampleAddonPreferences"),
]
 
prefix = "KSYNOPS_OT_"
prefix_ohters = "KSYNOPS_OH_"

def load_classes(class_paths):
    classes = []

    for path_parts, classmodule, class_name in class_paths:
        module_path = os.path.join(addon_path, path_parts, classmodule + ".py")
        spec = importlib.util.spec_from_file_location(class_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        cls = getattr(module, class_name)
        classes.append((cls,classmodule,path_parts))

    return classes

loaded_classes = load_classes(class_paths)


__subclasses__debug= False

if __subclasses__debug ==True:
    # KSYNOPS_OTがつくクラス名のみを抽出する
    ksynops_classes = [cls.__name__ for cls in bpy.types.Operator.__subclasses__() if cls.__name__.startswith(prefix)]

    # 抽出されたクラス名の表示
    for cls_name in ksynops_classes:
        print("###__subclasses__ Operator Debug ",cls_name)



def add_prefix(cls, prefix):
    new_cls = type(prefix + cls.__name__, cls.__bases__, dict(cls.__dict__))
    return new_cls

loaded_classes_prefix=[]
for cls,classmodule,part in loaded_classes:
    if part =="operators":
        new_cls = add_prefix(cls, prefix)
    elif part =="ohters":
        new_cls = add_prefix(cls, prefix_ohters)
    loaded_classes_prefix.append((new_cls,classmodule,part))


# クラス名を変えた場合はブレンダーを再起動する必要があるみたい。
# 一見、再読み込みで元のクラス名が読み込まれそうだが、あくまでもレジストレーションのクラス名が読み込まれるので、
# レジストレーションの設定でクラス名が決まっていればOK。で、再読み込みはあくまでもファイルだけが読み込まれる仕様

# オンにした場合は最初のレジストレーションでプリントされる
register_debug=False

def register_classes():
    for cls,classmodule,part in loaded_classes_prefix:
        if register_debug:
            print(f"REGISTERING {part} {classmodule}", cls)
        register_class(cls)


def unregister_classes():
    for cls,classmodule,part in loaded_classes_prefix:
        if register_debug:
            print(f"UN-REGISTERING {part} {classmodule}", cls)

        unregister_class(cls)