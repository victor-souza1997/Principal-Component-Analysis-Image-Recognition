#!/bin/sh
num=1
for file in $(ls *.jpg | sort -n); do
   mv "$file" "img_$num.jpg"
   convert $file -resize 220x300 -type Grayscale $file
   let num=$num+1
done
