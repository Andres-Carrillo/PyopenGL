import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Hello World', width=600, height=400)

with dpg.window(label="Hello, World!"):
    dpg.add_text("Hello, World!")
    dpg.add_button(label="Click Me", callback=lambda: print("Button clicked!"))
    dpg.add_input_text(label="Input Text", default_value="Type here...")
    dpg.add_slider_float(label="Slider", default_value=0.5, min_value=0.0, max_value=1.0)
    dpg.add_checkbox(label="Checkbox", default_value=True)
    dpg.add_radio_button(label="Radio Button", items=["Option 1", "Option 2", "Option 3"], default_value="Option 1")
    dpg.add_combo(label="Combo Box", items=["Item 1", "Item 2", "Item 3"], default_value="Item 1")
    dpg.add_listbox(label="List Box", items=["List Item 1", "List Item 2", "List Item 3"], default_value="List Item 1")
    dpg.add_color_picker(label="Color Picker", default_value=(1.0, 0.0, 0.0, 1.0))



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()