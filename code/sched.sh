#/bin/bash
day=$1
if [ "$day" = 'M' ]
then
cat ./Monday

elif [ "$day" = 'T' ]
then
cat ./Tuesday

elif [ "$day" = 'W' ]
then
cat ./Wednesday

elif [ "$day" = 'R' ]
then
cat ./Thursday

elif [ "$day" = 'F' ]
then
cat ./Friday

else
echo "Error: Syntax: sched <M,T,W,R, or F>"

fi
