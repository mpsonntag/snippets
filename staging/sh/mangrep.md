curl address | tr '<' '\n' | grep id=\"image\" | tr '"' '\n' | grep jpg

curl address | tr '<' '\n' | grep html | grep option