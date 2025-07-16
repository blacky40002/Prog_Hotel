#!/usr/bin/env python3
"""
Test avanzati per il sistema di gestione hotel
Questi test coprono scenari più complessi e casi limite
"""

from testMy import testEqual, testEccezione
from hotel import Hotel
from stanze import Singola, Doppia, Suite
from classi import Data, Prenotazione

def test_data_avanzati():
    """Test avanzati per la classe Data"""
    risultati = []
    print("========> Test avanzati Data")

    # Test 1: Date al limite dei mesi
    try:
        d_fine_gen = Data(31, 1)
        d_inizio_feb = Data(1, 2)
        risultati.append(testEqual(d_inizio_feb - d_fine_gen, 1))
        print("✓ Test differenza fine gennaio - inizio febbraio")
    except Exception as e:
        print(f"✗ Errore test date limite: {e}")
        risultati.append(False)

    # Test 2: Febbraio non bisestile
    try:
        Data(29, 2)  # Dovrebbe fallire
        risultati.append(False)
        print("✗ Febbraio 29 dovrebbe essere invalido")
    except:
        risultati.append(True)
        print("✓ Febbraio 29 correttamente rifiutato")

    # Test 3: Date uguali
    try:
        d1 = Data(15, 6)
        d2 = Data(15, 6)
        risultati.append(testEqual(d1 == d2, True))
        risultati.append(testEqual(d1 <= d2, True))
        risultati.append(testEqual(d1 >= d2, True))
        print("✓ Test date uguali")
    except Exception as e:
        print(f"✗ Errore test date uguali: {e}")
        risultati.append(False)

    # Test 4: Confronti complessi
    try:
        d_estate = Data(15, 7)
        d_inverno = Data(15, 1)
        risultati.append(testEqual(d_inverno < d_estate, True))
        risultati.append(testEqual(d_estate > d_inverno, True))
        print("✓ Test confronti stagionali")
    except Exception as e:
        print(f"✗ Errore confronti: {e}")
        risultati.append(False)

    # Test 5: Differenze tra mesi distanti
    try:
        d_inizio_anno = Data(1, 1)
        d_fine_anno = Data(31, 12)
        differenza = d_fine_anno - d_inizio_anno
        risultati.append(testEqual(differenza, 364))  # 2025 non è bisestile
        print("✓ Test differenza inizio-fine anno")
    except Exception as e:
        print(f"✗ Errore differenza anno: {e}")
        risultati.append(False)

    return risultati

def test_stanze_avanzati():
    """Test avanzati per le classi Stanza"""
    risultati = []
    print("========> Test avanzati Stanze")

    # Test 1: Suite con molti extra
    try:
        suite_lusso = Suite(999, 6, ["TV", "Frigo", "Jacuzzi", "Sauna", "Vista mare", "Balcone"], 500.0)
        prezzo_1_notte = suite_lusso.calcola_prezzo(1)
        # (500 * 1.5) + (6 * 10) = 750 + 60 = 810
        risultati.append(testEqual(prezzo_1_notte, 810.0))
        print("✓ Suite di lusso con 6 extra")
    except Exception as e:
        print(f"✗ Errore suite lusso: {e}")
        risultati.append(False)

    # Test 2: Doppia con prezzo alto
    try:
        doppia_costosa = Doppia(888, 300.0)
        prezzo_settimana = doppia_costosa.calcola_prezzo(7)
        # 300 * 1.2 * 7 = 2520
        risultati.append(testEqual(prezzo_settimana, 2520.0))
        print("✓ Doppia costosa per una settimana")
    except Exception as e:
        print(f"✗ Errore doppia costosa: {e}")
        risultati.append(False)

    # Test 3: Singola economica
    try:
        singola_economica = Singola(111, 25.0)
        prezzo_mese = singola_economica.calcola_prezzo(30)
        risultati.append(testEqual(prezzo_mese, 750.0))
        print("✓ Singola economica per un mese")
    except Exception as e:
        print(f"✗ Errore singola economica: {e}")
        risultati.append(False)

    # Test 4: Errori suite
    try:
        Suite(100, 3, ["TV"], 100.0)  # Meno di 4 posti
        risultati.append(False)
        print("✗ Suite con 3 posti dovrebbe essere invalida")
    except ValueError:
        risultati.append(True)
        print("✓ Suite con posti insufficienti correttamente rifiutata")
    except Exception as e:
        print(f"✗ Errore imprevisto: {e}")
        risultati.append(False)

    # Test 5: Suite senza extra
    try:
        Suite(100, 4, [], 100.0)  # Lista extra vuota
        risultati.append(False)
        print("✗ Suite senza extra dovrebbe essere invalida")
    except ValueError:
        risultati.append(True)
        print("✓ Suite senza extra correttamente rifiutata")
    except Exception as e:
        print(f"✗ Errore imprevisto: {e}")
        risultati.append(False)

    return risultati

