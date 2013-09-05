convert ${1} -alpha off -fill white -colorize 100% \
     -draw 'fill black polygon 0,0 0,15 15,0 fill white circle 15,15 15,0' \
     \( +clone -flip \) -compose Multiply -composite \
     \( +clone -flop \) -compose Multiply -composite \
     -background Gray50 -alpha Shape    thumbnail_mask.png

convert thumbnail_mask.png -bordercolor None -border 1x1 \
          -alpha Extract -blur 0x10  -shade 130x30 -alpha On \
          -background gray50 -alpha background -auto-level \
          -function polynomial  3.5,-5.05,2.05,0.3 \
          \( +clone -alpha extract  -blur 0x2 \) \
          -channel RGB -compose multiply -composite \
          +channel +compose -chop 1x1 \
          thumbnail_lighting.png


convert ${1} -alpha Set thumbnail_lighting.png \
          \( -clone 0,1 -alpha Opaque -compose Hardlight -composite \) \
          -delete 0 -compose In -composite \
          ${2}

rm -rf thumbnail_lighting.png thumbnail_mask.png
