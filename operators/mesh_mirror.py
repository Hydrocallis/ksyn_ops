import bpy

def get_translang(eng,trans):
    prev=bpy.context.preferences.view
    if prev.language =='ja_JP' and prev.use_translate_interface == True:
         return trans
    else:
         return eng

def bicect(location,plane_no):
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(
    plane_co = location, 
    plane_no = plane_no, 
    clear_inner = False, 
    clear_outer = True, 
    flip = False)


def add_mod(self):
    mirror_mod = None
    mirmodname="ksyn_mirror"
    
    for mod in bpy.context.object.modifiers:
        if mod.name == "ksyn_mirror":
            mirror_mod = mod

    if mirror_mod ==None:
        mirror_mod = bpy.context.object.modifiers.new(name=mirmodname, type='MIRROR')
    
    mirror_mod.use_clip = True

    # reset use axis
    mirror_mod.use_axis[0] = False
    mirror_mod.use_axis[1] = False
    mirror_mod.use_axis[2] = False

    if "X" in self.axis_mirror:
        mirror_mod.use_axis[0] = True

    if "Y" in self.axis_mirror:
        mirror_mod.use_axis[1] = True

    if "Z" in self.axis_mirror:
        mirror_mod.use_axis[2] = True


    if self.applymod == True:

        if bpy.context.mode== "EDIT_MESH":
            bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.ops.object.modifier_apply(modifier=mirmodname)



def drawmain(self):
    row= self.layout.row(align=True)
    gridbox = row.box() 
    row = self.layout.row(align=True)
    rowgridbox = gridbox.grid_flow(row_major =True,columns =4, align=True)
    rowgridbox.label(text="Bisect")
    rowgridbox.prop_enum(self,"axis_bicect","X")
    rowgridbox.prop_enum(self,"axis_bicect","Y")
    rowgridbox.prop_enum(self,"axis_bicect","Z")
    rowgridbox.label(text="Reverse")
    rowgridbox.prop_enum(self,"axis_bicect_reverse","X")
    rowgridbox.prop_enum(self,"axis_bicect_reverse","Y")
    rowgridbox.prop_enum(self,"axis_bicect_reverse","Z")
    row.separator()
    row= self.layout.row(align=True)
    row.label(text="Mirror")
    row.prop_enum(self,"axis_mirror","X")
    row.prop_enum(self,"axis_mirror","Y")
    row.prop_enum(self,"axis_mirror","Z")
    row= self.layout.row(align=True)
    row.prop(self,"look_editmode")
    row= self.layout.row(align=True)
    row.prop(self,"applymod")
    



def main(self):
    editmode = str(bpy.context.mode)

    location=bpy.context.object.location.xyz
    if bpy.context.mode!= "EDIT_MESH":

        bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.select_all(action='SELECT')

    x=0
    y=0
    z=0
    plane_no =(x,y,z)


    if "X" in self.axis_bicect:
        x=1
        if "X" in self.axis_bicect_reverse:
            x=-1
        plane_no =(x,0,0)
        bicect(location,plane_no)

    if "Y" in self.axis_bicect:

        y=1
        if "Y" in self.axis_bicect_reverse:
            y=-1
        plane_no =(0,y,0)
        bicect(location,plane_no)


    if "Z" in self.axis_bicect:
        z=1
        if "Z" in self.axis_bicect_reverse:
            z=-1
        plane_no =(0,0,z)
        bicect(location,plane_no)


    add_mod(self)

    if self.look_editmode != True:
        if editmode =='EDIT_MESH':
            editmode = "EDIT"
        bpy.ops.object.mode_set(mode=editmode)
    else:
        bpy.ops.object.mode_set(mode="EDIT")






class Meshmirror_operator(bpy.types.Operator):
    bl_idname = "object.meshmirror_operator"
    bl_label = "Mesh Mirror"

    bl_options = {'REGISTER', 'UNDO'}


    axis_bicect: bpy.props.EnumProperty(
        options={"ENUM_FLAG"}, 
        items=(("X", ) * 3, ("Y",) * 3, ("Z",) * 3)
        )
    
    axis_bicect_reverse: bpy.props.EnumProperty(
        options={"ENUM_FLAG"}, 
        items=(("X", ) * 3, ("Y",) * 3, ("Z",) * 3)
        )
    

    axis_mirror: bpy.props.EnumProperty(
        options={"ENUM_FLAG"}, 
        items=(("X", ) * 3, ("Y",) * 3, ("Z",) * 3)
        )
    
    look_editmode : bpy.props.BoolProperty(name="Edit Mode")
    
    
    applymod : bpy.props.BoolProperty(name=get_translang("Apply","適応"))
    
    

    def execute(self, context):

    
        main(self)

        return {'FINISHED'}
    
    def draw(self,context):
        drawmain(self)




