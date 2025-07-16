"""
Definire una classe Data per rappresentare una specifica data all'interno di un anno non bisestile.
#STATO:
- mappa_mesi: dizionario con chiave il numero del mese e valore il numero di giorni. Esempio: {1: 31, 2: 28, ...}. Sfruttare questa mappa per controllare la validità di una data e per calcolare la differenza tra due date.
- giorno: intero con valore compreso tra 1 e il numero di giorni del mese. 
- mese: intero con valore compreso tra 1 e 12.
Ogni volta che si modifica una di queste variabili di istanza, devono essere controllati tipo e valori e sollevate opportune eccezioni ValueError o TypeError se i parametri non sono validi.

#METODI:
- Costruttore che prende in input giorno, mese e anno e inizializza le variabili di istanza. Esempio di utilizzo: d = Data(1, 1)
- Metodi getter e setter per giorno e mese.
- Metodo per la rappresentazione in forma di stringa della data, rispettando il formato di esempio: "1/1"
- Metodo per il calcolo della differenza in giorni tra due date. Esempio di utilizzo: d2 - d1 dove d1 = Data(1, 1), d2 = Data(1, 2), risultato -> 31. Nota, d2 - d1 deve essere uguale a d1 - d2.
- Metodo per il confronto di uguaglianza tra due date.
- Metodo per il confronto di maggiore tra due date. Esempio di utilizzo: d1 < d2
- Metodo per il confronto di minore tra due date. Esempio di utilizzo: d1 > d2
- Metodo per il confronto di minore o uguale tra due date. Esempio di utilizzo: d1 <= d2
"""

class Data:
    mappa_mesi = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30,
                  12: 31}  # 2025 anno di riferimento non bisestile

    def __init__(self, giorno: int, mese: int, anno=2025):
        self._mese = None # Inizializziamo prima mese per evitare errori nel setter di giorno
        self.mese = mese
        self.giorno = giorno

    # metodi getter e setter per giorno e mese
    @property  # property ci permette di definire un metodo che può essere usato come un attributo
    def giorno(self):#qui ad esempio possiamo chiamare semplicemente data.giorno e ci chiama questo metodo, a differenza dei metodi getter e setter normali dove serve mettere Data.Getgiorno()
        return self._giorno #siccome si una la property dobbiamo fare sef._giorno e non self.giorno perchè se facessimo come nel secondo caso verrebbe chiamata la funzione ricorsivamente entrando in un loop.

    @giorno.setter  #possiamo usare il setter con lo stesso nome del getter e verrà selezionata una rispetto all'altra in base a quello che viene indicato poi tra le parentesi, per il setter dovremo mettere il valore che vogliamo assegnare, mentre per il getter non si mette nulla
    def giorno(self, valore):
        try:
            if self._mese is None:  # controllo che il mese sia stato impostato
                raise ValueError("Impossibile impostare il giorno: il mese non è ancora stato definito.")
            giorni_max = self.mappa_mesi.get(self._mese)
            gestione_errori_data(valore, int, 0, giorni_max + 1)
            self._giorno = valore
        except ValueError as e:
            raise TypeError(f"Errore nella creazione del giorno della Data con errore: {e}") from e

    @property
    def mese(self):
        return self._mese

    @mese.setter
    def mese(self, valore):
        try:
            gestione_errori_data(valore, int, 0, 13)
            self._mese = valore
        except ValueError as e:
            raise TypeError(f"Errore nella creazione del mese della Data con errore: {e}") from e

    # metodo per il calcolo della differenza in giorni tra due date
    def __sub__(self, other):#metodi che fanno l'overriding delle funzioni di stampa, in modo da poter usare la funzione print per stampare gli oggetti
        try:
            gestione_errori_data(other, Data)
            # Calcola i giorni dall'inizio dell'anno per self e other usando la mappa_mesi
            giorni_self = sum(Data.mappa_mesi[m] for m in range(1,  self.mese)) + self.giorno  # usiamo la funzione Sum per sommare i giorni dei mesi precedenti e aggiungere il giorno corrente
            giorni_other = sum(Data.mappa_mesi[m] for m in range(1, other.mese)) + other.giorno
            return abs(giorni_self - giorni_other)
        except ValueError as e:
            raise ValueError(f"Errore nel calcolo della differenza delle date con errore: {e}") from e

    # metodo per il confronto di uguaglianza tra due date
    def __eq__(self, other):
        try:
            gestione_errori_data(other, Data)
            return self._giorno == other.giorno and self._mese == other.mese
        except ValueError as e:
            raise TypeError(f"Errore nel confronto di uguaglianze delle date con errore: {e}") from e

    # metodo per il confronto di minore tra due date
    def __lt__(self, other):
        try:
            gestione_errori_data(other, Data)
            return (self._mese, self._giorno) < (other.mese, other.giorno)  # ritorna un valore booleano
        except ValueError as e:

            raise TypeError(f"Errore nel confronto di minore tra due date con errore: {e}") from e

    # metodo per il confronto di maggiore
    def __gt__(self, other):
        try:
            gestione_errori_data(other, Data)
            return (self.mese, self.giorno) > (other.mese, other.giorno)  # ritorna un valore booleano
        except ValueError as e:
            raise TypeError(f"Errore nel confronto di maggiore tra due date con errore: {e}") from e

    # metodo per il confronto di minore o uguale tra due date
    def __le__(self, other):
        try:
            gestione_errori_data(other, Data)
            return (self._mese, self._giorno) <= (other._mese, other._giorno)  # ritorna un valore booleano
        except ValueError as e:
            raise TypeError(f"Errore nel confronto di minore o uguale tra due date con errore: {e}") from e

    def __str__(self):
        return f"{self._giorno}/{self._mese}"



