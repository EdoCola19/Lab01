import random
from collections import defaultdict

class Domande:
    def __init__(self, file_name):
        self.domande_per_difficolta = defaultdict(list)
        self.carica_domande(file_name)

    def carica_domande(self, file_name="domande.txt"):
        try:
            with open(file_name, encoding="utf-8") as f:
                righe = [riga.strip() for riga in f.readlines()]
            for i in range(0, len(righe), 7):
                domanda = righe[i]
                difficolta = int(righe[i + 1])
                giusta = righe[i + 2]
                sbagliata1 = righe[i + 3]
                sbagliata2 = righe[i + 4]
                sbagliata3 = righe[i + 5]

                self.domande_per_difficolta[difficolta].append(
                        (domanda, giusta, sbagliata1, sbagliata2, sbagliata3))

        except FileNotFoundError:
            print("Errore: Il file non è stato trovato.")

        return self.domande_per_difficolta

    def get_domande_per_difficolta(self, livello):
        return self.domande_per_difficolta.get(livello, [])

class Game:
    def __init__(self,domande):
        self.domande = domande
        self.punteggio = 0
        self.difficolta_corrente = 0
        self.nickname = None


    def avvia(self):
        print("Il gioco ha inizio!")
        print("Inserisci la risposta corretta per avanzare e aumentare il punteggio, altrimenti perdi.")
        while True:
            domande_disponibili = self.domande.get_domande_per_difficolta(self.difficolta_corrente)

            if not domande_disponibili:
                print(f"Hai raggiunto il livello massimo di punteggio: {self.punteggio}")
                self.chiedi_nickname()
                break

            domanda, giusta,sbagliata1, sbagliata2, sbagliata3 = random.choice(domande_disponibili)
            opzioni = [giusta, sbagliata1, sbagliata2, sbagliata3]
            random.shuffle(opzioni)

            print(f"Livello {self.difficolta_corrente}) {domanda}:")
            for i, opzione in enumerate(opzioni, 1):
                print(f"        {i}. {opzione}")

            try:
                risposta = int(input("Inserisci la risposta: "))
                if opzioni[risposta -1] == giusta:
                    print("Risposta corretta! ")
                    self.punteggio +=1
                    self.difficolta_corrente +=1
                else:
                    print("Risposta Sbagliata!")
                    print(f"Il tuo punteggio è: {self.punteggio}")
                    self.chiedi_nickname()

                    break
            except (ValueError, IndexError):
                print("Errore nell'inserimento!")

    def chiedi_nickname(self):
        if self.nickname is None:
            self.nickname = input("Inserisci il tuo nickname: ")

    def output(self,nome_file):
        try:
            with open(nome_file, "a", encoding="utf-8")as file:
                file.write(f"\n{self.nickname}: {self.punteggio}")

            print("Punteggio salvato correttamente!")

        except Exception as e:
            print("Errore nel sovrascrivere il file.")







if __name__ == "__main__":
    domande = Domande("domande.txt")  # Crea l'oggetto con le domande
    gioco = Game(domande)  # Crea il gioco
    gioco.avvia()
    gioco.output("punti.txt")
