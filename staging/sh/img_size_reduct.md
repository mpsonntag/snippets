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

# batch prepend exif datetime image taken to filename
for IMG in *.jpg; do CBASE=`basename $IMG`; CA=`identify -format "%[EXIF:DateTimeOriginal]\n" $IMG`; CB="${CA//:/}"; CC="${CB// /_}"; CD="IMG_${CC}__${CBASE}"; mv -v $IMG $CD; done;


# conda env for exiv2
conda create -n img python=3.10
conda activate img
conda install -c conda-forge exiv2

## display exiv data using exiv2
exiv2 -P E [image].jpg
## filter exiv tags for datetime information
exiv2 -g date/i [image].jpg

## adjust all exiv dates by [HH:MM:ss] e.g. subtract 5h 12min 11s
exiv2 -v -a -5:12:11 ad [image].jpg
## batch adjust
exiv2 -v -a [+/-]HH[:MM[:ss]] ad *.jpg

## batch prepend datetime to basename
exiv2 -v -r IMG_%Y%m%d_%H%M%S__:basename: *.jpg

## note template
Exif dates and times of images with the ending "__IMG_XXXX.jpg" have been adjusted
