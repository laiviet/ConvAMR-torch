from __future__ import print_function
import argparse
import penman
DEBUG = False


class Node(object):
  def __init__(self, var, concept, is_constant=False):
    self.var = var
    self.concept = concept
    self.is_constant = is_constant


def linearize(lines):
  def normalize(line):
    return line.strip().replace('(', '( ').replace(')', ' )')

  # preprocess
  text = ''
  for line in lines:
    if len(text) > 0:
      text += ' ' + normalize(line)
    else:
      text = normalize(line)
  if DEBUG:
    print('Text: "%s"' % text)

  queue = []
  stack = []
  var_concept = {}
  var = None
  prev=None
  for tok in text.split(' '):
    if len(tok) == 0:
      continue
    if DEBUG:
      print('--> "%s"' % (tok), end=',')
    if tok == '(':
      if DEBUG:
        print('Do nothing 1')
    elif tok == ')':
      node = stack.pop()
      queue.append(node.concept)
      if DEBUG:
        print('Pop stack')
        show(queue)
    elif tok == '/':
      if DEBUG:
        print('Do nothing 3')
    elif tok.startswith(':'):
      queue.append(tok)
      if DEBUG:
        print('Append to queue 1')
        show(queue)
    else:
      if prev == '(':
        var = tok
        if DEBUG:
          print('New var')
      elif prev == '/':
        concept = tok
        var_concept[var] = concept
        nn = Node(var, concept)
        stack.append(nn)
        queue.append(concept)
        if DEBUG:
          print('Put to stack, append to queue 2')
          show(queue)
      elif prev.startswith(':'):
        if tok in var_concept:
          concept = var_concept[tok]
          queue.append(concept)
          queue.append(concept)
          if DEBUG:
            show(queue)
            print('Append to queue 2')
        else:
          constant = tok
          queue.append(constant)
          queue.append(constant)
          if DEBUG:
            show(queue)
            print('Append to queue 3')
    prev = tok

  return ' '.join(queue)


def show(queue):
  print(' '.join(queue))


def node_of(concept_var, new_concept):
  prefix = new_concept[0]
  chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
  if DEBUG:
    print('-> ' + new_concept)
  if prefix not in chars:
    prefix = 'x'
  if new_concept in concept_var:
    node = Node(concept_var[new_concept], new_concept)
    return node, True
  else:
    vars = concept_var.values()
    idx = 0
    v = prefix + str(idx)
    while v in vars:
      idx += 1
      v = prefix + str(idx)
    concept_var[new_concept] = v
    node = Node(v, new_concept)
    return node, False


def new_line(ntab, node, rel=None, node_exist=False):
  line = ''
  for i in range(ntab):
    line += '\t'
  if rel:
    if rel == ':quant':
      line += '%s %s' % (rel, node.concept)
      return line
    else:
      line += '%s ' % rel
  if node_exist:
    line += node.var
  else:
    line += '(%s / %s' % (node.var, node.concept)
  return line


def delinearize_old(linearized_amr):
  lines = []
  tokens = linearized_amr.split(' ')
  stack = []
  concept_var = {}
  rel = None
  line = ''

  for tok in tokens:
    if '(' in tok or ')' in tok:
      print('Tok contains parenthesis')
      break
    if tok.startswith(':'):
      if rel:
        print('Stop at: %s'%(tok))
        break
      else:
        rel = tok
    else:
      if len(stack) > 0:
        top = stack[-1]
        if tok == top.concept:
          stack.pop()
          if not top.is_constant:
            line += ')'
          if len(stack) ==0:
            break
          continue
        else:
          if rel == None:
            print('Rel = None')
            break

      if len(line) > 0:
        lines.append(line)
      node, exist = node_of(concept_var, tok)
      if rel == ':quant' or exist:
        node.is_constant = True

      line = new_line(len(stack), node, rel=rel, node_exist=exist)

      rel = None
      stack.append(node)

  if len(stack) > 1:
    for node in stack[1:]:
      line +=')'
  lines.append(line)
  return lines



def delinearize(linearized_amr):
  tokens = linearized_amr.split(' ')
  stack = []
  concept_var = {}
  triplets = []
  rel = None

  def get_var(tok, concept_var):
    vars = concept_var.values()
    if tok[0] in 'abcdefghijklmnopqrstuvwxyz':
      t = tok[0]
    else:
      t='x'
    if t not in vars:
      return t
    else:
      count = 1
      while t + str(count) in vars:
        count +=1
      return t + str(count)

  #print(linearized_amr)
  for tok in tokens:
    if '(' in tok or ')' in tok:
      #print('Tok contains parenthesis')
      break

    if tok.startswith(':'):
      # A relation
      if rel:
        #print('Two relations %s - %s'%('..',rel))
        break
      else:
        rel = tok[1:]
    else:
      # A concept
      if len(stack) == 0:
        #print('Length of stack = 0')
        var = get_var(tok, concept_var)
        triplets.append((var, 'instance', tok))
        concept_var[tok] = var
        stack.append((var, tok))
        root = var
      else:
        top_var, top_concept = stack[-1]
        if rel:
          #print(concept_var)
          if tok not in concept_var.keys():
            #print('%s not in %s'%(tok, str(concept_var)))
            var = get_var(tok, concept_var)
            triplets.append((var, 'instance', tok))
            concept_var[tok] = var
          else:
            var = concept_var[tok]
          triplets.append((top_var, rel, var))
          stack.append((var, tok))
          rel = None
        else:
          if top_concept == tok:
            stack.pop()
            if len(stack) == 0:
              break
          else:
            #print('Two concepts: %s - %s'%(top_concept, tok))
            break

    codec = penman.AMRCodec()
    graph = penman.Graph(triplets)
    #print(codec.encode(graph, top=root))
  return codec.encode(graph, top=root)

def test():
  # with open('sample.txt') as f:
  #   lines = f.readlines()
  # amr = linearize(lines)
  # print(amr)

  # linearized = 'consult-01 :ARG0 i i :ARG1 company :name name :op1 <<unk>> <<unk>> name company :ARG2 model :name name :op1 <<unk>> <<unk>> :op2 "( "( name :mod number number model :time tomorrow tomorrow :instrument phone-number-entity :value <<unk>> <<unk>> phone-number-entity :instrument phone-number-entity :value <<unk>> <<unk>> phone-number-entity consult-01'
  # amr = delinearize(linearized)
  # print(amr)
  # print('----------------------------------------------------------------------------------------')
  # linearized = 'adopt-01 :ARG0 company :name name :op1 "Promos" "Promos" name company :ARG1 technology :mod distance-quantity :quant 90 90 :unit nanometer nanometer distance-quantity :poss company :name name :op1 "Hynix" "Hynix" name company technology :location plant :poss company company :mod new new :location country :name name :op1 "Taiwan" "Taiwan" name :mod central central country plant :ARG1-of start-01 :time date-entity :year 2005 2005 <<unk>> 4 4 date-entity start-01 adopt-01'
  # amr = delinearize(linearized)
  # print(amr)

  print('----------------------------------------------------------------------------------------')
  linearized = '4 4 4 4'
  amr = delinearize(linearized)
  print(amr)
if __name__ == '__main__':
  test()
