import re

filename = "regex_sum_761235.txt"

print(sum([int(n) for n in re.findall('[0-9]+', open(filename).read())]))
