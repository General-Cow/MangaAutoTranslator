# TODO

## Current Working Goal
Just implement JSON position as the main method. Keeping clips for case where file format is not good for manual slicer.
Cleans up the code and makes saving stuff so much easier
Start implementing for bulk collection rather than one page at a time

## Home page
- [] Actually make it a real home page.

## Across Multiple
- [x] rework how I save and store pages and clips to better fit a good work flow.
- [] cross page session states. For example get the positions within manual slicer, go over to autotranslator, and read in manga reader without losing stuff
- [] multipage workflow

## Autotranslator
- [] Incorporate session states so moving to a different page doesnt erase translation
    - probably a multipage thing actually
- [] Custom input models/translation tools.
    - 'not listed' option that runs an ollama pull? for input model
- [] Keep playing with models.
    - [] Try Plamo using vllm setup. pfnet/plamo-2-translate
    - [] test non ollama methods generally, like vllm or hugging face methods
- [] Incorporate evaluation tools (much) later.
- [] Right now I open a new API call for every image. It might be smart to try reworking so I'm not reinputting the instructions for every image as every token costs money. Need to be cost effective with API calls.
- [] Add other API options and implement other proprietary models. Claude perhaps?
    - likely low priority just because API costs mean this just isn't really economical.
- [] add boxes to show position of text boxes when using json
- [] Very long term: Implement multiple agents voting on translations and/or agentic methods

### slicer_tools
- [] Warn that full page is going to suck so include a warning somewhere
- [] Implement text region detection.
    - need to look into different libraries, tools, and papers on this

## Manual Slicer
- [x] Be able to choose and clip collections of pages so I don't have to upload one at a time.
- [] need to fix png display issue in matplotlib window.
    - other pngs have seemed to work, may just be an issue specific to that image in particular.
- [x] save JSONs in same place as pg clips for use in replacing text bubbles
    - New file uploader makes this not really needed
- Consider reworking and removing clip slices and utilizing JSON only.
    - Considered done. clips < jsons
- [x] fix clip saving location path. Right now just saving in data.
- [] implement positions json to default to one json rather than a json per page

## Reader
- [] Do to _render_chapter something similar to what I did with _render_translations in the autotranslator
- [] Include insertion of translations in text bubbles
    - can use position JSONs from Manual Slicer to accomplish
    - Include numbers
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
Fix file structure to a consistent format and display here