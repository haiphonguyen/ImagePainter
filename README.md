
# Image Painter


**Image Painter** is a simple yet powerful image editing tool built with Python's Tkinter library for the graphical user interface (GUI) and Pillow (PIL) for image processing.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Supported Formats](#supported-formats)
- [Troubleshooting](#troubleshooting)

## Features

- **Freehand Drawing:** Use the brush tool to draw on your images with customizable colors and brush sizes.
- **Flood Fill:** Quickly fill contiguous areas with your chosen color.
- **Undo Functionality:** Revert your last action with ease.
- **Image Scaling:** Automatically scales images to fit within the application window while maintaining aspect ratio.
- **Save Options:** Save your edits by overwriting the original image or saving as a new copy.
- **User-Friendly Interface:** Intuitive toolbar with easy access to all tools and settings.

## Installation

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/phonguyen/ImagePainter.git
   cd ImagePainter
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install Pillow
   ```

4. **Verify Installation**

   Ensure that Tkinter is available by running:

   ```bash
   python -c "import tkinter"
   ```

   If no errors are returned, Tkinter is installed correctly.

## Usage

### Running the Application

1. **Prepare an Image**

   Ensure you have an image file (`.png`, `.jpg`, `.jpeg`) that you want to edit.

2. **Execute the Script**

   ```bash
   python main.py path_to_your_local_image
   ```

3. **Interacting with the Application**

   - **Toolbar:** Located at the bottom, containing buttons for color selection, tool selection (brush or flood fill), brush size adjustment, and saving options.
   - **Canvas:** Displays the loaded image. Use the mouse to draw or apply flood fill.


## Keyboard Shortcuts

- **Save Image:** `Ctrl + S`
- **Save As Copy:** `Ctrl + Shift + S`
- **Undo Last Action:** `Ctrl + Z`


## Supported Formats

- **Input Formats:** `.png`, `.jpg`, `.jpeg`
- **Output Formats:** Saves in the same format as the input image.


## Troubleshooting

- **Pillow Version Issues:**
  
  If you encounter errors related to resampling filters, ensure that you are using a compatible version of Pillow. The application is designed to work with Pillow versions **10.0.0 and above**. You can check your Pillow version with:

  ```bash
  pip show Pillow
  ```

  *To upgrade Pillow:*

  ```bash
  pip install --upgrade Pillow
  ```

- **Tkinter Not Found:**
  
  If you receive an error indicating that Tkinter is not available, install it using your system's package manager.

  - **Ubuntu/Debian:**

    ```bash
    sudo apt-get install python3-tk
    ```

  - **macOS:**
    
    Tkinter is usually included with Python on macOS. If not, consider reinstalling Python using the official installer from [python.org](https://www.python.org/downloads/mac-osx/).

  - **Windows:**
    
    Tkinter comes bundled with the standard Python installer.

- **Unsupported File Format:**
  
  Ensure that you are using supported image formats (`.png`, `.jpg`, `.jpeg`). Other formats may not work as expected.

- **Application Crashes on Launch:**
  
  Verify that all dependencies are installed correctly and that you are using a compatible Python version.
