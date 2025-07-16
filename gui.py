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
        self.root.geometry("900x700")
        self.root.title("🏨 Sistema Gestione Hotel")
        self.root.configure(bg="#f0f4f8")

        # Palette colori moderna
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e',
            'white': '#ffffff',
            'bg': '#f0f4f8'
        }

        # Font migliorati
        self.fonts = {
            'title': ('Segoe UI', 20, 'bold'),
            'subtitle': ('Segoe UI', 14, 'bold'),
            'normal': ('Segoe UI', 11),
            'small': ('Segoe UI', 9)
        }

        # Inizializza l'hotel
        self.hotel = Hotel()
        try:
            self.hotel.carica("hotel_base.txt")
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare hotel_base.txt: {e}")
            self.hotel = Hotel()

        # Configurazione dell'interfaccia
        self.crea_frame()
        self.crea_frame_cliente()
        self.crea_frame_manageriale()

        # Mostra il frame principale all'avvio
        self.mostra_frame_principale()

        # Bind per uscire con ESC
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    # Metodi per la configurazione dei frame
    def crea_frame(self):
        """Configura il frame principale con design migliorato"""
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg'])

        # Header elegante
        header_frame = tk.Frame(self.main_frame, bg=self.colors['primary'], height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="🏨 SISTEMA GESTIONE HOTEL",
                              font=self.fonts['title'],
                              bg=self.colors['primary'],
                              fg=self.colors['white'])
        title_label.pack(expand=True)

        # Frame contenuto principale
        content_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Sezione stanze con bordo
        stanze_frame = tk.Frame(content_frame, bg=self.colors['white'], relief='solid', bd=1)
        stanze_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        stanze_title = tk.Label(stanze_frame, text="📋 STANZE DISPONIBILI",
                               font=self.fonts['subtitle'],
                               bg=self.colors['white'],
                               fg=self.colors['primary'])
        stanze_title.pack(pady=20)

        # Canvas migliorato
        self.canvas = tk.Canvas(stanze_frame, bg=self.colors['white'], highlightthickness=0)
        scrollbar = tk.Scrollbar(stanze_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y", padx=(0, 10))
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=(0, 20))

        self.aggiorna_visualizzazioni_stanze()

        # Pulsanti con stile moderno
        btn_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, pady=20)

        # Stile pulsanti migliorato
        btn_clienti = tk.Button(btn_frame, text="👥 Area Clienti",
                               command=self.mostra_frame_cliente,
                               font=self.fonts['normal'],
                               bg=self.colors['secondary'],
                               fg=self.colors['white'],
                               relief='flat',
                               padx=25, pady=12,
                               cursor='hand2',
                               borderwidth=0)
        btn_clienti.pack(side=tk.LEFT, padx=(0, 15))

        btn_gestione = tk.Button(btn_frame, text="⚙️ Gestione Albergo",
                                command=self.mostra_frame_management,
                                font=self.fonts['normal'],
                                bg=self.colors['success'],
                                fg=self.colors['white'],
                                relief='flat',
                                padx=25, pady=12,
                                cursor='hand2',
                                borderwidth=0)
        btn_gestione.pack(side=tk.LEFT, padx=7)

        btn_esci = tk.Button(btn_frame, text="❌ Esci",
                           command=self.root.destroy,
                           font=self.fonts['normal'],
                           bg=self.colors['danger'],
                           fg=self.colors['white'],
                           relief='flat',
                           padx=25, pady=12,
                           cursor='hand2',
                           borderwidth=0)
        btn_esci.pack(side=tk.RIGHT, padx=(15, 0))

    def crea_frame_cliente(self):
        """Configura il frame area clienti con design migliorato"""
        self.client_frame = tk.Frame(self.root, bg=self.colors['bg'])

        # Header colorato
        header_frame = tk.Frame(self.client_frame, bg=self.colors['secondary'], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="👥 AREA CLIENTI",
                              font=self.fonts['title'],
                              bg=self.colors['secondary'],
                              fg=self.colors['white'])
        title_label.pack(expand=True)

        # Contenuto centrato
        content_frame = tk.Frame(self.client_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=80, pady=50)

        # Pulsanti con icone e colori diversi
        bottoni = [
            ("🛏️ Prenota una stanza", self.popup_prenotazione, self.colors['success']),
            ("❌ Disdici prenotazione", lambda: self.popup_input("Disdici", "ID prenotazione:", self.elimina_prenotazione), self.colors['warning']),
            ("💰 Prezzo prenotazione", lambda: self.popup_input("Prezzo", "ID prenotazione:", self.mostra_prezzo_prenotazione), self.colors['secondary']),
            ("📅 Stanze libere", lambda: self.popup_input("Stanze libere", "Data (gg/mm):", self.mostra_stanze_disponibili), self.colors['primary']),
            ("⬅️ Torna indietro", self.mostra_frame_principale, self.colors['dark'])
        ]

        for text, command, color in bottoni:
            btn = tk.Button(content_frame, text=text, command=command,
                           font=self.fonts['normal'],
                           bg=color, fg=self.colors['white'],
                           relief='flat', padx=40, pady=15,
                           cursor='hand2', width=30,
                           borderwidth=0)
            btn.pack(pady=12)

    def crea_frame_manageriale(self):
        """Configura il frame gestione albergo con design migliorato"""
        self.management_frame = tk.Frame(self.root, bg=self.colors['bg'])

        # Header
        header_frame = tk.Frame(self.management_frame, bg=self.colors['success'], height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="⚙️ GESTIONE ALBERGO",
                              font=self.fonts['title'],
                              bg=self.colors['success'],
                              fg=self.colors['white'])
        title_label.pack(expand=True)

        # Contenuto
        content_frame = tk.Frame(self.management_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=80, pady=50)

        # Pulsanti gestionali
        buttons = [
            ("📁 Carica hotel", lambda: self.popup_input("Carica", "Nome file:", self.carica_hotel), self.colors['primary']),
            ("💾 Salva hotel", lambda: self.popup_input("Salva", "Nome file:", self.salva_hotel), self.colors['secondary']),
            ("📋 Mostra prenotazioni", self.mostra_tutte_prenotazioni, self.colors['success']),
            ("🔍 Prenotazioni cliente", lambda: self.popup_input("Cerca cliente", "Nome cliente:", self.mostra_prenotazioni_per_cliente), self.colors['warning']),
            ("📊 Stato stanze per data", lambda: self.popup_input("Stato stanze", "Data (gg/mm):", self.mostra_stato_stanza), self.colors['danger']),
            ("⬅️ Torna indietro", self.mostra_frame_principale, self.colors['dark'])
        ]

        for text, command, color in buttons:
            btn = tk.Button(content_frame, text=text, command=command,
                           font=self.fonts['normal'],
                           bg=color, fg=self.colors['white'],
                           relief='flat', padx=40, pady=15,
                           cursor='hand2', width=30,
                           borderwidth=0)
            btn.pack(pady=12)

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
        """Aggiorna la visualizzazione delle stanze con design migliorato"""
        self.canvas.delete("all")
        y = 20

        for i, stanza in enumerate(self.hotel.stanze.values()):
            # Colori per tipo stanza
            if stanza.get_tipo_stanza() == "Singola":
                icon = "🛏️"
                color = self.colors['secondary']
            elif stanza.get_tipo_stanza() == "Doppia":
                icon = "🛏️🛏️"
                color = self.colors['success']
            else:  # Suite
                icon = "🏛️"
                color = self.colors['warning']

            text = f"{icon} {stanza.get_tipo_stanza()} {stanza.get_numero_stanza()}"

            if hasattr(stanza, 'get_extra'):
                text += f" (Extra: {', '.join(stanza.get_extra())})"

            # Card per ogni stanza con ombra
            card_bg = '#f8f9fa' if i % 2 == 0 else self.colors['white']

            # Bordo colorato
            self.canvas.create_rectangle(10, y-10, 450, y+20,
                                       fill=card_bg, outline=color, width=2)

            self.canvas.create_text(20, y+5, text=text, anchor="w",
                                  font=self.fonts['normal'], fill=color)
            y += 35

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