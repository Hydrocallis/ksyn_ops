
# フォルダ読み込みに必要なこと。　
# インポートするだけではだめで、
# フォルダの場合はレジスターに登録してあげないと、
# 中のININTファイルが読み込まれない仕様である。

bl_info = {
    "name": "KSYN OPS",
    "description": "Viewport custum",
    "author": "KSYN",
    "version": (0, 1, 7),
    "blender": (3, 2, 0),
    "location": "shift ctrl Q key",
    "warning": "",
    "doc_url": "",
    "category": "KSYN",
    }



# リロードモジュール　開始
def reload_unity_modules(name,debug=False):
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



from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )


from .utils.get_translang import get_translang
from .registration import register_classes,unregister_classes


# アドオンの項目の設定項目
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty

addon_keymapscuspie = []


class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    adminmode: BoolProperty(
        name="Admin Mode",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        # layout.label(text="This is a preferences view for our add-on")
        # layout.prop(self, "filepath")
        # layout.prop(self, "number")
        layout.prop(self, "adminmode")

        import rna_keymap_ui 
        layout = self.layout
        wm = context.window_manager
        kc = wm.keyconfigs.user
        old_km_name = "" 
        old_id_l = [] 
        for km_add, kmi_add in addon_keymapscuspie: 
            km = kc.keymaps[km_add.name] 
            for kmi_con in km.keymap_items: 
                if kmi_add.idname == kmi_con.idname: 
                    if not kmi_con.id in old_id_l:
                        kmi = kmi_con 
                        old_id_l.append(kmi_con.id) 
                        break 
            if kmi:
                if not km.name == old_km_name: 
                    layout.label(text=km.name,icon="DOT") 
                layout.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)
                layout.separator()
                old_km_name = km.name
                kmi = None

# 辞書登録関数　開始
import os,codecs,csv

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
            ExampleAddonPreferences,
            )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    panel.register()
    menu.register()
    properties.register()
    register_classes()




    # 通常の３Dモードの（オブジェクトモードでしか何故か登録できない）キーマップ登録
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True, ctrl=True)
        
        kmi.properties.name = "PIE_MT_viewnumpad_mypanel"# これが被ってるとバグる
        addon_keymapscuspie.append((km, kmi))

    wm = bpy.context.window_manager
    
    # メッシュモードでのキーマップ登録
    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Q', 'PRESS', shift=True, ctrl=True)
        kmi.properties.name = "PIE_MT_viewnumpad_mypanel"# これが被ってるとバグる
        addon_keymapscuspie.append((km, kmi))

    wm = bpy.context.window_manager
 

 	# 翻訳辞書の登録
    try:
        translation_dict = GetTranslationDict()
        bpy.app.translations.register(__name__, translation_dict)
    except: pass

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    panel.unregister()
    menu.unregister()
    properties.unregister()
    unregister_classes()


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
