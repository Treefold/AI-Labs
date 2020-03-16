# python_list_categ

l =  ["haha", "poc", "Poc", "POC", "haHA", "hei","hey", "HahA", "poc", "Hei"]

d = {}
for cuv in l:
    cuv.lower()
    if cuv.lower() in d.keys():
        d[cuv.lower()] += 1
    else:
        d[cuv.lower()] = 1

for cuv in d:
    print ("Cuvantul {} apare de {} ori".format(cuv, d[cuv]))