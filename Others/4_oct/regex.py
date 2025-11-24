import re
 
s = 'ABCDCDC'
match = re.findall(r'CDC', s)
print(match)