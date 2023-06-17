import struct

filepath = 'C:\\Users\\jamil\\projects\\OpenBugbear\\game\\out\\car_1\\collision.BMF'
filepath = 'C:\\Users\\jamil\\projects\\OpenBugbear\\game\\out\\car_1\\model.BMF'
#filepath = 'C:\\Users\\jamil\\projects\\OpenBugbear\\game\\out\\models\\stage4.BMF'
#filepath = 'C:\\Users\\jamil\\projects\\OpenBugbear\\game\\out\\models\\animal_run.BMF'

f = open(filepath, 'rb')
content = f.read()
f.close()

offset = 0

def read_shit(size):
    global offset
    global content
    result = content[offset:offset+size]
    offset += size
    return result

def get_unsigned():
    return struct.unpack('I', read_shit(4))[0]

def get_unsigned_short():
    return struct.unpack('H', read_shit(2))[0]

def get_float():
    return struct.unpack('f', read_shit(4))[0]

def get_char():
    return struct.unpack('c', read_shit(1))[0]

def get_string():
    current_character = None
    result = ""
    
    while True:
        current_character = get_char()
        if current_character == b'\x00':
            break
        result += current_character.decode("utf-8")
        
    return result

def skip_shit(size):
    global offset
    offset += size

class Header:
    def __init__(self, size = 0, name = ""):
        self.size = size
        self.name = name
        
def parse_header():
    return Header(get_unsigned(), get_string())

class MainObject:
    def __init__(self):
        self.info = ""
        
def parse_main(header : Header):
    global parsers
    global offset
    result = {}
    while offset < header.size:
        next_header = parse_header()
        result[next_header.name] = parsers[next_header.name](next_header)
    return result
    
def parse_info(header : Header):
    count = get_unsigned()
    result = []
    for i in range(count):
        result.append((get_string(), get_string()))
    return result

def parse_materiallist(header : Header):
    count = get_unsigned()
    result = []
    for i in range(count):
        next_header = parse_header()
        result.append(parsers[next_header.name](next_header))
    return result

def parse_material(header : Header):
    result = {}
    result["uint0"] = get_unsigned()
    result["uint1"] = get_unsigned()
    result["uint2"] = get_unsigned()
    result["uint3"] = get_unsigned()
    result["uint4"] = get_unsigned()
    result["float0"] = get_float()
    result["float1"] = get_float()
    result["float2"] = get_float()
    result["float3"] = get_float()
    result["float4"] = get_float()
    result["float5"] = get_float()
    result["float6"] = get_float()
    result["float7"] = get_float()
    result["float8"] = get_float()
    result["float9"] = get_float()
    result["float10"] = get_float()
    result["float11"] = get_float()
    result["float12"] = get_float()
    result["uint5"] = get_unsigned()
    result["float14"] = get_float()
    result["float15"] = get_float()
    result["uint6"] = get_unsigned()
    result["float17"] = get_float()
    result["name"] = get_string()
    result["path"] = get_string()
    result["ushort1"] = get_unsigned_short()
    return result

def parse_hierarchy(header : Header):
    count = get_unsigned()
    result = []
    for i in range(count):
        next_object = parse_header()
        result.append(parsers[next_object.name](next_object))
    return result

def parse_scene(header : Header):
    name = get_string()
    skip_shit(148)
    return name

def parse_mesh(header : Header):
    name = get_string()
    skip_shit(140)
    model_header = parse_header()
    result = {}
    result["name"] = name
    result["model"] = parsers[model_header.name](model_header)
    return result

def get_start_offset(header : Header):
    return offset - 4 - len(header.name) - 1

def parse_model(header : Header):
    start_offset = get_start_offset(header)
    uint_1 = get_unsigned()
    skip_shit(40)
    result = []
    while offset < start_offset + header.size:
        next_header = parse_header()
        result.append((next_header.name, parsers[next_header.name](next_header)))
    return result

def parse_vertex():
    x = get_float()
    z = get_float()
    y = get_float()
    return (
        x, y, z
    )

def parse_vertexlist(header : Header):
    count = get_unsigned()
    return [parse_vertex() for _ in range(count)]

def parse_poly():
    result = {}
    result["material_index"] = get_unsigned()
    result["poly"] = (
        get_unsigned(),
        get_unsigned(),
        get_unsigned()
    )
    return result

def parse_polylist(header : Header):
    count = get_unsigned()
    return [parse_poly() for _ in range(count)]

def parse_texture_coords():
    return (
        get_float(),
        get_float()
    )

def parse_batch2_vertex():
    return {
        "coords": parse_vertex(),
        "normals": parse_vertex(),
        "unknown_shit": get_unsigned(),
        "texture_coords": parse_texture_coords()
    }

def parse_batch2_poly():
    return (
        get_unsigned_short(),
        get_unsigned_short(),
        get_unsigned_short()
    )

def parse_batch2(header : Header):
    start_offset = get_start_offset(header)
    result = {}
    result["material_index"] = get_unsigned()
    vertex_count = get_unsigned()
    poly_count = get_unsigned()

    vertex_list = []
    for i in range(vertex_count):
        vertex_list.append(parse_batch2_vertex())
    
    poly_list = []
    for i in range(poly_count):
        poly_list.append(parse_batch2_poly())
    
    result["vertex_list"] = vertex_list
    result["poly_list"] = poly_list
    return result

