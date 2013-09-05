convert ${1} \
          -bordercolor white  -border 6 \
          -bordercolor grey60 -border 1 \
          -background  none   -rotate 6 \
          -background  black  \( +clone -shadow 60x4+4+4 \) +swap \
          -background  none   -flatten \
          ${2}
