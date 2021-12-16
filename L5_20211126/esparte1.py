class CSVFile():
    def __init__(self, name):
        self.name = name

    def get_data(self):
        lista_righe = []
        
        try:
            my_file = open(self.name, 'r')
        
            for item in my_file:
                riga = item.split(',')

                if(riga[0] != 'Date'):
                    riga[1] = riga[1][0:-1]
                    lista_righe.append(riga)
            
            my_file.close()
        except OSError:
            print('Impossibile aprire il file "{}"'.format(self.name))

        return lista_righe


file_shampoo = CSVFile('shampoo_sales.txt')
# file_shampoo = CSVFile('sales.txt')

print("Lista: {}".format(file_shampoo.get_data()))
#print(file_shampoo.name)
