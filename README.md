# AMR parser with Convolutional Seq2seq


We published the source code for the paper [ConvAMR: Abstract Meaning Representation Parsing for Legal Document](https://arxiv.org/abs/1711.06141)
```
@article{viet:2017:SCIDOCA,
  author    = {Lai Dac Viet and
               Vu Trong Sinh and
               Nguyen Le Minh and
               Ken Satoh},
  title     = {ConvAMR: Abstract meaning representation parsing for legal document},
  journal   = {CoRR},
  volume    = {abs/1711.06141},
  year      = {2017},
  url       = {http://arxiv.org/abs/1711.06141},
  archivePrefix = {arXiv},
  eprint    = {1711.06141},
}
```
## Installation

### Install torch and fairseq 
We recommend to install and run this with ``Ubuntu 16.04``, ``cuda 8.0``, ``cudnn 5.1``.

We recently (June 2019) tested it on ``Ubuntu 18.04``, ``cuda 8.0``, ``cudnn 5.1``. We got a lot of troubles while compiling torch, fairseq and dependencies. If you use Ubuntu 18.04, follow this [post](https://www.kadamwhite.com/archives/2018/install-torch-7-and-cuda-9-1-on-ubuntu-18-04-lts) to modify torch and fairseq installation scripts.

Torch installation can be found [here](http://torch.ch/docs/getting-started.html)

Fairseq installation can be found [here](https://github.com/facebookresearch/fairseq)

### Python dependencies

```
pip install nltk==3.4.3
pip install penman==0.6.2
```

### Train a model

We use following directories in this project:

``corpus`` train/dev/test splits of LDC2014T12 and LDC2017T10

``data`` text-format files, generated from corpus by ``cmdpreprocess.sh``

``data-bin`` binary-format files, generated from corpus by ``cmdpreprocess.sh``

``output`` for saving pretrained models and logs

``tmp`` parsed amr files, generated by ``amr/postprocess.py``

```
ROOT
|-corpus
  |-LDC2014T12
    |-training
    |-dev
    |-test
|-data
  |-LDC2014T12.fairseq
|-data-bin
  |-LDC2014T12.fairseq
|-output
  |-LDC2014T12.fairseq.fconv.r0
|-tmp
```

Step 1: Please copy training/dev/test of LDC2014T12 and LDC2017T10 into ``corpus`` directory, accordingly.

Step 2: Preprocess AMR file:

```
chmod +x cmdpreprocess.sh; ./cmdpreprocess.sh
```


Step 3: Train model:

```
chmod +x cmdtrain.sh; ./cmdtrain.sh
```
## Contact
If you find and issues, please raise an issue in github repository or contact us at ``vietl@uoregon.edu``.
