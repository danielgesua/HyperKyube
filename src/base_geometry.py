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
This module contains all helper objects that facilitate creation of rendered geometry.
'''

from __future__ import annotations

from typing import TYPE_CHECKING, List, Iterator
from numpy import float64,dot
from abc import ABC, abstractmethod

from global_scope import real_global_scope as the

if TYPE_CHECKING: 
    from rendered_geometry import WordBox,DragBox
    from parsing import Displacements

horizontal_edge_names = ['left','right']
vertical_edge_names = ['top','bottom']
edge_names = [*horizontal_edge_names,*vertical_edge_names]

class RenderedBox(ABC):
    ''' Interface for all boxes that can be displayed on the canvas. '''

    @property
    @abstractmethod
    def displacements(self) -> Displacements: pass

    @property
    @abstractmethod
    def color(self) -> str: pass

    def contains(self,point: List[int,int]) -> bool:
        ''' Return wether the point is within the bounds of this box. '''
        left = self.displacements.left
        top = the.buffered_image.height - self.displacements.top
        right = self.displacements.right
        bottom = the.buffered_image.height - self.displacements.bottom
        return (left <= point[0] <= right) and (top <= point[1] <= bottom)

class EdgeCenter():
    ''' Object that maintains the center position of a rendered edge. '''
    
    @property
    def position(self) -> float64:
        ''' Return the vector corresponding to the center coordinates of the edge. '''
        vector_1 = self.edge.axis * self.edge.displacement
        vector_2 = self.edge.perpendicular_axis * self.wordbox.rendered.center
        return vector_1 + vector_2

    @position.setter
    def position(self, value: List[int,int]):
        self.edge.displacement = dot(value,self.edge.axis)

    def __init__(self, edge: Edge) -> None:
        self.edge = edge
        self.wordbox = edge.wordbox

class Edge():
    ''' A single edge in a rendered wordbox. '''

    @property
    def displacement(self) -> int:
        ''' Get the rendered displacement value of the edge''' 
        return int(the.scale*getattr(self.core_displacements,self.name))

    @displacement.setter
    def displacement(self,value: int):
        ''' Set the core displacements of the edge based on a change in the rendered displacement.'''
        if self.name in vertical_edge_names: value = the.buffered_image.height - value
        new_value = int(value/the.scale)
        setattr(self.core_displacements,self.name,new_value)

    def __init__(self,wordbox: WordBox, name: str, axis: float64):
        self.core_displacements = wordbox.core.displacements
        self.axis = axis
        self.perpendicular_axis = float64([1,1]) - self.axis
        self.wordbox = wordbox
        self.center = EdgeCenter(self)
        self.dragbox: DragBox = None
        self.name = name

    def __repr__(self) -> str: return f'{self.displacement}'

class Edges():
    ''' Iterable collection of edges subdivided by subgroup that assists in edge creation. '''

    def __init__(self,wordbox: WordBox):
        self.left: Edge = None
        self.top: Edge = None
        self.right: Edge = None
        self.bottom: Edge = None
        horizontal = {name: Edge(wordbox,name,float64([1,0])) for name in horizontal_edge_names}
        vertical = {name: Edge(wordbox,name,float64([0,1])) for name in vertical_edge_names}
        self.horizontal = [edge for edge in horizontal.values()]
        self.vertical = [edge for edge in vertical.values()]
        self.as_list = [*self.horizontal,*self.vertical]
        self.__dict__ = {**self.__dict__,**horizontal,**vertical}

    def __iter__(self) -> Iterator[Edge]: return iter(self.as_list)