# -*- coding: utf-8 -*-

import sys
import os
import itertools
from collections import defaultdict

def ParseCsv(line):
  result = []
  i = 0
  while i < len(line):
    cur = ''
    if line[i] == '"':
      for c in itertools.takewhile(lambda c: c != '"', line[i + 1:]):
        cur += c
      i += len(cur) + 3
    else:
      for c in itertools.takewhile(lambda c: c != ',', line[i:]):
        cur += c
      i += len(cur) + 1
    result.append(cur)
  return result

class DateFinder:
  def __call__(self, line):
    self.date = ParseCsv(line)[2].split()[0]

class MapFiller:
  def __init__(self, map, date):
    self.map = map
    self.date = date

  def __call__(self, line):
    name, value, _ = ParseCsv(line)
    self.map[name][self.date] = value


data = defaultdict(lambda : dict())

search_path = sys.argv[1]

for f in os.listdir(search_path):
  if not f.endswith('.csv'):
    continue

  with open(os.path.join(search_path, f)) as csv:
    parser = DateFinder()

    first = True
    for line in csv.readlines():
      if first:
        first = False
      elif len(line.strip()) == 0:
        first = True
        parser = MapFiller(data, parser.date)
      else:
        parser(line)

dates = set()
for _, values in data.iteritems():
  dates |= set(values.keys())

dates = sorted(list(dates))
print '\t'.join([''] + dates)

total = 'Всего'
for name in [total] + sorted(list(set(data.keys()) - set([total]))):
  print '\t'.join([name] + [data[name].get(d, ' ') for d in dates])