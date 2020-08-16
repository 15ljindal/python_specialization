import re

filename = "regex_sum_761235.txt"

fh = open(filename)

sum = 0
for line in fh:
    nums = re.findall('[0-9]+', line)
    for n in nums:
        sum = sum + int(n)

print(sum)
