import datetime


class ExamException(Exception):
    pass

#Classe per leggere un generico file csv
class CSVFile():
    def __init__(self, name):
        self.name = name

        #Accetto solo nomi file di tipo stringa
        if not isinstance(self.name, str):
            raise ExamException('Nome file non valido')


    #Ritorna una lista di liste (righe), la lista interna contiene le colonne
    #modificata per considerare solo le prime due colonne
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


#Figlia di CSVFile, con modifiche il metodo get_data()
class NumericalCSVFile(CSVFile):

    #Prima di tornare la lista di liste, converte il secondo elemento della
    #lista interna, cioè la seconda colonna, a int
    def get_data(self):
        lista_righe = super().get_data()

        #vedere la funzione remove_invalid_timestamps()
        lista_righe = remove_invalid_timestamps(lista_righe)

        for riga in lista_righe:
            try:
                riga[1] = int(riga[1])
                riga[1] = 'MISSING' if riga[1] < 0 else riga[1]
            except ValueError:
                riga[1] = 'MISSING'

        return lista_righe

#Estende NumericalCSVFile, con modifiche sul metodo get_data()
class CSVTimeSeriesFile(NumericalCSVFile):
    
    #Faccio varie considerazioni sulla lista di liste specifiche di un 
    #file csv contenente una TimeSeries
    def get_data(self):
        lista_righe = super().get_data()

        #vedere la funzione is_timeseries_ordered()
        if not is_timeseries_ordered(lista_righe):
            raise ExamException('Time series non ordinata')

        #vedere la funzione timeseries_contains_duplicates()
        if timeseries_contains_duplicates(lista_righe):
            raise ExamException('Presente timestamp duplicato')

        #vedere la funzione add_missing_timestamps()
        lista_righe = add_missing_timestamps(lista_righe)

        return lista_righe


#aggiunge una lista interna quando manca il riferimento a uno o più mesi
#di un anno, esempio: [..., [''1949-02', 'MISSING'], ...]
def add_missing_timestamps(lista_righe):
    nuova_lista = []
    for i, riga in enumerate(lista_righe):

        #Caso in cui manca l'ultima data della lista
        if i == (len(lista_righe)-1) and riga[0][5:7] != '12':
            anno = riga[0][0:4]
            mese = '12'
            passeggeri = 'MISSING'
            riga_mancante = [anno + '-' + mese, passeggeri]
            lista_righe.append(riga_mancante)

        #Caso in cui ci troviamo tra il primo elemento e il penultimo compresi 
        if i != (len(lista_righe)-1):
            current_date = riga[0].replace('-', '')
            next_date = lista_righe[i+1][0].replace('-', '')

            #Manca il primo mese
            if i == 0 and riga[0][5:7] != '01':
                anno = riga[0][0:4]
                mese = '01'
                passeggeri = 'MISSING'
                riga_mancante = [anno + '-' + mese, passeggeri]
                lista_righe.insert(i, riga_mancante)

            #Manca l'ultimo mese di un anno 'interno', cioè non l'ultimo anno
            if int(riga[0][5:7]) == 12:
                if int(lista_righe[i+1][0][5:7]) != 1:
                    anno = lista_righe[i+2][0][0:4]
                    mese = '01'
                    passeggeri = 'MISSING'
                    riga_mancante = [anno + '-' + mese, passeggeri]
                    lista_righe.insert(i+1, riga_mancante)

            #Manca un mese diverso dal primo e l'ultimo di un anno 'interno'
            if int(riga[0][5:7]) != 12:
                if int(current_date) != int(next_date) - 1:
                    anno = riga[0][0:4]
                    mese = str(int(riga[0][5:7])+1).zfill(2)
                    passeggeri = 'MISSING'
                    riga_mancante = [anno + '-' + mese, passeggeri]
                    lista_righe.insert(i+1, riga_mancante)

    nuova_lista = lista_righe
    return nuova_lista


#Rimuove una lista interna, ciè una riga, quando la data di questa non è valida
def remove_invalid_timestamps(lista_righe):
    i = 0
    while i < len(lista_righe)-1:
        if not is_date_valid(lista_righe[i][0]):
            del lista_righe[i]
        else:
            i += 1

    return lista_righe

#Controlla la validità della data nel formato preferio
def is_date_valid(testo_data):
    flag = True
    try:
        #Tenta di creare un istanza di data fornita una stringa
        datetime.datetime.strptime(testo_data, '%Y-%m')
    except ValueError:
        flag = False

    return flag


#Controllo se la timeseries è ordinata confrontando quella fornita con 
#l'ordinata di quella fonrita
def is_timeseries_ordered(righe):
    date = [riga[0].replace('-', '') for riga in righe if riga[1]]
    return True if date == sorted(date) else False

#Controlla se la timeseries contiene timestamp duplicati confrontando lista
#lunghezza delle date (numeriche) con la lunghezza del set creato fonrite tali
#date. Quest'ultimo nella sua creazione rimuove i duplicati
def timeseries_contains_duplicates(righe):
    date = [riga[0].replace('-', '') for riga in righe]
    return True if len(date) != len(set(date)) else False

#Calcolo le variazioni tra un mese e l'altro, fonrita una lista dei passeggeri
#di tale anno
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

    #Caso anni scambiato
    if years[0] > years[1]:
        years[0], years[1] = years[1], years[0]

    #Caso anni non consecutivi
    if years[0] != years[1] - 1:
        raise ExamException('Anni non consecutivi')

    #Caso anni equialenti
    if years[0] == years[1]:
        raise ExamException('Anni forniti sono equivalenti')

    #Caso dati forniti in input non validi, cioè non interi
    if not isinstance(years[0], int) or not isinstance(years[1], int):
        raise ExamException('Anni forniti non validi')

    #Caso anno non presente nel file csv
    anni_disponibili = [int(data[0][0:4]) for data in time_series]
    if years[0] not in anni_disponibili or years[1] not in anni_disponibili:
        raise ExamException('Anno non presente tra i dati')

    #Creo liste di passeggeri per entrambi gli anni
    monthly_passengers_1 = [month[1]
                            for month in time_series if month[0][0:4] == str(years[0])]
    monthly_passengers_2 = [month[1]
                            for month in time_series if month[0][0:4] == str(years[1])]


    #Creo le liste con le variazioni per ciascun anno
    monthly_variations_1 = get_monthly_variations(monthly_passengers_1)
    monthly_variations_2 = get_monthly_variations(monthly_passengers_2)


    similarities_list = []
    for i in range(11):
        if monthly_variations_1[i] == 'MISSING' or monthly_variations_2[i] == 'MISSING':

            similarities_list.append(False)

        elif abs(monthly_variations_1[i] - monthly_variations_2[i]) <= 2:

            similarities_list.append(True)

        else:

            similarities_list.append(False)

    return similarities_list
