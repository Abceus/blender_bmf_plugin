import struct
import bpy

filepath = 'C:\\Users\\jamil\\projects\\OpenBugbear\\game\\out\\car_1\\collision.BMF'

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
        result[next_header] = parsers[next_header.name](next_header)
    
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

class Material:
    def __init__(self):
        self.uint1 = 0
        self.uint2 = 0
        self.uint3 = 0
        self.uint4 = 0
        self.uint5 = 0
        self.float1 = 0.0
        self.float2 = 0.0
        self.float3 = 0.0
        self.float4 = 0.0
        self.float5 = 0.0
        self.float6 = 0.0
        self.float7 = 0.0
        self.float8 = 0.0
        self.float9 = 0.0
        self.float10 = 0.0
        self.float11 = 0.0
        self.float12 = 0.0
        self.float13 = 0.0
        self.float14 = 0.0
        self.float15 = 0.0
        self.float16 = 0.0
        self.float17 = 0.0
        self.float18 = 0.0
        self.name = ""
        self.path = ""
        self.ushort1 = 0

def parse_material(header : Header):
    size = get_unsigned()
    result = Material()
    result.uint1 = get_unsigned()
    result.uint2 = get_unsigned()
    result.uint3 = get_unsigned()
    result.uint4 = get_unsigned()
    result.uint5 = get_unsigned()
    result.float1 = get_float()
    result.float2 = get_float()
    result.float3 = get_float()
    result.float4 = get_float()
    result.float5 = get_float()
    result.float6 = get_float()
    result.float7 = get_float()
    result.float8 = get_float()
    result.float9 = get_float()
    result.float10 = get_float()
    result.float11 = get_float()
    result.float12 = get_float()
    result.float13 = get_float()
    result.float14 = get_float()
    result.float15 = get_float()
    result.float16 = get_float()
    result.float17 = get_float()
    result.float18 = get_float()
    result.name = get_string()
    result.path = get_string()
    result.ushort1 = get_unsigned_short()
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
    return name

parsers = {
    "MAIN": parse_main,
    "INFO": parse_info,
    "MATERIALLIST": parse_materiallist,
    "MATERIAL": parse_material,
    "HIERARCHY": parse_hierarchy,
    "SCENE": parse_scene,
    "MESH": parse_mesh
}
    
main_header = parse_header()

result = parsers[main_header.name](main_header)
print(result)
