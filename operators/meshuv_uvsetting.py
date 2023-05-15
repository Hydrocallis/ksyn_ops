
import bpy, sys, os, subprocess,bmesh

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng
    
def getoverride():
    for screen in bpy.data.screens:
        if screen.name =='UV Editing':
            # print(screen.name)
            for area in screen.areas:
                if area.type == 'IMAGE_EDITOR':
                    override = {'area': area, 'region': area.regions} 
                    image_editor = area.spaces.active
                    break


                    #override context
    return override,image_editor  
  
def changeuvmesh(self):
    override,image_editor = getoverride()
    # 現在のピボットポイントを保存する
    pivot_point = image_editor.pivot_point
    image_editor.pivot_point = self.uv_pivot_point
    save_select_sync = bpy.context.scene.tool_settings.use_uv_select_sync
    bpy.context.scene.tool_settings.use_uv_select_sync = True

    if self.unwrap == True:
        bpy.ops.uv.unwrap()
    # check rotation mode
    factor = self.factor
    if self.cmd =="90rotation":
        factor =1.5708*self.rotatino_numbers
    
    try:
        if self.cmd == "scalesize":
            # print('###scale',)
            bpy.ops.transform.resize(override,
                                    value=(self.scale, self.scale, self.scale), 
                                    )

        elif self.cmd=="90rotation" or self.cmd=="rotationuv":    
            bpy.ops.transform.rotate(
                override,
                value=factor, 
                orient_axis='Z',
                )
        
    except NameError:
        self.report({'INFO'}, get_translang("Open the 'UV Editing' tab.",'「UV編集」タブを開いてください。'))

        print("Please open 'UV Editing' Tab")

    
    # ピボットポイントを元に戻す
    image_editor.pivot_point = pivot_point
    bpy.context.scene.tool_settings.use_uv_select_sync = save_select_sync

def change_matuvscale(self):
    factor = self.scale
    # Get the active material for the object
    obj = bpy.context.active_object
    mat = obj.active_material

    savemode = str(bpy.context.mode)
    if savemode == "EDIT_MESH":
        savemode = "EDIT"

    bpy.ops.object.mode_set(mode='EDIT')

    obj = bpy.context.active_object
    mat_c1 = mat
    c1_slots = [id for id, mat in enumerate(obj.data.materials) if mat == mat_c1]

    me = obj.data
    bm = bmesh.new()
    bm = bmesh.from_edit_mesh(me)
    uv_layer = bm.loops.layers.uv.verify()
    # currently blender needs both layers.
    bm.faces.layers.face_map.verify() 

    # scale UVs x factor
    for f in bm.faces:
        if f.material_index in c1_slots:
            for l in f.loops:
                l[uv_layer].uv *= factor


    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode=savemode)

def main_draw(self):
    self.layout.label(text=get_translang('UV Setting','UVの設定'))
    if self.cmd == "rotationuv":
        self.layout.prop(self,"factor")
    if self.cmd == "90rotation":
        self.layout.prop(self,"rotatino_numbers")
    if self.cmd == "uvscalechange" or self.cmd == "scalesize":
        self.layout.prop(self,"scale")
    self.layout.prop(self,"uv_pivot_point")
    self.layout.prop(self,"unwrap")

def main(self):
    if self.cmd == "rotationuv" or self.cmd =="90rotation" or self.cmd == "scalesize":
        changeuvmesh(self)
    if self.cmd == "uvscalechange":
        change_matuvscale(self)


class uvsetting(Operator):
    bl_idname = 'object.uv_setting'
    bl_label = 'Mesh UV Setting'
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'})

    factor: bpy.props.FloatProperty(name=get_translang('Rotation','回転量'),
                                    default = 1.5708,
                                    unit="ROTATION")
    
    scale: bpy.props.FloatProperty(name=get_translang('Scale','縮尺'),
                                   default = 1,
                                    )
    
    rotatino_numbers: bpy.props.IntProperty(name=get_translang('Count','繰り返し'),
                                            default = 1,
                                    )
    unwrap: bpy.props.BoolProperty(name=get_translang('Unwrap','展開'),
                                            default = False,
                                    )
    
    uv_pivot_pointitems = [
        ('MEDIAN', 'Median Point', "", 1),
        ('INDIVIDUAL_ORIGINS', "Individual Origins", "", 2),
        ]
    
    uv_pivot_point : bpy.props.EnumProperty(
            name = get_translang('Pivot','ピボット'),
            items = uv_pivot_pointitems
            )


    # 3Dで用のプロパティ
    # enum_prop : bpy.props.EnumProperty(items=[('X', "X", "One",1), ('Y', "Y", "Two",2), ('Z', "Z", "Two",3)])
  
    def execute(self, context):
        main(self)
        return {'FINISHED'}

    @classmethod
    def poll(self, context):
        return True
    def draw(self,context):
        main_draw(self)
      
