# 'convert' is part of the imagemagic suite
# cd to image directory
# will create a conv folder and convert all jpg images to 85% quality
mkdir conv; for IMG in $(ls *.jpg); do echo "$IMG"; convert $IMG -quality 85% conv/$IMG; done;

# display complete file information including image metadata
identify -verbose [image].jpg

# display photographic image take
identify -format "%[EXIF:DateTimeOriginal]\n" [image].jpg
