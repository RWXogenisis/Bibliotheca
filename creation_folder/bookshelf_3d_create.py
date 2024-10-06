
import trimesh
import numpy as np

def create_bookshelf():
    # Dimensions of the bookshelf
    shelf_width = 1.0
    shelf_depth = 0.3
    shelf_height = 1.8
    rack_thickness = 0.05
    rack_height = shelf_height / 4

    # Create the back panel of the bookshelf
    back_panel = trimesh.creation.box(extents=[shelf_width, rack_thickness, shelf_height])

    # Create the side panels of the bookshelf
    side_panel = trimesh.creation.box(extents=[rack_thickness, shelf_depth, shelf_height])
    left_side_panel = side_panel.copy()
    left_side_panel.apply_translation([-(shelf_width / 2 - rack_thickness / 2), 0, 0])

    right_side_panel = side_panel.copy()
    right_side_panel.apply_translation([(shelf_width / 2 - rack_thickness / 2), 0, 0])

    # Create the bottom panel of the bookshelf
    bottom_panel = trimesh.creation.box(extents=[shelf_width, shelf_depth, rack_thickness])
    bottom_panel.apply_translation([0, -(shelf_depth / 2 - rack_thickness / 2), -(shelf_height / 2 - rack_thickness / 2)])

    # Create the shelves
    shelves = []
    for i in range(4):
        shelf = trimesh.creation.box(extents=[shelf_width, shelf_depth, rack_thickness])
        shelf.apply_translation([0, -(shelf_depth / 2 - rack_thickness / 2), -(shelf_height / 2 - rack_thickness / 2) + (i + 1) * rack_height])
        shelves.append(shelf)

    # Combine all the parts into one mesh
    bookshelf_parts = [back_panel, left_side_panel, right_side_panel, bottom_panel] + shelves
    bookshelf = trimesh.util.concatenate(bookshelf_parts)

    return bookshelf

# Create the bookshelf model
bookshelf = create_bookshelf()

# Export the model to an STL file
bookshelf.export('bookshelf.stl')

# Visualize the bookshelf
bookshelf.show()
