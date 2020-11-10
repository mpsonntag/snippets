## yl setup

conda create -n yl python=3.8 -y

condact yl

pip install y_l
conda install -c conda-forge ffmpeg

## Upgrade

pip install --upgrade y_l

## Recipes

- display available formats

        yl [address] -F

- fetch a specific format

        yl [address] -f [format]

- fetch audio only (audio quality 0 high, 9 poor; requires ffmpeg)

        yl [address] -x --audio-quality 0 --audio-format aac

- rename the resulting file

        yl [address] -o [output_name]