def test_prenotazioni_complesse():
    """Test per scenari di prenotazione complessi"""
    risultati = []
    print("========> Test prenotazioni complesse")

    hotel = Hotel()

    # Aggiungi stanze di test
    hotel.aggiungi_stanza(Singola(101, 50.0))
    hotel.aggiungi_stanza(Doppia(102, 80.0))
    hotel.aggiungi_stanza(Suite(103, 4, ["TV", "Frigo", "Jacuzzi"], 200.0))

    # Test 1: Prenotazioni consecutive senza sovrapposizione
    try:
        id1 = hotel.prenota(101, Data(1, 1), Data(5, 1), "Cliente1", 1)
        id2 = hotel.prenota(101, Data(5, 1), Data(10, 1), "Cliente2", 1)  # Stesso giorno fine/inizio
        risultati.append(testEqual(id1, 1))
        risultati.append(testEqual(id2, 2))
        print("✓ Prenotazioni consecutive")
    except Exception as e:
        print(f"✗ Errore prenotazioni consecutive: {e}")
        risultati.append(False)
        risultati.append(False)

    # Test 2: Prenotazione lunga
    try:
        id3 = hotel.prenota(102, Data(1, 2), Data(28, 2), "ClienteLungo", 2)
        prezzo = hotel.prezzo_prenotazione(id3)
        # 27 notti * (80 * 1.2) * 2 persone = 27 * 96 * 2 = 5184
        risultati.append(testEqual(prezzo, 5184.0))
        print("✓ Prenotazione lunga (27 notti)")
    except Exception as e:
        print(f"✗ Errore prenotazione lunga: {e}")
        risultati.append(False)

    # Test 3: Sovrapposizione parziale
    try:
        hotel.prenota(103, Data(15, 3), Data(25, 3), "Cliente3", 3)
        hotel.prenota(103, Data(20, 3), Data(30, 3), "Cliente4", 2)  # Dovrebbe fallire
        risultati.append(False)
        print("✗ Sovrapposizione dovrebbe essere rifiutata")
    except ValueError:
        risultati.append(True)
        print("✓ Sovrapposizione correttamente rifiutata")
    except Exception as e:
        print(f"✗ Errore imprevisto: {e}")
        risultati.append(False)

    # Test 4: Troppe persone per stanza
    try:
        hotel.prenota(101, Data(1, 4), Data(5, 4), "FamigliaNumerosa", 5)  # Singola per 5 persone
        risultati.append(False)
        print("✗ Troppe persone dovrebbe essere rifiutato")
    except ValueError:
        risultati.append(True)
        print("✓ Troppe persone correttamente rifiutate")
    except Exception as e:
        print(f"✗ Errore imprevisto: {e}")
        risultati.append(False)

    return risultati

