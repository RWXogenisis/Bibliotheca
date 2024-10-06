import bpy
import json
import math

# Function to load mesh data from JSON
def load_mesh_data(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

# Function to create a material with transparency
def create_transparent_material(material_name, color, alpha):
    material = bpy.data.materials.get(material_name)
    if not material:
        material = bpy.data.materials.new(name=material_name)
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*color, alpha)  # Set color with alpha
            bsdf.inputs['Alpha'].default_value = alpha
    return material

# Function to create a mesh object from the data
def create_mesh_object(mesh_info):
    mesh = bpy.data.meshes.new(mesh_info['name'])
    obj = bpy.data.objects.new(mesh_info['name'], mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = mesh_info.get('location', (0, 0, 0))
    obj.rotation_euler = mesh_info.get('rotation', (0, 0, 0))
    mesh.from_pydata(mesh_info['vertices'], [], mesh_info['faces'])
    mesh.update()
    return obj

# Function to create a rectangular object
def create_blinking_rectangle(location, width=1, height=1, color=(1, 1, 1), id=1):
    # Create a mesh for the rectangle
    mesh = bpy.data.meshes.new("BlinkingRectangle")
    obj = bpy.data.objects.new("BlinkingRectangle", mesh)

    # Set the location
    obj.location = location

    # Create the rectangle geometry
    verts = [
        (-width / 2, -height / 2, 0),  # Bottom left
        (width / 2, -height / 2, 0),   # Bottom right
        (width / 2, height / 2, 0),    # Top right
        (-width / 2, height / 2, 0)    # Top left
    ]
    faces = [(0, 1, 2, 3)]  # One face with all four vertices

    # Create the mesh from the vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a transparent material with specified color
    material = create_transparent_material("BlinkingRectangleMaterial"+str(id), color, 0.5)  # Set opacity
    obj.data.materials.append(material)

    return obj

# Function to set the view to 3D Viewport
def set_viewport_to_3d():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    break

# Function to create continuous blinking effect
def blink_object(obj, start_frame, duration, blink_interval=5):
    mat = obj.active_material
    if mat:
        mat.use_nodes = True
        alpha_input = mat.node_tree.nodes["Principled BSDF"].inputs['Alpha']
        
        # Total number of blinks
        total_blinks = duration // (blink_interval * 2)

        # Loop to set keyframes for continuous blinking
        for i in range(total_blinks + 1):  # Add +1 to ensure it blinks at the end
            frame_on = start_frame + i * (blink_interval * 2)  # When the object is visible
            frame_off = frame_on + blink_interval  # When the object is invisible

            # Set keyframes for blinking
            # Fully visible
            alpha_input.default_value = 1  # Full opacity
            alpha_input.keyframe_insert(data_path='default_value', frame=frame_off)

            # Invisible 
            alpha_input.default_value = 0  # Initial opacity
            alpha_input.keyframe_insert(data_path='default_value', frame=frame_on)

        # Ensure the last keyframe is set to invisible
        last_blink_frame = start_frame + (total_blinks * (blink_interval * 2))
        if last_blink_frame + blink_interval < start_frame + duration:
            alpha_input.default_value = 0  # Final state is invisible
            alpha_input.keyframe_insert(data_path='default_value', frame=last_blink_frame + blink_interval)

# Function to parse book ID and get row, shelf, rack
def parse_book_id(book_id):
    row, shelf, rack = map(int, book_id.split('_'))
    return row, shelf, rack

# Function to normalize rotation angles between -180 and 180 degrees
def normalize_rotation(rotation):
    return [(angle + math.pi) % (2 * math.pi) - math.pi for angle in rotation]

# Function to adjust the camera view at a specific frame with linear interpolation
def set_camera_view(camera, location, rotation, frame, mag=50):
    # Normalize the camera rotation to avoid multiple rotations
    normalized_rotation = normalize_rotation(rotation)
    
    # Set camera location
    camera.location = location
    camera.keyframe_insert(data_path="location", frame=frame)

    # Set camera rotation (in Euler angles)
    camera.rotation_euler = normalized_rotation
    camera.keyframe_insert(data_path="rotation_euler", frame=frame)

    # Set focal length (magnification)
    camera.data.lens = mag
    camera.data.keyframe_insert(data_path="lens", frame=frame)

    # Set linear interpolation to avoid easing
    for fcurve in camera.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'  # Set interpolation to linear

# Function to highlight the bookshelf based on book ID (with camera change)
def highlight_bookshelf(book_id, mesh_data):
    row, shelf, rack = parse_book_id(book_id)

    # Locate the camera object
    camera = bpy.data.objects.get("Camera")  # Ensure you have the right camera

    if not camera:
        print("Camera not found!")
        return

    # Map bookshelves based on row
    row_map = {
        1: list(range(6)),    # Bookshelves 000-005
        2: list(range(6, 12)), # Bookshelves 006-011
        3: list(range(18, 24)),# Bookshelves 018-023
        4: list(range(12, 18)) # Bookshelves 012-017
    }

    camera_row_map = {
        0:[[-5.94722, -6.7615, 2.32527], [53.0842, -2.35959, -37.6813], 14.6545],
        1:[[-5.94722, -6.7615, 2.32527], [53.0842, -2.35959, -37.6813], 14.6545],
        2:[[-5.94722, -6.7615, 2.32527], [53.0842, -2.35959, -37.6813], 14.6545],
        3:[[-5.94722, -6.7615, 2.32527], [53.0842, -2.35959, -37.6813], 14.6545],
        4:[[-5.94722, -6.7615, 2.32527], [53.0842, -2.35959, -37.6813], 14.6545],
        5:[[-5.94722, -6.7615, 2.32527], [53.0842, -2.35959, -37.6813], 14.6545],
        8:[[-10.2519, 0.397276, 0.123977], [79.591, -1.87154, -91.5348], 23.4169],
        7:[[-10.2519, 0.397276, 0.123977], [79.591, -1.87154, -91.5348], 23.4169],
        18:[[8.92573, 0.397276, 0.123977], [257.452, -179.515, -85.8309], 23.4169],
        19:[[8.92573, 0.397276, 0.123977], [257.452, -179.515, -85.8309], 23.4169],
        20:[[8.92573, 0.397276, 0.123977], [257.452, -179.515, -85.8309], 23.4169],
        6:[[8.92573, 0.397276, 0.123977], [257.452, -179.515, -85.8309], 23.4169],
        10:[[8.92573, 0.397276, 0.123977], [257.452, -179.515, -85.8309], 23.4169],
        9:[[8.92573, 0.397276, 0.123977], [257.452, -179.515, -85.8309], 23.4169],
        22:[[-10.2519, 0.397276, 0.123977], [79.591, -1.87154, -91.5348], 23.4169],
        23:[[-10.2519, 0.397276, 0.123977], [79.591, -1.87154, -91.5348], 23.4169],
    }

    row_coord = {
        2: [-0.662948, 2.51565, 0.376559],
        1: [-0.662948, -2.295, 0.376559]
    }
    shelf_coord = {
        0: [-6.66758, -2.59314, 0.5], 
        1: [-4.28172, -2.59314, 0.5],
        2: [-1.8321, -2.59314, 0.5],
        5: [5.36978, -2.59314, 0.5],
        4: [2.92016, -2.59314, 0.5],
        3: [0.534299, -2.59314, 0.5],
        8: [-1.85335, -1.86021, 0.5],
        7: [-4.23922, -1.85842, 0.5],
        6: [-6.68883, -1.85659, 0.5],
        9: [0.513047, -1.86198, 0.5],
        10: [2.96267, -1.86381, 0.5],
        11: [5.34853, -1.8656, 0.5]
    }
    rack_coord = {
        0:[[-6.66329, -2.75929, 0.000329], [-6.66329, -2.75929, -0.403437], [-6.66329, -2.75929, -0.843847], [-6.66329, -2.75929, -1.30816]],
        1:[[-4.25876, -2.75929, 0.000329], [-4.25876, -2.75929, -0.403437], [-4.25876, -2.75929, -0.843847], [-4.25876, -2.75929, -1.30816]],
        2:[[-1.82408, -2.75929, 0.000329], [-1.82408, -2.75929, -0.403437], [-1.82408, -2.75929, -0.843847], [-1.82408, -2.75929, -1.30816]],
    }

    # Find the corresponding bookshelf for the row and shelf
    if row in row_map:
        shelf_index = row_map[row][shelf - 1]
        bookshelf_name = f"bookshelf.{shelf_index:03d}"

        # Find the object by name
        obj = bpy.data.objects.get(bookshelf_name)
        if obj:
            # Set camera view for row blinking
            set_camera_view(camera, location=(-10.2519, 0.397276, 3.35558), rotation=(245.239, -183.183, -265.667), frame=1)  # Example view for row
            # Create a blinking rectangle over the row (blue)
            row_location = row_coord[row]  # Adjust location for row
            row_width = 15  # Width can be adjusted based on your model
            row_height = 1.277  # Height for the rectangle
            rectangle_row = create_blinking_rectangle(row_location, width=row_width, height=row_height, color=(0, 0, 1), id=1)  # Blue color
            blink_object(rectangle_row, start_frame=1, duration=49)  # Blink for row

            # Set camera view for shelf blinking
            set_camera_view(camera, location=camera_row_map[row][0], rotation=camera_row_map[row][1], frame=100, mag=camera_row_map[row][2])  # Example view for shelf
            # Create a blinking rectangle over the bookshelf (orange)
            bookshelf_location = shelf_coord[shelf-1]
            bookshelf_width = 2  # Match with shelf width
            bookshelf_height = 1  # Height for the rectangle
            rectangle_bookshelf = create_blinking_rectangle(bookshelf_location, width=bookshelf_width, height=bookshelf_height, color=(1, 0.5, 0), id=2)  # Orange color
            blink_object(rectangle_bookshelf, start_frame=50, duration=49)  # Blink for bookshelf

            # Set camera view for rack blinking
            # set_camera_view(camera, location=camera_row_map[row][0], rotation=camera_row_map[row][1], frame=100, mag=camera_row_map[row][2])  # Example view for shelf
            # Create a blinking rectangle over the rack (green, vertical)
            rack_location = rack_coord[shelf-1][rack-1]  # Adjust for rack
            rack_width = 0.5  # Width for the vertical rectangle
            rack_height = 1.0  # Match height of the rack
            rectangle_rack = create_blinking_rectangle(rack_location, width=rack_width, height=rack_height, color=(0, 1, 0), id=3)  # Green color
            rectangle_rack.rotation_euler[0] = 1.5708  # Rotate to be vertical (90 degrees in radians)
            rectangle_rack.rotation_euler[1] = 1.5708  # Rotate to be vertical (90 degrees in radians)
            blink_object(rectangle_rack, start_frame=100, duration=49)  # Blink for rack

# Function to remove the default cube
def remove_default_cube():
    default_cube = bpy.data.objects.get("Cube")
    if default_cube:
        bpy.data.objects.remove(default_cube, do_unlink=True)

# Main execution
if __name__ == "__main__":
    json_path = "D:\\Karun's temp backup\\OSS\\mesh.json"  # Adjust to the correct path

    remove_default_cube()

    # Load mesh data
    mesh_data = load_mesh_data(json_path)

    # Create mesh objects for each entry
    for mesh_info in mesh_data:
        create_mesh_object(mesh_info)

    print("3D models created from JSON data.")

    # Example usage of book ID
    book_id = "01_01_02"  # First row, first shelf, first rack
    highlight_bookshelf(book_id, mesh_data)

    set_viewport_to_3d()

    print("Focus set on the bookshelf.")

# Run with blender --python test3.py