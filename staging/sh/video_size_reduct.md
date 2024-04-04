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
