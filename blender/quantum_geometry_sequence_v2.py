import bpy
import math
import os
from mathutils import Vector


ROOT = "/Volumes/Data/owncloud/root/research/articles/timesarrow/blender"
OUTPUT = os.path.join(ROOT, "renders", "quantum_geometry_v2")
FRAMES_DIR = os.path.join(OUTPUT, "frames")
BLEND_PATH = os.path.join(ROOT, "quantum_geometry_v2.blend")
VIDEO_PATH = os.path.join(OUTPUT, "quantum_geometry_v2.mp4")


def emission_material(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*color, 1.0)
    emission.inputs["Strength"].default_value = strength
    links.new(emission.outputs[0], output.inputs[0])
    return mat, emission


def set_strength(shader, values):
    for frame, strength in values:
        shader.inputs["Strength"].default_value = strength
        shader.inputs["Strength"].keyframe_insert(data_path="default_value", frame=frame)


def curve_line(name, start, end, mat, thickness=0.025):
    start = Vector(start)
    end = Vector(end)
    midpoint = (start + end) * 0.5
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.bevel_depth = thickness
    data.bevel_resolution = 2
    spline = data.splines.new("POLY")
    spline.points.add(1)
    spline.points[0].co = (*(start - midpoint), 1.0)
    spline.points[1].co = (*(end - midpoint), 1.0)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = midpoint
    data.materials.append(mat)
    return obj


def polyline(name, points, mat, thickness=0.012):
    data = bpy.data.curves.new(name, "CURVE")
    data.dimensions = "3D"
    data.bevel_depth = thickness
    data.bevel_resolution = 2
    spline = data.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for point, value in zip(spline.points, points):
        point.co = (*value, 1.0)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(mat)
    return obj


def sphere(name, location, radius, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16, ring_count=8, radius=radius, location=location
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return obj


def animate_scale(obj, keys):
    for frame, scale in keys:
        obj.scale = (scale, scale, scale)
        obj.keyframe_insert(data_path="scale", frame=frame)


def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def tetrahedron(name, location, face_mat, edge_mat, size=0.72):
    vertices = [
        (size, size, size),
        (size, -size, -size),
        (-size, size, -size),
        (-size, -size, size),
    ]
    faces = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2)]
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    mesh.materials.append(face_mat)

    for index, (a, b) in enumerate([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]):
        data = bpy.data.curves.new(name + "_Edge_" + str(index), "CURVE")
        data.dimensions = "3D"
        data.bevel_depth = 0.028
        data.bevel_resolution = 2
        spline = data.splines.new("POLY")
        spline.points.add(1)
        spline.points[0].co = (*vertices[a], 1.0)
        spline.points[1].co = (*vertices[b], 1.0)
        edge = bpy.data.objects.new(name + "_Edge_" + str(index), data)
        bpy.context.collection.objects.link(edge)
        data.materials.append(edge_mat)
        edge.parent = obj
        edge.location = (0.0, 0.0, 0.0)
    return obj


