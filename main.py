# Script di test Progetto recupero 622AA 2024/25
from testMy import *
from hotel import Hotel
from stanze import Singola, Doppia, Suite
from classi import Data, Prenotazione

x = Hotel()


def controllo():
    risultati = []
    print("==========> Inizio nuovo test <=============")

    ### test su Data
    try:
        err = 1
        d1 = Data(1, 1)
        err += 1
        d2 = Data(1, 2)
        risultati.append(True)
        print("==========> Date create correttamente")
    except Exception as e:
        print(f"Errore creazione data n {err}", e)
        return risultati

    # test metodi di Data
    # test da 1 a 9
    risultati.append(testEqual(d1, Data(1, 1)))
    risultati.append(testEqual(d1 == d2, False))
    risultati.append(testEqual(d1 < d2, True))
    risultati.append(testEqual(d1 > d2, False))
    risultati.append(testEqual(d1 <= Data(1, 1), True))
    risultati.append(testEqual(d1 - Data(1, 1), 0))
    risultati.append(testEqual(d2 - d1, 31))
    risultati.append(testEqual(d1 - d2, d2 - d1))
    risultati.append(testEqual(str(d2), "1/2"))

    ### Test su Prenotazione
    # test creazione prenotazioni
    try:
        err = 1
        p1 = Prenotazione(1, 101, d1, d2, "Tizio", 1)
        err += 1
        p2 = Prenotazione(2, 102, d1, d2, "Caio", 1)
        err += 1
        p3 = Prenotazione(3, 109, Data(2, 1), Data(3, 1), "Sempronio", 3)
        err += 1
        p4 = Prenotazione(4, 103, Data(1, 1), Data(2, 1), "Sempronio", 3)
        print("==========> Prenotazioni create correttamente")
    except Exception as e:
        print(f"Errore creazione prenotazione n {err}", e)
        return risultati

    if not all(risultati):
        print("Errori nella classe Prenotazione")
        return risultati

    ### Test su stanze
    # test creazione stanze
    try:
        err = 1
        s0 = Singola(100, 50.0)
        err += 1
        s1 = Singola(101, 50.0)
        err += 1
        s2 = Doppia(102, 50.0)
        err += 1
        s3 = Suite(103, 4, ["TV", "Frigo"], 200.0)
        print("==========> Stanze create correttamente")
    except Exception as e:
        print(f"Errore creazione stanza n {err}", e)
        return risultati

    # test altri metodi di Stanza
    # test da 10 a 15
    risultati.append(testEqual(s1 == s2, False))
    risultati.append(testEqual(str(s0), "Singola 100, 1 posto"))
    risultati.append(testEqual(str(s3), "Suite 103, 4 posti, con TV, Frigo"))
    risultati.append(testEqual(s0.calcola_prezzo(1), 50.0))
    risultati.append(testEqual(s3.calcola_prezzo(1), 320.0))

    ### test su Hotel (possono essere rilevati errori anche nelle classi precedenti che influenzano Hotel)
    # aggiungi stanze
    # test da 16 a 20
    x.aggiungi_stanza(s0)
    risultati.append(testEqual(x.get_stanza(100), s0))
    x.aggiungi_stanza(s1)
    risultati.append(testEqual(x.get_stanza(101), s1))
    x.aggiungi_stanza(s2)
    risultati.append(testEqual(x.get_stanza(102), s2))
    x.aggiungi_stanza(s3)
    risultati.append(testEqual(x.get_stanza(103), s3))
    risultati.append(testEccezione(len(risultati) + 1, TypeError, x.aggiungi_stanza, "A"))

    # get stanze
    # test da 21 a 24
    risultati.append(testEqual(x.get_stanze(), [s0, s1, s2, s3]))
    risultati.append(testEqual(x.get_stanze_tipo("Singola"), [s0, s1]))
    risultati.append(testEqual(x.get_stanze_sopra_prezzo(1, 55), [s2, s3]))
    risultati.append(testEqual(x.get_stanze_libere(d1), [s0, s1, s2, s3]))

    # meteodi prenotazioni
    # test da 25 a 35
    risultati.append(testEqual(x.prenota(101, d1, d2, "Tizio", 1), 1))
    risultati.append(testEqual(x.prenota(102, d1, d2, "Caio", 1), 2))
    risultati.append(testEqual(x.prenota(103, d1, Data(2, 1), "Sempronio", 3), 3))
    x.disdici(3)
    risultati.append(testEqual(x.prenota(103, d1, Data(2, 1), "Sempronio", 3), 4))
    risultati.append(testEqual(x.get_prenotazioni(), [p1, p2, p4]))
    risultati.append(testEqual(x.prenota(103, Data(1, 3), Data(1, 4), "Sempronio", 1), 5))
    risultati.append(testEqual(x.get_prenotazione(4), p4))
    risultati.append(testEqual(x.get_prenotazioni_data(Data(10, 1)), [p1, p2]))
    risultati.append(testEqual(x.get_prenotazioni_cliente("Sempronio"),
                               [p4, Prenotazione(5, 103, Data(1, 3), Data(1, 4), "Sempronio", 1)]))
    risultati.append(testEqual(x.get_prenotazioni_tipo_stanza("Singola"), [p1]))
    risultati.append(testEqual(x.get_numero_persone_data(Data(10, 1)), 2))

    # test prenotazioni errate
    # test da 36 a 41
    risultati.append(testEccezione(len(risultati) + 1, KeyError, x.prenota, 104, d1, d2, "Tizio", 1))
    risultati.append(testEccezione(len(risultati) + 1, ValueError, x.prenota, 103, d1, d2, "Tizio", 1))
    risultati.append(testEccezione(len(risultati) + 1, ValueError, x.prenota, 102, d1, d2, "Tizio", 10))
    risultati.append(testEccezione(len(risultati) + 1, ValueError, x.prenota, 101, Data(1, 1), Data(10, 1), "Tizio", 1))
    risultati.append(testEccezione(len(risultati) + 1, ValueError, x.prenota, 103, Data(1, 4), Data(10, 4), "Tizio", 1))
    risultati.append(testEccezione(len(risultati) + 1, ValueError, x.prenota, 103, Data(25, 2), Data(1, 3), "Tizio", 1))

    # test prezzi
    # test da 42 a 45
    risultati.append(testEqual(x.prezzo_prenotazione(1), 1550))
    risultati.append(testEqual(x.prezzo_prenotazione(2), 1860))
    risultati.append(testEqual(x.prezzo_prenotazione(4), 960))
    risultati.append(testEqual(x.prezzo_prenotazione(5), 9920))

    # test eq, str, salva, carica
    # test da 46 a 49
    risultati.append(testEqual(x, x))
    risultati.append(testEqual(str(x), "Hotel: 4 stanze (100, 101, 102, 103), 4 prenotazioni."))
    x.salva("hotel.txt")
    y = Hotel()
    y.aggiungi_stanza(Singola(100, 50.0))
    y.aggiungi_stanza(Singola(101, 30.0))
    y.aggiungi_stanza(Doppia(102, 40.0))
    y.aggiungi_stanza(Doppia(103, 60.0))
    y.aggiungi_stanza(Suite(104, 6, ["TV", "Frigo", "Jacuzzi", "Panorama"], 300.0))
    y.aggiungi_stanza(Suite(105, 4, ["TV", "Frigo"], 200.0))
    y.salva("hotel_base.txt")
    y.carica("hotel.txt")
    risultati.append(testEqual(x, y))
    risultati.append(testEqual(str(x), str(y)))

    # stampa finale hotel
    print("==========> Stampa finale hotel")
    print(x)
    print()
    return risultati


# eseguo i test automatici
risultati = controllo()

# abbiamo finito ?
if all(risultati) and len(risultati) == 49:
    print("\t****Test completati -- effettuare la consegna come da README")
else:
    testFalliti = [i + 1 for i, x in enumerate(risultati) if not x]
    if len(testFalliti) > 0:
        print(f"Test falliti: {len(testFalliti)}. Indici test: {testFalliti}")
    else:
        print("Test di creazione classe falliti")
