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
This module serves as a central location to import the pygubu builder into all subsequent classes that require it.
'''

import logging
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

builder = pygubu.Builder()
__builder_logger = logging.getLogger('pygubu.builder')
__builder_logger.setLevel(logging.ERROR)