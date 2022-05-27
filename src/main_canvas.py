#
#    HyperKyube: OCR Gui MultiTool.
#
#    Copyright 2022 Daniel Gesua
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#   

'''
Contains the image manipulations and canvas redrawing code needed to 
render the main canvas widget.
'''


from __future__ import annotations


import tkinter

from typing import Any, Callable, TYPE_CHECKING
from PIL import ImageTk,Image, ImageDraw,ImageOps
from functools import wraps

from gui_builder import builder
from global_scope import real_global_scope as the
from parsing import parse
from geometry import NewWordBox, RenderedBox, WordBoxes

PLACEHOLDER_IMAGE = 'assets/HyperKyube.tiff'
PLACEHOLDER_BOXFILE = 'assets/HyperKyube.box'

if TYPE_CHECKING: from main import GuiApp

def convert_to_rgb(bw_img: Image.Image) -> Image.Image:
    ''' Convert a black and white image into a color image. '''
    color_image = Image.new('RGB',bw_img.size)
    color_image.paste(bw_img)
    return color_image

def do_in_box_file_coordinates(method: Callable):
    ''' 
    Decorator: Flip the image upside down so it is in box file coordinates, 
    perform the image operation, and flip it once more so it is in proper orientation. 
    '''

    @wraps(method)
    def wrapper(self:Any,*args,**kwargs):
        the.buffered_image = ImageOps.flip(the.buffered_image)
        method(self,*args,**kwargs)
        the.buffered_image = ImageOps.flip(the.buffered_image)

    return wrapper


def with_refresh(method: Callable):
    ''' 
    Decorator: Refresh the gui by repainting the canvas and hiding tooltips 
    after execution of the decorated method.
    '''
    @wraps(method)
    def wrapper(self: GuiApp,*args,**kwargs):
        method(self,*args,**kwargs)
        self.canvas_manager.display_image()
        self.tooltip.hidetip()

    return wrapper


class CanvasManager():
    ''' Class that manages displaying images on the main canvas. '''

    def __init__(self):
        self.canvas: tkinter.Canvas = builder.get_object('image_display')
        self.load_original_image(PLACEHOLDER_IMAGE)
        the.boxes = WordBoxes(parse(PLACEHOLDER_BOXFILE))
        the.active_file_path = PLACEHOLDER_BOXFILE
        self.display_image()

    def load_original_image(self,img_path:str = None):
        ''' Load the original image from a file.'''
        self.original_image = convert_to_rgb(Image.open(img_path))

    def scale_image(self,img: Image.Image):
        ''' Return a copy of the image, scaled to the canvas size. '''
        the.scale = max(self.canvas.winfo_reqheight(),self.canvas.winfo_height())/img.height
        new_size = tuple((int(dimension*the.scale) for dimension in img.size))
        the.buffered_image = img.resize(new_size)

    def draw_rectangle(self, box: RenderedBox):
        ''' Draw a rectangle on the image with the given dimensions and return the image. '''
        rect = tuple(box.displacements)
        ImageDraw.Draw(the.buffered_image).rectangle(xy=rect,outline=box.color)

    @do_in_box_file_coordinates
    def draw_rectangles(self):
        ''' Draw all rectangles on the image from the boxes. '''
        for box in the.boxes: self.draw_rectangle(box.rendered)
        for dragbox in the.active_wordbox.dragboxes: self.draw_rectangle(dragbox)
        if isinstance(the.new_wordbox,NewWordBox): self.draw_rectangle(the.new_wordbox)

    def display_image(self):
        ''' Display an Image object on the canvas.'''
        self.scale_image(self.original_image)
        self.draw_rectangles()
        self.displayed_image = ImageTk.PhotoImage(the.buffered_image)
        self.canvas.create_image(0,0,anchor=tkinter.NW,image=self.displayed_image)
