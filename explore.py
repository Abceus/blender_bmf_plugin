import struct

filepath = 'C:\\Users\\jamil\\projects\\OpenBugbear\\game\\out\\car_1\\collision.BMF'
filepath = 'C:\\Users\\jamil\\projects\\OpenBugbear\\game\\out\\car_1\\model.BMF'
filepath = 'C:\\projects\\OpenBugbear\\game\\out\\models\\stage1.BMF'
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
        new_object = parsers[next_object.name](next_object)
        #if type(new_object) != dict:
        #    continue

        #if "name" not in new_object:
        #    continue

        #if (str)(new_object["name"]).find("sign") == -1:
        #    continue

        result.append(new_object)
    return result

def parse_scene(header : Header):
    name = get_string()
    skip_shit(148)
    return name

def get_transform_matrix():
    def get_matrix_row():
        x = get_float()
        z = get_float()
        y = get_float()
        w = get_float()
        return (x, y, z, w)
    
    row0 = get_matrix_row()
    row2 = get_matrix_row()
    row1 = get_matrix_row()
    row3 = get_matrix_row()
    return (
        row0,
        row1,
        row2,
        row3
    )

def parse_mesh(header : Header):
    result = {
        "name": get_string(),
        "unknown_float_0": get_float(),
        "transform_matrix": get_transform_matrix(),
        "coords": parse_vertex(),
        "unknown_float_1": get_float(),
        "unknown_float_2": get_float(),
        "unknown_float_3": get_float(),
        "unknown_unit_0": get_unsigned(),
        "unknown_float_4": get_float(),
        "unknown_float_5": get_float(),
        "unknown_float_6": get_float(),
        "unknown_float_7": get_float(),
        "unknown_float_8": get_float(),
        "unknown_float_9": get_float(),
        "unknown_float_10": get_float(),
        "unknown_float_11": get_float(),
        "unknown_float_12": get_float(),
        "unknown_float_13": get_float(),
        "unknown_unit_1": get_unsigned(),
    }
    
    model_header = parse_header()
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
    skip_shit(36)

    res = []
    size = get_unsigned()

    for i in range(size):

        result = {
            "name": "track" + str(i),
            "transform_matrix": (
                (1, 0, 0, 0),
                (0, 1, 0, 0),
                (0, 0, 1, 0),
                (0, 0, 0, 1),
            ),
            "coords": (0, 0, 0)
        }

        model_header = parse_header()
        result["model"] = parsers[model_header.name](model_header)
        res.append(result)

    return res

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
    from mathutils import Matrix

    result = decode_file()

    new_collection = bpy.data.collections.new('new_collection')
    bpy.context.scene.collection.children.link(new_collection)
    
    materials = []
    for material in result["MATERIALLIST"]:
        materials.append(material["name"])
        mat = bpy.data.materials.get(materials[-1])
        if mat is None:
            mat = bpy.data.materials.new(name=materials[-1])
    
    
    def add_model(model):
        if model == "Scene":
            return
        
        if type(model) == str:
            return

        polylist = None
        vertexlist = None

        batches = {
            "faces": [],
            "verts": [],
            "material_indexes": []
        }

        def create_object(new_mesh):
            new_mesh.transform(Matrix(model["transform_matrix"]))
            new_mesh.update()
            new_object = bpy.data.objects.new(model["name"], new_mesh)
            new_object.location = model["coords"]
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

        if batches["verts"]:
            create_object(create_vertexlist_object(batches["verts"], batches["faces"], model["name"], materials, batches["material_indexes"]))
    
    # for model in result["HIERARCHY"]:
        # add_model(model)

    for model in result["TRACK"]:
        add_model(model)


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

def nonblender_shit():
    result = decode_file()
    print(result)

blender_shit()
