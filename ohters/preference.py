
import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty


try:
    from ..registration import addon_keymapscuspie
    from set_module import install
    from .. import addon_updater_ops



except ImportError:

    from ksyn_ops.registration import addon_keymapscuspie # type: ignore
    from ksyn_ops.ohters.set_module import install # type: ignore
    from ksyn_ops import addon_updater_ops # type: ignore


class UpdaterProps:
    
    auto_check_update : bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False) # type: ignore

    updater_interval_months : bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)# type: ignore

    updater_interval_days : bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)# type: ignore

    updater_interval_hours : bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)# type: ignore

    updater_interval_minutes : bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)# type: ignore


class ExampleAddonPreferences(AddonPreferences,UpdaterProps):
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

        addon_updater_ops.update_settings_ui(self, context)


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
