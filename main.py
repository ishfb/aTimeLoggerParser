# -*- coding: utf-8 -*-

import sys
import os
import itertools
import datetime
from collections import defaultdict

def log(msg):
    print >>sys.stderr, msg

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
    self.date = ParseCsv(line)[2]


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

  filename = os.path.join(search_path, f)
  with open(filename) as csv:
    log('Start processing {}'.format(filename))
    parser = DateFinder()

    first = True
    for line in csv.readlines():
      if first:
        first = False
      elif len(line.strip()) == 0:
        first = True

        date_str = parser.date
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        if date.weekday() == 6:
            date += datetime.timedelta(days=1)
        elif date.weekday() != 0:
            log("Report {} doesn't start with Monday".format(f))
            sys.exit(2)

        parser = MapFiller(data, date)
      else:
        parser(line)

dates = set()
for _, values in data.iteritems():
  dates |= set(values.keys())

dates = sorted(list(dates))
print '\t'.join(['Неделя'] + ['{}-{}.{:02d}.{}'.format(d.day, d.day + 6, d.month, d.year % 100) for d in dates])

total = 'Всего'
for name in [total] + sorted(list(set(data.keys()) - set([total]))):
  print '\t'.join([name] + [data[name].get(d, ' ') for d in dates])