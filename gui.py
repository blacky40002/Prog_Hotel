import tkinter as tk
from tkinter import messagebox
from hotel import Hotel
from classi import Data, gestione_errori_data

"""
 Deve essere realizzata un'interfaccia grafica usando il modulo tkinter che carichi automaticamente il file 
 hotel_base.txt, permetta di mostrare sin da subito le stanze dell'hotel indicando tipo e numero della stanza 
 (con extra in caso di suite) e le seguenti funzionalità:
 - mostrare la lista di prenotazioni dell'hotel;
 - prenotazione di una stanza;
 - disdire la prenotazione di una stanza;
 - ottenere il prezzo di una prenotazione dato l'indice:
 - mostrare l'hotel ad una certa data inserendo i nomi dei clienti nelle stanze a quella data; #TODO da finire
 - ottenere le stanze libere ad una certa data;
 - ottenere le prenotazioni di uno specifico cliente inserendo il nome;
 - ottenere il numero di persone nell'albergo ad una certa data; #TODO da fare
 - salvare o caricare da file lo stato dell'hotel permettendo di inserire il nome del file.
 - uscire dall'applicazione 
 Per uscire dall'applicazione deve essere possibile usare sia mouse che tastiera.
 L'aspetto dell'interfaccia viene deciso dallo studente.
"""


class myApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Gestione Hotel")

        # Inizializza l'hotel
        self.hotel = Hotel()
        try:
            self.hotel.carica("hotel_base.txt")
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare hotel_base.txt: {e}")
            self.hotel = Hotel()  # Se il caricamento del file fallisce, crea un hotel vuoto per assicurare che l'applicazione sia comunque utilizzabile

        # Configurazione dell'interfaccia
        self.crea_frame()
        self.crea_frame_cliente()
        self.crea_frame_manageriale()

        # Mostra il frame principale all'avvio
        self.mostra_frame_principale()

        # Bind per uscire con ESC
        self.root.bind('<Escape>', lambda
            e: self.root.destroy())  # le lambda sono funzioni anonime che non hanno bisogno di essere definite, in questo caso serve per chiudere l'applicazione quando si preme ESC

    # Metodi per la configurazione dei frame
    def crea_frame(self):
        """Configura il frame principale"""
        self.main_frame = tk.Frame(self.root)

        # Canvas per visualizzare le stanze
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.aggiorna_visualizzazioni_stanze()

        # Pulsanti principali
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(btn_frame, text="Area Clienti", command=self.mostra_frame_cliente, width=15).pack(side=tk.LEFT,
                                                                                                    padx=5)
        tk.Button(btn_frame, text="Gestione Albergo", command=self.mostra_frame_management, width=15).pack(side=tk.LEFT,
                                                                                                           padx=5)
        tk.Button(btn_frame, text="Esci", command=self.root.destroy, width=15).pack(side=tk.RIGHT, padx=5)

    def crea_frame_cliente(self):
        """Configura il frame area clienti"""
        self.client_frame = tk.Frame(self.root, bg="lightblue")

        tk.Label(self.client_frame, text="Area Clienti", font=("Arial", 16)).pack(pady=20)

        # Lista di pulsanti con le relative funzioni
        bottoni = [
            ("Prenota una stanza", self.popup_prenotazione),
            (
            "Disdici prenotazione", lambda: self.popup_input("Disdici", "ID prenotazione:", self.elimina_prenotazione)),
            ("Prezzo prenotazione",
             lambda: self.popup_input("Prezzo", "ID prenotazione:", self.mostra_prezzo_prenotazione)),
            ("Stanze libere",
             lambda: self.popup_input("Stanze libere", "Data (gg/mm):", self.mostra_stanze_disponibili)),
            ("Torna indietro", self.mostra_frame_principale)
        ]

        for text, command in bottoni:
            tk.Button(self.client_frame, text=text, command=command, width=25).pack(pady=5)

    def crea_frame_manageriale(self):
        """Configura il frame gestione albergo"""
        self.management_frame = tk.Frame(self.root, bg="lightgreen")

        tk.Label(self.management_frame, text="Gestione Albergo", font=("Arial", 16)).pack(pady=20)

        # Lista di pulsanti con le relative funzioni
        buttons = [
            ("Carica hotel", lambda: self.popup_input("Carica", "Nome file:", self.carica_hotel)),
            ("Salva hotel", lambda: self.popup_input("Salva", "Nome file:", self.salva_hotel)),
            ("Mostra prenotazioni", self.mostra_tutte_prenotazioni),
            ("Prenotazioni cliente",
             lambda: self.popup_input("Cerca cliente", "Nome cliente:", self.mostra_prenotazioni_per_cliente)),
            ("Stato stanze per data",
             lambda: self.popup_input("Stato stanze", "Data (gg/mm):", self.mostra_stato_stanza)),
            ("Torna indietro", self.mostra_frame_principale)
        ]

        for text, command in buttons:
            tk.Button(self.management_frame, text=text, command=command, width=25).pack(pady=5)

    # Metodi per la gestione dei frame
    def mostra_frame_principale(self):
        self.nascondi_frames()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.aggiorna_visualizzazioni_stanze()

    def mostra_frame_cliente(self):
        self.nascondi_frames()
        self.client_frame.pack(fill=tk.BOTH, expand=True)

    def mostra_frame_management(self):
        self.nascondi_frames()
        self.management_frame.pack(fill=tk.BOTH, expand=True)

    def nascondi_frames(self):
        for frame in [self.main_frame, self.client_frame, self.management_frame]:
            frame.pack_forget()  # invece di distruggere il frame ogni volta lo nascondiamo così da non doverlo ricreare ogni volta

    # Metodi per la visualizzazione delle stanze
    def aggiorna_visualizzazioni_stanze(self):
        """Aggiorna la visualizzazione delle stanze ogni volta che viene fatto un qualche cambiamento"""
        self.canvas.delete("all")
        y = 20

        self.canvas.create_text(400, y, text="BENVENUTI NEL NOSTRO HOTEL\nEcco la lista delle stanze che offriamo:",
                                font=("Arial", 14, "bold"))
        y += 40

        for stanza in self.hotel.stanze.values():
            text = f"{stanza.get_tipo_stanza()} {stanza.get_numero_stanza()}"
            if hasattr(stanza,
                       'get_extra'):  # controlliamo se la stanza ha attributi extra con il hasattr che controlla se l'oggetto contiene quell attributo
                text += f" (Extra:{', '.join(stanza.get_extra())})"

            self.canvas.create_text(20, y, text=text, anchor="w",
                                    font=("Arial", 12))
            y += 20

    # Metodi generici per popup
    def popup_input(self, titolo, testo,
                    gestione_errore):  # funzione per creare piu volte un popup passandogli i vari valori
        popup = tk.Toplevel(self.root)
        popup.title(titolo)
        popup.geometry("300x150")

        tk.Label(popup, text=testo).pack(pady=10)
        entry = tk.Entry(popup)
        entry.pack(pady=5)

        tk.Button(popup, text="OK",
                  command=lambda: self.gestione_errori(gestione_errore, entry.get(), popup)).pack(pady=10)

    def popup_prenotazione(self):
        """Crea il popup specifico per la prenotazione"""
        popup = tk.Toplevel(self.root)
        popup.title("Prenota Stanza")
        popup.geometry("400x300")

        fields = [
            ("Numero stanza:", "101"),
            ("Data arrivo (gg/mm):", "01/01"),
            ("Data partenza (gg/mm):", "05/01"),
            ("Nome cliente:", "Pinco Panco"),
            ("Numero persone:", "1")
        ]

        entrate = []
        for label, default in fields:
            tk.Label(popup, text=label).pack(pady=2)
            entry = tk.Entry(popup)
            entry.insert(0, default)
            entry.pack(pady=2)
            entrate.append(entry)

        tk.Button(popup, text="Prenota",
                  command=lambda: self.prenota_stanza(entrate, popup)).pack(pady=10)

    def gestione_errori(self, callback, value, popup):
        # gestisce tutti gli errori cosi da non dover scrivere ogni volta il try catch, se non ci sono errori chiude il popup, altrimenti mostra l'errore
        try:
            callback(value)
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    # Metodi per le operazioni dell'hotel
    def prenota_stanza(self, entrate, popup):
        """Gestisce la prenotazione di una stanza"""
        try:

            data = [e.get() for e in entrate]
            gestione_errori_data(data[0], int)

            num_stanza = int(data[0])
            arrivo, partenza = Hotel.parsing_date(data[1], data[2])
            nome = data[3]
            persone = int(data[4])
            gestione_errori_data(nome, str)
            gestione_errori_data(persone, int, 1)
            id_pren = self.hotel.prenota(num_stanza, arrivo, partenza, nome, persone)
            messagebox.showinfo("Successo", f"Prenotazione creata (ID: {id_pren})")
            popup.destroy()
            self.aggiorna_visualizzazioni_stanze()
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def elimina_prenotazione(self, pren_id):
        """Disdice una prenotazione"""
        try:
            gestione_errori_data(pren_id, int)
            self.hotel.disdici(int(pren_id))
            messagebox.showinfo("Successo", "Prenotazione disdetta")
            self.aggiorna_visualizzazioni_stanze()
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def mostra_prezzo_prenotazione(self, pren_id):
        """Mostra il prezzo di una prenotazione"""
        try:
            gestione_errori_data(pren_id, int)

            prezzo = self.hotel.prezzo_prenotazione(int(pren_id))
            messagebox.showinfo("Prezzo", f"Prezzo: {prezzo}€")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def mostra_stanze_disponibili(self, data_str):
        """Mostra le stanze libere in una data"""
        try:
            data_arrivo, _ = Hotel.parsing_date(data_str, data_str)
            data = data_arrivo
            stanze = self.hotel.get_stanze_libere(data)

            message = "Stanze libere:\n" + "\n".join(
                f"{s.get_numero_stanza()} ({s.get_tipo_stanza()})"
                for s in stanze
            )
            messagebox.showinfo("Stanze libere", message)
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def carica_hotel(self, filename):
        """Carica lo stato dell'hotel da file"""
        try:
            self.hotel.carica(filename)
            self.aggiorna_visualizzazioni_stanze()

            messagebox.showinfo("Successo", "Hotel caricato correttamente")
            self.aggiorna_visualizzazioni_stanze()
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def salva_hotel(self, filename):
        """Salva lo stato dell'hotel su file"""
        try:
            self.hotel.salva(filename)
            messagebox.showinfo("Successo", "Hotel salvato correttamente")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def mostra_tutte_prenotazioni(self):
        """Mostra tutte le prenotazioni"""
        prenotazioni = self.hotel.get_prenotazioni()
        message = "Prenotazioni:\n" + "\n".join(str(p) for p in prenotazioni)
        messagebox.showinfo("Prenotazioni", message)

    def mostra_prenotazioni_per_cliente(self, nome):
        """Mostra le prenotazioni di un cliente"""
        prenotazioni = self.hotel.get_prenotazioni_cliente(nome)
        message = f"Prenotazioni per {nome}:\n" + "\n".join(str(p) for p in prenotazioni)
        messagebox.showinfo("Prenotazioni cliente", message)

    def mostra_stato_stanza(self, data_str):
        """Mostra lo stato delle stanze in una data"""
        try:

            data, _ = Hotel.parsing_date(data_str, data_str)
            prenotazioni = self.hotel.get_prenotazioni_data(data)

            message = f"Stato stanze al {data_str}:\n"
            for p in prenotazioni:
                message += f"Stanza {p.numero_stanza}: {p.nome_cliente}\n"

            messagebox.showinfo("Stato stanze", message)
        except Exception as e:
            messagebox.showerror("Errore", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = myApp(root)
    root.mainloop()