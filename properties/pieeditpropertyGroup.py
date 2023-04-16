
import bpy, sys, pathlib,re
from ..utils.englishname_trans import remove_japanese

from bpy.types import (
        Menu,
        Operator,
        Panel,
        PropertyGroup,
        )


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

def get_translang(eng,trans):
    prev = bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
        return trans
    else:
        return eng


def get_object_list_materialst(scene, context):
    index_obj_imagelist =enumerate(bpy.data.images)
    imagelist=[]
    for index,image in index_obj_imagelist:
        try:
            engjpimage=remove_japanese(image.name)
            if image.name =='Render Result' or image.name == 'Viewer Node':
                pass
            elif image.name != engjpimage:
                pass
            else:
                imagelist.append((image.name,engjpimage,image.name,index))
        except AttributeError:
            pass
    return imagelist


class fileexportbakeing():
    # (識別子, UI表示名, 説明文)
    bake_types = (
  
    ("COMBINED", "COMBINED", "", 1),
    ("DIFFUSE", "DIFFUSE", "", 2),
    ("NORMAL", "NORMAL", "", 3),
        )
    extentionitem = (
  
    (".png", "PNG", "", 1),
    (".jpg", "JPEG", "", 2),
        )
    
    image_sizeitems = (
  
    ("128", "128", "", 1),
    ("256", "256", "", 2),
    ("512", "512", "", 3),
    ("1024", "1024", "", 4),
    ("2048", "2048", "", 5),
    ("4096", "4096", "", 6),
        )
    


    bake_type : EnumProperty(
            name = "Bake Type",
            items = bake_types
            )
    
    filename_ext : EnumProperty(
            name = get_translang('Extension','拡張子'),
            items = extentionitem
            )
    
    image_sizes: bpy.props.EnumProperty(

        name=get_translang('Bake Image sizes','ベイク画像の大きさ'),
        items=image_sizeitems,
        default='1024',
        # options={'HIDDEN'}
    )
    savescale: bpy.props.EnumProperty(

        name=get_translang('Image sizes','保存画像の大きさ'),
        items=image_sizeitems,
        default='1024',
        # options={'HIDDEN'}
    )

    imagelist: bpy.props.EnumProperty(

        name=get_translang('Image sizes','ベイク先画像ノードがあるマテリアル'),
        items=get_object_list_materialst,
        # default='1024',
        
        # options={'HIDDEN'}
    )

    #     # 
    fullpath : bpy.props.StringProperty(
        name="fullpath",
        default="",
        options={'HIDDEN'}
        )

    samples : IntProperty(name="Samples",default=8, min=0,)
    margin : IntProperty(name="Margin",default=16, min=0,subtype="PIXEL",)
    quality : IntProperty(name="Quality",default=90, min=0, max=100,subtype="PERCENTAGE",)
    compression : IntProperty(name="Compression",default=15, min=0, max=100,subtype="PERCENTAGE",)
    add_mat_name : BoolProperty(name=get_translang('Add material name','ベイク画像にマテリアルネームを追加'))
    Bake_to_existing_node_texture : BoolProperty(name=get_translang('Bake to existing node texture','既存のノードテクスチャにベイクする'))
    trans_lang_english : BoolProperty(name=get_translang('Convert file names to English words only.','ファイル名を英単語のみ変換しておく。'))
    use_pass_direct : BoolProperty(name="Direct",default=False)
    use_pass_indirect : BoolProperty(name="Indirect",default=False)
    

 
class MyEDITPIEPropertyGroup(PropertyGroup,fileexportbakeing):
    # インスタンスミラーのXかYかのブール
    axis = (
        ("X", "X-axis", ""),      # (識別子, UI表示名, 説明文)
        ("Y", "Y-axis", ""),
        ("Z", "Z-axis", ""))

    transform_axis : EnumProperty(
        name = "Transform Axis",          # 名称
        description = "Transform Axis",   # 説明文
        items = axis)  
 
   
    # クリースを分かりやすくするためのブール
    def crease_themasupdate(self, context):

        if self.crease_themas_bool == False:
            color=(0.875, 0, 0.6) # default color
        else:
            color=(0, 0, 0) # black color
           
        context.preferences.themes['Default'].view_3d.edge_crease = color

           
    crease_themas_bool : BoolProperty(
                name = "crease_themas_bool",
                default = False,
                update = crease_themasupdate,
                                )
 


    # グリッドマテリアル生成用の
    uv_pie_selct_bool : BoolProperty(
                name = "uv_pie_selct_bool",
                default = False
                                )

    uv_grid_material_image_bool : BoolProperty(
                name = "uv_grid_material_image_bool",
                default = True
                                )

    uv_grid_material_duplicate_bool : BoolProperty(
                name = "uv_grid_material_duplicate_bool",
                default = False
                                )

    # blend_file_path = bpy.data.filepath
    # blend_directory = os.path.dirname(blend_file_path)
    # blender_fbxfilename = bpy.path.basename(bpy.context.blend_data.filepath).replace(".blend","")
    def uv_grid_scail_size_float_update(self, context):
        props = context.scene.myedit_property_group
        # print('###test',props.uv_grid_scail_size)
        gridscal = props.uv_grid_scail_size
        if "UVGRID" in bpy.context.object.data.materials[0].name:
            # bpy.context.object.data.materials[0].node_tree.nodes["Mapping"].inputs[3].default_value = (gridscal, gridscal, gridscal)
      
            bpy.context.object.data.materials[0].node_tree.nodes['cus-Mapping'].inputs['Scale'].default_value = (gridscal, gridscal, gridscal)
      
    uv_grid_scail_size : FloatProperty(
                name="uv_grid_scail_size",
                description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}\n FILENAME_IS={__file__}\n',# 説明文
                default= 0,
                # hard_max= 100,
                # hard_min = 0,
                update = uv_grid_scail_size_float_update,
                )


    # 選択したオブジェクトの色用の
    color_pic : FloatVectorProperty(
                 name = "Color Picker",
                 subtype = "COLOR",
                 size = 4,
                 min = 0.0,
                 max = 1.0,
                 default = (1.0,1.0,1.0,1.0))


    edit_int : IntProperty(
                name="int1",     # 変数名
                description = f' CLASS_NAME_IS={sys._getframe().f_code.co_name}\n FILENAME_IS={__file__}\n',# 説明文
                default=0,             # デフォルト値
                min=0,                 # 最小値
                max=20,                # 最大値
             
                            )
    # レストとポーズの入れ替え用のプロパティ
    def update_func(self, context):
        pass
        # print("my test function", self)

    def armature_poll(self, object):

        return object.type == 'ARMATURE'


    target_armature : PointerProperty(
                type = bpy.types.Object, name = "Armature", 
                update = update_func, 
                poll=armature_poll
                                                )
    
    fileexportbakeing()


