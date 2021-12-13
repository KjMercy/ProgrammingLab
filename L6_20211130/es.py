class CSVFile():
    def __init__(self, name):
        if type(name) is not str:
            raise Exception("Percorso file (name) non di tipo stringa")
        else:
            self.name = name


    def get_data(self, start=None, end=None):

        if start == None:
            start = 0;
        if start < 0:
            start = 0

        lista_righe = []
        
        try:
            if end is not None:
                my_file = open(self.name, 'r').readlines()[start:end+1] #end+1 perchè ignoro la riga header
            else:
                my_file = open(self.name, 'r').readlines()[start:]

            for item in my_file:
                riga = item.split(',')

                if(riga[0] != 'Date'):
                    riga[1] = riga[1].strip()
                    lista_righe.append(riga)
            
            #my_file.close()
        except OSError:
            print('Impossibile aprire il file "{}"'.format(self.name))

        return lista_righe


file_shampoo = CSVFile('shampoo.txt')
# print(file_shampoo.get_data(-3,3))
# print(file_shampoo.get_data())
# print(file_shampoo.get_data(30))