# TODO
## Home page
- [] Actually make it a real home page.

## Across Multiple
- [] rework how I save and store pages and clips to better fit a good work flow.

## Autotranslator
- [] Incorporate session states so moving to a different page doesnt erase translation
- [] Integrate the use of the json files to get the clips. Could be used in lieu of image slices.
- [x] Create json downloader of translated clips.
- [] Upload pretranslated clips? Or is viewer for that? Begs question of a rework.
- [] Custom input models/translation tools.
- [] Keep playing with models. Not very good so far.
- [] Incorporate evaluation tools later.
- [] Consider adding OCR model selection later. Will need to rework src/ocr_extractor.py then to include multiple options.
- [] Consider adding proprietary models with API calls. (i.e. OpenAI). DO NOT ACCIDENTALLY PUSH YOUR API KEY. Make it so it's manually loaded (and hidden)
- [] Clear button

### slicer_tools
- [] Implement manual slicing. Consider dropping since redundant with manual slicer page.
- [] Implement text region detection.

## Manual Slicer
- [x] add bulk download of boxes as clips. May need to create folder in accordance with autotranslator needs to save them in for reuseability as presliced clips.
- [] Be able to choose and clip collections of pages so I don't have to upload one at a time. That said is this important?
- [] need to fix png display issue in matplotlib window.
- [] save JSONs in same place as pg clips for use in replacing text bubbles
- [] HIGH PRI: fix clip saving location path. Right now just saving in data.

## Reader
- [x] create a reading page that loads saved translations to read full chapters/collections.
- [] Include insertion of translations in text bubbles (can use JSONs from Manual Slicer to accomplish)
- [] Improve reading UI. Buttons? Markdown?

## Workflow concept
Select collection of docs
slice each page, saving jsons and clips
translate clips by page, save translations
reload location/translations
view on page

or
 
 Slicer
 Translator
 (Possible placer page for text)
 Viewer

## File Structure
keep building out and place jsons
Data/
|-- Manga/
  |-- Chapter/
      |-- pg1
      |-- pg2
      |-- etc
      |--clips/
         |-- pg1
         |   |--clip1
         |   |--clip2
         |   |--clipetc
         |
         |-- pg2
             |etc 
         etc