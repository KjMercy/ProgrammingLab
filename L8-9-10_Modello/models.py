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
        somma_incrementi = 0

        for i, item in enumerate(data):
            if i < len(data)-1:
                somma_incrementi += data[i+1] - item

        return somma_incrementi / (len(data)-1)  # ritorna l'incremento medio


data = [50, 52, 60]
prediction = data[-1] + IncrementModel().predict(data)
print(f'Mesi precedenti: {data}')
print(f'Previsione: {prediction}')
