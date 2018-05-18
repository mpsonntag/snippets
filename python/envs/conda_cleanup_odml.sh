#!/usr/bin/env bash

echo -- Running odml_conda_deps_reset.sh
echo -- make sure we are clean and not in an environment.
source deactivate

echo -- Cleanup previous environments

/home/msonntag/Chaos/software/mconda2/bin/conda remove -n o2 --all -y
/home/msonntag/Chaos/software/mconda2/bin/conda remove -n ot2 --all -y
/home/msonntag/Chaos/software/mconda2/bin/conda remove -n o3 --all -y
/home/msonntag/Chaos/software/mconda2/bin/conda remove -n ot3 --all -y

echo -- Create test environments

/home/msonntag/Chaos/software/mconda2/bin/conda create -n o2 python=2.7 -y
/home/msonntag/Chaos/software/mconda2/bin/conda create -n ot2 python=2.7 -y
/home/msonntag/Chaos/software/mconda2/bin/conda create -n o3 python=3.5 -y
/home/msonntag/Chaos/software/mconda2/bin/conda create -n ot3 python=3.5 -y

echo -- List current environments

/home/msonntag/Chaos/software/mconda2/bin/conda info --envs

