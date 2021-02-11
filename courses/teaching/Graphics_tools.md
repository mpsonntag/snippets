Gimp
====
- there is a move tool

### Change transparency of a color
- select color tool
- right click image - colors - colors to alpha -
- find more information [here](http://graphicdesign.stackexchange.com/questions/36520/how-to-make-a-color-transparent-in-gimp).

### Round corners
- works only with jpg
- Filters - Decor - Round edges

### Crop images
- find out how [here](https://docs.gimp.org/en/gimp-tutorial-quickie-crop.html).

### Replace color in whole image
- find out how [here](http://andr.esmejia.com/posts/1-how-to-replace-all-pixels-of-one-color-with-another-color-using-the-gimp)

    - Select > By color
    - Select replacement color
    - Make sure "replace all" option is selected


Inkscape
========

### Default paper sizes
Find default paper sizes [here](http://www.papersizes.org/a-paper-sizes.htm).


### Set default measurement units
Default measurement units can be set at

    File -> Document properties -> Page tab


### Changing shape dimensions
Change shape dimensions ... up top, below menu bar:

    X, Y: coordinates within the canvas
    W, H: width, height of the actual shape


### Using guide lines (lines to guide drawing...)

- [guide tutorial](https://inkscapetutorials.org/2014/04/25/working-with-guides-in-inkscape/)
- click on the side ruler and drag towards the canvas - automatically creates a guide.
- double clicking a guide line enables fine positioning.


### Creating text boxes
- When creating text boxes, follow [this description](http://www.inkscapeforum.com/viewtopic.php?t=999); 
otherwise, resizing the box w/o scaling the contained text will not be possible:
 
- Select the Text Box Symbol
- Create arbitrary textbox
- Add text
- When resizing this textbox w/o changing the font size, select textbox and press F8
- In the right lower hand corner a handle will appear.
- Use this handle to resize the textbox w/o scaling the text.
- Resize the Textbox only in this mode.
- Exit mode and position the resized box using the normal top bar positioning.


### Text formatting
- Enter text box e.g. by double clicking.
- Formatting options e.g. superscript will become available in the top bar. 


### Object order
- send object one step to the back ... page down
- send object one step to the front ... page up


### Scaling images
- scale image while keeping aspect ratio
[here](http://graphicdesign.stackexchange.com/questions/26892/inkscape-scale-with-keep-aspect-ratio-as-default)


### Shortcuts
- Enable/Disable snap ... Shift + 5
- Enter Text properties ... Ctrl + Shift + t
- Enter Object properties ... Ctrl + Shift + o
- Group ... Ctrl + g
- Ungroup ... Ctrl + shift + g
- Edit selected text object : F8
- Send to back: end or page down
- Send to front: pos 1 or page up
- Enter unicode characters in textboxes: ctrl+u and unicode code e.g. Ctrl + u, 2022 for bullet point.

## Inkscape and accents

When you have the text cursor, press ctrl+U then type in a code from the linked page and press enter. 
Not all fonts have all characters.

http://jrgraphix.net/research/unicode_blocks.php?block=1

## Disable snap

A keyboard shortcut to disable the snap to feature, is the percent sign (% or SHIFT + 5 on most keyboards)
Or there is a button on the top right.
https://slackalaxy.com/2017/02/11/disable-snapping-in-inkscape/


## Add round corners to rectangular shapes
- draw rectangle.
- select rectangle, make sure rectangular tool is also still selected.
- a new toolbar appears up top - change Rx and Ry to the same values to define the radius of the corners.
- done.

## Add lines and arrows
    Draw a line (Shift+F6)
    Open Fill and Stroke dialog (Shift+Ctrl+F)
    Select Stroke Style tab
    Choose an arrow for the Start Marker or End Marker

## Rotate objects

    Select object
    -> object -> transform -> Rotate

How to adjust an arrowhead to a changed arrow body:

    copy an arrowhead from a straight (0°) arrow
    move it next to the arrow body its supposed to be affixed to
    rotate it until the base of the arrowhead and the base of the arrow body
    do not show a gap any longer.


## Gotchas

When trying to change spacing between lines in text boxes, make sure the textbox but not the text is
selected, otherwise the text spacing might not be changed.


Draw.io
=======

https://support.draw.io/

Use amazon web service / cisco charts for architecture schematics


## Bugfixing:

When the message "not supported by view" appears in textboxes, make sure, "formatted text" is unticked under text

https://desk.draw.io/support/solutions/articles/16000042487-why-does-the-text-of-svg-export-sometimes-not-display-correctly-in-ie-and-some-svg-editors-
 

