import os
from tkinter import Tk, filedialog, label, Button, OptionMenu, StringVar
from PIL import Image

def main():
    '''
    The main function that calls other functions to perform sprite conversion.
    
    '''
def image_to_pixels(input_path, sprite_size, pallete = None):
    '''
    Converts image to sprite with optional pallete.
    
    '''
def run_ui():
    '''
    Main application UI.
    
    '''
    root = Tk()
    root.title("Image to Sprite Converter")
    root.geometry("400x250")

    # Sprite size selection
    sprite_sizes = ["8x8", "16x16", "32x32", "64x64"]
    sprite_size_var = StringVar(root)
    sprite_size_var.set(sprite_sizes[0])

    # Selected files 
    selected_files = []

    def select_files():
        nonlocal selected_files
        selected_files = filedialog.askopenfilenames(
            title="Select Images", filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        file_label.config(text=f"Selected: {len(selected_files)} files")


    def convert_images():
        if not selected_files:
            file_label.config(text="No files selected!")
            return
        
        sprite_size = int(size_var.get())
        os.makedirs(output_folder,exist_ok=True)

        for path in selected_files:
            filename = os.path.basename(path)
            output_path = os.path.join(output_folder, f"sprite_{sprite_size}x{sprite_size}_" + filename)

            sprite = image_to_pixels(path, sprite_size)
            if sprite:
                sprite.save(output_path)
            
        file_label.config(text="Conversion completed!")
