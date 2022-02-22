class ExamException(Exception):
    pass


class CSVFile():
    def __init__(self, name):
        if type(name) is not str:
            raise Exception("Percorso file (name) non di tipo stringa")
        else:
            self.name = name

    def get_data(self):
        lista_righe = []

        try:
            my_file = open(self.name, 'r')

            for item in my_file:
                riga = item.split(',')

                if(riga[0] != 'date'):
                    riga[1] = riga[1][0:-1]
                    lista_righe.append(riga)

            my_file.close()
        except OSError:
            print('Impossibile aprire il file "{}"'.format(self.name))

        return lista_righe


class NumericalCSVFile(CSVFile):
    def get_data(self):
        lista_righe = super().get_data()

        for riga in lista_righe:

            for i, elemento in enumerate(riga):

                if(i == 1):
                    try:
                        riga[1] = int(elemento)
                    except ValueError:
                        riga[1] = 'MISSING'

        return lista_righe


class CSVTimeSeriesFile(NumericalCSVFile):
    def get_data(self):
        lista_righe = super().get_data()

        for riga in lista_righe:
            pass

        return lista_righe


def get_monthly_variations(monthly_passengers):
    monthly_variations = []

    for i, current_month in enumerate(monthly_passengers):

        if i < (len(monthly_passengers) - 1):

            if current_month != 'MISSING' and monthly_passengers[i+1] != 'MISSING':
                monthly_variations.append(
                    abs(current_month - monthly_passengers[i+1]))
            else:
                monthly_variations.append('MISSING')

    return monthly_variations


def detect_similar_monthly_variations(time_series, years):

    anni_disponibili = [int(data[0][0:4]) for data in time_series]
    if years[0] not in anni_disponibili or years[1] not in anni_disponibili:
        raise ExamException('Anno non presente tra i dati')

    monthly_passengers_1 = [month[1]
                            for month in time_series if month[0][0:4] == str(years[0])]
    monthly_passengers_2 = [month[1]
                            for month in time_series if month[0][0:4] == str(years[1])]

    # print(monthly_passengers_1)
    # print(monthly_passengers_2)

    monthly_variations_1 = get_monthly_variations(monthly_passengers_1)
    monthly_variations_2 = get_monthly_variations(monthly_passengers_2)

    # print(monthly_variations_1)
    # print(monthly_variations_2)

    similarities_list = []
    for i in range(11):
        if monthly_variations_1[i] == 'MISSING' or monthly_variations_2[i] == 'MISSING':

            similarities_list.append(False)

        elif abs(monthly_variations_1[i] - monthly_variations_2[i]) <= 2:

            similarities_list.append(True)

        else:

            similarities_list.append(False)

    return similarities_list


# TEST
time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
anni = list(range(1949, 1960))

for i, year in enumerate(anni):
    if year is not anni[-1]:
        years = [year, anni[i+1]]
        print(detect_similar_monthly_variations(time_series, years))
