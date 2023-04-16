import bpy

def set_data():

    editmode =   bpy.context.mode
    if editmode == "EDIT_MESH":
        editmode = "EDIT"
    coursorloc = bpy.context.scene.cursor.location.xyz

    return editmode, coursorloc

 
def set_ops(editmode, coursorloc):

    area = next((a for a in bpy.context.screen.areas if a.type == "VIEW_3D"), None)
    if area is not None:
        with bpy.context.temp_override(area=area):
            bpy.ops.view3d.snap_cursor_to_selected()


    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    bpy.ops.object.mode_set(mode = editmode)


    bpy.context.scene.cursor.location = coursorloc 


def orijinset():
    editmode, coursorloc = set_data()

    set_ops(editmode, coursorloc)