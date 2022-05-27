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


from typing import TYPE_CHECKING, Union
from PIL import Image

if TYPE_CHECKING: from geometry import NewWordBox, WordBox, WordBoxes, DragBox

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
        self.boxes: WordBoxes = None
        self.active_wordbox: Union[WordBox,NoActiveWordBox] = NoActiveWordBox()
        self.new_wordbox: NewWordBox = None
        self.active_dragbox: DragBox = None
        self.active_file_path: str = ''

real_global_scope = RealGlobalScope()