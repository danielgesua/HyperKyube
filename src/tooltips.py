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
Responsible for handling the creation, positioning and display of OCR text as a tooltip
that displays when a given wordbox gets hovered over with the mouse.
'''


from __future__ import annotations


from idlelib.tooltip import Hovertip
from global_scope import real_global_scope as the
from rendered_geometry import WordBox, NoActiveWordBox
from tkinter import Toplevel, TclError


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

    def showtip(self):
        ''' 
        display the tooltip.
        NOTE: This method overloads the original HoverTip method to fix an error that was raised when
        shrinking the window then quickly moving the mouse up to a wordbox. The only functional
        difference is that the code check for the existance of a tip window before lifting it.
        '''
        if self.tipwindow: return
        self.tipwindow = tw = Toplevel(self.anchor_widget)
        # show no border on the top level window
        tw.wm_overrideredirect(1)
        try:
            # This command is only needed and available on Tk >= 8.4.0 for OSX.
            # Without it, call tips intrude on the typing process by grabbing
            # the focus.
            tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass

        self.position_window()
        self.showcontents()
        self.tipwindow.update_idletasks()  # Needed on MacOS -- see #34275.
        if self.tipwindow: self.tipwindow.lift()  # work around bug in Tk 8.5.18+ (issue #24570)            
