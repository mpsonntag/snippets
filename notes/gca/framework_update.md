## general upgrade problems
I figured out a way to still build GCA-Web using the current framework.
Unfortunately this increases the already long build time of the project to about 30min while looking for 15 minutes at dependencies that fail to be downloaded.

major upgrade problems:

activator
- the tool we used to build the project, test and run the application does not exist any more
- as far as I have been able to figure out, we need to move to plain sbt
- don't know what that entails


see here for details:
https://www.lightbend.com/blog/introducing-a-new-way-to-get-started-with-lightbend-technologies-and-saying-goodbye-to-activator

play framework: we are 5 versions behind, with as far as I was able to figure out, 2 larger changes behind.
the scala language needs to be upgraded from 2.11.1 to 2.13
the build tool sbt needs to be upgraded from 0.13.5 version 1.3.5?

## short term upgrade/migration plan

We'll probably first need to move to an sbt only installation w/o activator:

instead of activator fetch sbt from:
https://www.scala-sbt.org/download.html

unfortunately it seems that a lot of the typesafe play plugins that we use are not compatible with scala 2.13 and sbt 1.3.x which is what the latest play version 2.8 requires.

## other long term problems

- next problem:
  the os on the docker container itself is outdated as well and probably needs to be updated for future


- and longer term problem:
  - application cache for offline viewing will become deprecated in april 2020
  -> might affect offline viewing but it will be superseded by service workers which we already have implemented. 
        https://www.chromestatus.com/features/6192449487634432

