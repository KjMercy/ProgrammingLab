import datetime


class ExamException(Exception):
    pass


class CSVFile():
    def __init__(self, name):
        self.name = name

    def get_data(self):
        lista_righe = []

        try:
            my_file = open(self.name, 'r')

            for item in my_file:
                riga = item.split(',')

                if(riga[0] != 'date'):
                    riga[-1] = riga[-1].strip()
                    lista_righe.append(riga[0:2])

            my_file.close()
        except OSError:
            raise ExamException(
                'Impossibile aprire il file "{}"'.format(self.name))

        return lista_righe


class NumericalCSVFile(CSVFile):
    def get_data(self):
        lista_righe = super().get_data()

        lista_righe = remove_invalid_timestamps(lista_righe)

        for riga in lista_righe:
            try:
                riga[1] = int(riga[1])
                riga[1] = 'MISSING' if riga[1] < 0 else riga[1]
            except ValueError:
                riga[1] = 'MISSING'

        return lista_righe


class CSVTimeSeriesFile(NumericalCSVFile):
    def get_data(self):
        lista_righe = super().get_data()

        if not is_timeseries_ordered(lista_righe):
            raise ExamException('Time series non ordinata')

        if timeseries_contains_duplicates(lista_righe):
            raise ExamException('Presente timestamp duplicato')

        lista_righe = add_missing_timestamps(lista_righe)

        # for riga in lista_righe:
            # print(riga)

        return lista_righe


def add_missing_timestamps(lista_righe):
    nuova_lista = []
    for i, riga in enumerate(lista_righe):

        if i == (len(lista_righe)-1) and riga[0][5:7] != '12':
            anno = riga[0][0:4]
            mese = '12'
            passeggeri = 'MISSING'
            riga_mancante = [anno + '-' + mese, passeggeri]
            lista_righe.append(riga_mancante)

        if i != (len(lista_righe)-1):
            current_date = riga[0].replace('-', '')
            next_date = lista_righe[i+1][0].replace('-', '')

            if i == 0 and riga[0][5:7] != '01':
                anno = riga[0][0:4]
                mese = '01'
                passeggeri = 'MISSING'
                riga_mancante = [anno + '-' + mese, passeggeri]
                lista_righe.insert(i, riga_mancante)

            if int(riga[0][5:7]) == 12:
                if int(lista_righe[i+1][0][5:7]) != 1:
                    anno = lista_righe[i+2][0][0:4]
                    mese = '01'
                    passeggeri = 'MISSING'
                    riga_mancante = [anno + '-' + mese, passeggeri]
                    lista_righe.insert(i+1, riga_mancante)

            if int(riga[0][5:7]) != 12:
                if int(current_date) != int(next_date) - 1:
                    anno = riga[0][0:4]
                    mese = str(int(riga[0][5:7])+1).zfill(2)
                    passeggeri = 'MISSING'
                    riga_mancante = [anno + '-' + mese, passeggeri]
                    lista_righe.insert(i+1, riga_mancante)

    nuova_lista = lista_righe
    return nuova_lista


def remove_invalid_timestamps(lista_righe):
    i = 0
    while i < len(lista_righe)-1:
        if not is_date_valid(lista_righe[i][0]):
            del lista_righe[i]
        else:
            i += 1

    return lista_righe


def is_date_valid(testo_data):
    flag = True
    try:
        datetime.datetime.strptime(testo_data, '%Y-%m')
    except ValueError:
        flag = False

    return flag


def is_timeseries_ordered(righe):
    date = [riga[0].replace('-', '') for riga in righe if riga[1]]
    return True if date == sorted(date) else False


def timeseries_contains_duplicates(righe):
    date = [riga[0].replace('-', '') for riga in righe]
    return True if len(date) != len(set(date)) else False


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

    if years[0] > years[1]:
        years[0], years[1] = years[1], years[0]

    if years[0] != years[1] - 1:
        raise ExamException('Anni non consecutivi')

    if years[0] == years[1]:
        raise ExamException('Anni forniti sono equivalenti')

    if not isinstance(years[0], int) or not isinstance(years[1], int):
        raise ExamException('Anni forniti non validi')

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
# time_series_file = CSVTimeSeriesFile(name='dat.csv')
time_series = time_series_file.get_data()
anni = list(range(1949, 1960))
# print(time_series)

for i, year in enumerate(anni):
    if year is not anni[-1]:
        years = [year, anni[i+1]]
        print(detect_similar_monthly_variations(time_series, years))
