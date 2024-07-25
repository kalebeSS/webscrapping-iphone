from bs4 import BeautifulSoup
import requests
import pandas as pd
import schedule
import time

class Robot:
    def __init__(self) -> None:
        self.site = 'https://lista.mercadolivre.com.br/iphone-12#D[A:iphone%2012]'
        self.response = requests.get(self.site)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')

    def retorna_telefones(self):
        telefones = self.soup.find_all('h2', class_='ui-search-item__title')
        valores = self.soup.find_all('span', class_='andes-money-amount__fraction')

        resultados = []

        for telefone, valor in zip(telefones, valores):
            telefone_nome = telefone.text
            valor_telefone = valor.text.replace('.', '')

            try:
                valor_telefone = int(valor_telefone)
                if 2000 < valor_telefone < 2500:
                    resultados.append((telefone_nome, valor_telefone))
            except ValueError:
                continue

        return resultados

    def cria_tabela(self):
        dados = self.retorna_telefones()

        if dados:
            df = pd.DataFrame(dados, columns=['Telefone', 'Valor'])
            df.to_csv('Telefones.csv', index=False)
            print("Arquivo CSV atualizado.")
        else:
            print("Nenhum dado encontrado no intervalo especificado.")

def tarefa():
    robô = Robot()
    robô.cria_tabela()

schedule.every(20).minutes.do(tarefa)

print("Agendamento iniciado. A tarefa será executada a cada 20 minutos.")

while True:
    schedule.run_pending()
    time.sleep(1)

