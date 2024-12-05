bl_info = {
    "name": "SD5",
    "blender": (4, 3, 0),
    "category": "Python utility",
}

import bpy, sys
from os import path
from bpy.app.handlers import persistent


@persistent
def sd5_handler(scene, depsgraph):

    sd5_texts = []
    for sd5_text in bpy.data.texts:
        if sd5_text.name.startswith("SD5_"):
            sd5_texts.append(sd5_text)
    if not sd5_texts:
        return
    else:
        for sd5_script in sd5_texts:
            sd5_namespace = {}
            exec(sd5_script.as_string(), sd5_namespace)
            sd5_name = sd5_namespace["sd5"].name
            sd5_mesh = sd5_namespace["sd5"].mesh
            
            if bpy.data.objects.get(sd5_name) and bpy.data.objects.get(sd5_name).select_get():
                return
            
            del_mesh = None
            for temp_mesh in bpy.data.meshes:
                temp_name = sd5_name + "_TEMP"
                if temp_name in temp_mesh.name or sd5_name + "." in temp_mesh.name:
                    temp_mesh.name = temp_name + "_DELETE"
                    del_mesh = temp_mesh
            
            temp_mesh = bpy.data.meshes.new(sd5_name + "_TEMP")
            temp_obj = bpy.data.objects.get(sd5_name)
    
            if temp_obj == None:
                temp_obj = bpy.data.objects.new(sd5_name, temp_mesh)
                if not bpy.data.collections.get("SD5"):
                    sd5_collection = bpy.data.collections.new("SD5")
                    bpy.data.scenes["Scene"].collection.children.link(sd5_collection)
                bpy.data.collections["SD5"].objects.link(temp_obj)
    
            temp_mesh.from_pydata(sd5_mesh[0], [], sd5_mesh[1], shade_flat=False)
            temp_obj.data = temp_mesh
            temp_mesh.name = sd5_name
            if del_mesh:
                bpy.data.meshes.remove(del_mesh)
    return

def register():
    current_dir = path.dirname(path.realpath(__file__))
    lib_dir = path.join(current_dir, "")
    if lib_dir not in sys.path: sys.path.append(lib_dir)
    bpy.app.handlers.depsgraph_update_post.append(sd5_handler)


def unregister():
    for handler in bpy.app.handlers.depsgraph_update_post:
        if handler.__name__ == "sd5_handler":
            bpy.app.handlers.depsgraph_update_post.remove(handler)
    bpy.app.handlers.depsgraph_update_post
    current_dir = path.dirname(path.realpath(__file__))
    lib_dir = path.join(current_dir, "")
    if lib_dir in sys.path: sys.path.remove(lib_dir)


if __name__ == "__main__":
    register()