"""
Definire una classe Prenotazione per rappresentare una prenotazione di una stanza di un hotel.
Le pronotazioni saranno solo all'interno dello stesso anno solare. Ad esempio, non è possibile avere come data di arrivo il 27/12 e come data di partenza il 5/1.
#STATO:
- id_prenotazione: intero non negativo.
- numero_stanza: intero positivo.
- data_arrivo: oggetto di tipo Data.
- data_partenza: oggetto di tipo Data, non deve essere precedente alla data di arrivo.
- nome_cliente: stringa non vuota.
- numero_persone: intero positivo.
Ogni volta che si modifica una di queste variabili di istanza, devono essere controllati tipo e valori e sollevate opportune eccezioni ValueError o TypeError se i parametri non sono validi.

#METODI:
- Costruttore che prende in input il numero della stanza, la data di arrivo, la data di partenza, il nome del cliente e il numero di persone. Esempio di utilizzo: p = Prenotazione(101, Data(1, 1), Data(5, 1), "Mario Rossi", 2)
- Metodi getter e setter per il numero della stanza, la data di arrivo, la data di partenza, il nome del cliente e il numero di persone.
- Metodo per la rappresentazione in forma di stringa della prenotazione. Rispettando il formato di esempio: "Prenotazione 1 per stanza 101 da 1/1 a 5/1 a nome Mario Rossi per 1 persone"
- Metodo per il confronto di uguaglianza profonda tra due prenotazioni.
"""



