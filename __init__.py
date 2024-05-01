
# フォルダ読み込みに必要なこと。　
# インポートするだけではだめで、
# フォルダの場合はレジスターに登録してあげないと、
# 中のININTファイルが読み込まれない仕様である。

bl_info = {
    "name": "KSYN OPS",
    "description": "Viewport custum",
    "author": "KSYN",
    "version": (1, 0, 1),
    "blender": (3, 2, 0),
    "location": "shift ctrl Q key",
    "warning": "",
    "doc_url": "",
    "category": "KSYN",
    }



# リロードモジュール　開始
def reload_unity_modules(name, debug=False):
    import os
    import importlib
   
    utils_modules = sorted([name[:-3] for name in os.listdir(os.path.join(__path__[0], "utils")) if name.endswith('.py')])

    for module in utils_modules:
        impline = "from . utils import %s" % (module)
        if debug == True:
            print("##UTILS RELOAD %s" % (".".join([name] + ['utils'] + [module])))

        exec(impline)
        importlib.reload(eval(module))


    ### Operatorリロード
    from .registration import class_paths
    
    for path, module,cls in class_paths:
        if path:
            impline = "from . %s import %s" % (".".join([path]), module)
            # print('###KSYN_OPS OPARATOER RELOAD FILE ',impline)
        else:
            impline = "from . import %s" % (module)

        if debug == True:
            print("###OPARATOER RELOAD  %s" % (".".join([name + path + module+str(cls)])))
            pass

        exec(impline)
        # print('###modules',module)
        importlib.reload(eval(module))



    # UTILIS以外のモジュールを再読み込み(これによって相互的にモジュール互換のあるものの問題を解消する)
    utils_modules = sorted([name[:-3] for name in os.listdir(os.path.join(__path__[0], "utils")) if name.endswith('.py')])

    for module in utils_modules:
        impline = "from . utils import %s" % (module)
        exec(impline)
        importlib.reload(eval(module))


# UTILIS以外のモジュールを再読み込み
if "bpy" in locals():
    import importlib
    reloadable_modules = [ # リストに読み込むものをまとめる
    # フォルダを再登録
    "panel",
    "properties",
    "menu",
    "registration",

    ]

    for module in reloadable_modules: # リスト内のものがすでにあれば、reloadを発動する
        if module in locals():
            importlib.reload(locals()[module])

if 'bpy' in locals():
    reload_unity_modules(bl_info['name'])

# リロードモジュール　終了


import bpy, sys, os, subprocess

from . import properties
from . import panel
from . import menu

from .registration import register_classes,unregister_classes
from ksyn_ops.registration import addon_keymapscuspie# type: ignore
from ksyn_ops.operators.create_autoliner_empy import OUTLINER_MT_objectregister,OUTLINER_MT_objectunregister # type: ignore
from ksyn_ops.operators.translate_property import translate_property_register,translate_property_unregister# type: ignore

from .operators.mod_status import mod_status_register,mod_status_unregister

# アドオンの項目の設定項目

from bpy.utils import previews
from . import addon_updater_ops
 


# 辞書登録関数　開始
import codecs,csv

def GetTranslationDict():
    dict = {}
    # 直下に置かれているcsvファイルのパスを代入
    path = os.path.join(os.path.dirname(__file__), "translation_dictionary.csv")
    with codecs.open(path, 'r', 'utf-8') as f:
        reader = csv.reader(f)
        dict['ja_JP'] = {}
        for row in reader:
            for context in bpy.app.translations.contexts:
                dict['ja_JP'][(context, row[1].replace('\\n', '\n'))] = row[0].replace('\\n', '\n')
    return dict
# 辞書登録関数　終わり


# クラスの登録
classes = (
            )

ksynops_preview_collections = {}

def register_icons():
    pcoll = previews.new()
    addon_dir = os.path.dirname(__file__)
    pcoll.load("diff", os.path.join(addon_dir, "icons", "diff.png"), 'IMAGE')
    pcoll.load("join", os.path.join(addon_dir, "icons", "join.png"), 'IMAGE')
    pcoll.load("int", os.path.join(addon_dir, "icons", "int.png"), 'IMAGE')
    pcoll.load("slice", os.path.join(addon_dir, "icons", "slice.png"), 'IMAGE')
    pcoll.load("slice_int", os.path.join(addon_dir, "icons", "slice-int.png"), 'IMAGE')
    pcoll.load("slice_gap", os.path.join(addon_dir, "icons", "slice-gap.png"), 'IMAGE')
    ksynops_preview_collections["main"] = pcoll

def register():
    addon_updater_ops.register(bl_info)

    register_icons()

    panel.register()
    menu.register()
    properties.register()
    register_classes()
    OUTLINER_MT_objectregister()
    translate_property_register()
    mod_status_register()


    # 通常の３Dモードの（オブジェクトモードでしか何故か登録できない）キーマップ登録
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True, ctrl=True)
        
        kmi.properties.name = "KSYN_MT_viewnumpad_panel"# これが被ってるとバグる
        addon_keymapscuspie.append((km, kmi))


    wm = bpy.context.window_manager
    
 
    # メッシュモードでのキーマップ登録
    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True, ctrl=True)
        kmi.properties.name = "KSN_MT_node_editerpiemenu_menu"# これが被ってるとバグる
        addon_keymapscuspie.append((km, kmi))

    wm = bpy.context.window_manager
 

 	# 翻訳辞書の登録
    try:
        translation_dict = GetTranslationDict()
        bpy.app.translations.register(__name__, translation_dict)
    except: pass

def unregister_icons():
    # Remove the preview collection
    pcoll = ksynops_preview_collections.pop("main")
    previews.remove(pcoll)
    ksynops_preview_collections["main"] = pcoll

def unregister():
    addon_updater_ops.unregister()

    unregister_icons()

    panel.unregister()
    menu.unregister()
    properties.unregister()
    unregister_classes()
    OUTLINER_MT_objectunregister()
    translate_property_unregister
    mod_status_unregister()


    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymapscuspie:
            km.keymap_items.remove(kmi)
    addon_keymapscuspie.clear()

	# 翻訳辞書の登録解除
    try:
        bpy.app.translations.unregister(__name__)
    except: pass


if __name__ == "__main__":
    register()
