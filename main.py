# REVIEW theres like 5 repeated global current_dir throughout the entire code

import dearpygui.dearpygui as dpg
import os
import subprocess
import platform
import mimetypes
import datetime

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
    """Update interface to show working directory's files in a grid."""
    for button in dpg.get_item_children("FileWindow")[1]:
        dpg.delete_item(button)

    add_basic_fields()

    with dpg.table(
        parent="FileWindow",
        header_row=True,
        resizable=True,
        borders_innerH=True,
        borders_outerH=True,
    ):
        # Column for file/folder names
        dpg.add_table_column(label="Name")
        # Column for file size
        dpg.add_table_column(label="Size")
        # Column for file type
        dpg.add_table_column(label="Type")
        # Column for last modification
        dpg.add_table_column(label="Last modified")

        for item in contents:
            item_path = os.path.join(directory, item)

            with dpg.table_row():
                if os.path.isfile(item_path):
                    # It's a file
                    dpg.add_button(
                        label=item,
                        callback=file_clicked,
                        user_data=item,
                    )

                    # Calculate item size with correct measure
                    item_size = os.path.getsize(item_path)
                    if item_size >= 1048576:  # 1 MB
                        display_item_size = f"{item_size / 1048576:.2f} MB"
                    elif item_size >= 1024:  # 1 KB
                        display_item_size = f"{item_size / 1024:.2f} KB"
                    else:
                        display_item_size = f"{item_size} B"

                    dpg.add_text(display_item_size)

                    file_type, _ = mimetypes.guess_type(item_path)
                    dpg.add_text(file_type if file_type is not None else "Unknown")

                    mod_time = os.path.getmtime(item_path)
                    last_modified_date = datetime.datetime.fromtimestamp(
                        mod_time
                    ).strftime("%Y-%m-%d %H:%M:%S")

                    dpg.add_text(last_modified_date)

                else:
                    # It's a folder
                    dpg.add_button(
                        label=item,
                        callback=folder_clicked,
                        user_data=item,
                    )


def add_basic_fields():
    """Add and display essential UI components."""
    # Create a theme for the button
    with dpg.theme() as ui_theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core
            )  # Optional, rounded corners

    # Back button
    back_button = dpg.add_button(
        label="Back",
        callback=back_button_clicked,
        parent="FileWindow",
        arrow=True,
        direction=dpg.mvDir_Left,
    )

    # Apply the theme to the back button
    dpg.bind_item_theme(back_button, ui_theme)

    # Current PATH
    dpg.add_text(
        current_dir,
        parent="FileWindow",
    )

    dpg.add_separator(parent="FileWindow")


# Helper functions


# Main Window

dpg.create_context()
dpg.create_viewport(
    title="File Manager",
    decorated=True,
    width=800,
    height=600,
)
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

# General configs
# REVIEW Font looks ugly
# dpg.set_global_font_scale(1.25)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
