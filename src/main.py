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
Main entry point of the application. Contains the root object and handles various 
user-triggered GUI events like clicks, keyboard strokes and prompts.
'''

from __future__ import annotations


import pathlib
import tkinter

from global_scope import real_global_scope as the
from gui_builder import builder
from rendered_geometry import DragBox, NewWordBox, WordBoxes
from parsing import parse
from tooltips import WordBoxToolTip
from about import AboutDialog
from dialogs import prompt_for_boxfile_to_open, prompt_for_image_to_process
from main_canvas import CanvasManager, with_refresh
from mirror_canvas import MirrorCanvas
from tesseract_automation import make_lstmbox_file


PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "gui.ui"


class GuiApp:

    @property
    def creating_wordbox(self) -> bool: return isinstance(the.new_wordbox, NewWordBox)

    @property
    def adjusting_dragbox(self) -> bool: return the.active_dragbox is not None

    def __init__(self, master=None): 
        self.tk = tkinter
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow: tkinter.Toplevel = builder.get_object('outer_window', master)
        self.mainwindow.geometry(f'474x600')
        self.canvas_manager = CanvasManager()
        self.mirror_canvas = MirrorCanvas()
        self.about_dialogue = AboutDialog()
        self.tooltip = WordBoxToolTip(self.canvas_manager.canvas,'',0)
        builder.connect_callbacks(self)
    
    def run(self):
        self.mainwindow.mainloop()

    @with_refresh
    def load_boxfile(self, file_name: str):
        ''' Load a box-file/image combination on the main canvas.'''

        def find_corresponding_image(file_path: pathlib.Path):
            ''' Find the first image that corresponds to this box file and return its path.'''
            directory = file_path.parent
            glob_pattern = f'{file_path.stem}.tif*'
            match = map(str,directory.glob(glob_pattern))
            return next(match)   

        file_path = pathlib.Path(file_name)
        the.active_file_path = str(file_path.with_suffix('.box'))
        img_file_path = find_corresponding_image(file_path)
        self.canvas_manager.load_original_image(img_file_path)
        the.boxes = WordBoxes(parse(the.active_file_path))

    def obtain_and_load_boxfile(self, event: tkinter.Event = None):
        ''' Load the boxfile provided by the user.'''
        if (file_name := prompt_for_boxfile_to_open()): self.load_boxfile(file_name)

    def make_boxfile_from_image(self, event: tkinter.Event = None):
        '''
        Request an image from the user. If the user selects one then run Tesseract on it
        to make a boxfile and load it.
        '''
        if (file_name := prompt_for_image_to_process()): 
            make_lstmbox_file(file_name)
            self.load_boxfile(file_name)
            

    def save_boxfile(self, event: tkinter.Event = None):
        ''' Save the corrected wordbox data to the active file. '''
        with open(file=the.active_file_path,mode='w') as box_file:
            box_file.write(the.boxes.file_representation)

    @with_refresh
    def activate_selection(self, event: tkinter.Event):
        ''' 
        Select an item based on the clicked location:

         * If a dragbox is clicked then select it.
         * Otherwise if a wordbox is clicked select it.
         * Otherwise create a NewWordBox with the clicked point as one corner.

        Happens for single click.
        '''
        clicked_point = [event.x,event.y]
        clickable_objects = (DragBox,the.boxes)
        selected = any((obj.activate(clicked_point) for obj in clickable_objects))
        if not selected: the.new_wordbox = NewWordBox(first_corner=clicked_point)

    @with_refresh
    def drag_selection(self, event: tkinter.Event):
        ''' 
        Perform the drag and drop operation:
        
         * If dragging a dragbox then correct the edge by adjusting its center position accordingly.
         * If creating a new wordbox then continuously adjust its dimensions so it displays properly.

        '''
        cursor_location = [event.x,event.y]
        if self.adjusting_dragbox: the.active_dragbox.adjust(cursor_location)
        elif self.creating_wordbox: the.new_wordbox.adjust(cursor_location)
    
    @with_refresh
    def finish_selected_action(self, event: tkinter.Event):
        ''' 
        Complete the current action: 

         * If drag and dropping a dragbox, then deactivate the dragbox so that subsequent motion does 
           not affect the placement.
         * If creating a new box, then finalize its creation and delete the NewWordBox item.

        Usually happens during mouse button release
        '''
        the.active_dragbox = None
        if self.creating_wordbox: the.new_wordbox.create()

    @with_refresh
    def delete_wordbox(self, event: tkinter.Event = None):
        ''' 
        Delete the current active wordbox. Triggered by pressing delete. 
        '''
        if the.active_wordbox: the.boxes.delete(the.active_wordbox)

    @with_refresh
    def edit_text(self,event: tkinter.Event):
        ''' 
        Edit text of the wordbox by launching a text editor dialogue. Usually during doubleclick.
        '''
        if the.boxes.activate([event.x,event.y]): the.active_wordbox.launch_text_editor_dialog()

    def copy_text(self, event: tkinter.Event = None):
        ''' Copy the text of the selected boxfile. '''
        if the.active_wordbox:
            self.mainwindow.clipboard_clear()
            self.mainwindow.clipboard_append(the.active_wordbox.core.text)

    def activate_required_tooltips(self,event: tkinter.Event):
        '''
        Activate tooltip of wordbox under the mouse pointer.
        '''
        wordbox = the.boxes.select([event.x,event.y]) 
        self.tooltip.display(wordbox)

    @with_refresh
    def adjust_window(self,event: tkinter.Event): 
        ''' Adjust the window components to fit the window. '''
        return None

    def display_about_dialogue(self, event: tkinter.Event = None):
        ''' Show the about dialogue to display information about the software. '''
        self.about_dialogue.show()

    def exit(self, event: tkinter.Event = None):
        ''' Close the program. '''
        self.mainwindow.destroy()
        
            

if __name__ == '__main__':
    app = GuiApp()
    app.run()