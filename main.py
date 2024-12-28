import sys
import os
from tkinter import (Tk, Canvas, Frame, Button, Scale, colorchooser, messagebox, Label, NW)
from tkinter import BOTH, LEFT, RIGHT, TOP, BOTTOM, X, HORIZONTAL
from PIL import Image, ImageTk, ImageDraw, ImageColor


class ImagePainter:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Image Painter")
        self.image_path = image_path

        # Define maximum window size
        self.max_width = 800
        self.max_height = 600

        # Initialize undo stack
        self.undo_stack = []

        # Load and prepare the image
        self.original_image = Image.open(self.image_path).convert("RGB")
        self.scaled_image, self.scale_ratio = self.auto_scale_image(self.original_image)
        self.image = self.scaled_image.copy()
        self.draw = ImageDraw.Draw(self.image)

        # Set up the Tkinter Canvas
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas = Canvas(root, width=self.scaled_image.width, height=self.scaled_image.height, cursor="cross")
        self.canvas.pack()

        # Display the image on the canvas
        self.canvas_image = self.canvas.create_image(0, 0, anchor=NW, image=self.tk_image)

        # Initialize tool attributes
        self.current_color = "#FF0000"  # Default color: Red for visibility
        self.brush_size = 5             # Default brush size
        self.last_x, self.last_y = None, None  # Previous mouse coordinates
        self.current_tool = "brush"     # Default tool

        # Setup the toolbar with functionalities
        self.setup_toolbar()

        # Bind mouse events for painting and flood fill
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Bind keyboard shortcuts for saving and undo
        self.root.bind("<Control-s>", self.save_override)
        self.root.bind("<Control-S>", self.save_override)
        self.root.bind("<Control-Shift-s>", self.save_as_copy)
        self.root.bind("<Control-Shift-S>", self.save_as_copy)
        self.root.bind("<Control-z>", self.undo)       # Bind Ctrl+Z to undo

    # Scales the image to fit within the maximum window size while maintaining aspect ratio.
    def auto_scale_image(self, image):
        original_width, original_height = image.size
        print(f"Original image size: {original_width}x{original_height}")

        # Determine scaling ratio
        ratio = min(self.max_width / original_width, self.max_height / original_height, 1)
        print(f"Scaling ratio: {ratio}")

        # Calculate new dimensions
        new_width = int(round(original_width * ratio))
        new_height = int(round(original_height * ratio))
        print(f"Scaled image size: {new_width}x{new_height}")

        # Resize the image if necessary
        if ratio < 1:
            # Use a compatible resampling filter
            resample_filter = self.get_resample_filter()
            scaled_image = image.resize((new_width, new_height), resample=resample_filter)
        else:
            scaled_image = image.copy()
            
        return scaled_image, ratio

    # Retrieves the appropriate resampling filter based on Pillow version.
    def get_resample_filter(self):
        try:
            return Image.Resampling.LANCZOS
        except AttributeError:
            return Image.LANCZOS

    # Sets up the toolbar with buttons and sliders for color selection, brush size, and saving.
    def setup_toolbar(self):
        toolbar = Frame(self.root, bd=1, relief='raised')
        toolbar.pack(side=TOP, fill=X)

        # Color Picker Button
        color_btn = Button(toolbar, text="Color", command=self.choose_color)
        color_btn.pack(side=LEFT, padx=2, pady=2)

        # Brush Tool Button
        brush_btn = Button(toolbar, text="Brush", command=self.select_brush)
        brush_btn.pack(side=LEFT, padx=2, pady=2)

        # Flood Fill Tool Button
        flood_fill_btn = Button(toolbar, text="Flood Fill", command=self.select_flood_fill)
        flood_fill_btn.pack(side=LEFT, padx=2, pady=2)

        # Brush Size Slider with Label
        size_label = Label(toolbar, text="Brush Size:")
        size_label.pack(side=LEFT, padx=(10, 2), pady=2)
        self.size_slider = Scale(toolbar, from_=1, to=50, orient=HORIZONTAL, command=self.change_brush_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=LEFT, padx=2, pady=2)

        # Spacer Label for better layout
        spacer = Label(toolbar, text="  ")
        spacer.pack(side=LEFT, padx=20)

        # Save Buttons
        save_btn = Button(toolbar, text="Save (Ctrl+S)", command=self.save_override)
        save_btn.pack(side=RIGHT, padx=2, pady=2)
        save_as_btn = Button(toolbar, text="Save As Copy (Ctrl+Shift+S)", command=self.save_as_copy)
        save_as_btn.pack(side=RIGHT, padx=2, pady=2)

    # Opens a color picker dialog and sets the current color to the selected color.
    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code and color_code[1]:
            self.current_color = color_code[1]
            print(f"Selected color: {self.current_color}")

    # Sets the current tool to brush.
    def select_brush(self):
        self.current_tool = "brush"
        print("Brush tool selected.")

    # Sets the current tool to flood fill.
    def select_flood_fill(self):
        self.current_tool = "flood_fill"
        print("Flood Fill tool selected.")

    # Changes the brush size based on the slider value.
    def change_brush_size(self, val):
        self.brush_size = int(val)

    # Handles the mouse button press event.
    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y
        if self.current_tool == "brush":
            # Save the current image state to the undo stack before drawing
            self.undo_stack.append(self.image.copy())
        elif self.current_tool == "flood_fill":
            # Save the current image state to the undo stack before flood fill
            self.undo_stack.append(self.image.copy())
            # Perform flood fill
            x = int(round(event.x))
            y = int(round(event.y))
            # Clamp coordinates to ensure they are within bounds
            x = min(max(x, 0), self.image.width - 1)
            y = min(max(y, 0), self.image.height - 1)
            print(f"Seed point coordinates: ({x}, {y})")
            try:
                rgb_color = ImageColor.getrgb(self.current_color)
            except ValueError:
                messagebox.showerror("Color Error", "Selected color is invalid.")
                print("Invalid color selected.")
                return

            try:
                original_color = self.image.getpixel((x, y))
                print(f"Clicked pixel color: {original_color}")
                if original_color == (0, 0, 0):
                    messagebox.showinfo("Flood Fill", "Cannot flood fill on black pixels.")
                    print("Attempted to flood fill on black pixels. Operation skipped.")
                    return  # Do nothing if clicked on black pixels
                if original_color == rgb_color:
                    messagebox.showinfo("Flood Fill", "Selected color is the same as the target color. No fill performed.")
                    print("Selected color is the same as target color. Operation skipped.")
                    return
                self.flood_fill(x, y, rgb_color)
                # Update the canvas with the flood-filled image
                self.update_canvas()
                print(f"Flood filled at ({x}, {y}) with color {rgb_color}.")
            except IndexError:
                messagebox.showerror("Flood Fill Error", "Clicked coordinates are out of image bounds.")
                print(f"Clicked coordinates ({x}, {y}) are out of image bounds.")
            except Exception as e:
                messagebox.showerror("Flood Fill Error", f"An error occurred during flood fill: {e}")
                print(f"Error during flood fill: {e}")

    # Draws on the image as the mouse is dragged or applies flood fill on click.
    def paint(self, event):
        x, y = event.x, event.y
        if self.current_tool == "brush" and self.last_x is not None and self.last_y is not None:
            fill_color = self.current_color

            # Draw a line between the last and current mouse positions
            self.draw.line([self.last_x, self.last_y, x, y], fill=fill_color, width=self.brush_size)
            # Update the canvas with the new image
            self.update_canvas()
            # Update the last positions
            self.last_x, self.last_y = x, y
        elif self.current_tool == "flood_fill":
            # Flood fill is triggered on mouse press, not drag
            pass

    # Handles the mouse button release event.
    def on_button_release(self, event):
        if self.current_tool == "brush":
            self.last_x, self.last_y = None, None
        elif self.current_tool == "flood_fill":
            self.last_x, self.last_y = None, None

    # Performs flood fill on the image at the specified coordinates with the given color.
    def flood_fill(self, x, y, replacement_color):
        try:
            # Ensure image is in RGB mode
            if self.image.mode != "RGB":
                self.image = self.image.convert("RGB")
                self.draw = ImageDraw.Draw(self.image)

            original_color = self.image.getpixel((x, y))
            if original_color == replacement_color:
                print("Replacement color is the same as the original color. No fill performed.")
                return  # No need to fill if the color is the same

            width, height = self.image.size
            pixels = self.image.load()
            stack = [(x, y)]
            while stack:
                current_x, current_y = stack.pop()
                if current_x < 0 or current_x >= width or current_y < 0 or current_y >= height:
                    continue  # Skip out-of-bounds coordinates
                if pixels[current_x, current_y] != original_color:
                    continue
                pixels[current_x, current_y] = replacement_color
                stack.append((current_x - 1, current_y))
                stack.append((current_x + 1, current_y))
                stack.append((current_x, current_y - 1))
                stack.append((current_x, current_y + 1))
            print(f"Performed flood fill at ({x}, {y}) with color {replacement_color}.")
        except Exception as e:
            print(f"Error during flood fill: {e}")
            messagebox.showerror("Flood Fill Error", f"An error occurred during flood fill: {e}")

    # Updates the canvas with the current image.
    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvas_image, image=self.tk_image)

    # Saves the edited image to the original file path.
    def save_override(self, event=None):
        try:
            # If the image was scaled, save the original size
            if self.scale_ratio != 1:
                # Resize the edited image back to original size
                resized_image = self.image.resize(self.original_image.size, resample=self.get_resample_filter())
                resized_image.save(self.image_path)
            else:
                self.image.save(self.image_path)
            messagebox.showinfo("Save", "Image saved successfully!")
            print(f"Image saved to {self.image_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")
            print(f"Error saving image: {e}")

    # Saves the edited image as a copy with "-edited" appended to the filename.
    def save_as_copy(self, event=None):
        try:
            # If the image was scaled, save the original size
            if self.scale_ratio != 1:
                resized_image = self.image.resize(self.original_image.size, resample=self.get_resample_filter())
            else:
                resized_image = self.image

            directory, filename = os.path.split(self.image_path)
            name, ext = os.path.splitext(filename)
            new_name = f"{name}-edited{ext}"
            new_path = os.path.join(directory, new_name)
            resized_image.save(new_path)
            messagebox.showinfo("Save As", f"Image saved as {new_name}!")
            print(f"Image saved as {new_name}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")
            print(f"Error saving image as copy: {e}")

    # Undoes the last adjustment made to the image.
    def undo(self, event=None):
        if self.undo_stack:
            # Pop the last image state from the stack
            self.image = self.undo_stack.pop()
            self.draw = ImageDraw.Draw(self.image)

            # Update the canvas with the reverted image
            self.update_canvas()
            messagebox.showinfo("Undo", "Last adjustment has been undone.")
            print("Undo performed.")
        else:
            messagebox.showinfo("Undo", "No more adjustments to undo.")
            print("Undo stack is empty.")

# Main function to run the application.
def main():
    if len(sys.argv) != 2:
        print("Usage: image_painter.exe <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.isfile(image_path):
        print(f"File not found: {image_path}")
        sys.exit(1)

    if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        print("Unsupported file format. Please use .jpg or .png images.")
        sys.exit(1)

    root = Tk()
    app = ImagePainter(root, image_path)
    root.mainloop()


if __name__ == "__main__":
    main()