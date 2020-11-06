import re

s = "are are smarter than dogs"

result = re.findall("(are).*(than)", s)

print(result)
