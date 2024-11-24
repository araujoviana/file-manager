# REVIEW theres like 5 repeated global current_dir throughout the entire code

import dearpygui.dearpygui as dpg
import os
import subprocess
import platform

home_dir = os.path.expanduser("~")
contents = os.listdir(home_dir)  # Current directory's files
current_dir = home_dir  # Always starts in home directory

# Interaction functions


def file_clicked(sender, app_data, user_data):
    """Open clicked file using appropriate program."""
    global current_dir
    file_path = os.path.join(current_dir, user_data)

    # Opens file with system's default
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.call(("open", file_path))
    else:  # Linux
        subprocess.call(("xdg-open", file_path))


# Navigation functions


def folder_clicked(sender, app_data, user_data):
    """
    Step into clicked folder.

    Updates current directory and displayed files
    """
    global current_dir  # REVIEW there must be a better way of doing this

    # Appends clicked folder to current path
    new_dir = os.path.join(
        home_dir,
        user_data,
    )
    new_dir = os.path.join(current_dir, user_data)
    contents = os.listdir(new_dir)
    current_dir = new_dir

    display_working_dir_files(new_dir, contents)


def back_button_clicked(sender, app_data, user_data):
    """Update current directory to parent."""
    global current_dir
    current_dir = os.path.dirname(current_dir)
    contents = os.listdir(current_dir)

    display_working_dir_files(current_dir, contents)


# Display functions


def display_working_dir_files(directory, contents):
    """Update interface to show working directory's files."""
    for button in dpg.get_item_children("FileWindow")[1]:
        dpg.delete_item(button)

    add_basic_fields()

    for item in contents:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            # It's a folder
            dpg.add_button(
                label=item, callback=folder_clicked, user_data=item, parent="FileWindow"
            )
        else:
            # It's a file
            dpg.add_button(
                label=item, callback=file_clicked, user_data=item, parent="FileWindow"
            )


def add_basic_fields():
    """Add and display essential UI components."""
    dpg.add_button(label="<-", callback=back_button_clicked, parent="FileWindow")


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

    add_basic_fields()

    display_working_dir_files(home_dir, contents)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
