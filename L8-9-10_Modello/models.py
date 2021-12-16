from matplotlib import pyplot


def incrementoMedioInLista(lista):
    somma_incrementi = 0

    for i, item in enumerate(lista):
        if i < len(lista)-1:
            somma_incrementi += lista[i+1] - item

    return somma_incrementi / (len(lista)-1)  # ritorna l'incremento medio


class Model():
    '''Modello base, astratto, che deve essere esteso'''

    def fit(self, data):
        # Fit non implementato nella classe base
        raise NotImplementedError('Metodo non implementato')

    def predict(self, data):
        # Predict non implementato nella classe base
        raise NotImplementedError('Metodo non implementato')


class IncrementModel(Model):

    # data è una lista di valori per gli n mesi, in questo caso, passati
    def predict(self, data):
        """Ritorna l'incremento (positivo o negativo) che è previsto avverrà nel mese successivo"""
        return data[-1] + incrementoMedioInLista(data)


# Esercizio Lezione 8
# data = [50, 52, 60]
# print(f'Mesi precedenti: {data}')
# print(f'Previsione: {IncrementModel().predict(data)}')


class FitIncrementModel(IncrementModel):

    def __init__(self):
        self.global_avg_increment = None

    def fit(self, data):
        self.global_avg_increment = incrementoMedioInLista(data)

    def predict(self, data):
        if self.global_avg_increment != None:
            return data[-1] + (self.global_avg_increment + incrementoMedioInLista(data[-3:]))/2
        else:
            return super().predict(data[-3:])


data = [8, 19, 31, 41, 50, 52, 60]
modello = FitIncrementModel()
prediction = modello.predict(data)
print(f'Senza fit: {prediction}')
modello.fit(data[0:-3])
prediction = modello.predict(data)
print(f'Con fit: {prediction}')


# converto prima tutti gli elementi della lista in float perchè altrimetni si lamenta quando aggiunge la prediction
data = [float(i) for i in data]
pyplot.plot(data + [prediction], color='tab:red')
pyplot.plot(data, color='tab:blue')
pyplot.show()
