import bpy, os , sys,pathlib
from math import degrees,radians
from mathutils import Vector

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,

        )
from ksyn_ops.utils.englishname_trans import remove_japanese

from bpy.props import (
                        StringProperty, 
                        IntProperty, 
                        FloatProperty, 
                        EnumProperty, 
                        BoolProperty,
                        PointerProperty,
                        FloatVectorProperty,
                        StringProperty
                        )


# マテリアルが含まれる.blendファイルのパス
p_file = pathlib.Path(__file__)

filepath=  str(p_file.parents[1].joinpath("asset", 'asset_001.blend'))

# make_enum_material_listで読み込みたいマテリアルリスト（それ以外は省く）
desired_materials = ['Wood Carving Texture_v1_03', 'Edge detect', 'Brick Texture _v1.02']


# filepath = r"D:\マイドライブ\blender scrpt\addons\pie_3d_menu\asset\asset_001.blend"
#

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng
    
def get_material_by_name(matname):
    """
    指定した名前のマテリアルをシーン内から検索し、あればそれを返す。
    なければNoneを返す。
    """
    for checkmat in bpy.data.materials:
        if checkmat.name == matname:
            return checkmat
    return None

def import_materials_from_file(filepath,matname):
    # ファイルを開く
    with bpy.data.libraries.load(filepath) as (data_from, data_to):

        # マテリアルをインポート
        data_to.materials = [m for m in data_from.materials if m == matname]

    # インポートされたマテリアルを返す

    datalist = data_from.materials
    # print('###',datalist)
    datalistfilter = []
    if data_to.materials == []:
        material=None
    else:
        material=data_to.materials[0]
    return material,datalist

def append_mat(materials):
    # マテリアルを適用するオブジェクトのリスト
    objects_to_apply_material = bpy.context.selected_objects

    if materials == None:
        print("No materials available"," please cheke material list")
    else:
        # 各オブジェクトにマテリアルを適用する
        for obj in objects_to_apply_material:
            # オブジェクトのマテリアルを削除
            #    obj.data.materials.clear()
            #  アクティブなマテリアルスロットに新しいマテリアルを適用

            obj.active_material =materials

def check_matappend(self):
    checkmat = get_material_by_name(self.matname)
    if checkmat ==None:
        # マテリアルをインポート
        materials,datalist = import_materials_from_file(filepath,self.matname)
    else:
        if self.duplicate_material== True:
            materials,datalist = import_materials_from_file(filepath,self.matname)
        else:
            materials = checkmat
            datalist = None    
    append_mat(materials)
    return materials
    # print("datalist",datalist if datalist != None else "alwady scene the materia")

def uv_or_object_coordinate(self):
    if self.check_dict["Texture Coordinate"] == True:
        tree = bpy.context.object.active_material.node_tree
        lnew=tree.links.new
        output = tree.nodes["Texture Coordinate"].outputs[self.coordinate_oupttype]
        inputmain = tree.nodes['MAIN']
        input =  inputmain.inputs['Vector']
        lnew(output,input)

def option_change(self,materials):
    if self.check_dict["scalevalue"] ==  True:
        value = materials.node_tree.nodes['MAIN'].inputs['Scale'].default_value
        materials.node_tree.nodes['MAIN'].inputs['Scale'].default_value = value /self.scale_valuse
    if self.check_dict["Rotation"] ==  True:
        vecotorrotaiton = Vector((self.rotation_valuse[0],self.rotation_valuse[1],self.rotation_valuse[2]))
        materials.node_tree.nodes['MAIN'].inputs['Rotation'].default_value =vecotorrotaiton
    if self.check_dict["Smooth"] ==  True:
        materials.node_tree.nodes['Group.005'].inputs['Smooth'].default_value = self.smooth
        if bpy.context.scene.render.engine != 'CYCLES':
            bpy.context.scene.render.engine = 'CYCLES'
        if bpy.context.space_data.shading.type != 'RENDERED':
            bpy.context.space_data.shading.type = 'RENDERED'
    