class Prenotazione:
    id_counter = 1  # creiamo un contatore per gli id delle prenotazioni che rimane presente nel sistema e poi lo aggiorniamo quando creiamo una nuova prenotazione
    def __init__(self, id_prenotazione=None, numero_stanza=0, data_arrivo=None, data_partenza=None, nome_cliente="",
                 numero_persone=0):
        if id_prenotazione is None:  # controlliamo se c'è un id, e in caso contrario creiamo un id automatico
            self.id_prenotazione = Prenotazione.id_counter
            Prenotazione.id_counter += 1
        else:
            gestione_errori_data(id_prenotazione, int, 0)
            self.id_prenotazione = id_prenotazione
        self.numero_stanza = numero_stanza
        self.data_arrivo = data_arrivo
        self.data_partenza = data_partenza
        self.nome_cliente = nome_cliente
        self.numero_persone = numero_persone

    # - Metodi getter e setter per il numero della stanza, la data di arrivo, la data di partenza, il nome del cliente e il numero di persone.

    @property
    def id_prenotazione(self):
        return self._id_prenotazione

    @id_prenotazione.setter
    def id_prenotazione(self, value):
        try:
            gestione_errori_data(value, int, 0)
            self._id_prenotazione = value
        except ValueError as e:
            raise TypeError(f"Errore con la creazione della prenotazione con errore: {e}") from e

    @property
    def numero_stanza(self):
        return self._numero_stanza

    @numero_stanza.setter
    def numero_stanza(self, value):
        try:
            gestione_errori_data(value, int, 0)
            self._numero_stanza = value
        except TypeError as e:
            raise TypeError(f"errore con la creazione della stanza con errore: {e}") from e

    @property
    def data_arrivo(self):
        return self._data_arrivo

    @data_arrivo.setter
    def data_arrivo(self, value):
        try:
            gestione_errori_data(value, Data)
            self._data_arrivo = value
        except ValueError as e:
            raise TypeError(f"Errore con la data di arrivo della prenotazione con errore: {e}") from e

    @property
    def data_partenza(self):
        return self._data_partenza

    @data_partenza.setter
    def data_partenza(self, value):
        try:
            gestione_errori_data(value, Data)
            if self.data_arrivo is None:
                raise ValueError("Impostare la data di arrivo prima della data di partenza")
            if value < self.data_arrivo:
                raise ValueError("La data di partenza non può essere precedente alla data di arrivo.")
            # Controllo prenotazioni a cavallo anno
            if value.mese < self.data_arrivo.mese:
                raise ValueError("Prenotazioni a cavallo dell'anno non ammesse")
            self._data_partenza = value
        except ValueError as e:
            raise TypeError(f"Errore nella creazione della data di partenza della prenotazione con errore: {e}") from e

    @property
    def nome_cliente(self):
        return self._nome_cliente

    @nome_cliente.setter
    def nome_cliente(self, value):
        try:
            value = value.strip()
            gestione_errori_data(value, str)
            lunghezza_nome = len(value)
            if lunghezza_nome > 20 or lunghezza_nome < 3:  # controllo lunghezza nome
                raise ValueError("Il nome deve essere lungo almeno 3 caratteri ed un massimo di 20")
            self._nome_cliente = value
        except ValueError as e:
            raise TypeError(f"Errore nella creazione del nome  con errore: {e}") from e

    @property
    def numero_persone(self):
        return self._numero_persone

    @numero_persone.setter
    def numero_persone(self, value):
        try:
            gestione_errori_data(value, int, 0)
            self._numero_persone = value
        except ValueError as e:
            raise TypeError(f"Errore con il numero della prenotazione con errore: {e}") from e

    # - Metodo per la rappresentazione in forma di stringa della prenotazione. Rispettando il formato di esempio: "Prenotazione 1 per stanza 101 da 1/1 a 5/1 a nome Mario Rossi per 1 persone"

    def __str__(self):
        persone_str = "persona" if self.numero_persone == 1 else "persone"
        return f"Prenotazione {self.id_prenotazione} per stanza {self.numero_stanza} dal {self.data_arrivo.giorno}/{self.data_arrivo.mese} al {self.data_partenza.giorno}/{self.data_partenza.mese} a nome {self.nome_cliente} per {self.numero_persone} {persone_str}"

    # - Metodo per il confronto di uguaglianza profonda tra due prenotazioni.
    def __eq__(self, other):
        if not isinstance(other, Prenotazione):
            return False
        return (
                self.numero_stanza == other.numero_stanza and
                self.data_arrivo == other.data_arrivo and
                self.data_partenza == other.data_partenza and
                self.nome_cliente == other.nome_cliente and
                self.numero_persone == other.numero_persone
        )

def gestione_errori_data(data, tipo_dato, minimo=None, massimo=None):
    """Funzione per gestire gli errori in maniera generica, in modo da non dover ripetere il codice per ogni classe"""

    if tipo_dato is int:
        if isinstance(data, str):  # conversione da stringa a int per GUI
            try:
                data = int(data.strip())
            except ValueError:
                raise TypeError(f"Il valore '{data}' deve essere un numero.")

    # Controllo del tipo di dato
    if not isinstance(data, tipo_dato):
        raise TypeError(f"Il valore deve essere di tipo {tipo_dato.__name__}.")

    # Controllo dei limiti (solo per int e float)
    if tipo_dato is int:
        if minimo is not None and data < minimo:
            raise ValueError(f"Il valore deve essere maggiore o uguale a {minimo}.")
        if massimo is not None and data >= massimo:
            raise ValueError(f"Il valore deve essere minore di {massimo}.")

    if tipo_dato is float:
        if minimo is not None and data <= minimo:
            raise ValueError(f"Il prezzo deve essere maggiore di {minimo}.")

    # Controllo per stringhe non vuote
    if tipo_dato is str and len(data.strip()) == 0:
        raise ValueError("La stringa non può essere vuota.")

    return data
