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
I know someone will shoot me for this...

This module contains a namespace used to hold objects of a global scope, which must be
widely shared amongst various classes and modules.

It avoids parameter hell without causing signifficant namespace polution by implementing a new 
convention: Much like "self" is used to access attributes of class instances, the RealGlobalScope
instance "real_global_scope" aliased as "the" can be used to access singular global variables.

For example: 

- "the.scale" refers to the scale factor used to convert from the image and file coordinates
  to the coordinates of the (potentially larger or smaller) canvas.

- "the.buffered_image" refers to the image that is currently being processed to display on the
  canvas.

- "the.boxes" refers to all the wordboxes parsed from the current boxfile.

- "the.active_wordbox" refers to the current wordbox that has been selected by the user,
  or an instance of NoActiveWordBox otherwise.

- "the.new_wordbox" refers to a NewWordBox object reference if there is a wordbox currently
  being created, or None otherwise. 

- "the.active_dragbox" refers to the dragbox currently being dragged during dimension adjustments
  or None otherwise.

- "the.active_file_path" refers to a string containing the fully qualified path to the box
  file that's currently loaded.
'''

from typing import TYPE_CHECKING, Union
from PIL import Image

if TYPE_CHECKING: from rendered_geometry import NewWordBox, WordBox, WordBoxes, DragBox

class NoActiveWordBox():
    ''' Dummy object to represent no wordbox is selected. '''
    dragboxes = []
    rendered = None

    def __bool__(self): return False

class RealGlobalScope():
    ''' Wrapper class that acts as a namespace for all global objects and can be instantiated and imported everywhere. '''

    def __init__(self) -> None:
        self.scale: float = 1.0
        self.buffered_image: Image.Image = None
        self.mirror_image: Image.Image = None
        self.boxes: WordBoxes = None
        self.active_wordbox: Union[WordBox,NoActiveWordBox] = NoActiveWordBox()
        self.new_wordbox: NewWordBox = None
        self.active_dragbox: DragBox = None
        self.active_file_path: str = ''

real_global_scope = RealGlobalScope()