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
All code related to the function of the mirror canvas resides in this module. 
The mirror canvas is the canvas on the right which mirrors the main canvas
by showing to-scale OCR text of all the wordboxes.
'''

from __future__ import annotations
import tkinter
from typing import Any, Callable
from functools import wraps
from PIL import Image, ImageOps, ImageTk,ImageFont
from PIL.ImageDraw import ImageDraw, Draw

from global_scope import real_global_scope as the
from gui_builder import builder
from rendered_geometry import WordBox, RenderedBox
from main_canvas import CanvasManager

def do_in_box_file_coordinates(method: Callable):
    ''' 
    Decorator: Flip the image upside down so it is in box file coordinates, 
    perform the image operation, and flip it once more so it is in proper orientation. 
    '''

    @wraps(method)
    def wrapper(self:Any,*args,**kwargs):
        the.mirror_image = ImageOps.flip(the.mirror_image)
        method(self,*args,**kwargs)
        the.mirror_image = ImageOps.flip(the.mirror_image)

    return wrapper

FONT = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf',100)
_TRANSPARENT_COLOR = (255,255,255,0,)
_BLACK_OPAQUE = (0,0,0,255,)

class MirrorCanvas():
    ''' Object that mirrors the main canvas by displaying all the OCR'd text to scale. '''

    def __init__(self): 
        the.mirror_image = Image.new('RGB',the.buffered_image.size,'white')
        self.canvas: tkinter.Canvas = builder.get_object('mirror_canvas')

    def draw_rectangle(self, box: RenderedBox):
        ''' Draw a rectangle on the image with the given dimensions and return the image. '''
        rect = tuple(box.displacements)
        Draw(the.mirror_image).rectangle(xy=rect,outline=box.color)

    def draw_word(self,box: WordBox):
        ''' Draw a wordbox on the mirror image. '''
        initial_size = FONT.getsize(box.core.text)
        word_canvas = Image.new('RGBA',initial_size,_TRANSPARENT_COLOR)
        position = (initial_size[0]//2,initial_size[1]//2,)
        ImageDraw(word_canvas).text(position,box.core.text,fill=_BLACK_OPAQUE,font=FONT,anchor='mm')
        word = word_canvas.resize(box.rendered.size).transpose(Image.FLIP_TOP_BOTTOM)
        x = box.rendered.displacements.left
        y = box.rendered.displacements.top - word.size[1]
        the.mirror_image.paste(word,(x,y,),word)
        self.draw_rectangle(box.rendered) 

    @do_in_box_file_coordinates
    def draw_words(self):
        ''' Draw all the words from the boxes. '''
        for box in the.boxes: self.draw_word(box)


    def display_image(self):
        ''' Display the mirror image on the mirror canvas. '''
        the.mirror_image = Image.new('RGB',the.buffered_image.size,'white')
        self.draw_words()
        self.displayed_image = ImageTk.PhotoImage(the.mirror_image)
        self.canvas.create_image(0,0,anchor=tkinter.NW,image=self.displayed_image)
        