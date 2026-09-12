"""Higher-quality 3D quantum-geometry sequence for T37."""

import bpy, math, os
from mathutils import Vector

ROOT = "/Volumes/Data/owncloud/root/research/articles/timesarrow/blender"
OUT = os.path.join(ROOT, "renders", "quantum_geometry_v4")
FRAMES = os.path.join(OUT, "frames")


def material(name, base, metallic=.0, roughness=.35, emission=None, strength=0.0, alpha=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Alpha"].default_value = alpha
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1)
        bsdf.inputs["Emission Strength"].default_value = strength
    if alpha < 1:
        m.surface_render_method = 'DITHERED'
    return m


def line(name, a, b, mat, radius=.025):
    a, b = Vector(a), Vector(b); d = b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=radius, depth=d.length, location=(a+b)/2)
    o=bpy.context.object; o.name=name; o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); o.data.materials.append(mat)
    return o


def node(name, p, mat, radius=.105):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=radius, location=p)
    o=bpy.context.object; o.name=name; o.data.materials.append(mat); return o


def scale_keys(o, keys):
    for f,s in keys: o.scale=(s,s,s); o.keyframe_insert(data_path='scale', frame=f)


def opacity_keys(mat, keys):
    bsdf=mat.node_tree.nodes.get('Principled BSDF')
    for f,a in keys:
        bsdf.inputs['Alpha'].default_value=a; bsdf.inputs['Alpha'].keyframe_insert('default_value', frame=f)


