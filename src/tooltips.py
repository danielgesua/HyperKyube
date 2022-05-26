from __future__ import annotations

from idlelib.tooltip import Hovertip
from global_scope import real_global_scope as the
from geometry import WordBox, NoActiveWordBox

class WordBoxToolTip(Hovertip):
    ''' A tooltip that appears at the bottom '''

    @property
    def message(self): 
        ''' Return the tool tip text. '''
        return self.text

    @message.setter
    def message(self, value: str):
        ''' Re-set the message on the tooltip if it is new. '''
        if self.text != value:
            self.hidetip()
            self.text = value
            if value != '': self.showtip()
    
    def __init__(self, anchor_widget, text, hover_delay=1000):
        self.x,self.y = 0,0
        super().__init__(anchor_widget, text, hover_delay)

    def calculate_position(self, wordbox: WordBox):
        ''' Set the position of the tooltip to just above the box. '''
        edges = filter(lambda edge: edge.name in ('left','top'),wordbox.rendered.edges) 
        [self.x,self.y] = [edge.displacement for edge in edges]
        self.y = the.buffered_image.height - self.y - 25
    
    def get_position(self): 
        ''' Give the HoverTip object the location it needs. This method has to be overloaded. '''
        return self.x,self.y

    def display(self,wordbox: WordBox):
        ''' Display the tooltip for the wordbox. '''
        if isinstance(wordbox,NoActiveWordBox):
            self.hidetip()
            self.text = ''
        else:
            self.calculate_position(wordbox)
            self.message = wordbox.core.text            
