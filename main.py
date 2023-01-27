from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-0.85, (1.0, 1.0, 1.0))
scene.set_background_color((0.43, 0.65, 0.85))     # set as sky color: RGB(109, 166, 217)
scene.set_directional_light((0.5, 1, -1), 0.2, (1, 0.8, 0.6))
# scene.set_directional_light((1, 1, -1), 0.2, (0.43, 0.65, 0.85))

@ti.func
def create_block(pos, size, color, color_noise):
    for I in ti.grouped(
            ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]),
                       (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.func
def create_round(center, radius, step, color, color_noise):
    for I in ti.grouped(ti.ndrange(
        (-radius, radius), (0, step), (-radius, radius)
    )):
        if vec2(I[0], I[2]).norm() < radius:
            scene.set_voxel(center + I, 1, color + color_noise * ti.random())
    
@ti.func
def create_cylinder(pos, base_radius, top_radius, step, color, color_noise):
    for i in range(base_radius - top_radius):
        create_round(pos + vec3(0, i*step, 0), base_radius - i, step, color, color_noise)

@ti.func
def create_fan_one(pos, dir, width, length, color, color_noise):
    # fans are on the top of the windmill and in YZ plane
    # decide the direction of the fan
    d_y, d_z = -1, 1
    d_w, d_l = 1, 2
    if dir == 0:    # left-bottom
        d_y,d_z = -1, 1
    elif dir == 2:  # right-top
        d_y, d_z = 1, -1

    for i in range(length):
        scene.set_voxel(pos + vec3(0, d_y*i*d_w, d_z*i*d_l), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, d_y*i*d_w, d_z*i*d_l) + vec3(0, -d_z*(width-1)*d_l, d_y*(width-1)*d_w), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, d_y*i*d_w, d_z*i*d_l+d_z), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, d_y*i*d_w, d_z*i*d_l+d_z) + vec3(0, -d_z*(width-1)*d_l, d_y*(width-1)*d_w), 1, color + color_noise * ti.random())
    for i in range(1, width):
        scene.set_voxel(pos + vec3(0, -d_z*i*d_l, d_y*i*d_w), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, -d_z*i*d_l, d_y*i*d_w) + vec3(0, d_y*length*d_w-d_y, d_z*length*d_l), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, -d_z*i*d_l+d_z, d_y*i*d_w), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, -d_z*i*d_l+d_z, d_y*i*d_w) + vec3(0, d_y*length*d_w-d_y, d_z*length*d_l), 1, color + color_noise * ti.random())
   
@ti.func
def create_fan_two(pos, dir, width, length, color, color_noise): 
    d_y, d_z = -1, 1
    d_w, d_l = 1, 2
    if dir == 1:    # left-bottom
        d_y,d_z = -1, -1
    elif dir == 3:  # right-top
        d_y, d_z = 1, 1
        
    for i in range(length):
        scene.set_voxel(pos + vec3(0, d_y*i*d_l, d_z*i*d_w), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, d_y*i*d_l, d_z*i*d_w) + vec3(0, -d_z*(width-1)*d_w, d_y*(width-1)*d_l), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, d_y*i*d_l+d_y, d_z*i*d_w), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, d_y*i*d_l+d_y, d_z*i*d_w) + vec3(0, -d_z*(width-1)*d_w, d_y*(width-1)*d_l), 1, color + color_noise * ti.random())
        
    for i in range(1, width):
        scene.set_voxel(pos + vec3(0, -d_z*i*d_w, d_y*i*d_l), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, -d_z*i*d_w, d_y*i*d_l) + vec3(0, d_y*length*d_l, d_z*length*d_w-d_z), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, -d_z*i*d_w, d_y*i*d_l-d_y), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + vec3(0, -d_z*i*d_w, d_y*i*d_l-d_y) + vec3(0, d_y*length*d_l, d_z*length*d_w-d_z), 1, color + color_noise * ti.random())

@ti.func
def create_window(pos, width, height, color, color_noise):
    for i in range(width):
        scene.set_voxel(pos + ivec3(0, 0, i), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + ivec3(0, height-1, i), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + ivec3(0, height+1, i), 1, color + color_noise * ti.random())
    for i in range(1, height-1):
        scene.set_voxel(pos + ivec3(0, i, 0), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + ivec3(0, i, width-1), 1, color + color_noise * ti.random())
    for i in range(-1, width+1):
        scene.set_voxel(pos + ivec3(0, height, i), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + ivec3(1, height, i), 1, color + color_noise * ti.random())
    for i, j in ti.ndrange((1, height-1), (1, width-1)):
        scene.set_voxel(pos + ivec3(0, i, j), 1, vec3(0.20)+vec3(0.10)*ti.random()) # set the inside of the window RGB (139, 155, 176)

@ti.func
def create_bracket(pos, len, color, color_noise):
    for i in range(2*len+1):    # create the bracket in YZ plane
        scene.set_voxel(pos + ivec3(0, 0, -len+i), 1, color + color_noise * ti.random())
        scene.set_voxel(pos + ivec3(0, -len+i, 0), 1, color + color_noise * ti.random())
    for i, j in ti.ndrange((-1, 2), (-1, 2)):    # create the bracket in XY plane
        scene.set_voxel(pos + ivec3(0, i, j), 1, color + color_noise * ti.random())
    for k, i, j in ti.ndrange((-4, -1), (-1, 2), (-1, 2)):
        scene.set_voxel(pos + ivec3(k, i, j), 1, color + color_noise * ti.random())
    for i in range(-1, 2):
        scene.set_voxel(pos + ivec3(i, 0, 0), 1, vec3(0))
     
