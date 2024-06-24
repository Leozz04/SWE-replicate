import re

f = re.findall(r"\((.*?)\)","(awdhakwd)")
m = re.search(r'(?<=)\w+', 'spam-egg')
m.group(0)
print(m)