def build_scene():
    os.makedirs(FRAMES_DIR, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    grid_mat, grid_shader = emission_material("SmoothSpacetime", (0.02, 0.25, 1.0), 2.0)
    link_mat, link_shader = emission_material("SpinNetworkLinks", (1.0, 0.11, 0.02), 0.0)
    node_mat, node_shader = emission_material("SpinNetworkNodes", (1.0, 0.62, 0.05), 0.0)
    face_mat, face_shader = emission_material("QuantumCells", (0.16, 0.04, 0.7), 1.4)
    edge_mat, edge_shader = emission_material("QuantumCellEdges", (1.0, 0.72, 0.08), 6.0)
    area_mat, area_shader = emission_material("AreaQuantum", (0.02, 0.75, 1.0), 5.0)

    set_strength(grid_shader, [(1, 2.0), (38, 2.0), (76, 0.0)])
    set_strength(link_shader, [(28, 0.0), (72, 5.0)])
    set_strength(node_shader, [(28, 0.0), (72, 4.0), (130, 4.0), (150, 0.6)])

    # Smooth spacetime: a slightly curved continuous grid.
    for i in range(-5, 6):
        row = []
        column = []
        for j in range(-6, 7):
            x = j * 0.9
            y = i * 0.9
            z = 0.17 * math.sin(x * 0.75) * math.cos(y * 0.65)
            row.append((x, y, z))
            column.append((y, x, z))
        polyline("SpacetimeGrid", row, grid_mat)
        polyline("SpacetimeGrid", column, grid_mat)

    # A shallow 3D spin network, rather than a perfectly flat square diagram.
    positions = {}
    for x in range(-1, 2):
        for y in range(-1, 2):
            z = 0.18 * math.sin(1.7 * x + 0.8 * y)
            positions[(x, y)] = Vector((x * 1.8, y * 1.8, z))

    nodes = {}
    for key, position in positions.items():
        node = sphere("SpinNetworkNode", position, 0.12, node_mat)
        animate_scale(node, [(28, 0.001), (64, 1.0), (128, 1.0), (148, 0.42)])
        nodes[key] = node

    for (x, y), start in positions.items():
        for neighbor in ((x + 1, y), (x, y + 1)):
            if neighbor in positions:
                link = curve_line("SpinNetworkLink", start, positions[neighbor], link_mat, 0.032)
                animate_scale(link, [(30, 0.001), (72, 1.0)])

    # Every node acquires a small tetrahedral cell.
    cells = {}
    for key, position in positions.items():
        cell = tetrahedron("QuantumCell", position, face_mat, edge_mat, size=0.68)
        animate_scale(cell, [(105, 0.001), (148, 0.38)])
        cells[key] = cell

    # The selected central cell grows while the others recede.
    center = cells[(0, 0)]
    animate_scale(center, [(105, 0.001), (148, 0.38), (182, 0.38), (226, 0.86)])
    center.rotation_euler = (0.0, 0.0, 0.0)
    center.keyframe_insert(data_path="rotation_euler", frame=148)
    center.rotation_euler = (math.radians(8), math.radians(-10), math.radians(28))
    center.keyframe_insert(data_path="rotation_euler", frame=240)

    for key, cell in cells.items():
        if key != (0, 0):
            animate_scale(cell, [(105, 0.001), (148, 0.38), (188, 0.38), (226, 0.18)])

    # A glowing disk pierced by one link represents a discrete area contribution.
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=48,
        radius=0.46,
        depth=0.035,
        location=(0.9, 0.0, 0.08),
        rotation=(0.0, math.radians(90), 0.0),
    )
    area_disk = bpy.context.object
    area_disk.name = "DiscreteAreaSurface"
    area_disk.data.materials.append(area_mat)
    animate_scale(area_disk, [(145, 0.001), (166, 1.0), (188, 1.0), (205, 0.001)])

    # A camera move from the continuous grid to one highlighted quantum cell.
    bpy.ops.object.camera_add(location=(8.8, -11.2, 8.4))
    camera = bpy.context.object
    camera.name = "QuantumGeometryCamera"
    camera.data.lens = 50
    point_at(camera, (0, 0, 0))
    camera.keyframe_insert(data_path="location", frame=1)
    camera.keyframe_insert(data_path="rotation_euler", frame=1)

    camera.location = (7.6, -9.4, 6.8)
    point_at(camera, (0, 0, 0))
    camera.keyframe_insert(data_path="location", frame=125)
    camera.keyframe_insert(data_path="rotation_euler", frame=125)

    camera.location = (6.2, -8.0, 5.3)
    point_at(camera, (0, 0, 0.15))
    camera.keyframe_insert(data_path="location", frame=240)
    camera.keyframe_insert(data_path="rotation_euler", frame=240)
    bpy.context.scene.camera = camera

    world = bpy.context.scene.world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.002, 0.006, 0.025, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.06

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 240
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.resolution_percentage = 100
    scene.render.fps = 24

    # Smooth camera/object interpolation.
    for action in bpy.data.actions:
        for fcurve in action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = "BEZIER"

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)

    captures = [
        (1, "01_smooth_spacetime"),
        (64, "02_network_emerging"),
        (112, "03_spin_network"),
        (158, "04_tetrahedral_cells"),
        (176, "05_discrete_area"),
        (240, "06_four_valent_node"),
    ]
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
