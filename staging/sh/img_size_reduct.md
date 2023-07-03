# 'convert' is part of the imagemagic suite
# cd to image directory
# will create a conv folder and convert all jpg images to 85% quality
mkdir conv; for IMG in $(ls *.jpg); do echo "$IMG"; convert $IMG -quality 85% conv/$IMG; done;

# move original images to its own folder; convert all images to 85% quality in root dir
FEND="*.jpg"; echo "-- convert jpg in $PWD to 85% quality"; mkdir -v original; mv -v $FEND original; for IMG in $(ls original/$FEND); do CURR=`basename $IMG`; echo "$IMG to $CURR"; convert $IMG -quality 85% $CURR; done;

# batch rename file extension in case of mixed file ending format
for f in *.JPG; do mv -v "$f" "${f//.JPG/.jpg}"; done;

# batch replace whitespace with underscore
# currently only works with files featuring a file ending
for FILE in *.*; do mv -v "$FILE" ${FILE// /_}; done;

# batch convert png to jpg
FEND="*.png"; echo "-- convert png in $PWD to jpg"; mkdir -v pngconv; mv -v $FEND pngconv; for IMG in $(ls pngconv/$FEND); do CURR=`basename ${IMG%.*}`; echo "$IMG to $CURR"; convert $IMG "$CURR.jpg"; done;

# display complete file information including image metadata
identify -verbose [image].jpg

# display photographic image take
identify -format "%[EXIF:DateTimeOriginal]\n" [image].jpg
