# define an empty list
places = []

# open file and read the content in a list
with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]

        # add item to the list
        places.append(currentPlace)
        
segments = list(filter(lambda x: x!="", places[0].replace('(','').replace(')','').split(' ')))
transactions = []
for i in range(0,20, 5):
    transaction = {'id':segments[i], 'byer':segments[i+1], 'ip':segments[i+2], 'products':segments[i+4].split(',')}
    transactions.append(transaction)
print(transactions)

