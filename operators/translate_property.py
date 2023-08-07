import bpy,sys
import requests

from bpy.props import StringProperty
from bpy.types import Operator, Panel


def get_addon_pref():
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons["ksyn_ops"].preferences
    return addon_prefs

class TranslatePropertyOperator(Operator):
    bl_idname = "scene.translate_property"
    bl_label = "Translate Property"
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    

    def execute(self, context):
        scene = bpy.context.scene
        addon_prefs = get_addon_pref()
        addon_prefs.api_key

        # Deepl APIのURLとAPIキーを設定
        url = "https://api-free.deepl.com/v2/translate"
        api_key = addon_prefs.api_key
        # print('###',api_key)
        if api_key !="":
                

            # 翻訳するテキストとターゲット言語をパラメータとして設定
            params = {
                "auth_key": api_key,
                "text": scene.source_word,
                "target_lang": scene.target_language
            }

            # Deepl APIにリクエストを送信
            response = requests.post(url, data=params)

            # レスポンスのJSONデータを取得
            translation = response.json()["translations"][0]["text"]

            # 翻訳結果を設定
            scene.translated_word = translation
        else:
            self.report({'INFO'}, "Please input api key")


        return {'FINISHED'}

class TranslatePropertyPanel(Panel):
    bl_idname = "SCENE_PT_translate_property"
    bl_label = "Translate Property"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "source_word")
        layout.prop(scene, "target_language")
        layout.prop(scene, "translated_word")
        layout.operator("scene.translate_property")


#######BOTTM#############

class KSYNOPS_WM_MT_button_context(bpy.types.Menu):
    bl_label = ""
    # Leave empty for compatibility.
    def draw(self, context): pass


# Your draw function.
def draw(self, context):

    if hasattr(context, "button_prop"):
        # print("Property:", context.button_prop.identifier)
        if context.button_prop.identifier == "source_word" :
            self.layout.separator()
            self.layout.operator("screen.active_dptinut_property_add").cmd = context.button_prop.identifier
            self.layout.separator()


def context_botom_append():
    # Register menu only if it doesn't already exist.
    rcmenu = getattr(bpy.types, "KSYNOPS_WM_MT_button_context", None)
    if rcmenu is None:
        bpy.utils.register_class(KSYNOPS_WM_MT_button_context)
        rcmenu = KSYNOPS_WM_MT_button_context

    # Retrieve a python list for inserting draw functions.
    draw_funcs = rcmenu._dyn_ui_initialize()
    draw_funcs.append(draw)


def context_botom_remove():
    # Register menu only if it doesn't already exist.
    rcmenu = getattr(bpy.types, "WM_MT_button_context", None)
    if rcmenu is None:
        bpy.utils.register_class(KSYNOPS_WM_MT_button_context)
        rcmenu = KSYNOPS_WM_MT_button_context

    # Retrieve a python list for inserting draw functions.
    draw_funcs = rcmenu._dyn_ui_initialize()
    # draw_funcs.remove(draw)



#######BOTTM#############




def translate_property_register():
    context_botom_append()

    bpy.types.Scene.source_word = StringProperty(
        name="Source Word",
        description="Enter the word to translate"
    )

    bpy.types.Scene.target_language = StringProperty(
        name="Target Language",
        description="Enter the target language code",
        default = "EN"
    )
    
    bpy.types.Scene.translated_word = StringProperty(
        name="translated_word",
        description="Enter the target language code"
    )

def translate_property_unregister():
    context_botom_remove()

    del bpy.types.Scene.source_word
    del bpy.types.Scene.target_language
    del bpy.types.Scene.translated_word
