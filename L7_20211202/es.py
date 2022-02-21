class CSVFile():
    def __init__(self, name):
        if type(name) is not str:
            raise Exception('Percorso file (name) non di tipo stringa')
        else:
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
            print('OSError: Impossibile aprire il file "{}"'.format(self.name))
        except Exception:
            print('Impossibile aprire il file')

        return lista_righe


class NumericalCSVFile(CSVFile):
    def get_data(self):
        lista_righe = super().get_data()
        for riga in lista_righe:

            for i, elemento in enumerate(riga):

                if(i != 0):
                    try:
                        riga[i] = float(elemento)
                    except ValueError:
                        print('Errore di valore, elemento = {}'.format(elemento))
                        riga[i] = 0.0

        return lista_righe


# file = NumericalCSVFile('sales.txt')
# print(file.get_data())
