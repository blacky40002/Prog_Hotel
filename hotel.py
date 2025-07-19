from stanze import *
from classi import *

"""
Definire una classe Hotel che rappresenta un hotel.
#STATO:
- stanze: dizionario con chiave il numero della stanza e valore l'oggetto stanza.
- prenotazioni: dizionario con chiave un intero e valore l'oggetto prenotazione.
- id_prenotazioni: intero progressivo inizializzato a 1 e incrementato ogni volta che una prenotazione viene aggiunta, da usare come chiave per le prenotazioni.
#METODI:
- Costruttore che inizializza le variabili di istanza. Esempio di utilizzo: h = Hotel()
- Metodo per il confronto di uguaglianza profonda tra due hotel.
- Metodo per la rappresentazione in forma di stringa dell'hotel. Rispettando il formato di esempio: "Hotel: 3 stanze (101,102,103), 2 prenotazioni." (Nota: non è necessario stampare i dettagli delle stanze e delle prenotazioni).
- Metodi specificati in seguito.
"""

"""
Inserisce una nuova stanza nell'hotel.
:param stanza oggetto di tipo Stanza da aggiungere all'hotel
:raise TypeError: se i parametri non hanno il tipo corretto
:raise ValueError: se i parametri non sono nel range di valori ammessi
"""


