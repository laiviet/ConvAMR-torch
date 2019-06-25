AMR parser with Convolutional Seq2seq


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

We derive and modify the [``fairseq``](https://github.com/facebookresearch/fairseq-py) project form  facebook research.

## Installation
Please follow this [guideline](https://github.com/pytorch/pytorch#installation) to install the pytorch version 0.4

Install the dependencies and clone metrics for evaluating AMR parser:

```
chmod +x install_dep.sh
./install_dep.sh <python-3.6-environment-name>
```

## Contact
If you find and issues, please raise an issue in github repository or contact us at ``vietl@uoregon.edu``.
