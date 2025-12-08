import os
from tkinter import Tk, filedialog, StringVar, OptionMenu, Toplevel, DoubleVar
from tkinter import ttk, Scale, HORIZONTAL
from PIL import Image, ImageTk, ImageEnhance

Palettes = {
    "Default": None,
    "Gameboy": [
        (15, 56, 15),
        (48, 98, 48),
        (139, 172, 15),
        (155, 188, 15)],
    "NES":[
        (124, 124, 124), (0, 0, 252), (0, 0, 188), (68, 40, 188),
        (148, 0, 132), (168, 0, 32), (168, 16, 0), (136, 20, 0),
        (80, 48, 0), (0, 120, 0), (0, 104, 0), (0, 88, 0),
        (0, 64, 88), (0, 0, 0), (0, 0, 0), (0, 0, 0)
    ],
    "Pico-8":[
         (0, 0, 0), (29, 43, 83), (126, 37, 83), (0, 135, 81),
        (171, 82, 54), (95, 87, 79), (194, 195, 199), (255, 241, 232),
        (255, 0, 77), (255, 163, 0), (255, 240, 36), (0, 231, 86),
        (41, 173, 255), (131, 118, 156), (255, 119, 168), (255, 204, 170)
    ],
}

def make_palette(rbg_list):
    '''
    Creates a palette image from a list of RGB tuples.
    
    '''
    if rbg_list is None:
        return None
    
    flat = []
    for (r, g, b) in rbg_list:
        flat.extend([r, g, b])

    pad_len = 256 * 3 - len(flat)
    if pad_len > 0:
        flat.extend([0] * pad_len)

    palette_img = Image.new("P", (16, 16))
    palette_img.putpalette(flat)
    return palette_img

Palette_Images = {
    name: (None if rgba is None else make_palette(rgba)) for name, 
    rgba in Palettes.items()
    }

def main():
    '''
    The main function that calls other functions to perform sprite conversion.
    
    '''
    run_ui()

def image_to_pixels(input_path, sprite_size, brightness=1.0, contrast=1.0, saturation=1.0, palette_name="Default"):
    '''
    Converts image to sprite with optional pallete.
    
    '''
    img = Image.open(input_path).convert("RGBA")
    rgb = img.convert("RGB")
    a = img.getchannel("A")

    # Image Adjustments
    rgb = ImageEnhance.Brightness(rgb).enhance(brightness)
    rgb = ImageEnhance.Contrast(rgb).enhance(contrast)
    rgb = ImageEnhance.Color(rgb).enhance(saturation)

    img = Image.merge("RGBA", (*rgb.split(),a))

    small = img.resize((sprite_size, sprite_size), Image.NEAREST)

    palette_img = Palette_Images.get(palette_name)
    if palette_img is not None:
        rgb_small = small.convert("RGB").quantize(palette=palette_img).convert("RGB")
        alpha_small = small.getchannel("A")

        small = Image.merge("RGBA", (*rgb_small.split(), alpha_small))


    return small

def run_ui():
    '''
    Main application UI.
    
    '''
    root = Tk()
    root.title("Image to Sprite Converter")
    root.geometry("800x500")

    # Sprite size selection
    sprite_sizes = ["8x8", "16x16", "32x32", "64x64", "128x128"]
    sprite_size_var = StringVar(root)
    sprite_size_var.set(sprite_sizes[0])

    # Palette selection
    palette_names = list(Palettes.keys())
    palette_var = StringVar(root)
    palette_var.set(palette_names[0])

    # Selected files 
    selected_files = []

    # Slider values
    brightness_var = DoubleVar(value=1.0)
    contrast_var = DoubleVar(value=1.0)
    saturation_var = DoubleVar(value=1.0)

    # Preview Window Variables
    preview_window = None
    preview_label = None
    preview_img = None

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

            sprite = image_to_pixels(path, sprite_size, 
                                     brightness_var.get(), 
                                     contrast_var.get(), 
                                     saturation_var.get(),
                                     palette_name=palette_var.get())
            sprite.save(output_path)

        file_label.config(text="Conversion completed!")

    def update_preview(*args):
        nonlocal preview_window, preview_label, preview_img
        if not selected_files:
            return

        try:
            sprite_size = int(sprite_size_var.get().split("x")[0])
        except Exception:
            sprite_size = 16

        sprite = image_to_pixels(
        selected_files[0], sprite_size, 
        brightness_var.get(), 
        contrast_var.get(), 
        saturation_var.get(),
        palette_name=palette_var.get()
        )

        scale_factor = max(4, 512 // max(1, sprite_size))
        display_w = sprite_size * scale_factor
        display_h = sprite_size * scale_factor
        display_img = sprite.resize((display_w, display_h), Image.NEAREST)

        tk_img = ImageTk.PhotoImage(display_img.convert("RGBA"))

        if preview_window is None or not preview_window.winfo_exists():
            preview_window = Toplevel(root)
            preview_window.title("Preview")
            preview_label = ttk.Label(preview_window, image=tk_img)
            preview_label.image = tk_img
            preview_label.pack(padx=10, pady=10)

        else:
            preview_label.config(image=tk_img)
            preview_label.image = tk_img

    ttk.Label(root, text="Image to Sprite Converter", font=("Arial", 16)).pack(pady=10)
    ttk.Button(root, text="Select Images", command=select_files).pack()

    file_label = ttk.Label(root, text="No files selected")
    file_label.pack(pady=5)

    top_row = ttk.Frame(root)
    top_row.pack(fill="x", pady=10)

    ttk.Label(root, text="Select Sprite Size:").pack()
    OptionMenu(root, sprite_size_var, sprite_sizes[0], *sprite_sizes[1:]).pack(pady=5)

    ttk.Label(top_row, text="Palette:").grid(row=0, column=2, sticky="w", padx=(12,0))
    OptionMenu(top_row, palette_var, palette_names[0], *palette_names[1:], command=lambda e: update_preview()).grid(row=0, column=3, padx=6)

    ttk.Label(root, text="Brightness").pack()
    Scale(root, from_=0.2, to=2.5, orient=HORIZONTAL, resolution=0.1,
          variable=brightness_var, command=lambda e:update_preview()).pack(fill="x", padx=20)

    ttk.Label(root, text="Contrast").pack()
    Scale(root, from_=0.2, to=2.5, orient=HORIZONTAL, resolution=0.1,
          variable=contrast_var,command=lambda e:update_preview()).pack(fill="x", padx=20)

    ttk.Label(root, text="Saturation").pack()
    Scale(root, from_=0.2, to=2.5, orient=HORIZONTAL, resolution=0.1,
          variable=saturation_var,command=lambda e:update_preview()).pack(fill="x", padx=20)

    ttk.Button(root, text="Convert Images", command=convert_images).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()