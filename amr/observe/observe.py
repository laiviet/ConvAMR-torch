import os
import codecs
import amr.utils as utils
from os.path import join
from multiprocessing import Pool
from collections import Counter


def split_long_short(file_paths, prefix='default', threshhold=20):
  data = []
  for file in file_paths:
    data.append(utils.read_amr_format(file))

  short_data, long_data = [], []

  for d in data:
    if (d['text'].split(' ')) > threshhold:
      long_data.append(d)
    else:
      short_data.append(d)
  utils.save_amr_format(short_data, 'tmp/%s.short_data.amr.txt' % (prefix))
  utils.save_amr_format(long_data, 'tmp/%s.long_data.amr.txt' % (prefix))


def normalize_amr(str):
  str = str.replace('\n', ' ')
  str = str.replace('(', '( ').replace(')', ' )')
  str = str.replace('/', ' / ')
  str = str.replace('   ', ' ')
  str = str.replace('  ', ' ').replace('  ', ' ')
  str = str.replace('  ', ' ').replace('  ', ' ')
  return str

def analyze(amrobj):
  str = ' '.join(amrobj['doc'])
  counter = Counter(normalize_amr(str).split(' '))
  return counter


def wordsense_observation(path):
  data = []
  for fname in os.listdir(path):
    print('Read file: %s'%(fname))
    x= utils.read_amr_format(join(path, fname))
    print(type(x))
    data += x
  pool = Pool(20)
  counter = Counter()
  result = pool.map(analyze, data)
  for c in result:
    counter.update(c)

  word_counter = Counter()
  for 


if __name__ == '__main__':
  wordsense_observation('corpus/')
