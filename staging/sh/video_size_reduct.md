## ffmpeg documentation

https://ffmpeg.org/ffmpeg.html

## using ffmpeg to convert dvd to mp4

conda create -n movie python=3.10
condact
conda install ffmpeg
-- the current conda ffmpeg does not support h265 as an encoding library yet...
conda install -c conda-forge exiftool
-- edit metadata

### DVD to single file with unchanged quality
cat VTS_0*_*VOB | ffmpeg -i - -vcodec h264 -acodec mp2 [movie].mp4

### DVD to single file using deinterlace option
    cat VTS_0*_*VOB | ffmpeg -i - -vf yadif -vcodec h264 -acodec mp2 [movie].mp4

### DVD to single file with quality option
The ‘-crf’ option sets the quality of the ripped file. The range of the CRF scale is 0–51, where 0 is lossless , 23 is the default, and 51 is the worst quality possible.

cat VTS_0*_*VOB | ffmpeg -i - -vcodec h264 -crf 24 -acodec mp2 [movie].mp4

### different audio options
-acodec aac

### farther interesting options

-t      ... recording duration e.g. for tests before converting a full movie
-ss     ... starting timestamp in [s]; can use the `HH:MM:SS.xxx` format to specify ms

procedure from dvd to mp4

- check if vobs can be played with vlc without issue 
- if yes, use the concat VOB and convert directly to mp4 approach using ffmpeg
- if no:
- open DVD video folder with VLC; start movie; record full movie to lossless mpg
- convert from mpg to mp4 using ffmpeg
ffmpeg -i "path/to/your-vid.mpg" -acodec copy -vcodec copy -f mp4 "path/to/output-file.mp4"
- convert to lower quality and reduced size and pipe sdterr output to textfile
ffmpeg -i input.mp4 -vcodec h264 -crf 24 output.mp4 2> out.txt


### Issues

when experiencing audio issues e.g. receiving only one of the voice channels,
make sure to convert audio to basic audio e.g. -acodec mp2

when experiencing audio issues e.g.

    [ac3 @ 0x55bae702e3c0] expacc 127 is out-of-range
    [ac3 @ 0x55bae702e3c0] error decoding the audio block
    Error while decoding stream #0:3: Error number -16976906 occurred
    [ac3 @ 0x55bae702e3c0] exponent 25 is out-of-range
    [ac3 @ 0x55bae702e3c0] error decoding the audio block

leading to repeating video sequences or missing audio, convert audio and video
separately and then merge both video and audio

# video and audio indexes are examples; use ffprobe to identify the correct ones
ffmpeg -i [input.ext] -vcodec h264 -crf 24 -map 0:v:0 out_vid_only.mp4
ffmpeg -i [input.ext] -map 0:a:2 -acodec mp2 out_audio_only.mp2
ffmpeg -i out_vid_only.mp4 -i out_audio_only.mp2 out.mp4
or 
# -c ... -codec ... -c copy = copy input over instead of going through a decode->filter->encode process.
ffmpeg -i out_vid_only.mp4 -i out_audio_only.mp2 -c copy out.mp4

Test first which audio codecs are available using the ffprobe command:

    ffprobe -analyzeduration 100M -probesize 100M [input.ext]

Then select the appropriate audio and video indexes

### Concatenate mp4

cat merge.txt
file '/home/file1.mp4'
file '/home/file1.mp4'
ffmpeg -f concat -safe 0 -i merge.txt -c copy out.mp4

### Trim mp4

Create a snippet starting at point 00:00:00 for duration one minute

    ffmpeg -ss 00:00:00 -t 00:01:00 -i input.mp4 -c copy output.mp4

### Check for errors or warnings

- set loglevel verbosity to errors
ffmpeg -v error -i [input.ext] -f null -

- set loglevel verbosity to errors and warnings
ffmpeg -v warning -i [input.ext] -f null -

#!/usr/bin/env bash

ffmpeg -i [input.ext] -vcodec h264 -crf 24 -acodec mp2 output.mp4
