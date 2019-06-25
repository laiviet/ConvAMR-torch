#!/bin/bash

SRC_LANG="snt"
DST_LANG="amr"

MODEL=fconv
DATASET=LDC2014T12
LINEAR=fairseq

ROOT=`pwd`
MAX_EPOCH=200
RUN=r0

source activate py27 

GOLD_PATH=$ROOT/data/$DATASET.$LINEAR/test.$DATASET.amr.txt
DATA_DIR=$ROOT/data-bin/$DATASET.$LINEAR
TEST_SENTENCE=$ROOT/data/$DATASET.$LINEAR/test.$DATASET.snt

# Fully convolutional sequence-to-sequence model
SAVE_DIR=output/$DATASET.$LINEAR.$MODEL.$RUN
mkdir $SAVE_DIR
fairseq train -sourcelang $SRC_LANG \
                      -targetlang $DST_LANG \
                      -datadir $DATA_DIR \
                      -model fconv \
                      -nenclayer 4 \
                      -nlayer 3 \
                      -dropout 0.2 \
                      -optim nag \
                      -lr 0.25 \
                      -clip 0.1 \
                      -momentum 0.99 \
                      -timeavg \
                      -bptt 0 \
                      -savedir $SAVE_DIR \
                      -maxepoch $MAX_EPOCH > $ROOT/output/$DATASET.$LINEAR.$MODEL.$RUN.log

python -m amr.postprocess --fairseq --system $SAVE_DIR/gen-b01.txt


#echo "---------------- Evaluation ----------------"

cd $ROOT/smatch
python smatch.py --significant 6 \
                 -f $ROOT/tmp/output_$DATASET.$LINEAR.$MODEL.${RUN}_gen-b01.txt.tmp.amr.txt $GOLD_PATH
