import os
from tkinter import Tk, filedialog, StringVar, OptionMenu, Toplevel
from tkinter import ttk
from PIL import Image, ImageTk

def main():
    '''
    The main function that calls other functions to perform sprite conversion.
    
    '''
    run_ui()

def image_to_pixels(input_path, sprite_size, pallete = None):
    '''
    Converts image to sprite with optional pallete.
    
    '''

    img = Image.open(input_path).convert("RGB")
    
    small = img.resize((sprite_size, sprite_size), Image.NEAREST)

    if pallete:
            small = small.quantize(palette=pallete)


    return small

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
        
        sprite_size = int(sprite_size_var.get().split("x")[0])
        
        output_folder = "converted_sprites"
        os.makedirs(output_folder,exist_ok=True)

        for path in selected_files:
            filename = os.path.basename(path)
            output_path = os.path.join(output_folder, f"sprite_{sprite_size}x{sprite_size}_" + filename)

            sprite = image_to_pixels(path, sprite_size)
            if sprite:
                sprite.save(output_path)
            
        file_label.config(text="Conversion completed!")

    def preview_image():

        if not selected_files:
            file_label.config(text="No files selected!")
            return

        sprite_size = int(sprite_size_var.get().split("x")[0])

        sprite = image_to_pixels(selected_files[0], sprite_size)
        if sprite is None:
            return
        
        display_image = sprite.resize((sprite_size*16, sprite_size*16), Image.NEAREST)

        preview_window = Toplevel(root)
        preview_window.title("Sprite Preview")

        tk_img = ImageTk.PhotoImage(display_image)

        img_label = ttk.Label(preview_window, image=tk_img)
        img_label.image = tk_img
        img_label.pack(pady=10)

        preview_window.mainloop()

    ttk.Label(root, text="Sprite Converter", font=("Arial", 16)).pack(pady=10)
    ttk.Button(root, text="Select Images", command=select_files).pack()

    file_label = ttk.Label(root, text="No files selected")
    file_label.pack(pady=5)

    ttk.Label(root, text="Select Sprite Size:").pack()
    OptionMenu(root, sprite_size_var, sprite_sizes[0], *sprite_sizes).pack(pady=5)

    ttk.Button(root, text="Convert Images", command=convert_images).pack(pady=10)
    ttk.Button(root, text="Preview First Image", command=preview_image).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()