def parse_track(header : Header):
    skip_shit(40)
    model_header = parse_header()
    result = { model_header.name: parsers[model_header.name](model_header) }
    return result

def parse_camera2(header : Header):
    name = get_string()
    skip_shit(152)
    return "camera " + name

def parse_light(header : Header):
    name = get_string()
    skip_shit(188)
    return "light " + name
    

parsers = {
    "MAIN": parse_main,
    "INFO": parse_info,
    "MATERIALLIST": parse_materiallist,
    "MATERIAL": parse_material,
    "HIERARCHY": parse_hierarchy,
    "SCENE": parse_scene,
    "MESH": parse_mesh,
    "MODEL": parse_model,
    "VERTEXLIST": parse_vertexlist,
    "POLYLIST": parse_polylist,
    "BATCH2": parse_batch2,
    "TRACK": parse_track,
    "CAMERA2": parse_camera2,
    "LIGHT": parse_light
}
    

def decode_file():
    main_header = parse_header()
    return parsers[main_header.name](main_header)


def blender_shit():
    import bpy

    result = decode_file()

    new_collection = bpy.data.collections.new('new_collection')
    bpy.context.scene.collection.children.link(new_collection)
    
    materials = []
    for material in result["MATERIALLIST"]:
        materials.append(material["name"])
        mat = bpy.data.materials.get(materials[-1])
        if mat is None:
            mat = bpy.data.materials.new(name=materials[-1])
    
    
    for model in result["HIERARCHY"]:
        if model == "Scene":
            continue

        polylist = None
        vertexlist = None

        batches = {
            "faces": [],
            "verts": [],
            "material_indexes": []
        }

        def create_object(new_mesh):
            new_object = bpy.data.objects.new(model["name"], new_mesh)
            new_collection.objects.link(new_object)

        def create_from_lists():
            if polylist != None and vertexlist != None:
                faces = [x["poly"] for x in polylist]
                material_indexes = [x["material_index"] for x in polylist]
                create_object(create_vertexlist_object(vertexlist, faces, model["name"], materials, material_indexes))

        for submodel in model["model"]:
            if submodel[0] == "POLYLIST":
                polylist = submodel[1]
                create_from_lists()
                continue

            if submodel[0] == "VERTEXLIST":
                vertexlist = submodel[1]
                create_from_lists()
                continue

            
            new_batch = {
                "faces": [x for x in submodel[1]["poly_list"]],
                "verts": [x["coords"] for x in submodel[1]["vertex_list"]],
                "material_indexes": [submodel[1]["material_index"] for x in submodel[1]["poly_list"]]
            }

            # merge batches
            verts_offset = len(batches["verts"])
            batches["verts"] += new_batch["verts"]
            batches["faces"] += [(vert[0]+verts_offset, vert[1]+verts_offset, vert[2]+verts_offset) for vert in new_batch["faces"]]
            batches["material_indexes"] += new_batch["material_indexes"]


        create_object(create_vertexlist_object(batches["verts"], batches["faces"], model["name"], materials, batches["material_indexes"]))

def create_vertexlist_object(verts, faces, name, materials, material_indexes):
    import bpy

    new_mesh = bpy.data.meshes.new(name=name + "_mesh")
    new_mesh.from_pydata(verts, [], faces)
    new_mesh.update()
    
    for material in materials:
        mat = bpy.data.materials.get(material)
        new_mesh.materials.append(mat)
    
    for i in range(len(material_indexes)):
        new_mesh.polygons[i].material_index = material_indexes[i]

    return new_mesh

'''
def blender_shit2():
    import bpy
    import mathutils

    result = decode_file()
    
    model_index = 23

    verts = []
    for vert in result["HIERARCHY"][model_index]["model"]["BATCH2"]["vertex_list"]:
        verts.append(vert["coords"])
            
    faces = []
    for poly in result["HIERARCHY"][model_index]["model"]["BATCH2"]["poly_list"]:
        faces.append(poly)

    new_mesh = bpy.data.meshes.new(name="New Object Mesh")
    new_mesh.from_pydata(verts, [], faces)
    new_mesh.update()

    new_object = bpy.data.objects.new('new_object', new_mesh)

    new_collection = bpy.data.collections.new('new_collection')
    bpy.context.scene.collection.children.link(new_collection)

    new_collection.objects.link(new_object)
    
    for material in result["MATERIALLIST"]:
        mat = bpy.data.materials.get(material["name"])
        if mat is None:
            mat = bpy.data.materials.new(name=material["name"])
            
        new_mesh.materials.append(mat)
    new_mesh.use_auto_smooth = True
    normals = [x["normals"] for x in result["HIERARCHY"][model_index]["model"]["BATCH2"]["vertex_list"]]
    #normals = [(1.0, 0.0, 0.0) for x in result["HIERARCHY"][1]["model"]["BATCH2"]["unknown_list"]]
    new_mesh.normals_split_custom_set_from_vertices(normals)
    new_mesh.update()
    
    #for i in range(len(result["HIERARCHY"][1]["model"]["POLYLIST"])):
    #    new_mesh.polygons[i].material_index = result["HIERARCHY"][1]["model"]["POLYLIST"][i]["material_index"]
'''

def nonblender_shit():
    result = decode_file()
    print(result)

blender_shit()
