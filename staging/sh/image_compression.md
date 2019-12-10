- download the latest `figures` and `figures_mobile` from gate
- run the cleanup script (`cleanup_existing`) with `figures_mobile` 
  as source and `figures` as target to remove all figures that 
  have already been converted.
- run the conversion script (`image_conversion`) converting all
  images to JPG in a new folder.
- check the output files manually to see if any PNGs had 
  troubles converting any transparent background. If yes
  fix these from the original file with GIMP.
