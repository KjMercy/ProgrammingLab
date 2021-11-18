def sommaElementiLista(lista):
    somma = 0
    for item in lista:
        somma = somma + item
    return somma

my_list = [1,2,3,4,5,6,7,8,9,10]

print("Somma con la mia funzione {}".format(sommaElementiLista(my_list)))

# è inutile farla come sopra, tanto esiste già la funzione
# built-in sum()

print("Somma con la funzione sum() {}".format(sum(my_list)))