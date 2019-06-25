from amr.linearize import linearize, delinearize
from os.path import join, basename
from multiprocessing import Pool
from nltk.tokenize import TweetTokenizer
from amr.utils import read_amr_format
from amr.utils import save_amr_format
import io
import argparse
import os
import subprocess

tokenizer = TweetTokenizer()


def save(sentences, file_path):
  text = u''
  for snt in sentences:
    text += snt + u'\n'
  with io.open(file_path, 'w', encoding='utf8') as f:
    f.write(text[:-1])


def split(data):
  '''
  data: a list of object
  '''
  train, valid, test = [], [], []
  for idx, sample in enumerate(data):
    if idx % 5 == 0:
      test.append(sample)
    elif idx % 5 == 1:
      valid.append(sample)
    else:
      train.append(sample)
  return train, valid, test


def preprocess_feature(obj):
  # preprocess sentence
  tokens = tokenizer.tokenize(obj['snt'])
  snt = ' '.join(tokens)
  # preprocess amr
  linear_amr = linearize(obj['doc'])
  return (snt, linear_amr, obj)


def lin_deline(amr_obj):
  amr = amr_obj['doc']
  amr = linearize(amr)
  amr = delinearize(amr)
  amr_obj['doc'] = amr
  return amr_obj


############ TEST ####################

parser = argparse.ArgumentParser()
parser.add_argument('--linearize', default=False,
                    action='store_true', help='Linearize the given file')
parser.add_argument('--delinearize', default=False,
                    action='store_true', help='De-linearize the given file')
parser.add_argument('--bound', default=False,
                    action='store_true', help='Calculate upper-bound')
parser.add_argument('--smatch', default='/home/vietld/jaist/fairseq/smatch',
                    action='store_true', help='SMATCH root directory')

parser.add_argument('-i', '--input', required=True, help='Input file path')
parser.add_argument('-o', '--output', help='Output file path')

args = parser.parse_args()

if args.linearize:
  p = Pool(20)
  print('Linearize file: %s' % (args.input))
  filename = basename(args.input)
  directory = args.input[:-len(filename)]
  data = read_amr_format(args.input, return_dict=False)
  sentences = [x['snt'] for x in data]
  amrs = [x['doc'] for x in data]

  amrs_linearized = []
  for x in data:
    try:
      amrs_linearized.append(linearize(x['doc']))
    except:
      print('Error at linearizing: '+x['id'])
  prefix = filename.split('.')[0]
  save(sentences, join(directory, '%s.snt' % (args.output)))
  save(amrs_linearized, join(directory, '%s.amr' % (args.output)))

elif args.delinearize:
  p = Pool(20)
  print('Delinearization file: ')
  filename = basename(args.input)
  directory = args.input[:-len(filename)]
  with io.open(args.input) as f:
    lines = f.readlines()
  amrs = p.map(delinearize, lines)
  data = {}
  for idx, amr in enumerate(amrs):
    data[idx] = {'id': str(idx),
                 'snt': 'Unknown',
                 'doc': amr}
  save_amr_format(data, '%s.lin-delin.amr.txt' % (args.output))
elif args.bound:
  print('Calculate upper bound')
  p = Pool(20)
  gold_path = os.path.abspath(args.input)
  print('Linearize file: %s' % (args.input))
  filename = basename(args.input)
  directory = args.input[:-len(filename)]
  data = read_amr_format(args.input, return_dict=False)

  #result = [lin_deline(x) for x in data]
  result = p.map(lin_deline, data)

  output_path = join('tmp', 'bound.%s' % (filename))
  output_path = os.path.abspath(output_path)
  save_amr_format(result, output_path,end='')
  command = 'python smatch.py --significant 6 -f %s %s' % (gold_path, output_path)
  subprocess.check_call(command.split(' '), cwd=args.smatch)
