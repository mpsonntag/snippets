# 'convert' is part of the imagemagic suite
# cd to image directory
# will create a conv folder and convert all jpg images to 85% quality
mkdir conv; for IMG in $(ls *.jpg); do echo "$IMG"; convert $IMG -quality 85% conv/$IMG; done;

# move original images to its own folder; convert all images to 85% quality in root dir
echo "-- convert jpg in $PWD to 85% quality"; mkdir -v original; mv -v *.jpg original; for IMG in $(ls original/*.jpg); CURR=`basename $IMG`; do echo "$IMG to $CURR"; convert $IMG -quality 85% $CURR; done;

# display complete file information including image metadata
identify -verbose [image].jpg

# display photographic image take
identify -format "%[EXIF:DateTimeOriginal]\n" [image].jpg
