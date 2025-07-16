import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import platform
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
 - mostrare l'hotel ad una certa data inserendo i nomi dei clienti nelle stanze a quella data;
 - ottenere le stanze libere ad una certa data;
 - ottenere le prenotazioni di uno specifico cliente inserendo il nome;
 - ottenere il numero di persone nell'albergo ad una certa data;
 - salvare o caricare da file lo stato dell'hotel permettendo di inserire il nome del file.
 - uscire dall'applicazione 
 Per uscire dall'applicazione deve essere possibile usare sia mouse che tastiera.
"""


class HotelApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_style()

        # Inizializza l'hotel
        self.hotel = Hotel()
        self.load_initial_data()

        # Crea l'interfaccia
        self.create_main_interface()

        # Configurazione tasti rapidi compatibili cross-platform
        self.setup_keyboard_shortcuts()

    def setup_window(self):
        """Configura la finestra principale in modo cross-platform"""
        self.root.title("🏨 Gestione Hotel - Sistema di Prenotazione")

        # Dimensioni e posizionamento cross-platform
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = min(1200, int(screen_width * 0.8))
        window_height = min(800, int(screen_height * 0.8))

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(800, 600)

        # Icona e configurazioni specifiche per OS
        try:
            if platform.system() == "Windows":
                self.root.iconbitmap(default='')  # Rimuove l'icona di default
            self.root.configure(bg='#f0f0f0')
        except:
            pass

    def setup_style(self):
        """Configura lo stile moderno"""
        self.style = ttk.Style()

        # Colori moderni
        self.colors = {
            'primary': '#2c3e50',      # Blu scuro
            'secondary': '#3498db',    # Blu chiaro
            'success': '#27ae60',      # Verde
            'warning': '#f39c12',      # Arancione
            'danger': '#e74c3c',       # Rosso
            'light': '#ecf0f1',        # Grigio chiaro
            'white': '#ffffff',
            'text': '#2c3e50'
        }

        # Configura stili ttk
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')

        # Stili personalizzati
        self.style.configure('Modern.TButton',
                           font=('Segoe UI', 10),
                           padding=(10, 8))

        self.style.configure('Header.TLabel',
                           font=('Segoe UI', 14, 'bold'),
                           foreground=self.colors['primary'])

        self.style.configure('Subheader.TLabel',
                           font=('Segoe UI', 11, 'bold'),
                           foreground=self.colors['secondary'])

    def load_initial_data(self):
        """Carica i dati iniziali dell'hotel"""
        try:
            self.hotel.carica("hotel_base.txt")
            print("✅ Hotel caricato correttamente da hotel_base.txt")
        except Exception as e:
            messagebox.showwarning("Avviso",
                                 f"Impossibile caricare hotel_base.txt: {e}\n"
                                 "Verrà creato un hotel vuoto.")
            self.hotel = Hotel()

    def setup_keyboard_shortcuts(self):
        """Configura i tasti rapidi cross-platform"""
        # Tasto per uscire
        self.root.bind('<Escape>', lambda e: self.confirm_exit())

        # Tasti rapidi per funzioni comuni (cross-platform)
        if platform.system() == "Darwin":  # macOS
            self.root.bind('<Command-q>', lambda e: self.confirm_exit())
            self.root.bind('<Command-n>', lambda e: self.show_booking_dialog())
            self.root.bind('<Command-s>', lambda e: self.show_save_dialog())
            self.root.bind('<Command-o>', lambda e: self.show_load_dialog())
        else:  # Windows/Linux
            self.root.bind('<Control-q>', lambda e: self.confirm_exit())
            self.root.bind('<Control-n>', lambda e: self.show_booking_dialog())
            self.root.bind('<Control-s>', lambda e: self.show_save_dialog())
            self.root.bind('<Control-o>', lambda e: self.show_load_dialog())

    def create_main_interface(self):
        """Crea l'interfaccia principale moderna"""
        # Frame principale con padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        self.create_header(main_container)

        # Separator
        ttk.Separator(main_container, orient='horizontal').pack(fill=tk.X, pady=(10, 20))

        # Contenuto principale
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Layout a due colonne
        self.create_left_panel(content_frame)
        self.create_right_panel(content_frame)

        # Footer con informazioni
        self.create_footer(main_container)

    def create_header(self, parent):
        """Crea l'header dell'applicazione"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Titolo principale
        title_label = ttk.Label(header_frame,
                               text="🏨 Sistema di Gestione Hotel",
                               style='Header.TLabel')
        title_label.pack(side=tk.LEFT)

        # Info hotel
        hotel_info = f"Stanze: {len(self.hotel.stanze)} | Prenotazioni: {len(self.hotel.prenotazioni)}"
        info_label = ttk.Label(header_frame,
                              text=hotel_info,
                              style='Subheader.TLabel')
        info_label.pack(side=tk.RIGHT)

    def create_left_panel(self, parent):
        """Crea il pannello sinistro con le stanze"""
        left_frame = ttk.LabelFrame(parent, text="🏠 Stanze Disponibili", padding="15")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Scrollable text area per le stanze
        self.rooms_display = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            width=40,
            height=20,
            font=('Courier New', 10),
            state=tk.DISABLED
        )
        self.rooms_display.pack(fill=tk.BOTH, expand=True)

        # Bottone per aggiornare
        ttk.Button(left_frame,
                  text="🔄 Aggiorna Vista",
                  command=self.update_rooms_display,
                  style='Modern.TButton').pack(pady=(10, 0))

        # Aggiorna immediatamente
        self.update_rooms_display()

    def create_right_panel(self, parent):
        """Crea il pannello destro con i controlli"""
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Sezione Clienti
        self.create_client_section(right_frame)

        # Separator
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=15)

        # Sezione Gestione
        self.create_management_section(right_frame)

        # Separator
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=15)

        # Sezione File
        self.create_file_section(right_frame)

    def create_client_section(self, parent):
        """Crea la sezione clienti"""
        client_frame = ttk.LabelFrame(parent, text="👥 Area Clienti", padding="10")
        client_frame.pack(fill=tk.X, pady=(0, 10))

        buttons = [
            ("📅 Nuova Prenotazione", self.show_booking_dialog, self.colors['success']),
            ("❌ Cancella Prenotazione", self.show_cancel_dialog, self.colors['danger']),
            ("💰 Calcola Prezzo", self.show_price_dialog, self.colors['warning']),
            ("🗓️ Stanze Libere", self.show_free_rooms_dialog, self.colors['secondary'])
        ]

        for text, command, color in buttons:
            btn = ttk.Button(client_frame, text=text, command=command,
                           style='Modern.TButton', width=25)
            btn.pack(pady=3, fill=tk.X)

    def create_management_section(self, parent):
        """Crea la sezione gestione"""
        mgmt_frame = ttk.LabelFrame(parent, text="⚙️ Gestione Hotel", padding="10")
        mgmt_frame.pack(fill=tk.X, pady=(0, 10))

        buttons = [
            ("📋 Tutte le Prenotazioni", self.show_all_bookings),
            ("🔍 Prenotazioni Cliente", self.show_client_bookings_dialog),
            ("🏠 Stato Stanze per Data", self.show_room_status_dialog),
            ("👥 Persone Presenti", self.show_people_count_dialog)
        ]

        for text, command in buttons:
            btn = ttk.Button(mgmt_frame, text=text, command=command,
                           style='Modern.TButton', width=25)
            btn.pack(pady=3, fill=tk.X)

    def create_file_section(self, parent):
        """Crea la sezione file"""
        file_frame = ttk.LabelFrame(parent, text="💾 Gestione File", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))

        buttons = [
            ("📂 Carica Hotel", self.show_load_dialog),
            ("💾 Salva Hotel", self.show_save_dialog),
            ("🚪 Esci", self.confirm_exit)
        ]

        for text, command in buttons:
            btn = ttk.Button(file_frame, text=text, command=command,
                           style='Modern.TButton', width=25)
            btn.pack(pady=3, fill=tk.X)

    def create_footer(self, parent):
        """Crea il footer con informazioni"""
        footer_frame = ttk.Frame(parent)
        footer_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Separator(footer_frame, orient='horizontal').pack(fill=tk.X, pady=(0, 10))

        # Informazioni di sistema
        os_info = f"Sistema: {platform.system()} {platform.release()}"
        shortcut_info = "Tasti rapidi: ESC=Esci, Ctrl+N=Prenota, Ctrl+S=Salva, Ctrl+O=Carica"
        if platform.system() == "Darwin":
            shortcut_info = shortcut_info.replace("Ctrl", "Cmd")

        ttk.Label(footer_frame, text=os_info, font=('Segoe UI', 8)).pack(side=tk.LEFT)
        ttk.Label(footer_frame, text=shortcut_info, font=('Segoe UI', 8)).pack(side=tk.RIGHT)

    def update_rooms_display(self):
        """Aggiorna la visualizzazione delle stanze"""
        self.rooms_display.config(state=tk.NORMAL)
        self.rooms_display.delete(1.0, tk.END)

        if not self.hotel.stanze:
            self.rooms_display.insert(tk.END, "🚫 Nessuna stanza disponibile nell'hotel.")
        else:
            self.rooms_display.insert(tk.END, "🏨 BENVENUTI NEL NOSTRO HOTEL\n")
            self.rooms_display.insert(tk.END, "=" * 40 + "\n\n")

            # Raggruppa per tipo
            tipos = {}
            for stanza in self.hotel.stanze.values():
                tipo = stanza.get_tipo_stanza()
                if tipo not in tipos:
                    tipos[tipo] = []
                tipos[tipo].append(stanza)

            for tipo, stanze in sorted(tipos.items()):
                self.rooms_display.insert(tk.END, f"📍 {tipo.upper()}:\n")
                for stanza in sorted(stanze, key=lambda x: x.get_numero_stanza()):
                    text = f"   🏠 Stanza {stanza.get_numero_stanza()} - {stanza.get_posti()} posti"
                    if hasattr(stanza, 'get_extra'):
                        text += f" - Extra: {', '.join(stanza.get_extra())}"
                    text += f" - €{stanza.get_prezzo_base():.0f}/notte\n"
                    self.rooms_display.insert(tk.END, text)
                self.rooms_display.insert(tk.END, "\n")

        self.rooms_display.config(state=tk.DISABLED)

        # Aggiorna header
        self.update_header_info()

    def update_header_info(self):
        """Aggiorna le informazioni nell'header"""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Label) and "Stanze:" in grandchild.cget("text"):
                                hotel_info = f"Stanze: {len(self.hotel.stanze)} | Prenotazioni: {len(self.hotel.prenotazioni)}"
                                grandchild.config(text=hotel_info)

    def show_booking_dialog(self):
        """Mostra il dialog per le prenotazioni"""
        dialog = tk.Toplevel(self.root)
        dialog.title("📅 Nuova Prenotazione")
        dialog.geometry("450x400")
        dialog.transient(self.root)
        dialog.grab_set()

        # Centra il dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="📅 Nuova Prenotazione",
                 style='Header.TLabel').pack(pady=(0, 20))

        # Form fields
        fields = [
            ("Numero stanza:", "101"),
            ("Data arrivo (gg/mm):", "01/01"),
            ("Data partenza (gg/mm):", "05/01"),
            ("Nome cliente:", "Mario Rossi"),
            ("Numero persone:", "1")
        ]

        entries = []
        for label, default in fields:
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=25)
            entry.insert(0, default)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            entries.append(entry)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)

        ttk.Button(btn_frame, text="✅ Prenota",
                  command=lambda: self.process_booking(entries, dialog),
                  style='Modern.TButton').pack(side=tk.RIGHT, padx=(5, 0))

        ttk.Button(btn_frame, text="❌ Annulla",
                  command=dialog.destroy,
                  style='Modern.TButton').pack(side=tk.RIGHT)

    def process_booking(self, entries, dialog):
        """Processa la prenotazione"""
        try:
            data = [e.get().strip() for e in entries]

            num_stanza = int(data[0])
            arrivo, partenza = Hotel.parsing_date(data[1], data[2])
            nome = data[3]
            persone = int(data[4])

            gestione_errori_data(nome, str)
            gestione_errori_data(persone, int, 0)

            id_pren = self.hotel.prenota(num_stanza, arrivo, partenza, nome, persone)

            messagebox.showinfo("✅ Successo",
                               f"Prenotazione creata con successo!\n"
                               f"ID Prenotazione: {id_pren}\n"
                               f"Stanza: {num_stanza}\n"
                               f"Cliente: {nome}")

            dialog.destroy()
            self.update_rooms_display()

        except Exception as e:
            messagebox.showerror("❌ Errore", f"Errore nella prenotazione:\n{str(e)}")

    def show_input_dialog(self, title, prompt, callback):
        """Mostra un dialog di input generico"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("350x200")
        dialog.transient(self.root)
        dialog.grab_set()

        # Centra il dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=prompt, style='Subheader.TLabel').pack(pady=(0, 15))

        entry = ttk.Entry(main_frame, width=30, font=('Segoe UI', 11))
        entry.pack(pady=10)
        entry.focus()

        def on_ok():
            try:
                callback(entry.get().strip())
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("❌ Errore", str(e))

        def on_enter(event):
            on_ok()

        entry.bind('<Return>', on_enter)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)

        ttk.Button(btn_frame, text="✅ OK", command=on_ok,
                  style='Modern.TButton').pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="❌ Annulla", command=dialog.destroy,
                  style='Modern.TButton').pack(side=tk.RIGHT)

    def show_cancel_dialog(self):
        """Mostra dialog per cancellare prenotazione"""
        self.show_input_dialog("❌ Cancella Prenotazione",
                              "Inserisci l'ID della prenotazione da cancellare:",
                              self.cancel_booking)

    def cancel_booking(self, booking_id):
        """Cancella una prenotazione"""
        gestione_errori_data(booking_id, int)
        self.hotel.disdici(int(booking_id))
        messagebox.showinfo("✅ Successo", "Prenotazione cancellata con successo!")
        self.update_rooms_display()

    def show_price_dialog(self):
        """Mostra dialog per calcolare prezzo"""
        self.show_input_dialog("💰 Calcola Prezzo",
                              "Inserisci l'ID della prenotazione:",
                              self.show_price)

    def show_price(self, booking_id):
        """Mostra il prezzo di una prenotazione"""
        gestione_errori_data(booking_id, int)
        prezzo = self.hotel.prezzo_prenotazione(int(booking_id))
        messagebox.showinfo("💰 Prezzo Prenotazione",
                           f"Prezzo totale: €{prezzo:.2f}")

    def show_free_rooms_dialog(self):
        """Mostra dialog per stanze libere"""
        self.show_input_dialog("🗓️ Stanze Libere",
                              "Inserisci la data (gg/mm):",
                              self.show_free_rooms)

    def show_free_rooms(self, date_str):
        """Mostra le stanze libere in una data"""
        data_arrivo, _ = Hotel.parsing_date(date_str, date_str)
        stanze = self.hotel.get_stanze_libere(data_arrivo)

        if not stanze:
            message = "🚫 Nessuna stanza libera in questa data."
        else:
            message = f"🗓️ Stanze libere il {date_str}:\n\n"
            for s in stanze:
                message += f"🏠 Stanza {s.get_numero_stanza()} ({s.get_tipo_stanza()}) - €{s.get_prezzo_base():.0f}/notte\n"

        messagebox.showinfo("🗓️ Stanze Libere", message)

    def show_all_bookings(self):
        """Mostra tutte le prenotazioni"""
        prenotazioni = self.hotel.get_prenotazioni()
        if not prenotazioni:
            message = "📋 Nessuna prenotazione presente."
        else:
            message = f"📋 Prenotazioni presenti ({len(prenotazioni)}):\n\n"
            for p in prenotazioni:
                message += f"🆔 {str(p)}\n\n"

        # Usa una finestra separata per liste lunghe
        self.show_text_window("📋 Tutte le Prenotazioni", message)

    def show_text_window(self, title, content):
        """Mostra una finestra con testo scrollabile"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("600x400")
        window.transient(self.root)

        # Centra la finestra
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
        y = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)
        window.geometry(f"+{x}+{y}")

        frame = ttk.Frame(window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD,
                                               font=('Segoe UI', 10))
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)

        ttk.Button(frame, text="✅ Chiudi", command=window.destroy,
                  style='Modern.TButton').pack(pady=10)

    def show_client_bookings_dialog(self):
        """Mostra dialog per prenotazioni cliente"""
        self.show_input_dialog("🔍 Prenotazioni Cliente",
                              "Inserisci il nome del cliente:",
                              self.show_client_bookings)

    def show_client_bookings(self, client_name):
        """Mostra le prenotazioni di un cliente"""
        prenotazioni = self.hotel.get_prenotazioni_cliente(client_name)
        message = f"🔍 Prenotazioni per {client_name}:\n\n"
        for p in prenotazioni:
            message += f"🆔 {str(p)}\n\n"

        self.show_text_window(f"🔍 Prenotazioni - {client_name}", message)

    def show_room_status_dialog(self):
        """Mostra dialog per stato stanze"""
        self.show_input_dialog("🏠 Stato Stanze",
                              "Inserisci la data (gg/mm):",
                              self.show_room_status)

    def show_room_status(self, date_str):
        """Mostra lo stato delle stanze in una data"""
        data, _ = Hotel.parsing_date(date_str, date_str)
        prenotazioni = self.hotel.get_prenotazioni_data(data)

        if not prenotazioni:
            message = f"🏠 Nessuna stanza occupata il {date_str}"
        else:
            message = f"🏠 Stato stanze il {date_str}:\n\n"
            for p in prenotazioni:
                message += f"🏠 Stanza {p.numero_stanza}: {p.nome_cliente} ({p.numero_persone} persone)\n"

        messagebox.showinfo("🏠 Stato Stanze", message)

    def show_people_count_dialog(self):
        """Mostra dialog per conteggio persone"""
        self.show_input_dialog("👥 Persone Presenti",
                              "Inserisci la data (gg/mm):",
                              self.show_people_count)

    def show_people_count(self, date_str):
        """Mostra il numero di persone presenti in una data"""
        data, _ = Hotel.parsing_date(date_str, date_str)
        count = self.hotel.get_numero_persone_data(data)
        messagebox.showinfo("👥 Persone Presenti",
                           f"Persone presenti il {date_str}: {count}")

    def show_save_dialog(self):
        """Mostra dialog per salvare"""
        self.show_input_dialog("💾 Salva Hotel",
                              "Inserisci il nome del file:",
                              self.save_hotel)

    def save_hotel(self, filename):
        """Salva l'hotel su file"""
        if not filename.endswith('.txt'):
            filename += '.txt'
        self.hotel.salva(filename)
        messagebox.showinfo("✅ Successo", f"Hotel salvato in: {filename}")

    def show_load_dialog(self):
        """Mostra dialog per caricare"""
        self.show_input_dialog("📂 Carica Hotel",
                              "Inserisci il nome del file:",
                              self.load_hotel)

    def load_hotel(self, filename):
        """Carica l'hotel da file"""
        if not filename.endswith('.txt'):
            filename += '.txt'
        self.hotel.carica(filename)
        messagebox.showinfo("✅ Successo", f"Hotel caricato da: {filename}")
        self.update_rooms_display()

    def confirm_exit(self):
        """Conferma uscita dall'applicazione"""
        if messagebox.askyesno("🚪 Conferma Uscita",
                              "Sei sicuro di voler uscire dall'applicazione?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()

