import bpy
import math
import os
from mathutils import Vector


ROOT = "/Volumes/Data/owncloud/root/research/articles/timesarrow/blender"
OUTPUT = os.path.join(ROOT, "renders", "quantum_geometry_v3")
FRAMES_DIR = os.path.join(OUTPUT, "frames")
BLEND_PATH = os.path.join(ROOT, "quantum_geometry_v3.blend")
VIDEO_PATH = os.path.join(OUTPUT, "z2_link_flip_v3.mp4")


def emission_material(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeEmission")
    shader.inputs["Color"].default_value = (*color, 1.0)
    shader.inputs["Strength"].default_value = strength
    links.new(shader.outputs[0], output.inputs[0])
    return mat, shader


def animate_strength(shader, keys):
    for frame, strength in keys:
        shader.inputs["Strength"].default_value = strength
        shader.inputs["Strength"].keyframe_insert(data_path="default_value", frame=frame)


def animate_color(shader, keys):
    for frame, color in keys:
        shader.inputs["Color"].default_value = (*color, 1.0)
        shader.inputs["Color"].keyframe_insert(data_path="default_value", frame=frame)


def curve_line(name, start, end, mat, thickness=0.035, z_offset=0.0):
    start = Vector(start)
    end = Vector(end)
    start.z += z_offset
    end.z += z_offset
    midpoint = (start + end) * 0.5
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.bevel_depth = thickness
    data.bevel_resolution = 3
    spline = data.splines.new("POLY")
    spline.points.add(1)
    spline.points[0].co = (*(start - midpoint), 1.0)
    spline.points[1].co = (*(end - midpoint), 1.0)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = midpoint
    data.materials.append(mat)
    return obj


def curve_loop(name, points, mat, thickness=0.045, z_offset=0.0):
    adjusted = [(x, y, z + z_offset) for x, y, z in points]
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.bevel_depth = thickness
    data.bevel_resolution = 3
    spline = data.splines.new("POLY")
    spline.points.add(len(adjusted) - 1)
    for point, value in zip(spline.points, adjusted):
        point.co = (*value, 1.0)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(mat)
    return obj


def sphere(name, location, radius, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=20, ring_count=12, radius=radius, location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj


def arrowhead(name, location, direction, mat, size=0.17):
    bpy.ops.mesh.primitive_cone_add(
        vertices=4,
        radius1=size,
        radius2=0.0,
        depth=size * 2.2,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    obj.rotation_mode = "QUATERNION"
    obj.rotation_quaternion = Vector(direction).normalized().to_track_quat("Z", "Y")
    return obj


def scale_keys(obj, keys):
    for frame, value in keys:
        obj.scale = (value, value, value)
        obj.keyframe_insert(data_path="scale", frame=frame)


def add_text(body, location, size, mat, camera):
    data = bpy.data.curves.new(body, "FONT")
    data.body = body
    data.align_x = "CENTER"
    data.size = size
    data.extrude = 0.004
    obj = bpy.data.objects.new(body, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(camera.location) - obj.location).to_track_quat("Z", "Y").to_euler()
    data.materials.append(mat)
    return obj


def build_scene():
    os.makedirs(FRAMES_DIR, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    positive_color = (0.04, 0.5, 1.0)
    flipped_color = (0.9, 0.04, 0.4)
    cyan, cyan_shader = emission_material("StablePositiveLinks", positive_color, 4.0)
    gold, gold_shader = emission_material("CentralVertex", (1.0, 0.5, 0.04), 5.0)
    white, white_shader = emission_material("LoopHighlight", (0.8, 0.95, 1.0), 5.0)
    pulse_mat, pulse_shader = emission_material("FlipPulse", (1.0, 0.82, 0.15), 6.0)
    text_mat, text_shader = emission_material("ExplanatoryText", (0.65, 0.88, 1.0), 2.2)
    node_mat, node_shader = emission_material("NeighborVertices", (0.45, 0.65, 1.0), 1.8)

    # Camera first so text can face it.
    bpy.ops.object.camera_add(location=(0.0, -10.0, 9.5))
    camera = bpy.context.object
    camera.name = "Z2FlipCamera"
    camera.data.lens = 53
    camera.rotation_euler = (Vector((0.0, 0.0, 0.0)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = camera

    positions = {}
    for x in range(-1, 2):
        for y in range(-1, 2):
            positions[(x, y)] = Vector((x * 1.8, y * 1.8, 0.0))

    # Vertices of the small lattice.
    for key, position in positions.items():
        mat = gold if key == (0, 0) else node_mat
        radius = 0.19 if key == (0, 0) else 0.13
        node = sphere("CentralVertex" if key == (0, 0) else "NeighborVertex", position, radius, mat)
        if key == (0, 0):
            scale_keys(node, [(1, 1.0), (72, 1.0), (88, 1.35), (104, 1.0), (192, 1.0)])

    # Links; only the four links incident on the central vertex flip.
    for (x, y), start in positions.items():
        for neighbor in ((x + 1, y), (x, y + 1)):
            if neighbor not in positions:
                continue
            end = positions[neighbor]
            touches_center = (x, y) == (0, 0) or neighbor == (0, 0)
            if not touches_center:
                curve_line("StableLink", start, end, cyan, 0.035)
                continue

            other = end if (x, y) == (0, 0) else start
            outward = (other - positions[(0, 0)]).normalized()
            midpoint = (start + end) * 0.5

            state_mat, state_shader = emission_material("FlippingLinkState", positive_color, 4.5)
            animate_color(
                state_shader,
                [(1, positive_color), (88, positive_color), (108, flipped_color), (192, flipped_color)],
            )
            curve_line("FlippingLink", start, end, state_mat, 0.045, z_offset=0.012)

            arrow = arrowhead(
                "LinkStateArrow",
                midpoint + outward * 0.04 + Vector((0, 0, 0.07)),
                outward,
                state_mat,
                size=0.20,
            )
            arrow.rotation_quaternion = outward.to_track_quat("Z", "Y")
            arrow.keyframe_insert(data_path="rotation_quaternion", frame=88)
            arrow.rotation_quaternion = (-outward).to_track_quat("Z", "Y")
            arrow.keyframe_insert(data_path="rotation_quaternion", frame=108)

    # Highlight the upper-right plaquette after the flip.
    c = positions[(0, 0)]
    top = positions[(0, 1)]
    top_right = positions[(1, 1)]
    right = positions[(1, 0)]
    loop = curve_loop("GaugeInvariantPlaquette", [tuple(c), tuple(top), tuple(top_right), tuple(right), tuple(c)], white, 0.05, 0.08)
    scale_keys(loop, [(1, 0.001), (124, 0.001), (140, 1.0), (192, 1.0)])

    # A pulse at the transformed vertex makes the local operation legible.
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.34,
        minor_radius=0.035,
        major_segments=48,
        minor_segments=8,
        location=(0.0, 0.0, 0.16),
    )
    pulse = bpy.context.object
    pulse.name = "LocalFlipPulse"
    pulse.data.materials.append(pulse_mat)
    scale_keys(pulse, [(1, 0.05), (68, 0.05), (90, 1.0), (111, 0.05), (192, 0.05)])

    local_text = add_text("LOCAL Z2 FLIP", (0.0, -3.15, 0.0), 0.38, text_mat, camera)
    scale_keys(local_text, [(1, 0.001), (62, 0.001), (74, 1.0), (114, 1.0), (130, 0.001), (192, 0.001)])

    loop_text = add_text("PLAQUETTE PRODUCT: +1  ->  +1", (0.65, 2.72, 0.0), 0.27, text_mat, camera)
    scale_keys(loop_text, [(1, 0.001), (145, 0.001), (160, 1.0), (192, 1.0)])

    # World and render settings.
    world = bpy.context.scene.world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.002, 0.006, 0.025, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.06

    bpy.ops.object.light_add(type="AREA", location=(1.5, -3.5, 7.5))
    light = bpy.context.object
    light.data.energy = 500
    light.data.size = 5
    light.rotation_euler = (Vector((0, 0, 0)) - light.location).to_track_quat("-Z", "Y").to_euler()

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 192
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.fps = 24

    for action in bpy.data.actions:
        for fcurve in action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = "BEZIER"

    captures = [
        (24, "01_initial_link_states"),
        (72, "02_local_flip_selected"),
        (96, "03_flip_propagating"),
        (120, "04_links_flipped"),
        (140, "05_loop_highlighted"),
        (192, "06_gauge_invariant_result"),
    ]
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    scene.render.image_settings.file_format = "PNG"
    for frame, name in captures:
        scene.frame_set(frame)
        scene.render.filepath = os.path.join(FRAMES_DIR, name + ".png")
        bpy.ops.render.render(write_still=True)

    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    scene.render.filepath = VIDEO_PATH
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    bpy.ops.render.render(animation=True)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)


if __name__ == "__main__":
    build_scene()
