# ##### BEGIN GPL LICENSE BLOCK #####
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software Foundation,
#Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

#<pep8-80 compliant>


"""
todo:
	- integrate into wavefront addon

changelog:
	"version": (1,0,0)
		- working copy
"""

# ----------------------------------------------------------------------------#

import bpy
import os
from bpy.props import *

#addon description
bl_info = {
	"name": "import Wavefront OBJ Batch",
	"author": "Daniel Grauer (kromar)",
	"version": (1, 0, 0),
	"blender": (2, 6, 4),
	"category": "Import-Export",
    "category": "VirtaMed",
	"location": "File > Import > Wavefront (.obj) Batch",
	"description": "imports all .obj files from a selected folder",
	"warning": '',    #used for warning icon and text in addons panel
	"wiki_url": "",
	"tracker_url": "",
	}

print(80 * "-")
print("ObjBatch import")

#extension filter (alternative use mimetypes)
ext_list = ['obj'];

def LoadObjSet(filepath, filename):
	for file in os.listdir(filepath):
		#only use specified extensions
		if file.split('.')[-1].lower() in ext_list:

			bpy.ops.import_scene.obj(filepath = os.path.join(filepath, file))
			print("imported: " + file)

	print("obj Batch import finished!")

# ----------------------------------------------------------------------------#

class ObjBatchImporter(bpy.types.Operator):
	"""Load Obj Batch"""
	bl_idname = "import_mesh.objbatch"
	bl_label = "Import ObjBatch"
	bl_options =  {'PRESET'}

	filename = StringProperty(
							name = "File Name", 
							description = "filepath", 
							default = "", 
							maxlen = 1024, 
							options = {'ANIMATABLE'}, 
							subtype = 'NONE'
							)
	filepath = StringProperty(
							name = "File Name", 
							description = "filepath", 
							default = "", 
							maxlen = 1024, 
							options = {'ANIMATABLE'}, 
							subtype = 'NONE'
							)
	axis_forward = EnumProperty(
				            name="Forward",
				            items=(('X', "X Forward", ""),
				                   ('Y', "Y Forward", ""),
				                   ('Z', "Z Forward", ""),
				                   ('-X', "-X Forward", ""),
				                   ('-Y', "-Y Forward", ""),
				                   ('-Z', "-Z Forward", ""),
				                   ),
				            default='-Z',
				            )
	axis_up = EnumProperty(
				            name="Up",
				            items=(('X', "X Up", ""),
				                   ('Y', "Y Up", ""),
				                   ('Z', "Z Up", ""),
				                   ('-X', "-X Up", ""),
				                   ('-Y', "-Y Up", ""),
				                   ('-Z', "-Z Up", ""),
				                   ),
				            default='Y',
				            )
				            

	def execute(self, context):
		LoadObjSet(self.properties.filepath, self.properties.filename)
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}

# ----------------------------------------------------------------------------#

def menu_func(self, context):
	#clear the default name for import
	default_name = ""

	self.layout.operator(ObjBatchImporter.bl_idname, text = "Wavefront (.obj) Batch").filename = default_name

# ----------------------------------------------------------------------------#

def register():
	bpy.utils.register_module(__name__)
	bpy.types.INFO_MT_file_import.append(menu_func)

def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.INFO_MT_file_import.remove(menu_func)

if __name__ == "__main__":
	register()


print("initialized")
print(80 * "-")
