import bpy
from libfive.stdlib import *

def set_control(s, control_name):
    control = bpy.data.objects.get(control_name)
    s = s.move(control.location)
    s = s.rotate_x(control.rotation_euler[0], control.location)
    s = s.rotate_y(-control.rotation_euler[1], control.location)
    s = s.rotate_z(control.rotation_euler[2], control.location)
    s = s.scale_xyz(control.scale, control.location)
    return s

def mesh_from_bounds(s, res, bounds_name):
    b = bpy.data.objects.get(bounds_name).scale
    bl = bpy.data.objects.get(bounds_name).location
    s = s.optimized()
    s = s.get_mesh(xyz_min=[-b[0]+bl[0],-b[1]+bl[1],-b[2]+bl[2]], 
                 xyz_max=[b[0]+bl[0],b[1]+bl[1],b[2]+bl[2]],
                  resolution=res)
    return s

def shape_on_curve(s, curve_mesh_name, blend=0.5, resize=1):
    c = bpy.data.objects.get(curve_mesh_name)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    c = c.evaluated_get(depsgraph)
    attr = c.data.attributes
    cs = emptiness()
    for index in range(len(c.data.vertices)):
        size = attr['size'].data[index].value * resize
        position = attr['position'].data[index].vector
        rotation = attr['rotation'].data[index].vector
        cs_tmp = s.move(position)
        cs_tmp = cs_tmp.rotate_x(rotation[0], position)
        cs_tmp = cs_tmp.rotate_y(-rotation[1], position)
        cs_tmp = cs_tmp.rotate_z(rotation[2], position)
        cs_tmp = cs_tmp.scale_xyz([size,size,size], position)
        cs = blend(cs, cs_tmp, blend)
    return cs