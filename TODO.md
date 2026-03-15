# TODO

## Current Working Goal
Just implement JSON position as the main method. Keeping clips for case where file format is not good for manual slicer.
Cleans up the code and makes saving stuff so much easier
Start implementing for bulk collection rather than one page at a time

## Home page
- [] Actually make it a real home page.

## Across Multiple
- [] rework how I save and store pages and clips to better fit a good work flow.
- [] cross page session states. For example get the positions within manual slicer, go over to autotranslator, and read in manga reader without losing stuff
- [] multipage workflow

## Autotranslator
- [] Incorporate session states so moving to a different page doesnt erase translation
    - probably a multipage thing actually
- [x] Clean up page by moving _compute_translations and _render_translations to a different script
- [] Custom input models/translation tools.
    - 'not listed' option that runs an ollama pull? for input model
- [] Keep playing with models.
- [] Incorporate evaluation tools (much) later.
- [] Consider adding OCR model selection later.
    - Will need to rework src/ocr_extractor.py then to include multiple options.
- [] Right now I open a new API call for every image. It might be smart to try reworking so I'm not reinputting the instructions for every image as every token costs money. Need to be cost effective with API calls.
- [x] Consider adding proprietary models with API calls. (i.e. OpenAI). DO NOT ACCIDENTALLY PUSH YOUR API KEY. Make it so it's manually loaded (and hidden)
    - [X] Implement OpenAI
        - The one page of random_manga1 using GPT 5 with high effort cost $0.10, used 436 input tokens, and about 10K output tokens (fucking somehow)
            - input cost was trivial, like a tenth of a cent. Output was pretty much the whole cost. 
        - [x] need to try different reasoning options
            - didnt really seem to make a difference literally at all cost wise.
                - What the hell does reasoning even do? I may have misunderstood what it does.
        - [x] HIGH PRI: Fix _render to render api translations.
            - [x] Test fix
- [] Add other API options and implement other proprietary models. Claude perhaps?
    - likely low priority just because API costs mean this just isn't really economical.
- [x] Clear button
- [] add boxes to show position of text boxes when using json
- [] Very long term: Implement multiple agents voting on translations and/or agentic methods

### slicer_tools
- [x] Implement full page?
    - [] its going to suck so include a warning somewhere
- [] Implement text region detection.
    - need to look into different libraries, tools, and papers on this

## Manual Slicer
- [] Be able to choose and clip collections of pages so I don't have to upload one at a time.
    - That said is this important?Depends on work flow I suppose.
- [] need to fix png display issue in matplotlib window.
    - other pngs have seemed to work, may just be an issue specific to that image in particular.
- [] save JSONs in same place as pg clips for use in replacing text bubbles
    - This is more a question of how I want to handle work flow.
- Consider reworking and removing clip slices and utilizing JSON only.
    - Seems to be a faster process. Perhaps try benchmarking?
    - IMPORTANT NOTE: This would simplify file structure.
- [] fix clip saving location path. Right now just saving in data.

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