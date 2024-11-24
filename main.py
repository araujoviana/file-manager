import dearpygui.dearpygui as dpg

import os

home_dir = os.path.expanduser("~")
contents = os.listdir(home_dir)

# Navigation functions


# TODO Open files, this only navigates through folders
def file_clicked(sender, app_data, user_data):
    parent_id = dpg.get_item_parent(sender)

    # Log
    working_directory_files = dpg.get_item_children(parent_id)[1]
    print(f"File clicked:{user_data}")
    print(f"Parent ID: {parent_id}")
    print(f"Children: {working_directory_files}")

    new_dir = os.path.join(
        home_dir,
        user_data,
    )
    contents = os.listdir(new_dir)
    print(new_dir)
    display_working_dir_files(new_dir, contents)


def display_working_dir_files(directory, contents):
    for button in dpg.get_item_children("FileWindow")[1]:
        dpg.delete_item(button)

    for file in contents:
        dpg.add_button(
            label=file, callback=file_clicked, user_data=file, parent="FileWindow"
        )


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
    tag="FileWindow",
):

    display_working_dir_files(home_dir, contents)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
