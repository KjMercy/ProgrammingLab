my_file = open("shampoo_sales.txt", "r")

#print(my_file.read())
##print(my_file.read()[0:50])

##Versione più sofisticata
# my_file_contents = my_file.read()

# if len(my_file_contents) > 50:
#     print(my_file_contents[0:50]+'...')
# else:
#     print(my_file_contents)

##Riga per riga
###Per quale motivo? - ottimizzazione memoria
# print(my_file.readline())
# print(my_file.readline())

##Sintassi più pythonica
for line in my_file:
    print(line)

my_file.close()