def tetra(name, center, face_mat, edge_mat, size=.48):
    root=bpy.data.objects.new(name+'Root',None); bpy.context.collection.objects.link(root); root.location=center
    verts=[Vector(v)*size for v in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
    mesh=bpy.data.meshes.new(name+'Mesh'); mesh.from_pydata(verts,[],[(0,1,2),(0,3,1),(0,2,3),(1,3,2)])
    o=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(o); o.data.materials.append(face_mat); o.parent=root
    for i,(a,b) in enumerate([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]):
        edge=line(name+'Edge',verts[a],verts[b],edge_mat,.018); edge.parent=root
    return root


def build():
    os.makedirs(FRAMES,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
    navy=material('Grid',(0.015,.05,.10),roughness=.55,emission=(.02,.24,.55),strength=1.8)
    linkmat=material('Links',(.08,.28,.42),metallic=.25,roughness=.25,emission=(.05,.48,.72),strength=2.0)
    nodemat=material('Nodes',(.8,.35,.06),metallic=.15,roughness=.22,emission=(1,.28,.03),strength=1.3)
    facemat=material('Cells',(.08,.22,.48),metallic=.12,roughness=.3,emission=(.08,.22,.65),strength=.45,alpha=.34)
    edgemat=material('CellEdges',(.35,.66,.95),metallic=.3,roughness=.2,emission=(.18,.55,1),strength=2.4)
    areamat=material('Area',(.05,.58,.52),roughness=.2,emission=(.04,1,.72),strength=2.8,alpha=.72)

    # Curved continuous surface, deliberately finer and subtler than v2.
    grid=[]
    for i in range(-7,8):
        for axis in (0,1):
            pts=[]
            for j in range(-18,19):
                x=(j*.34 if axis==0 else i*.55); y=(i*.55 if axis==0 else j*.34)
                z=.16*math.sin(x*.72)*math.cos(y*.58)-.65
                pts.append((x,y,z))
            for a,b in zip(pts,pts[1:]): grid.append(line('ContinuousGeometry',a,b,navy,.009))
    for o in grid: scale_keys(o,[(1,1),(72,1),(110,.001)])

    pos={(x,y):Vector((x*1.65,y*1.65,.18*math.sin(1.3*x+.7*y))) for x in range(-1,2) for y in range(-1,2)}
    network=[]
    for p in pos.values(): network.append(node('SpinNetworkNode',p,nodemat,.12))
    for k,p in pos.items():
        for n in ((k[0]+1,k[1]),(k[0],k[1]+1)):
            if n in pos: network.append(line('SpinNetworkLink',p,pos[n],linkmat,.035))
    for o in network: scale_keys(o,[(42,.001),(92,1)])

    cells={}
    for k,p in pos.items(): cells[k] = tetra('QuantumCell', p + Vector((0, 0, .12)), facemat, edgemat, .42)
    for o in cells.values(): scale_keys(o,[(132,.001),(170,1)])

    # One actual disk pierced by the right-hand link.
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.42,depth=.035,location=(.82,0,.1),rotation=(0,math.pi/2,0))
    disk=bpy.context.object; disk.name='DiscreteArea'; disk.data.materials.append(areamat); scale_keys(disk,[(155,.001),(185,1),(215,1),(232,.001)])

    # Fade peripheral cells while the central tetrahedron becomes the handoff focus.
    for key,o in cells.items():
        scale_keys(o,[(132,.001),(170,1),(218,1),(270,1 if key == (0,0) else .22)])
    cells[(0,0)].rotation_euler=(0,0,0); cells[(0,0)].keyframe_insert('rotation_euler',frame=218)
    cells[(0,0)].rotation_euler=(math.radians(12),math.radians(-18),math.radians(24)); cells[(0,0)].keyframe_insert('rotation_euler',frame=300)

    bpy.ops.object.camera_add(location=(7.8,-10.8,7.2)); cam=bpy.context.object; cam.data.lens=54
    for f,loc,target in [(1,(8.8,-12.5,8.2),(0,0,-.3)),(145,(7.2,-10.0,6.6),(0,0,0)),(300,(5.6,-8.0,4.7),(0,0,.15))]:
        cam.location=loc; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.keyframe_insert('location',frame=f); cam.keyframe_insert('rotation_euler',frame=f)
    bpy.context.scene.camera=cam

    world=bpy.context.scene.world; world.use_nodes=True; world.node_tree.nodes['Background'].inputs['Color'].default_value=(.002,.006,.018,1); world.node_tree.nodes['Background'].inputs['Strength'].default_value=.12
    for kind,loc,energy,size,color in [('AREA',(2,-4,7),900,5,(.35,.65,1)),('AREA',(-5,1,3),700,4,(1,.22,.08))]:
        bpy.ops.object.light_add(type=kind,location=loc); l=bpy.context.object; l.data.energy=energy; l.data.shape='DISK'; l.data.size=size; l.data.color=color; l.rotation_euler=(Vector((0,0,0))-l.location).to_track_quat('-Z','Y').to_euler()

    scene=bpy.context.scene; scene.frame_start=1; scene.frame_end=300; scene.render.engine='BLENDER_EEVEE_NEXT'
    scene.eevee.taa_render_samples=32
    scene.render.resolution_x=1920; scene.render.resolution_y=1080; scene.render.resolution_percentage=100; scene.render.fps=30
    scene.render.image_settings.file_format='PNG'; scene.render.film_transparent=False
    scene.view_settings.look='AgX - Medium High Contrast'
    scene.render.image_settings.color_mode='RGBA'
    scene.render.ffmpeg.format='MPEG4'; scene.render.ffmpeg.codec='H264'; scene.render.ffmpeg.constant_rate_factor='HIGH'
    for action in bpy.data.actions:
        for fc in action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation='BEZIER'
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'quantum_geometry_v4.blend'))
    for f,n in [(1,'01_continuous_geometry'),(80,'02_network_emerging'),(125,'03_spin_network'),(170,'04_quantum_cells'),(190,'05_discrete_area'),(300,'06_tetrahedral_focus')]:
        scene.frame_set(f); scene.render.filepath=os.path.join(FRAMES,n+'.png'); bpy.ops.render.render(write_still=True)
    if os.environ.get('T37_STILLS_ONLY') == '1':
        return
    scene.render.image_settings.file_format='FFMPEG'; scene.render.ffmpeg.format='MPEG4'; scene.render.ffmpeg.codec='H264'
    scene.render.ffmpeg.constant_rate_factor='HIGH'; scene.render.filepath=os.path.join(OUT,'quantum_geometry_v4'); bpy.ops.render.render(animation=True)

if __name__=='__main__': build()
