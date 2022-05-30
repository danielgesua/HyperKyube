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
This module contains all objects related to geometric entities rendered on the main canvas.
'''


from __future__ import annotations

from typing import List
from numpy import float64, dot

from parsing import Displacements, WordBoxCore
from global_scope import NoActiveWordBox, real_global_scope as the
from dialogs import prompt_for_wordbox_text, display_invalid_value_error
from base_geometry import Edges, Edge, RenderedBox

    
class DragBox(RenderedBox):
    ''' 
    Object that represents a draggable box that's visible on the edges of the active wordbox,
    and can be dragged to modify their position. 
    '''

    @staticmethod
    def activate(point: List[int,int]) -> DragBox|None:
        ''' Activate the dragbox at point and return Truthy if succesful, or Falsey otherywise. ''' 
        the.active_dragbox = next(DragBox.containing(point),None)
        return the.active_dragbox

    @staticmethod
    def containing(point: List[int,int]) -> filter: 
        ''' Return all dragboxes from active wordbox containing the point. '''
        return filter(lambda db: db.contains(point),the.active_wordbox.dragboxes)

    @property
    def displacements(self) -> Displacements:
        return Displacements(
            left = dot(self.center.position,[1,0]) - self.size,
            top = dot(self.center.position,[0,1]) + self.size,
            right = dot(self.center.position,[1,0]) + self.size,
            bottom = dot(self.center.position,[0,1]) - self.size
        )

    @property
    def color(self): return 'red'

    def adjust(self,new_location: List[int,int]) -> None: 
        ''' Adjust the position to a new location. '''
        self.center.position = new_location

    def __init__(self, edge: Edge, size: int = 4) -> None:
        ''' Create the dragbox from the edge's center and add self to the edge. '''
        self.center = edge.center
        self.size = size

class RenderedWordBox(RenderedBox):
    ''' The screen representation of a word box.'''

    @property
    def color(self): return 'red' if self == the.active_wordbox.rendered else 'black'

    @property
    def displacements(self):
        ''' Return the displacements of the edges in the rendered wordbox as a Displacements object. '''
        return Displacements(**{edge.name:edge.displacement for edge in self.edges})

    @property
    def center(self) -> float64:
        ''' Return the center of the box as a numpy array. '''
        x = sum([edge.displacement for edge in self.edges.horizontal])/2
        y = sum([edge.displacement for edge in self.edges.vertical])/2
        return float64([x,y])

    def __init__(self,wordbox: WordBox):
        self.edges = Edges(wordbox)


class WordBox():
    ''' A box bounding a word. '''

    @classmethod
    def Empty(cls: WordBox) -> WordBox: return cls(WordBoxCore.Empty())

    @property
    def dragboxes(self): 
        ''' Return the dragboxes '''
        return (edge.dragbox for edge in self.rendered.edges)

    def create_dragboxes(self):
        ''' Create the dragbox for each edge and register it. '''
        for edge in self.rendered.edges: edge.dragbox = DragBox(edge)

    def launch_text_editor_dialog(self):
        ''' 
        Output a persistent dialogue to let user change the text of this wordbox. 
        Prevent user from canceling it or providing an empty string. 
        '''
        while not (value := prompt_for_wordbox_text(self)): 
            display_invalid_value_error()
        self.core.text = value

    def __init__(self, core: WordBoxCore):
        self.core = core
        self.rendered = RenderedWordBox(wordbox=self)
        self.create_dragboxes()

class NewWordBox(RenderedWordBox):
    ''' Transient helper class for wordbox creation using rectangular drag selection. '''

    @property
    def color(self): return 'blue'

    def _update_displacements(self):
        ''' Update the displacements based on the corners. '''
        x_values,y_values = tuple(zip(*self.corners))
        displacements = {
            'left': min(x_values),
            'right': max(x_values),
            'top': min(y_values),
            'bottom':max(y_values)
        }
        for edge in self.edges: edge.displacement = displacements[edge.name]

    def adjust(self,new_location: List[int,int]):
        ''' Adjust the second corner of the box to the new location.'''
        self.corners[1] = new_location
        self._update_displacements()

    def _make_wordbox(self):
        ''' Complete creation of the wordbox. '''
        wordbox = WordBox(self.wordbox.core)
        the.boxes.as_list.append(wordbox)
        wordbox.launch_text_editor_dialog()

    def create(self):
        ''' If the box has two corners then finish creation. In the end self destruct. '''
        if self.corners[0] != self.corners[1]: self._make_wordbox() 
        the.new_wordbox = None

    def __init__(self, first_corner: List[int,int]):
        self.corners = [first_corner,first_corner]
        self.wordbox = WordBox.Empty()
        self.wordbox.rendered = self
        super().__init__(self.wordbox)

class WordBoxes():
    ''' Collection of all existing word boxes. '''

    @property
    def file_representation(self) -> str:
        ''' Return the string containing the box file representation of the collection. '''
        words = (box.core.file_representation for box in self)
        return ''.join(words)

    def delete(self,wordbox: WordBox): 
        ''' Remove the wordbox from the list and reset the active wordbox. '''
        self.as_list.remove(wordbox)
        the.active_wordbox = NoActiveWordBox()

    def activate(self,point: List[int,int]) -> WordBox|NoActiveWordBox: 
        ''' Activate the wordbox at the selected location and return Truthy if succesful or Falsey otherwise.'''
        the.active_wordbox = self.select(point)
        return the.active_wordbox

    def select(self,point: List[int,int]) -> WordBox|NoActiveWordBox: 
        ''' Return the first wordbox located at the selected point, or an empty wordbox if there isn't one. '''
        return next(self.containing(point),NoActiveWordBox())

    def containing(self, point: List[int,int]): 
        ''' Return a filter of all boxes located at the selected point. '''
        return filter(lambda box: box.rendered.contains(point), self)
        
    def __init__(self, cores: List[WordBoxCore]): self.as_list = [WordBox(core) for core in cores]

    def __iter__(self): return iter(self.as_list)

