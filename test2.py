import bpy
import json
import time  # Import the time module

# Function to load mesh data from JSON
def load_mesh_data(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

# Function to create a mesh object from the data
def create_mesh_object(mesh_info):
    # Create a new mesh
    mesh = bpy.data.meshes.new(mesh_info['name'])
    obj = bpy.data.objects.new(mesh_info['name'], mesh)

    # Link the object to the active scene
    bpy.context.collection.objects.link(obj)

    # Set the object's location and rotation
    obj.location = mesh_info.get('location', (0, 0, 0))
    obj.rotation_euler = mesh_info.get('rotation', (0, 0, 0))

    # Create mesh from vertices and faces
    mesh.from_pydata(mesh_info['vertices'], [], mesh_info['faces'])
    
    # Update the mesh with the new data
    mesh.update()

    return obj

# Function to set the view to the 3D Viewport
def set_viewport_to_3d():
    # Loop through all areas to find the 3D Viewport
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            # Set the shading type to Material Preview
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'  # Set shading to Material Preview
                    break

# Function to blink an object
def blink_object(obj, blinks=5, interval=0.5):
    original_visibility = obj.hide_viewport
    # Blink the object by toggling visibility
    for _ in range(blinks):
        obj.hide_viewport = not original_visibility
        bpy.context.view_layer.update()
        time.sleep(interval)  # Use sleep to create the blinking effect
        obj.hide_viewport = original_visibility
        bpy.context.view_layer.update()
        time.sleep(interval)

# Function to remove the default cube if it exists
def remove_default_cube():
    default_cube = bpy.data.objects.get("Cube")
    if default_cube:
        bpy.data.objects.remove(default_cube, do_unlink=True)

# Main execution
if __name__ == "__main__":
    # Path to the JSON file
    json_path = "D:\\Karun's temp backup\\OSS\\mesh.json"  # Update with your path

    # Remove the default cube
    remove_default_cube()

    # Load mesh data from JSON
    mesh_data = load_mesh_data(json_path)

    # Create mesh objects for each entry in the data
    for mesh_info in mesh_data:
        obj = create_mesh_object(mesh_info)
        blink_object(obj)  # Blink the created object

    print("3D models created from JSON data.")

    # Set the viewport to 3D View and switch to Material Preview
    set_viewport_to_3d()

    print("Live preview is set. You can manually focus on the models in the 3D viewport.")
