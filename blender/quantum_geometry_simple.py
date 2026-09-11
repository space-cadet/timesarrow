import bpy
import math
import os
from mathutils import Vector


ROOT = "/Volumes/Data/owncloud/root/research/articles/timesarrow/blender"
RENDER_DIR = os.path.join(ROOT, "renders")
BLEND_PATH = os.path.join(ROOT, "quantum_geometry_simple.blend")
PNG_PATH = os.path.join(RENDER_DIR, "quantum_geometry_simple.png")


def material(name, color, strength=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*color, 1.0)
    emission.inputs["Strength"].default_value = strength
    links.new(emission.outputs[0], out.inputs[0])
    return mat


def curve_line(name, points, mat, thickness=0.025):
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
    return obj


def scale_animation(obj, start, end):
    obj.scale = (0.001, 0.001, 0.001)
    obj.keyframe_insert(data_path="scale", frame=start)
    obj.scale = (1.0, 1.0, 1.0)
    obj.keyframe_insert(data_path="scale", frame=end)


def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def add_tetrahedron(location, face_mat, edge_mat):
    s = 1.05
    vertices = [(s, s, s), (s, -s, -s), (-s, s, -s), (-s, -s, s)]
    faces = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2)]
    mesh = bpy.data.meshes.new("TetrahedronMesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("QuantumTetrahedron", mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    mesh.materials.append(face_mat)

    for i, (a, b) in enumerate([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]):
        edge = curve_line("TetrahedronEdge", [vertices[a], vertices[b]], edge_mat, 0.04)
        edge.parent = obj
    return obj


def build():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    grid_mat = material("Smooth spacetime", (0.03, 0.18, 0.65), 1.5)
    link_mat = material("Spin network", (1.0, 0.16, 0.03), 5.0)
    node_mat = material("Nodes", (1.0, 0.55, 0.04), 3.0)
    tetra_mat = material("Tetrahedron faces", (0.15, 0.04, 0.55), 1.0)
    edge_mat = material("Tetrahedron edges", (1.0, 0.75, 0.1), 6.0)

    # Continuous grid: the opening image.
    for i in range(-4, 5):
        horizontal = []
        vertical = []
        for j in range(-4, 5):
            x = j * 1.15
            y = i * 1.15
            z = 0.18 * math.sin(x) * math.cos(y)
            horizontal.append((x, y, z))
            vertical.append((y, x, z))
        line_a = curve_line("SpacetimeGrid", horizontal, grid_mat, 0.012)
        line_b = curve_line("SpacetimeGrid", vertical, grid_mat, 0.012)
        for line in (line_a, line_b):
            line.scale = (1, 1, 1)
            line.keyframe_insert(data_path="scale", frame=1)
            line.keyframe_insert(data_path="scale", frame=32)
            line.scale = (0.001, 0.001, 0.001)
            line.keyframe_insert(data_path="scale", frame=52)

    # A small graph grows in as the smooth grid recedes.
    positions = {}
    for x in range(-1, 2):
        for y in range(-1, 2):
            positions[(x, y)] = (x * 1.8, y * 1.8, 0.0)

    nodes = {}
    for key, pos in positions.items():
        nodes[key] = sphere("SpinNetworkNode", pos, 0.13, node_mat)
        scale_animation(nodes[key], 25, 55)

    for (x, y), start in positions.items():
        for neighbor in ((x + 1, y), (x, y + 1)):
            if neighbor in positions:
                edge = curve_line("SpinNetworkLink", [start, positions[neighbor]], link_mat, 0.035)
                scale_animation(edge, 25, 55)

    # The center node expands into a four-valent quantum tetrahedron.
    center = nodes[(0, 0)]
    center.scale = (1, 1, 1)
    center.keyframe_insert(data_path="scale", frame=62)
    center.scale = (0.001, 0.001, 0.001)
    center.keyframe_insert(data_path="scale", frame=75)

    tetra = add_tetrahedron(positions[(0, 0)], tetra_mat, edge_mat)
    tetra.scale = (0.001, 0.001, 0.001)
    tetra.keyframe_insert(data_path="scale", frame=58)
    tetra.scale = (1, 1, 1)
    tetra.keyframe_insert(data_path="scale", frame=88)
    tetra.rotation_euler = (0, 0, math.radians(25))
    tetra.keyframe_insert(data_path="rotation_euler", frame=120)

    bpy.ops.object.camera_add(location=(8.6, -10.5, 8.0))
    camera = bpy.context.object
    camera.data.lens = 52
    point_at(camera, (0, 0, 0))
    camera.keyframe_insert(data_path="location", frame=1)
    camera.keyframe_insert(data_path="rotation_euler", frame=1)
    camera.location = (4.5, -6.0, 3.8)
    point_at(camera, (0, 0, 0.3))
    camera.keyframe_insert(data_path="location", frame=120)
    camera.keyframe_insert(data_path="rotation_euler", frame=120)
    bpy.context.scene.camera = camera

    bpy.ops.object.light_add(type="AREA", location=(2, -4, 8))
    light = bpy.context.object
    light.data.energy = 700
    light.data.size = 5
    point_at(light, (0, 0, 0))

    world = bpy.context.scene.world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.005, 0.01, 0.04, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.08

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 120
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 360
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = PNG_PATH
    scene.frame_set(120)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    build()
