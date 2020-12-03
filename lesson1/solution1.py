import sys

digit_string = sys.argv[1]

result=0
for i in digit_string:
    result += int(i)
print(result)