def test_hotel_gestione_avanzata():
    """Test avanzati per la gestione dell'hotel"""
    risultati = []
    print("========> Test gestione hotel avanzata")

    hotel = Hotel()

    # Setup iniziale
    hotel.aggiungi_stanza(Singola(201, 60.0))
    hotel.aggiungi_stanza(Doppia(202, 90.0))
    hotel.aggiungi_stanza(Suite(203, 5, ["TV", "Frigo"], 250.0))

    # Aggiungi alcune prenotazioni
    hotel.prenota(201, Data(10, 6), Data(15, 6), "Alice", 1)
    hotel.prenota(202, Data(12, 6), Data(18, 6), "Bob", 2)
    hotel.prenota(203, Data(14, 6), Data(20, 6), "Charlie", 4)

    # Test 1: Stanze libere in data specifica
    try:
        libere_prima = hotel.get_stanze_libere(Data(5, 6))  # Prima di tutte le prenotazioni
        libere_durante = hotel.get_stanze_libere(Data(15, 6))  # Durante le prenotazioni
        libere_dopo = hotel.get_stanze_libere(Data(25, 6))  # Dopo tutte le prenotazioni

        risultati.append(testEqual(len(libere_prima), 3))
        risultati.append(testEqual(len(libere_durante), 0))
        risultati.append(testEqual(len(libere_dopo), 3))
        print("✓ Test stanze libere in date diverse")
    except Exception as e:
        print(f"✗ Errore stanze libere: {e}")
        risultati.append(False)
        risultati.append(False)
        risultati.append(False)

    # Test 2: Numero persone in data specifica
    try:
        persone_15_giugno = hotel.get_numero_persone_data(Data(15, 6))
        # Alice (1) + Bob (2) + Charlie (4) = 7
        risultati.append(testEqual(persone_15_giugno, 7))
        print("✓ Conteggio persone presenti")
    except Exception as e:
        print(f"✗ Errore conteggio persone: {e}")
        risultati.append(False)

    # Test 3: Prenotazioni per cliente
    try:
        # Aggiungi altra prenotazione per Bob su date che non si sovrappongono
        hotel.prenota(201, Data(1, 7), Data(5, 7), "Bob", 1)  # Tornato a 201 ma con date diverse
        prenotazioni_bob = hotel.get_prenotazioni_cliente("Bob")
        risultati.append(testEqual(len(prenotazioni_bob), 2))
        print("✓ Prenotazioni multiple per cliente")
    except Exception as e:
        print(f"✗ Errore prenotazioni cliente: {e}")
        risultati.append(False)

    # Test 4: Rimozione stanza con prenotazioni
    try:
        num_prenotazioni_prima = len(hotel.get_prenotazioni())
        hotel.rimuovi_stanza(202)  # Stanza con prenotazione di Bob
        num_prenotazioni_dopo = len(hotel.get_prenotazioni())

        # Dovrebbe aver rimosso una prenotazione
        risultati.append(testEqual(num_prenotazioni_dopo, num_prenotazioni_prima - 1))
        print("✓ Rimozione stanza con prenotazioni")
    except Exception as e:
        print(f"✗ Errore rimozione stanza: {e}")
        risultati.append(False)

    return risultati

def test_casi_limite():
    """Test per casi limite e edge cases"""
    risultati = []
    print("========> Test casi limite")

    # Test 1: Hotel vuoto
    try:
        hotel_vuoto = Hotel()
        hotel_vuoto.get_stanze()
        risultati.append(False)
        print("✗ Hotel vuoto dovrebbe generare errore")
    except ValueError:
        risultati.append(True)
        print("✓ Hotel vuoto correttamente gestito")
    except Exception as e:
        print(f"✗ Errore imprevisto: {e}")
        risultati.append(False)

    # Test 2: Prenotazione di 1 notte
    try:
        hotel = Hotel()
        hotel.aggiungi_stanza(Singola(301, 100.0))
        id_pren = hotel.prenota(301, Data(1, 8), Data(2, 8), "Veloce", 1)
        prezzo = hotel.prezzo_prenotazione(id_pren)
        risultati.append(testEqual(prezzo, 100.0))  # 1 notte * 100 * 1 persona
        print("✓ Prenotazione di una sola notte")
    except Exception as e:
        print(f"✗ Errore prenotazione breve: {e}")
        risultati.append(False)

    # Test 3: Date al confine dell'anno
    try:
        data_fine_anno = Data(31, 12)
        data_inizio_anno = Data(1, 1)
        # Non dovrebbe essere possibile prenotare a cavallo dell'anno
        hotel.prenota(301, data_fine_anno, data_inizio_anno, "Capodanno", 1)
        risultati.append(False)
        print("✗ Prenotazione a cavallo anno dovrebbe fallire")
    except ValueError:
        risultati.append(True)
        print("✓ Prenotazione a cavallo anno correttamente rifiutata")
    except Exception as e:
        print(f"✗ Errore imprevisto: {e}")
        risultati.append(False)

    # Test 4: Stanze con prezzi molto alti
    try:
        suite_di_lusso = Suite(999, 10, ["TV", "Frigo", "Jacuzzi", "Sauna", "Vista panoramica"], 1000.0)
        prezzo_notte = suite_di_lusso.calcola_prezzo(1)
        # (1000 * 1.5) + (5 * 10) = 1500 + 50 = 1550
        risultati.append(testEqual(prezzo_notte, 1550.0))
        print("✓ Suite di lusso con prezzo alto")
    except Exception as e:
        print(f"✗ Errore suite lusso: {e}")
        risultati.append(False)

    return risultati

