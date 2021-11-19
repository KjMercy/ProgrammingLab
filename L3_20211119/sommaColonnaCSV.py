my_file = open('shampoo_sales.txt','r')

def sommaSales(file):
    somma = 0
    for line in my_file:
        elements = line.split(',')
        if elements[0] != 'Date':
            somma = somma + float(elements[1])
    return somma

print('La somma delle vendite e\': {:.2f}'.format(sommaSales(my_file)))

my_file.close()