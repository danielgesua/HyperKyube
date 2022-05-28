# HyperKyube: OCR Gui MultiTool.

Free and open-source GUI tool designed to automate and simplify
various tasks related to Google's Tesseract-OCR API. 

It's primary purpose is currently to edit lstmbox box files for training the LSTM engine, but the plan is to expand it's features to include:

* Copying OCR text to the clipboard.
* Automating various Tesseract CLI tasks such as:
  * LSTM Training.
  * Running OCR on images.
  * Creation of box files from images.
  * Displaying confidence statistics.
  * Etc.
* Previewing and correcting OCR text prior to file creation.
* Maybe even (in the long term) enabling continuous supervised learning engines that allow tesseract to get better with usage for particular input texts. 

# Dependencies

HyperKyube has a few dependencies. The Gui runs based on python's native tkinter library, and the image manipulations use Python Imaging Library (aka [Pillow](https://github.com/python-pillow/Pillow)).

Apart from that, the development was greatly facilitated by a killer GUI builder called [Pygubu](https://github.com/alejandroautalan/pygubu), and the file parser makes light usage of [Pydantic](https://github.com/samuelcolvin/pydantic) dataclasses for typecasting.

Finally the rendered geometry uses [Numpy](https://pypi.org/project/numpy/) for a few simple vector operations.

Installation of the dependencies is easy and explained in the installation section below. 

This project would not have been possible if it wasn't for these excellent technologies, so&ndash;once you're done checking out this project&ndash;we suggest you check out the giants on whose shoulders it stands. 

# Installation

Although we expect it to happen soon, HyperKyube is not yet registered in the Python Package Index (PIP), or distributed in binary form as a ".EXE" file. In the meantime installation will require cloning the repository, and pip installing the requirements.

To clone the repository you'll need Git:

1) Open up a git terminal like Git Bash and navigate to the directory you'd like to use for HyperKyube.
2) Run the following command to clone the repo to this folder:

```bash
git clone https://github.com/danielgesua/HyperKyube.git
```

3) After cloning is done&ndash;assuming they haven't already been installed&ndash;you'll also need to install the dependencies. The easiest way to do this is with the Python Package Index (PIP). Run the following command:

```bash
pip install -r requirements.txt
```
  **NOTE:** For the more reliable results you may *first* wanna upgrade your pip installation. This can easily be done by using the following command:

```bash
pip install --upgrade pip
```

# Getting Started: Making an LSTM Box File Using Tesseract v. 5.1.0.

To begin using the application you will need a box file to edit.

To make the LSTM box file you will need to install the CLI for [Tesseract version 5.1.0](https://github.com/tesseract-ocr/tesseract). 

To test wether tesseract is properly installed simply open up the platform shell and type:

```bash
tesseract --version
```

The version information should be printed.

With tesseract installed, simply navigate to the folder where your .tiff is stored and replace the word "image_name" with the actual name of your image in the command below:

```bash
tesseract image_name.tiff image_name lstmbox
```

**NOTE:** The name is repeated on purpose (it is **not** a typo). Tesseract's first argument is the name of the image to OCR and the second argument is the *basename* (ie the name minus the extension) of the *output* file. For tesseract's LSTM training to work the .box file basename *must* match the .tiff basename. This is also true for HyperKyube.

# Getting Started: HyperKyube Instructions

## Opening the HyperKyube Gui.

Once it has been installed as described in the installation instructions the application can be started by using python to run the main script:

1) Open up your operating systems shell.
2) Navigate to the src folder of the project.
3) Then depending on your platform...
   * In windows (assuming python is installed). 
        ```bash
        python -m main.py
        ```

   * In UNIX based systems (Like MacOS and Linux):
        ```bash
        python3 -m main.py
        ```

    **NOTE:** While we have no reason to expect any incompatibilities, HyperKyube has not yet been tested for MacOS or other Apple OS's. Please let us know if you experience any issues.

This should open the gui window. Remember: To get started editing box files you'll need a test image in .tiff format, and an LSTM box file created as described above.

## Editing the LSTM Box files.

HyperKyube is very simple and intuitive, but here's the controls in a nutshell.

### Opening Files:
To open the box file for editing simply file->open from the main menu or press Ctrl + O, then select the file. 

The image should appear with boxes arround each item of identified text. 

### Viewing OCR-recognized Text:
To read Tesseracts OCR interpretation of each box simply hover over it with the cursor. A tooltip should appear with the recognized text.

### Editing OCR-recognized Text:
To edit the text simply doubleclick the box and enter the corrections into the dialog.

### Adding Missing Boxes:
If any text is "unboxed" a new box can be created by simply clicking and draging the mouse over it diagonally to draw it from one corner to the opposite one. Once the mouse button is released, HyperKyube will prompt you to type the text corresponding to that box.

### Deleting Extra Boxes:
Sometimes Tesseract will box over an image that does not contain text. To delete extra boxes such as these, simply select them with left click and press the delete key.

### Adjusting Dimensions:
To adjust the dimensions of an existing box just left-click it to select it then drag-and-drop the dragbox for the corresponding side you wish to adjust.

### Saving Your Work:
To save the changes you can do so from the main menu using file->save or press Ctrl + S. 

# Supporting the Project

If you like what we do please consider donating or contributing your feedback to the project.

Your support is greatly appreciated.


