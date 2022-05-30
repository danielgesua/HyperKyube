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
Module primarily responsible for parsing box file data out of lstm box file format and
exposing it in a more convenient model for the creation of rendered geometry.
'''

from __future__ import annotations


import re
from types import SimpleNamespace
from typing import List
from pydantic.dataclasses import dataclass
from dataclasses import astuple


SPLITTING_PATTERN = r'''(?P<text>.)\s # String containing the letter on that row
    (?P<left>\d+)\s      # Left edge displacement value
    (?P<bottom>\d+)\s    # Bottom edge displacement value
    (?P<right>\d+)\s     # Right edge displacement value
    (?P<top>\d+)\s\d+\n  # Top edge displacement value'''

letter_splitter = re.compile(SPLITTING_PATTERN,flags=re.VERBOSE)


@dataclass
class Displacements():
    ''' Data class containing the displacement values from the origin for each edge in a box. '''
    left: int
    top: int
    right: int
    bottom: int

    @property
    def file_representation(self): return f'{self.left} {self.bottom} {self.right} {self.top} 0\n'

    def __iter__(self): return iter(astuple(self)) 


class WordBoxCore(SimpleNamespace):
    ''' A simple namespace contianing the core attributes of a box bounding a word. '''

    @classmethod
    def Empty(cls: WordBoxCore):
        ''' Return an empty core with default values for everything. '''
        default_displacements = {key: 0 for key in 'left,top,right,bottom'.split(',')}
        return cls(text="",**default_displacements)

    @property
    def file_representation(self) -> str:
        ''' Return a string containing the file representation of this box as it appears in a box file.'''
        letters = [letter for letter in self.text + '\t']
        displacements = self.displacements.file_representation
        rows = (f'{letter} {displacements}' for letter in letters)
        return ''.join(rows)

    def __init__(self, row_match:re.Match = None,**kwargs) -> None:
        ''' Create a core using either a regex match from file or explicitly passed parameters. '''
        kwargs = kwargs if row_match is None else row_match.groupdict()
        self.text: str = kwargs.pop('text') 
        self.displacements = Displacements(**kwargs)



def load_data(file: str) -> str:
    ''' Get the raw data from the file. '''
    with open(file,mode='r') as f: raw_data = f.read()
    return raw_data


def parse(file: str) -> List[WordBoxCore]:
    ''' Parse the data from the box file into word box objects consisting of simple namespaces. '''

    def _parse_character_boxes(raw_data: str) -> List[WordBoxCore]:
        ''' Convert the raw data string into namespaces of all character boxes.'''
        unparsed_rows = letter_splitter.finditer(raw_data)
        character_boxes = list(map(WordBoxCore,unparsed_rows))
        return character_boxes

    def _extract_words(character_boxes: List[WordBoxCore]) -> List[str]:
        ''' Extract a list of words out of the parsed character data. '''
        characters = [symbol.text for symbol in character_boxes]
        words = "".join(characters).split('\t')
        return words

    def _make_word_boxes(character_boxes: List[WordBoxCore], words: List[str]):
        ''' Make word boxes out of the character boxes. '''
        boxes = [box for box in character_boxes if box.text == '\t']
        for box,word in zip(boxes,words): box.text = word
        return boxes

    raw_data = load_data(file)
    character_boxes = _parse_character_boxes(raw_data)
    words = _extract_words(character_boxes)
    boxes = _make_word_boxes(character_boxes,words)
    return boxes