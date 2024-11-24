import dearpygui.dearpygui as dpg
import os

home_dir = os.path.expanduser("~")
contents = os.listdir(home_dir)  # Current directory's files
current_dir = home_dir  # Always starts in home directory

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

    for file in contents:
        dpg.add_button(
            label=file, callback=folder_clicked, user_data=file, parent="FileWindow"
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