def test_salvataggio_caricamento():
    """Test per salvataggio e caricamento dell'hotel"""
    risultati = []
    print("========> Test salvataggio/caricamento")

    # Test 1: Salvataggio e caricamento completo
    try:
        hotel_originale = Hotel()
        hotel_originale.aggiungi_stanza(Singola(401, 75.0))
        hotel_originale.aggiungi_stanza(Doppia(402, 120.0))
        hotel_originale.aggiungi_stanza(Suite(403, 6, ["TV", "Frigo", "Jacuzzi"], 300.0))

        hotel_originale.prenota(401, Data(1, 9), Data(5, 9), "TestCliente", 1)
        hotel_originale.prenota(402, Data(10, 9), Data(15, 9), "AltroCliente", 2)

        # Salva
        hotel_originale.salva("test_hotel.txt")

        # Carica in nuovo hotel
        hotel_caricato = Hotel()
        hotel_caricato.carica("test_hotel.txt")

        # Verifica uguaglianza
        risultati.append(testEqual(hotel_originale, hotel_caricato))
        print("✓ Salvataggio e caricamento completo")

    except Exception as e:
        print(f"✗ Errore salvataggio/caricamento: {e}")
        risultati.append(False)

    # Test 2: File corrotto
    try:
        hotel_test = Hotel()
        hotel_test.carica("file_inesistente.txt")
        risultati.append(False)
        print("✗ File inesistente dovrebbe generare errore")
    except:
        risultati.append(True)
        print("✓ File inesistente correttamente gestito")

    return risultati

def main():
    """Esegue tutti i test avanzati"""
    print("=== INIZIO TEST AVANZATI ===\n")

    tutti_risultati = []

    # Esegui tutti i test
    tutti_risultati.extend(test_data_avanzati())
    tutti_risultati.extend(test_stanze_avanzati())
    tutti_risultati.extend(test_prenotazioni_complesse())
    tutti_risultati.extend(test_hotel_gestione_avanzata())
    tutti_risultati.extend(test_casi_limite())
    tutti_risultati.extend(test_salvataggio_caricamento())

    # Risultati finali
    test_passati = sum(tutti_risultati)
    test_totali = len(tutti_risultati)
    test_falliti = test_totali - test_passati

    print(f"\n=== RISULTATI FINALI ===")
    print(f"Test totali: {test_totali}")
    print(f"Test passati: {test_passati}")
    print(f"Test falliti: {test_falliti}")

    if test_falliti == 0:
        print("🎉 TUTTI I TEST SONO PASSATI!")
    else:
        print(f"⚠️  {test_falliti} test hanno fallito")
        test_falliti_indici = [i+1 for i, x in enumerate(tutti_risultati) if not x]
        print(f"Indici test falliti: {test_falliti_indici}")

    return test_falliti == 0

if __name__ == "__main__":
    main()
