import dearpygui.dearpygui as dpg

import os

home_dir = os.path.expanduser("~")
contents = os.listdir(home_dir)

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
        dpg.add_button(label=file)


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
