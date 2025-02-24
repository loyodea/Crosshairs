import json
import tkinter as tk
from PIL import Image, ImageTk
import keyboard
import threading
from pynput import mouse

root = tk.Tk()

canvas = None

# Make sure that these two are the biggest crosshair you plan on using!!!!
background_path = 'Crosshairs/Hide.png'
overlay_path = 'Crosshairs/Hide.png'
transparent_color = 'black'
# Make sure that these two are the biggest crosshair you plan on using!!!!

# Flags to either hide crosshair or print keys
hide = False
debug = False
# Add keybinds for each crosshair (add another list if needed and don't forget to add another update_window in the function on line 57!!)
with open('binds.json', 'r') as file:
    data = json.load(file)
keybinds_default = data['keybinds_default']
keybinds_plus = data['keybinds_plus']
keybinds_shotgun = ['keybinds_shotgun']
keybinds_hide = data['keybinds_hide']
keybinds_quit = data['keybinds_quit']
keybinds_debug = data['keybinds_debug']

print(f'----> edit binds.json to change keybinds')
print('----> to change a crosshair simply change one of the files in the Crosshairs folder (make sure it has the same '
      'name as one that already exists or it wont work)')
print(f'----> to see what button you are pressing press {keybinds_debug}')
print(f'----> to hide crosshair press {keybinds_hide} can also be configured in main.py')
print(f'----> to quit press {keybinds_quit}')


def update_window(background_path, overlay_path, transparent_color):
    global canvas, root

    # Load the background and overlay images
    background = Image.open(background_path).convert("RGBA")
    overlay = Image.open(overlay_path).convert("RGBA")

    # Resize the overlay image to match the background image size
    bg_width, bg_height = background.size
    overlay = overlay.resize((bg_width, bg_height), Image.LANCZOS)

    # Blend the images with some transparency
    alpha = 0.0  # Adjust alpha for transparency
    blended = Image.blend(background, overlay, alpha)

    # Remove window decorations and make it topmost
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.attributes('-transparentcolor', transparent_color)

    # Set the geometry of the window to the size of the image
    root.geometry(
        f'{bg_width}x{bg_height}+{(root.winfo_screenwidth() - bg_width) // 2}+{(root.winfo_screenheight() - bg_height) // 2}')

    # Convert the blended image to a format that Tkinter can use
    blended = blended.convert("RGBA")
    blended_tk = ImageTk.PhotoImage(blended)

    # Create a canvas to hold the image
    if canvas is None:
        canvas = tk.Canvas(root, width=bg_width, height=bg_height, highlightthickness=0, bg=transparent_color)
        canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=blended_tk)
    canvas.image = blended_tk  # Keep a reference to the image to prevent it from being garbage collected


# Function to handle key press event ADD MORE CROSSHAIRS HERE!!
def on_key_event(e):
    global hide
    global debug
    if debug:
        print(f'keyboard pressed: {e.name}')
    if e.name in keybinds_default and not hide:
        update_window("Crosshairs/default.png", 'Crosshairs/default.png', 'black')

    elif e.name in keybinds_plus and not hide:
        update_window('Crosshairs/plus.png', 'Crosshairs/plus.png', 'black')

    elif e.name in keybinds_shotgun and not hide:
        update_window('Crosshairs/DefaultShotgun.png', 'Crosshairs/DefaultShotgun.png', 'black')

    elif e.name in keybinds_hide:
        if not hide:
            update_window('Crosshairs/Hide.png', 'Crosshairs/Hide.png', 'black')
            hide = True
        else:
            update_window("Crosshairs/default.png", 'Crosshairs/default.png', 'black')
            hide = False
    elif e.name in keybinds_debug:
        if not debug:
            debug = True
        else:
            debug = False
    elif e.name == keybinds_quit[0]:
        root.quit()
        root.update()


# Function to start listening for hotkey
def keyboard_listener():
    keyboard.on_press(on_key_event)


def mouse_listener():
    def on_click(x, y, button, pressed):
        global hide
        global debug

        if debug:
            print(f'mouse pressed: {button.name}')
        if button.name in keybinds_default and not hide:
            update_window("Crosshairs/default.png", 'Crosshairs/default.png', 'black')

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


# Start the keyboard listener in a separate thread
keyboard_listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
keyboard_listener_thread.start()

# Start the mouse listener in a separate thread
mouse_listener_thread = threading.Thread(target=mouse_listener, daemon=True)
mouse_listener_thread.start()

# Create and display the initial window
update_window(background_path, overlay_path, transparent_color)
root.mainloop()
