
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty


try:
    from ..registration import addon_keymapscuspie
    from set_module import install

except ImportError:

    from ksyn_ops.registration import addon_keymapscuspie # type: ignore
    from ksyn_ops.ohters.set_module import install # type: ignore

class ExampleAddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = "ksyn_ops"


    api_key: StringProperty(
        name='API Key', description='API Key for the DeepL API', subtype='PASSWORD', default='') # type: ignore
    

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    ) # type: ignore
    number: IntProperty(
        name="Example Number",
        default=4,
    )# type: ignore
    adminmode: BoolProperty(
        name="Admin Mode",
        default=False,
    )# type: ignore

    def draw(self, context):
        layout = self.layout
        # layout.label(text="This is a preferences view for our add-on")
        # layout.prop(self, "filepath")
        # layout.prop(self, "number")
        layout.prop(self, "adminmode")
        layout.prop(self, "api_key")
        install(self)

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
