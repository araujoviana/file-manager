import dearpygui.dearpygui as dpg

import os

home_dir = os.path.expanduser("~")
contents = os.listdir(home_dir)

# Navigation functions


# TODO Open files, this only navigates through folders
def file_clicked(sender, app_data, user_data):
    parent_id = dpg.get_item_parent(sender)

    working_directory_files = dpg.get_item_children(parent_id)[1]

    # Log
    print(f"File clicked:{user_data}")
    print(f"Parent ID: {parent_id}")
    print(f"Children: {working_directory_files}")

    for file in working_directory_files:

        if dpg.get_item_type(file) == "mvAppItemType::mvButton":
            dpg.delete_item(file)
            print(f"Hiding {file}")

    # HACK doesn't work on windows, unless you add a ternary checking for os(?)
    contents = os.listdir(home_dir + "/" + user_data)


# Main window
dpg.create_context()
dpg.create_viewport(title="File Manager", decorated=True, width=800, height=600)
dpg.setup_dearpygui()

with dpg.window(
    label="",
    width=800,
    height=600,
    no_move=True,
    no_title_bar=True,
    no_close=True,
    no_resize=True,
    no_collapse=True,
):
    for file in contents:
        dpg.add_button(label=file, callback=file_clicked, user_data=file)


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
