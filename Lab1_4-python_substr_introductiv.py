# python_substr_introductiv

s = input("Your string is ")
# a
for i in range(0, len(s)):
    print (s[i:] + s[:i])

# b
print ("\n")
for i in range(0, len(s)):
    print (s[-i:] + s[:-i])

# c
print ("\n")
for i in range(1, len(s)//2 + 1):
    print (s[:i] + '|' + s[-i:])    