import bpy
import time
import json 

# Load the bookshelf mesh data from JSON
def load_mesh_data(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)

# Highlight the specified parts of the bookshelf
def highlight_bookshelf(book_id, mesh_data):
    row, shelf, rack = map(int, book_id.split('_'))

    # Mapping rows to the corresponding part numbers based on the data you provided
    row_to_part = {
        1: range(0, 6),
        2: range(6, 12),
        3: range(18, 24),
        4: range(12, 18),
        5: range(24, 30),
        6: range(30, 36)
    }

    # Find the 3D view area
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            with bpy.context.temp_override(area=area):
                # Top view and highlight row + shelf
                bpy.ops.view3d.view_axis(type='TOP')

                # Highlight row and shelf
                row_parts = row_to_part.get(row, [])
                shelf_part = row_parts[shelf - 1] if 1 <= shelf <= 6 else None

                if shelf_part is not None:
                    part_name = f"bookshelf.{shelf_part:03d}"
                    part = bpy.data.objects.get(part_name)
                    
                    if part:
                        highlight_object(part)
                        blink_object(part, 5, (1, 0, 0, 1))  # Blink in red
                        
                        # Switch to front view and highlight rack
                        bpy.ops.view3d.view_axis(type='FRONT')
                        highlight_rack(part, rack)
                    else:
                        print(f"Part '{part_name}' not found.")
            break
    else:
        print("3D Viewport not found.")

# Highlighting the object
def highlight_object(obj):
    mat = bpy.data.materials.get("HighlightMaterial") or bpy.data.materials.new(name="HighlightMaterial")
    mat.diffuse_color = (1, 0, 0, 1)  # Set red color
    obj.data.materials.clear()  # Remove previous materials
    obj.data.materials.append(mat)

# Blink the object
def blink_object(obj, blinks, color):
    for _ in range(blinks):
        obj.hide_viewport = True
        bpy.context.view_layer.update()
        time.sleep(0.5)
        obj.hide_viewport = False
        highlight_object(obj)
        bpy.context.view_layer.update()
        time.sleep(0.5)

# Highlight the specific rack inside the shelf
def highlight_rack(shelf, rack):
    rack_index = rack - 1  # Assuming rack indexing starts from 1
    if 0 <= rack_index < len(shelf.children):
        rack_part = shelf.children[rack_index]
        blink_object(rack_part, 5, (1, 0, 0, 1))  # Blink in red
        
# Main execution
if __name__ == "__main__":
    book_id = "01_01_01"  # Example book ID

    # Path to the JSON file
    json_path = "D:\\Karun's temp backup\\OSS\\mesh.json"  # Update with your path

    # Load mesh data
    mesh_data = load_mesh_data(json_path)
    
    # Highlight the corresponding part of the bookshelf
    highlight_bookshelf(book_id, mesh_data)