@ti.func 
def create_windmill(pos, base_radius, top_radius, tower_step, color_pillar, color_window, color_hat, color_fan):
    create_cylinder(pos, base_radius, top_radius, tower_step, color_pillar, vec3(0.3))
    create_cylinder(pos+ivec3(0, tower_step*(base_radius - top_radius), 0), top_radius+2, 1, 1, color_hat, vec3(0.15))
    
    tower_height = tower_step*(base_radius - top_radius) + 1  # calculate tower height
    create_bracket(pos+ivec3(11, tower_height, 0), 3, vec3(0.05), vec3(0.00))
    
    create_fan_one(pos+ivec3(11, tower_height+2, 4), 0, 3, 9, vec3(0.0), vec3(0.0))
    create_fan_one(pos+ivec3(11, tower_height-2, -4), 2, 3, 9, vec3(0.0), vec3(0.0))
    create_fan_two(pos+ivec3(11, tower_height-5, +1), 1, 3, 9, vec3(0.0), vec3(0.0))
    create_fan_two(pos+ivec3(11, tower_height+5, -1), 3, 3, 9, vec3(0.0), vec3(0.0))
    
    window1_height = tower_step*(base_radius - top_radius - 2) + 1
    window2_height = tower_step*(base_radius - top_radius - 4) + 1
    create_window(pos+ivec3(8, window1_height, -3), 5, 5, color_window, vec3(0.0))
    create_window(pos+ivec3(10, window2_height, -3), 5, 5, color_window, vec3(0.0))
        
@ti.func
def create_sand_rock(pos, color_sand, color_rock):
    height = pos[1]
    for i, j in ti.ndrange((-60, 60), (-60, 60)):
        if ti.random(float) < 0.006:
            scene.set_voxel(ivec3(i, height, j), 1, color_sand)
    for i in range(8):
        x = int(ti.random(float) * 120 - 60)
        z = int(ti.random(float) * 120 - 60)
        
        center = ivec3(x, height+1, z)
        radius = ti.random(int)%4+2
        for I in ti.grouped(ti.ndrange((-8, 8), (-8, 8), (-8, 8))):
            if vec3(I).norm() < radius:
                scene.set_voxel(I+center, 1, color_rock)
            elif vec3(I).norm() == radius:
                if ti.random(float) < 0.5:
                    scene.set_voxel(I+center, 1, color_rock)
                   
@ti.func
def create_sealine(height, color_waves, color_sea, shore=1):
    # shore1: x = 15 * sin(2*pi*z/150) + 0.15*z
    # shore2: x = 20 * sin(2*pi*z/120) + 0.20*z
    for z in range(-60, 60):
        x = z
        if shore == 1:
            x = 15*ti.sin(2*pi*(z+60)/160)+0.3*(z+60)-10
        else:
            x = 20*ti.sin(2*pi*(z+60)/200)+0.4*(z+60)+10
        scene.set_voxel(ivec3(x, height, z), 1, color_waves)
        # set sea level
        for i in range(x+1, 60):
            scene.set_voxel(ivec3(i, height, z), 1, color_sea)
        # set waves    
        for i in range(-60, x):
            if ti.random(float)*((x-i)**2) < 1:
                scene.set_voxel(ivec3(i, height, z), 1, color_waves)
        for I in ti.grouped(ti.ndrange((-2,3),(-2,3),(-2,3))):
            if ti.random(float)*(ivec3(I).norm()**4) < 0.4:
                scene.set_voxel(ivec3(x ,height, z)+I, 1, color_waves)
    
@ti.kernel
def initialize_voxels():
    for i in range(4):
        create_block(ivec3(-60, -(i + 1)**2 - 40, -60),
                     ivec3(120, 2 * i + 1, 120),
                     vec3(0.5 - i * 0.1) * vec3(1.0, 0.8, 0.6),
                     vec3(0.05 * (3 - i)))

    # create sand RGB(244, 205, 109)
    create_block(ivec3(-60, -40, -60), ivec3(120, 1, 120), vec3(0.65, 0.65, 0.35), vec3(0))
    create_sand_rock(ivec3(-60, -39, -60), color_sand=vec3(0.65, 0.65, 0.35), color_rock=vec3(0.26))
    # the floor is on -40
    create_windmill(ivec3(-25, -39, -20), 12, 6, 6, vec3(0.7), vec3(0.00, 0.61, 0.93), vec3(0.05), vec3(0.9))
    # waves RGB(165, 202, 239)      sea RGB(0, 84, 181)
    create_sealine(-39, vec3(0.65, 0.79, 0.94), vec3(0.0, 0.33, 0.71))
    create_sealine(-38, vec3(0.65, 0.79, 0.94), vec3(0.0, 0.33, 0.71),2)

initialize_voxels()

scene.finish()