def draw_main(self):
    self.layout.prop(self,"matname")
    self.layout.prop(self,"duplicate_material")
    if self.check_dict["scalevalue"] ==  True:
        self.layout.prop(self,"scale_valuse")
    if self.check_dict["Smooth"] ==  True:
        self.layout.prop(self,"smooth")
    if self.check_dict["Rotation"] ==  True:
        self.layout.prop(self,"rotation_valuse")
    if self.check_dict["Texture Coordinate"] ==  True:
        self.layout.prop(self,"coordinate_oupttype")

def material_option_cheker(self,materials):
    self.check_dict = {"scalevalue" : True,"Rotation" : True,"Texture Coordinate" : True,"Smooth" : True}

    try:
        Scale = materials.node_tree.nodes['MAIN'].inputs['Scale']
        
    except KeyError:
        self.check_dict["scalevalue"] = False
    try:
        Rotation = materials.node_tree.nodes['MAIN'].inputs['Rotation']
    except KeyError:
        self.check_dict["Rotation"] = False

    try:
        tree = materials.node_tree
        output = tree.nodes["Texture Coordinate"]
    except KeyError:
        self.check_dict["Texture Coordinate"] = False
    try:
        smooth=materials.node_tree.nodes['Group.005'].inputs['Smooth']
    except KeyError:
        self.check_dict["Smooth"] = False



    return self.check_dict

def line_num():
    import inspect
    import os

    stack = inspect.stack()
    current_file = stack[1][1]
    current_line = stack[1][2]
    script_name = os.path.basename(current_file)

    # 関数を呼び出したスタックフレームを取得し、呼び出した元の関数名を取得する
    caller_frame = stack[1].frame
    caller_method = caller_frame.f_code.co_name
    caller_methods = [caller_method]

    # スタックフレームを遡りながら呼び出した元の関数名を取得する
    while caller_frame.f_back and caller_frame.f_back.f_code.co_name != "<module>":
        caller_frame = caller_frame.f_back
        caller_method = caller_frame.f_code.co_name
        caller_methods.insert(0, caller_method)

    # '>' 区切りで親メソッド名を連結する
    caller_str = ' > '.join(caller_methods)

    return script_name + " Line: " + str(current_line) + " Caller: " + caller_str

def set_material_mode():
    bpy.context.scene.render.engine = 'CYCLES'
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'


def main(self):
    materials=check_matappend(self)
    material_option_cheker(self,materials)
    option_change(self,materials)
    uv_or_object_coordinate(self)
    set_material_mode()

def make_enum_material_list(scene, context):
    material, datalist = import_materials_from_file(filepath, "")
    matlist = []
    for index, mat in enumerate(datalist):
        matname = remove_japanese(mat)
        if matname in desired_materials:
            matlist.append((matname, matname, "", index))
    return matlist




class options:

    coorditems = [
        ("UV","UV","",1),
        ("Object","Object","",2),

        ]
    coordinate_oupttype : EnumProperty(
        items=coorditems,
        name=get_translang("Coordinate","コーディネート"),

        )
    matname : EnumProperty(
        items=make_enum_material_list,
        name='タイプ',

        )

    cmd: bpy.props.StringProperty(default="", options={'HIDDEN'})

    duplicate_material: bpy.props.BoolProperty(
                                    name=get_translang('Duplicate Material','マテリアルを複製'),
                                    default=False,
                                    )
    scale_valuse: bpy.props.FloatProperty(
                                    name=get_translang('Scale','Scale'),
                                    default=1,
                                    )
    smooth: bpy.props.FloatProperty(
                                    name=get_translang('Smooth','Smooth'),
                                    default=0.01,
                                    )
    
    rotation_valuse: bpy.props.FloatVectorProperty(
                                    name=get_translang('Rotation','Rotation'),
                                    subtype='XYZ'
                                    )

class matterialappend(Operator,options):
    bl_idname = "object.material_append"
    bl_label = get_translang("Material Append","マテリアル適応")
    bl_description = f" CLASS_NAME_IS={sys._getframe().f_code.co_name}\n ID_NAME_IS={bl_idname}\n FILENAME_IS={__file__}\n "
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        main(self)
        return {'FINISHED'}
    def draw(self, context):
        draw_main(self)
