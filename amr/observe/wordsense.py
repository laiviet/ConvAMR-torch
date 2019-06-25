import os
import codecs
import amr.utils as utils
from os.path import join
from multiprocessing import Pool
from collections import Counter

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


def split_sense(str):
  parts = str.split('-')
  try:
    int(parts[-1])
    if len(parts) >1:
    	return str[:len(str)-len(parts[-1])-1], True
    else:
    	return str, False
  except:
    return str, False

def print_top(counter, top_n=100):
	for word, freq in counter.most_common(top_n):
		print('%20s %5d'%(word, freq))


def wordsense_observation(path):
  data = []
  for fname in os.listdir(path):
    print('Read file: %s'%(fname))
    x= utils.read_amr_format(join(path, fname))
    # print(type(x))
    data += x
  pool = Pool(20)
  counter = Counter()
  result = pool.map(analyze, data)
  for c in result:
    counter.update(c)

  word_counter = Counter()
  sense_counter = Counter()
  print(type(counter))


  for sense in counter:
    freq = counter[sense]
    word, is_sense = split_sense(sense)
    if is_sense:
      word_counter.update({word: freq})
      sense_counter.update({sense: freq})
  # print top
  # print_top(word_counter, 20)
  # print('------')
  # print_top(sense_counter,20)

  print('Number of sense: %d'%(len(sense_counter)))
  print('Number of word: %d'%(len(word_counter)))
  print('Sense/word: %f'%(float(len(sense_counter))/len(word_counter)))

  mul_sense_counter = dict()
  for sense in sense_counter:
  	word, _ = split_sense(sense)
  	if word not in mul_sense_counter:
  		mul_sense_counter[word] = set([sense])
  	else:
  		sense_set = mul_sense_counter[word]
  		sense_set.add(sense)
  		mul_sense_counter[word] = sense_set
  x = [word for word, sense_set in mul_sense_counter.items() if len(sense_set)>1]
  print('Multiple-sense word: %d'%(len(x)))
  print('   percentage: %f'%(float(len(x))/len(word_counter)))	

if __name__ == '__main__':
  wordsense_observation('corpus/')
