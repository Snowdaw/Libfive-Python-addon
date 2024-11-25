bl_info = {
    "name": "Python Libfive binaries",
    "blender": (4, 3, 0),
    "category": "Python utility",
}

import bpy, sys
from os import path


def menu_func(self, context):
    self.layout.operator(ObjectMoveX.bl_idname)

def register():
    current_dir = path.dirname(path.realpath(__file__))
    lib_dir = path.join(current_dir, "")
    if lib_dir not in sys.path: sys.path.append(lib_dir)

def unregister():
    current_dir = path.dirname(path.realpath(__file__))
    lib_dir = path.join(current_dir, "")
    if lib_dir in sys.path: sys.path.remove(lib_dir)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
