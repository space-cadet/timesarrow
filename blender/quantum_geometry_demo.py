import bpy
import math
import os
from mathutils import Vector


PROJECT_DIR = "/Volumes/Data/owncloud/root/research/articles/timesarrow"
ASSET_DIR = os.path.join(PROJECT_DIR, "blender")
RENDER_DIR = os.path.join(ASSET_DIR, "renders")
BLEND_PATH = os.path.join(ASSET_DIR, "quantum_geometry_demo.blend")
VIDEO_PATH = os.path.join(RENDER_DIR, "quantum_geometry_demo.mp4")
STILL_PATH = os.path.join(RENDER_DIR, "quantum_geometry_demo.png")


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.curves, bpy.data.meshes, bpy.data.materials,
                       bpy.data.cameras, bpy.data.lights):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def emission_material(name, color, strength=1.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeEmission")
    shader.inputs["Color"].default_value = (*color, 1.0)
    shader.inputs["Strength"].default_value = strength
    links.new(shader.outputs[0], out.inputs[0])
    return mat, shader


def principled_material(name, color, metallic=0.0, roughness=0.45):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def add_polyline(name, points, material, bevel=0.018):
    curve = bpy.data.curves.new(name, type="CURVE")
    curve.dimensions = "3D"
    curve.resolution_u = 2
    curve.bevel_depth = bevel
    curve.bevel_resolution = 3
    spline = curve.splines.new("POLY")
    spline.points.add(len(points) - 1)
    for p, co in zip(spline.points, points):
        p.co = (*co, 1.0)
    obj = bpy.data.objects.new(name, curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj


def add_uv_sphere(name, location, radius, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=radius, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return obj


def add_tetrahedron(name, location, material, edge_material):
    # A regular tetrahedron centered at the origin.
    raw = [
        (1, 1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
    ]
    scale = 1.18
    verts = [(x * scale, y * scale, z * scale) for x, y, z in raw]
    faces = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2)]
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)

    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    for i, (a, b) in enumerate(edges):
        add_polyline(name + "Edge" + str(i), [verts[a], verts[b]], edge_material, bevel=0.035).parent = obj
    return obj


def animate_scale(obj, frame_a, scale_a, frame_b, scale_b):
    obj.scale = (scale_a, scale_a, scale_a)
    obj.keyframe_insert(data_path="scale", frame=frame_a)
    obj.scale = (scale_b, scale_b, scale_b)
    obj.keyframe_insert(data_path="scale", frame=frame_b)


def point_camera(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_label(body, location, size, material):
    curve = bpy.data.curves.new(body, type="FONT")
    curve.body = body
    curve.align_x = "CENTER"
    curve.size = size
    curve.extrude = 0.005
    obj = bpy.data.objects.new(body, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (math.radians(72), 0, 0)
    obj.data.materials.append(material)
    return obj


def make_scene():
    clear_scene()

    navy = (0.015, 0.035, 0.09)
    cyan = (0.08, 0.45, 1.0)
    cyan_dim = (0.03, 0.14, 0.42)
    orange = (1.0, 0.22, 0.035)
    gold = (1.0, 0.62, 0.08)
    violet = (0.28, 0.08, 0.65)
    white = (0.65, 0.9, 1.0)

    grid_mat, grid_shader = emission_material("Smooth spacetime", cyan_dim, 2.2)
    network_mat, network_shader = emission_material("Spin network links", orange, 5.0)
    node_mat = principled_material("Spin network nodes", gold, metallic=0.2, roughness=0.3)
    tetra_mat = principled_material("Quantum tetrahedron", violet, metallic=0.15, roughness=0.28)
    edge_mat, edge_shader = emission_material("Tetrahedron edges", gold, 8.0)
    label_mat, label_shader = emission_material("Labels", white, 2.0)
    star_mat, star_shader = emission_material("Stars", (0.35, 0.55, 1.0), 3.0)

    # A gently curved grid represents smooth, continuous spacetime.
    grid_collection = bpy.data.collections.new("SmoothSpacetimeGrid")
    bpy.context.scene.collection.children.link(grid_collection)
    for i in range(-5, 6):
        pts_x = []
        pts_y = []
        for j in range(-5, 6):
            x = j * 1.25
            y = i * 1.25
            z = 0.22 * math.sin(x * 0.55) * math.cos(y * 0.48)
            pts_x.append((x, y, z))
            pts_y.append((y, x, z))
        for pts in (pts_x, pts_y):
            obj = add_polyline("SpacetimeGrid", pts, grid_mat, bevel=0.012)
            for coll in list(obj.users_collection):
                coll.objects.unlink(obj)
            grid_collection.objects.link(obj)

    # A small star field gives the opening a cosmic scale.
    for i in range(32):
        angle = i * 2.39996
        radius = 7.0 + (i % 5) * 1.4
        loc = (math.cos(angle) * radius, math.sin(angle) * radius, 2.5 + (i % 7) * 0.55)
        star = add_uv_sphere("Star", loc, 0.018 + (i % 3) * 0.012, star_mat)
        animate_scale(star, 1, 0.0, 22, 1.0)

    # The final graph is present from the beginning but grows into view.
    graph_positions = {}
    for ix in range(-2, 3):
        for iy in range(-2, 3):
            z = 0.35 * math.sin(ix * 0.8) * math.cos(iy * 0.7)
            graph_positions[(ix, iy)] = (ix * 1.55, iy * 1.55, z)

    graph_nodes = []
    graph_links = []
    for (ix, iy), pos in graph_positions.items():
        node = add_uv_sphere("SpinNetworkNode", pos, 0.105, node_mat)
        animate_scale(node, 1, 0.001, 42, 1.0)
        graph_nodes.append(node)
        if (ix + 1, iy) in graph_positions:
            link = add_polyline("SpinLink", [pos, graph_positions[(ix + 1, iy)]], network_mat, bevel=0.027)
            animate_scale(link, 1, 0.001, 42, 1.0)
            graph_links.append(link)
        if (ix, iy + 1) in graph_positions:
            link = add_polyline("SpinLink", [pos, graph_positions[(ix, iy + 1)]], network_mat, bevel=0.027)
            animate_scale(link, 1, 0.001, 42, 1.0)
            graph_links.append(link)

    # Highlight the center node and expand it into a tetrahedral quantum cell.
    center = graph_positions[(0, 0)]
    center_node = [n for n in graph_nodes if n.location.length < 0.2][0]
    animate_scale(center_node, 1, 0.001, 42, 1.0,)
    center_node.keyframe_insert(data_path="scale", frame=62)
    center_node.scale = (0.001, 0.001, 0.001)
    center_node.keyframe_insert(data_path="scale", frame=78)

    tetra = add_tetrahedron("FourValentQuantumTetrahedron", center, tetra_mat, edge_mat)
    animate_scale(tetra, 1, 0.001, 58, 0.001)
    tetra.scale = (1.0, 1.0, 1.0)
    tetra.keyframe_insert(data_path="scale", frame=88)
    tetra.rotation_euler = (0.0, 0.0, math.radians(24))
    tetra.keyframe_insert(data_path="rotation_euler", frame=120)

    # Four highlighted face-center markers indicate the four incident links.
    raw_faces = [Vector((1, 1, 1)), Vector((1, -1, -1)), Vector((-1, 1, -1)), Vector((-1, -1, 1))]
    for i, v in enumerate(raw_faces):
        direction = v.normalized()
        marker = add_uv_sphere("QuantumAreaMarker", Vector(center) + direction * 1.05, 0.07, edge_mat)
        animate_scale(marker, 1, 0.001, 84, 0.001)
        marker.scale = (1.0, 1.0, 1.0)
        marker.keyframe_insert(data_path="scale", frame=100)

    # Minimal labels: they fade in only when the relevant object is visible.
    label_smooth = add_label("SMOOTH SPACETIME", (-0.2, -5.7, 0.35), 0.34, label_mat)
    label_smooth.scale = (1, 1, 1)
    label_smooth.keyframe_insert(data_path="scale", frame=1)
    label_smooth.keyframe_insert(data_path="scale", frame=34)
    label_smooth.scale = (0.001, 0.001, 0.001)
    label_smooth.keyframe_insert(data_path="scale", frame=50)

    label_quantum = add_label("QUANTUM GEOMETRY", (0.0, -3.0, 1.8), 0.36, label_mat)
    label_quantum.scale = (0.001, 0.001, 0.001)
    label_quantum.keyframe_insert(data_path="scale", frame=55)
    label_quantum.scale = (1, 1, 1)
    label_quantum.keyframe_insert(data_path="scale", frame=80)

    label_vertex = add_label("FOUR-VALENT NODE", (0.0, -2.4, 2.4), 0.30, label_mat)
    label_vertex.scale = (0.001, 0.001, 0.001)
    label_vertex.keyframe_insert(data_path="scale", frame=82)
    label_vertex.scale = (1, 1, 1)
    label_vertex.keyframe_insert(data_path="scale", frame=108)

    # Fade the smooth grid as the graph appears.
    grid_shader.inputs["Strength"].default_value = 2.2
    grid_shader.inputs["Strength"].keyframe_insert(data_path="default_value", frame=1)
    grid_shader.inputs["Strength"].keyframe_insert(data_path="default_value", frame=28)
    grid_shader.inputs["Strength"].default_value = 0.0
    grid_shader.inputs["Strength"].keyframe_insert(data_path="default_value", frame=58)

    # Camera.
    bpy.ops.object.camera_add(location=(13.5, -16.5, 10.8))
    camera = bpy.context.object
    camera.name = "DemoCamera"
    camera.data.lens = 48
    point_camera(camera, (0, 0, 0))
    camera.keyframe_insert(data_path="location", frame=1)
    camera.keyframe_insert(data_path="rotation_euler", frame=1)
    camera.location = (10.5, -12.5, 8.0)
    point_camera(camera, (0, 0, 0))
    camera.keyframe_insert(data_path="location", frame=58)
    camera.keyframe_insert(data_path="rotation_euler", frame=58)
    camera.location = (5.2, -7.2, 4.3)
    point_camera(camera, (0, 0, 0.45))
    camera.keyframe_insert(data_path="location", frame=120)
    camera.keyframe_insert(data_path="rotation_euler", frame=120)
    bpy.context.scene.camera = camera

    # Lighting.
    bpy.ops.object.light_add(type="AREA", location=(3.5, -4.5, 9.0))
    key = bpy.context.object
    key.data.energy = 900
    key.data.shape = "DISK"
    key.data.size = 6
    point_camera(key, (0, 0, 0))
    bpy.ops.object.light_add(type="POINT", location=(-4, 2, 4))
    fill = bpy.context.object
    fill.data.energy = 250
    fill.data.color = (0.12, 0.28, 1.0)

    # World and render settings.
    world = bpy.context.scene.world
    world.color = navy
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (*navy, 1.0)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.08

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 120
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 360
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.render.fps = 24
    scene.render.filepath = VIDEO_PATH
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    scene.render.filepath = VIDEO_PATH

    scene.frame_set(120)
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = STILL_PATH
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    bpy.ops.render.render(write_still=True)

    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.filepath = VIDEO_PATH
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)


if __name__ == "__main__":
    make_scene()