class Hotel:
    def __init__(self):
        self.stanze = {}
        self.prenotazioni = {}
        self.id_prenotazioni = 1

    def __eq__(self, other):
        return self.stanze == other.stanze and self.prenotazioni == other.prenotazioni and self.id_prenotazioni == other.id_prenotazioni

    def __str__(self):
        stanze_str = ", ".join(str(num) for num in sorted(self.stanze.keys()))
        return f"Hotel: {len(self.stanze)} stanze ({stanze_str}), {len(self.prenotazioni)} prenotazioni."

    def aggiungi_stanza(self, stanza):
        gestione_errori_data(stanza, Stanza)
        if stanza.get_numero_stanza() in self.stanze:
            raise ValueError("La stanza è già presente nell'hotel")
        self.stanze[stanza.get_numero_stanza()] = stanza

    """
    Prenota una stanza nell'hotel e incrementa id_prenotazioni se la prenotazione va a buon fine.
    Crea un oggetto Prenotazione con id_prenotazioni e i parametri in ingresso, e lo aggiunge al dizionario delle prenotazioni.
    :param numero_stanza: numero della stanza da prenotare
    :param data_arrivo: oggetto di tipo Data rappresentante la data di arrivo
    :param data_partenza: oggetto di tipo Data rappresentante la data di partenza
    :param nome_cliente: stringa rappresentante il nome del cliente
    :param numero_persone: intero rappresentante il numero di persone
    :return indice della prenotazione
    :raise TypeError: se i parametri non hanno il tipo corretto
    :raise ValueError: se la stanza è già occupata nelle date indicate
    :raise KeyError: se la stanza non è presente nell'hotel
    """

    def prenota(self, numero_stanza, data_arrivo, data_partenza, nome_cliente, numero_persone):
        gestione_errori_data(data_arrivo, Data)
        gestione_errori_data(data_partenza, Data)
        gestione_errori_data(nome_cliente, str)
        gestione_errori_data(numero_persone, int, 0)

        if numero_stanza not in self.stanze:
            raise KeyError(f"La stanza {numero_stanza} non esiste")

        # Controllo che data_arrivo sia precedente a data_partenza
        if data_arrivo >= data_partenza:
            raise ValueError("La data di arrivo deve essere precedente alla data di partenza")

        stanza = self.stanze[numero_stanza]
        # Supponendo che ora usi proprietà: stanza.posti invece di stanza.get_posti()
        if numero_persone > stanza.get_posti():
            raise ValueError(f"La stanza {numero_stanza} non può ospitare più di {stanza.posti} persone")

        if not self.stanza_disponibile(numero_stanza, data_arrivo, data_partenza):
            raise ValueError(f"La stanza {numero_stanza} non è disponibile per il periodo richiesto")

        id_prenotazione = self.id_prenotazioni
        self.id_prenotazioni += 1
        prenotazione = Prenotazione(id_prenotazione, numero_stanza, data_arrivo, data_partenza, nome_cliente,
                                    numero_persone)
        self.prenotazioni[id_prenotazione] = prenotazione
        return id_prenotazione

    """
    Disdice una prenotazione dell'hotel.
    :param indice della prenotazione da disdire
    :raise KeyError: se la prenotazione non è presente nell'hotel
    """

    def disdici(self, indice):
        self.controllo_indice(indice)
        del self.prenotazioni[indice]

    """
    Rimuove una stanza dall'hotel e tutte le prenotazioni relative a quella stanza.
    :param numero_stanza: numero della stanza da rimuovere
    :raise KeyError: se la stanza non è presente nell'hotel
    """

    def rimuovi_stanza(self, numero_stanza):
        gestione_errori_data(numero_stanza, int)
        if numero_stanza not in self.stanze:
            raise KeyError("La stanza non è presente nell'hotel")
        prenotazioni_da_eliminare = [
            id_pren for id_pren, pren in self.prenotazioni.items()
            # .items() prende la chiave e il valore del dizionario "spacchettandoli"
            if pren.numero_stanza == numero_stanza]
        for id_pren in prenotazioni_da_eliminare:
            del self.prenotazioni[id_pren]

        del self.stanze[numero_stanza]

    """
    Restituisce una stanza specifica dell'hotel.
    :param numero_stanza: numero della stanza da restituire
    :return: la stanza con numero_stanza
    :raise KeyError: se la stanza non è presente nell'hotel
    """

    def get_stanza(self, numero_stanza):
        try:
            gestione_errori_data(numero_stanza, int)

            if numero_stanza not in self.stanze:
                raise KeyError("La stanza non è presente nell'hotel")
            return self.stanze[numero_stanza]
        except KeyError as e:
            raise KeyError(f"La stanza {numero_stanza} non è presente nell'hotel") from e

    """
    Restituisce la lista delle stanze presenti nell'hotel.
    :return: la lista delle stanze presenti nell'hotel
    """

    def get_stanze(self):
        stanze = list(self.stanze.values())
        if not stanze:
            raise ValueError("Nessuna stanza presente nell'hotel")
        return stanze

    """
    Restituisce la lista delle stanze per tipo passato presenti nell'hotel.
    :param tipo: stringa rappresentante il tipo di stanza da cercare
    :return: la lista delle stanze per tipo passato presenti nell'hotel
    """

    def get_stanze_tipo(self, tipo):
        if tipo not in ["Singola", "Doppia", "Suite"]:
            raise ValueError("Tipo stanza non valido")
        return [stanza for stanza in self.stanze.values() if stanza.get_tipo_stanza() == tipo]

    """
    Restituisce la lista delle prenotazioni presenti nell'hotel.
    :return: la lista delle prenotazioni presenti nell'hotel
    """

    def get_prenotazioni(self):
        return list(self.prenotazioni.values())

    """
    Restituisce una prenotazione specifica dell'hotel.
    :param indice: indice della prenotazione da restituire
    :return: la prenotazione con indice
    :raise KeyError: se la prenotazione non è presente nell'hotel
    """

    def get_prenotazione(self, indice):
        gestione_errori_data(indice, int)
        self.controllo_indice(indice)
        return self.prenotazioni[indice]

    """
    Restituisce la lista delle prenotazioni presenti nell'hotel in una data specifica.
    :param data: data da cercare
    :return: la lista delle prenotazioni presenti nell'hotel in una data specifica
    :raise TypeError: se data non è un oggetto di tipo Data
    """

    def get_prenotazioni_data(self, data):
        return [prenotazione for prenotazione in self.prenotazioni.values()
                if prenotazione.data_arrivo <= data <= prenotazione.data_partenza]

    """
    Restituisce il prezzo di una prenotazione specifica ottenuto dal prezzo della stanza per il numero di persone.
    :param indice: indice della prenotazione da cercare
    :return: il prezzo della prenotazione con indice
    :raise KeyError: se la prenotazione non è presente nell'hotel
    """

    def prezzo_prenotazione(self, indice):
        gestione_errori_data(indice, int)
        self.controllo_indice(indice)
        pren = self.prenotazioni[indice]
        notti = pren.data_partenza - pren.data_arrivo
        stanza = self.stanze[pren.numero_stanza]
        # calcolo prezzo della stanza per 'notti'
        prezzo_stanza = stanza.calcola_prezzo(notti)
        # moltiplico per il numero di persone
        return prezzo_stanza * pren.numero_persone

    """
    Restituisce la lista delle prenotazioni presenti nell'hotel per un cliente specifico.
    :param cliente: nome del cliente da cercare
    :return: la lista delle prenotazioni presenti nell'hotel per un cliente specifico
    """

    def get_prenotazioni_cliente(self, cliente):
        gestione_errori_data(cliente, str)
        prenotazioni_cliente = [prenotazione for prenotazione in self.prenotazioni.values() if
                                prenotazione.nome_cliente == cliente]
        if not prenotazioni_cliente:
            raise ValueError("Nessuna prenotazione per questo cliente")
        return prenotazioni_cliente

    """
    Restituisce la lista delle stanze libere nell'hotel in una data specifica.
    :param data: data da cercare
    :return: la lista delle stanze libere nell'hotel in una data specifica
    :raise TypeError: se data non è un oggetto di tipo Data
    """

    def get_stanze_libere(self, data):
        gestione_errori_data(data, Data)
        stanze_libere = []
        for stanza in self.stanze.values():
            if self.stanza_disponibile(stanza.numero_stanza, data, data):
                stanze_libere.append(stanza)
        return stanze_libere

    """
    Restituisce la lista delle prenotazioni presenti nell'hotel per un tipo di stanza specifico.
    :param tipo_stanza: stringa rappresentante il tipo di stanza da cercare
    :return: la lista delle prenotazioni presenti nell'hotel per un tipo di stanza specifico
    """

    def get_prenotazioni_tipo_stanza(self, tipo_stanza):
        tipo_stanza = tipo_stanza.capitalize()
        return [prenotazione for prenotazione in self.prenotazioni.values()
                if self.stanze[prenotazione.numero_stanza].get_tipo_stanza() == tipo_stanza]

    def get_stanze_sopra_prezzo(self, numero_notti, prezzo):
        gestione_errori_data(numero_notti, int)
        prezzo = float(prezzo)
        if prezzo <= 1:
            raise ValueError("Il prezzo deve essere maggiore di 1")
        stanze_sopra_prezzo = []
        for stanza in self.stanze.values():
            if stanza.calcola_prezzo(numero_notti) > prezzo:
                stanze_sopra_prezzo.append(stanza)
        return stanze_sopra_prezzo

    """
    Restituisce il numero totale di persone presenti nell'hotel in una data specifica.
    :param data: data da cercare
    :return: il numero totale di persone presenti nell'hotel in una data specifica
    :raise TypeError: se data non è un oggetto di tipo Data
    """

    def get_numero_persone_data(self, data):
        gestione_errori_data(data, Data)
        data = Data(data.giorno, data.mese)
        persone_presenti = 0
        for prenotazione in self.prenotazioni.values():
            if prenotazione.data_arrivo <= data and prenotazione.data_partenza >= data:
                persone_presenti += prenotazione.numero_persone
        return persone_presenti

    """
    Salva lo stato dell'hotel su un file. Le eccezioni non devono essere gestite in questo metodo.
    :param nomefile: nome del file su cui salvare lo stato dell'hotel
        """

    def salva(self, nomefile):
        with open(nomefile, 'w', encoding='utf-8') as file:
            file.write("Hotel\n")
            # Salvataggio delle stanze
            for stanza in self.stanze.values():
                tipo = stanza.get_tipo_stanza()
                file.write(f"{tipo},{stanza.get_numero_stanza()},{stanza.get_posti()},{stanza.get_prezzo_base()}\n")
            # Salvataggio delle prenotazioni
            for prenotazione in self.prenotazioni.values():
                file.write(
                    f"{prenotazione.id_prenotazione},{prenotazione.numero_stanza},{prenotazione.data_arrivo},"
                    f"{prenotazione.data_partenza},{prenotazione.nome_cliente},{prenotazione.numero_persone}\n"
                )

    """
    Carica lo stato dell'hotel da un file e sostituisce lo stato corrente se il caricamento va a buon fine. Le eccezioni non devono essere gestite in questo metodo.
    :param nomefile: nome del file da cui caricare lo stato dell'hotel
    :raise ValueError: se il file non è nel formato corretto (es. se non è presente il nome dell'hotel)
    """

    def carica(self, nomefile):
        with open(nomefile, 'r', encoding='utf-8') as file:
            righe = file.readlines()
            if not righe or righe[0].strip() != "Hotel":
                raise ValueError("Formato file non valido, manca l'intestazione 'Hotel'")

            # Pulisco lo stato attuale dell'hotel
            nuovo_stanze = {}
            nuovo_prenotazioni = {}

            # Processo ogni riga
            for riga in righe[1:]:  # saltiamo la prima riga
                riga = riga.strip()
                if not riga:
                    continue

                parti = riga.split(',')

                # Se è una stanza (formato: Tipo,Numero,Posti,Prezzo)
                if len(parti) == 4:
                    tipo, numero, posti, prezzo = parti
                    numero = int(numero)
                    posti = int(posti)
                    prezzo = float(prezzo)

                    # Controllo doppioni
                    if numero in nuovo_stanze:
                        raise ValueError(f"Stanza duplicata trovata nel file: stanza numero {numero}")

                    if tipo == "Singola":
                        nuovo_stanze[numero] = Singola(numero, prezzo)
                    elif tipo == "Doppia":
                        nuovo_stanze[numero] = Doppia(numero, prezzo)
                    elif tipo == "Suite":
                        nuovo_stanze[numero] = Suite(numero, posti, ["TV", "Frigo"], prezzo)
                    else:
                        raise ValueError(f"Tipo di stanza non riconosciuto: {tipo}")

                # Se è una prenotazione (formato: ID,NumeroStanza,DataArrivo,DataPartenza,NomeCliente,NumeroPersone)
                elif len(parti) == 6:
                    id_pren, num_stanza, data_arr, data_part, nome, persone = parti
                    id_pren = int(id_pren)
                    num_stanza = int(num_stanza)
                    persone = int(persone)
                    data_arrivo, data_partenza = Hotel.parsing_date(data_arr, data_part)
                    # Parsing delle date

                    # Controllo doppioni prenotazioni
                    if id_pren in nuovo_prenotazioni:
                        raise ValueError(f"Prenotazione duplicata trovata nel file: ID prenotazione {id_pren}")

                    nuovo_prenotazioni[id_pren] = Prenotazione(id_pren, num_stanza, data_arrivo, data_partenza, nome,
                                                               persone)

                else:
                    raise ValueError("Il file contiene una riga con formato non riconosciuto")

            # Se siamo arrivati qui sovrascriviamo i dati attuali
            self.stanze = nuovo_stanze
            self.prenotazioni = nuovo_prenotazioni
            self.id_prenotazioni = max([0] + list(nuovo_prenotazioni.keys())) + 1

    def stanza_disponibile(self, numero_stanza, data_arrivo, data_partenza):
        """
        Verifica se la stanza (identificata da numero_stanza) è disponibile
        per l'intervallo [data_arrivo, data_partenza].
        """
        for pren in self.prenotazioni.values():
            if pren.numero_stanza == numero_stanza:

                if data_arrivo <= pren.data_partenza and data_partenza >= pren.data_arrivo:
                    return False
        return True

    @staticmethod  # metodo statico che invece di essere usato sull'istanza della classe attuale, permette di essere chiamato direttamente
    def parsing_date(data_arr, data_part):
        try:
            g_arr, m_arr = map(int, data_arr.split('/'))
            g_part, m_part = map(int, data_part.split('/'))

            data_arrivo = Data(g_arr, m_arr)
            data_partenza = Data(g_part, m_part)
            return data_arrivo, data_partenza
        except ValueError:
            raise ValueError("Inserire solo numeri nel formato gg/mm (es: 01/05)")

    def controllo_indice(self, indice):
        if indice not in self.prenotazioni:
            raise KeyError("La prenotazione non è presente nell'hotel")
