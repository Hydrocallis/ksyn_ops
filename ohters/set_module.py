import bpy,subprocess,sys,os
import textwrap


try:
    from ksyn_ops.utils.get_translang import get_translang # type: ignore

except ImportError:

    from ..utils.get_translang import get_translang


import importlib
import pkgutil
addonname="ksyops"

def install(self,modulename="pywin32",installmodulename="win32clipboard"):

    install_box =self.layout.box()
    install_box.label(text=get_translang(f'Module settings for {modulename}',f'{modulename}のモジュール設定'), icon="TOOL_SETTINGS")

    # Check if PIL is installed
    try:

        loader = pkgutil.find_loader(modulename)
        module_exists = loader is not None
    except ImportError:
        module_exists = False
    try:

        loader = pkgutil.find_loader(installmodulename)
        module_exists = loader is not None
    except ImportError:
        module_exists = False

    if module_exists:
        install_box.label(text=f"{modulename} module is installed", icon='FUND')
        install_box.operator(f"{addonname}.uninstall_module", icon='REMOVE',text=f"Uninstall {modulename}").cmd= modulename
        # モジュールが存在する場合の処理
        
        try:
            # モジュールをインポート
            module = importlib.import_module(installmodulename)
            # バージョンを出力
            print(f"{installmodulename}モジュールのバージョン:", module.__version__)
              
            module = importlib.import_module(installmodulename)

            version = module.__version__
            # print(f"{modulename} version: {version}")

            install_box.label(text=f"{modulename}({installmodulename}) module version: {version}")

        except (AttributeError, ImportError):
            pass
            # print("バージョン情報が見つかりませんでした。")

      
    
    
    else:
        install_box.label(text=f"{modulename} module is NOT installed", icon='CANCEL')

        # Install PIL button
        install_box.operator(f"{addonname}.install_module", text=f"install {modulename}",icon='ADD').cmd= modulename

    # Uninstall PIL button (if PIL is installed)
    # import importlib.util

    # # モジュールが存在するか確認
    # spec = importlib.util.find_spec(installmodulename)

    # if spec is not None:
    #     install_box.label(text=f"{installmodulename} module not found")

    # else:



def popup_list_message(self,title, messages,icon="INFO"):
    wrapped_messages = []
    for message in messages:
        wrapped_message = textwrap.wrap(message, width=80)
        wrapped_messages.extend(wrapped_message)

    def draw(self, context):
        # self.layout.operator("bake.simpleobjectbake",text=get_translang('Adapting baked materials','ベイクしたマテリアルを適応')).cmd = "add_mat"
        for mes in wrapped_messages:
            self.layout.label(text=mes)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


class PipInstall(bpy.types.Operator):
    bl_idname = f"{addonname}.install_module"
    bl_label = "Install module"

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore

    def execute(self, context):

        blender_exec = sys.executable

        try:
            output = subprocess.check_output([blender_exec, "-m", "pip", "install", self.cmd])
            # bpy.ops.wm.popup_menu(text=f"PIL installed successfully:\n{output.decode()}", title="Install PIL")
            popup_list_message(self,f"{self.cmd} installed successfully", [output.decode()])
        except subprocess.CalledProcessError as e:
            # bpy.ops.wm.popup_menu(text=f"Failed to install PIL:\n{e.output.decode()}", title="Install PIL", icon='ERROR')
            popup_list_message(self,"ERROR", [e])

            
        return {'FINISHED'}

class PipUninstall(bpy.types.Operator):
    bl_idname = f"{addonname}.uninstall_module"
    bl_label = "Uninstall module"

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore

    def execute(self, context):
        blender_exec =  sys.executable
        
        if self.cmd =="pywin32":
            try:
                output = subprocess.check_output([blender_exec, "-m", "pip", "uninstall", "-y", "Pillow"],stderr=subprocess.STDOUT).decode().strip()
                message = output
                print('###mes',message)
                # self.report({'INFO'}, message)
            except subprocess.CalledProcessError as e:
                message = "Failed to uninstall Pillow. Error message:\n" + str(e)
                # self.report({'ERROR'}, message)
                # ポップアップメッセージを表示する
                # bpy.context.window_manager.popup_menu(popup_message, title="Message", icon='INFO')
            popup_list_message(self,"PIL uninstalled successfully", [message])


        return {'FINISHED'}

class PipListInstall(bpy.types.Operator):
    """Check Install  package"""
    bl_idname = f"{addonname}.checkinstall"
    bl_label = "Check Install"
    
    def execute(self, context):
        blender_exec =  sys.executable


        # Check if Pillow is installed
        try:
            output = subprocess.check_output([blender_exec, "-m", "pip", "list"])
            # Convert the byte string to a regular string
            output_str = output.decode("utf-8")

            # Split the string into a list of lines
            lines = output_str.split("\n")

            # Split the string into a list of lines and remove empty lines
            lines = [line for line in output_str.split("\n") if line.strip()]


            # Extract the package names
            package_names = [line.split()[0] for line in lines]
            print('###package_names',package_names)

            # Check if Pillow and opencv-python are installed
            if "pywin32" in package_names and "opencv-python" in package_names:
                message = get_translang("Both Pillow and opencv-python are installed.",
                                        "Pillowとopencv-pythonの両方がインストールされています。")
                icon = "CHECKBOX_HLT"

            else:
                message = get_translang("Neither Pillow nor opencv-python is installed.",
                                        "Pillowもopencv-pythonもインストールされていません。")
                icon = "CHECKBOX_DEHLT"

            title = "Installation Check"
            print(f"{title}: {message} ({icon})")


        except subprocess.CalledProcessError as e:
            message = f"Failed to check Pillow installation: {e}"
            title = "Error"

        # bpy.context.window_manager.popup_menu(popup_message, title="Message", icon='INFO')
        popup_list_message(self,title, [message],icon=icon)

        return {'FINISHED'}

class OpenAddonPreferences(bpy.types.Operator):
    bl_idname = f"{addonname}.open_addon_preferences"
    bl_label = "Open Addon Preferences"

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'}) # type: ignore


    def execute(self, context):

        # from ksyn_ops import get_addonname

        addon_name ="ksyn_ops"
        print('###',addon_name)

        preferences = bpy.context.preferences
        addon_prefs = preferences.addons[addon_name].preferences

        bpy.ops.screen.userpref_show("INVOKE_DEFAULT")
        addon_prefs.active_section = 'ADDONS'
        bpy.ops.preferences.addon_expand(module = addon_name)
        bpy.ops.preferences.addon_show(module = addon_name)


        if self.cmd == "INSTALL_SETTINGS":
            addon_prefs.tab_item="INSTALL_SETTINGS"
            
        elif self.cmd == "CANVAS_SETTINGS":
            addon_prefs.tab_item="CANVAS_SETTINGS"
        elif self.cmd == "KEY_MAP_SETTING":
            addon_prefs.tab_item="KEY_MAP_SETTING"

        

        return {'FINISHED'}
    