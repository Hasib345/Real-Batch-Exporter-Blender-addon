# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "RB_Export",
    "author": "Hasib345",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "location": "View3D > N-Panel > RB_Export ",
    "description": "Addon to allow batch export in different formates",
    "category": 'Batch Export'}

import bpy
from bpy.props import BoolProperty, BoolVectorProperty, FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, EnumProperty, StringProperty, PointerProperty

class RB_ExportOperator(bpy.types.Operator):
    """ToolTip of RB_ExportOperator"""
    bl_idname = "addongen.rb_export_operator"
    bl_label = "RB_Export Operator"
    bl_options = {'REGISTER'}


    #@classmethod
    #def poll(cls, context):
    #    return context.object is not None

    def execute(self, context):
        Rb = context.preferences.addons[__name__].preferences
        file_path = Rb.file_path+Rb.file_name
        textures = Rb.file_path+Rb.textures
        triangulate = Rb.file_path+Rb.triangulate
        apply_modifiers = Rb.file_path+Rb.apply_modifiers
        selection = Rb.file_path+Rb.selection

        if Rb.dae:
            bpy.ops.wm.collada_export(filepath=file_path,use_texture_copies = textures ,
                                      apply_global_orientation = apply_modifiers , selected=selection,
                                      triangulate =triangulate)
            self.report({'INFO'}, "Collada Exported!")
        if Rb.abc:
            bpy.ops.wm.alembic_export(filepath=file_path+'.abc', selected=selection, triangulate=triangulate)
            self.report({'INFO'}, "Alembic Exported!")
        if Rb.usd:
            bpy.ops.wm.usd_export(filepath=file_path+'.usd', selected_objects_only=selection,  export_textures=textures)
            self.report({'INFO'}, "USD Exported!")
        if Rb.obj:
            bpy.ops.wm.obj_export(filepath=file_path+'.obj', apply_modifiers=apply_modifiers, export_selected_objects=selection, 
                                export_pbr_extensions=textures, 
                                export_triangulated_mesh=triangulate)
            self.report({'INFO'}, "Obj Exported!")

        if Rb.ply:
            bpy.ops.wm.ply_export(filepath=file_path+'.ply', apply_modifiers=apply_modifiers, export_selected_objects=selection, 
                                export_triangulated_mesh=triangulate)
            self.report({'INFO'}, "Ply Exported!")
        if Rb.stl:
            bpy.ops.export_mesh.stl(filepath=file_path+'.stl', use_selection=selection, use_mesh_modifiers=apply_modifiers, )
            self.report({'INFO'}, "Stl Exported!")
        if Rb.fbx:
            bpy.ops.export_scene.fbx(filepath=file_path+'.fbx', use_selection=selection, use_mesh_modifiers=apply_modifiers,   
            use_triangles=triangulate, embed_textures=textures)
            self.report({'INFO'}, "Fbx Exported!")
        if Rb.gbl:
            bpy.ops.export_scene.gltf( filepath=file_path, export_format='GLTF_EMBEDDED',
                                  use_selection = selection )
            self.report({'INFO'}, "gltf Exported!")
        if Rb.x3d:
            bpy.ops.export_scene.x3d(filepath=file_path+'.x3d', use_selection=selection, use_mesh_modifiers=apply_modifiers, use_triangulate=triangulate)
            self.report({'INFO'}, "X3d Exported!")


        self.report({'INFO'}, "All Files Exported!")


        return {'FINISHED'}

    #def invoke(self, context, event):
    #    wm.modal_handler_add(self)
    #    return {'RUNNING_MODAL'}
    #    return wm.invoke_porps_dialog(self)
    #def modal(self, context, event):
    #def draw(self, context):

class RB_ExportPanel(bpy.types.Panel):
    """Docstring of RB_ExportPanel"""
    bl_idname = "VIEW3D_PT_rb_export"
    bl_label = "RB_Export Panel"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category= 'RB_Export'

    #Panels in ImageEditor are using .poll() instead of bl_context.
    #@classmethod
    #def poll(cls, context):
    #    return context.space_data.show_paint

    def draw(self, context):
        layout = self.layout
        Rb = context.preferences.addons[__name__].preferences
        
        row = layout.row(align = True)
        row.prop(Rb , 'fbx' , toggle = True)
        row.prop(Rb , 'dae', toggle = True)
        
        row = layout.row(align = True)
        row.prop(Rb , 'abc', toggle = True)
        row.prop(Rb , 'usd', toggle = True)
        
        row = layout.row(align = True)
        row.prop(Rb , 'obj', toggle = True)
        row.prop(Rb , 'ply', toggle = True)
        
        row = layout.row(align = True)
        row.prop(Rb , 'stl', toggle = True)
        row.prop(Rb , 'gbl', toggle = True)
        
        row = layout.row(align = True)
        row.prop(Rb , 'x3d', toggle = True)
        

        row = layout.row(align = True)
        row.label(text='File Name')
        row.prop(Rb , 'file_name')
        
        row = layout.row(align = True)
        row.label(text='File Path')
        row = layout.row(align = True)
        row.prop(Rb , 'file_path')

        if Rb.batch_export_op:
            ic = 'RIGHTARROW'
        else:
            ic  = 'DOWNARROW_HLT'
        col = layout.column()
        col.prop(Rb , 'batch_export_op' , icon= ic)
        if Rb.batch_export_op:
            col.prop(Rb , 'textures' ,toggle = True)
            col.prop(Rb , 'triangulate',toggle = True )
            col.prop(Rb , 'apply_modifiers' ,toggle = True)
            col.prop(Rb , 'selection' , toggle = True)

        
        layout.operator(RB_ExportOperator.bl_idname, text = "Batch Export", icon = 'SEQ_STRIP_DUPLICATE')
        
        
class RB_ExportProps(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    
    fbx:BoolProperty(name="Fbx", description="", default=False)
    dae:BoolProperty(name="Dae", description="", default=False)
    abc:BoolProperty(name="Abc", description="", default=False)
    usd:BoolProperty(name="Usd", description="", default=False)
    obj:BoolProperty(name="Obj", description="", default=False)
    ply:BoolProperty(name="Ply", description="", default=False)
    stl:BoolProperty(name="Stl", description="", default=False)
    gbl:BoolProperty(name="gbl", description="", default=False)
    x3d:BoolProperty(name="x3d", description="", default=False)
    batch_export_op:BoolProperty(name="Batch Export Options", description="", default=False)
    triangulate:BoolProperty(name="Triangulate", description="", default=False)
    apply_modifiers:BoolProperty(name="Apply Modifiers", description="", default=False)
    selection:BoolProperty(name="Export Selection", description="", default=False)
    
    
    file_path:bpy.props.StringProperty(name = "", default = "", subtype = 'DIR_PATH')
    
    file_name:bpy.props.StringProperty(name = "", default = "", subtype = 'FILE_NAME')

    textures : BoolProperty(name="Export Textures", description="", default=False)



        

        
    



def register():
    bpy.utils.register_class(RB_ExportOperator)
    bpy.utils.register_class(RB_ExportProps)
    bpy.utils.register_class(RB_ExportPanel)
    

def unregister():
    bpy.utils.unregister_class(RB_ExportOperator)
    bpy.utils.unregister_class(RB_ExportPanel)
    bpy.utils.unregister_class(RB_ExportProps)

if __name__ == "__main__":
    register()
