#!/bin/bash

source activate py27
DATASET=LDC2014T12
LINEAR=fairseq


echo "---------------------------------------"
echo "Dataset ${DATASET}.$LINEAR"

INPUT=data/$DATASET.$LINEAR
python -m amr.preprocess --linearize \
                        -i $INPUT/train.$DATASET.amr.txt \
                        -o train.$DATASET

python -m amr.preprocess --linearize \
                        -i $INPUT/valid.$DATASET.amr.txt \
                        -o valid.$DATASET
python -m amr.preprocess --linearize \
                        -i $INPUT/test.$DATASET.amr.txt \
                        -o test.$DATASET


fairseq preprocess -sourcelang snt \
                   -targetlang amr \
                   -trainpref $INPUT/train.$DATASET \
                   -validpref $INPUT/valid.$DATASET \
                   -testpref $INPUT/test.$DATASET \
                   -destdir data-bin/$DATASET.$LINEAR



