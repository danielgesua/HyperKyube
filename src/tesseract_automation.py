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
Responsible for automating the various functions of tesseract-ocr from within the GUI.
'''

from pytesseract.pytesseract import run_tesseract
from pathlib import Path

def make_lstmbox_file(file_path: str):
    ''' Run tesseract's LSTM box routine on the desired tiff image. '''
    path = Path(file_path)
    output_basename = path.with_suffix('')
    run_tesseract(str(path),str(output_basename),'.box','eng','lstmbox')
