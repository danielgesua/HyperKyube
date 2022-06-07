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
This module contains code to make OS specific adjustments for compatabitity reasons
'''

from PIL import ImageFont
import platform

if 'win' in platform.system().lower():
    font_name = 'lucon'
elif 'linux' in platform.system().lower():
    font_name = 'Pillow/Tests/fonts/FreeMono.ttf'


try:
    FONT = ImageFont.truetype(font_name,100)
except OSError:
    FONT = ImageFont.load_default()

