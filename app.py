import tkinter as tk
from tkinter import messagebox
from abc import ABC, abstractmethod

#Singleton

class TicketManager:
    __instance = None

    def __init__(self):
        self.tickets = []

    @staticmethod
    def getInstance():
        if TicketManager.__instance is None:
            TicketManager.__instance = TicketManager()
        return TicketManager.__instance

    def addTicket(self, ticket):
        self.tickets.append(ticket)
        print("Bilet adăugat:", ticket)

    def getTicket(self, ticket_id):
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                print("Bilet găsit:", ticket)
                return ticket
        print("Biletul nu a fost găsit!")
        return None

    def deleteTicket(self, ticket_id):
        for ticket in self.tickets:
            if ticket.id == ticket_id:
                self.tickets.remove(ticket)
                print("Bilet șters:", ticket)
                return
        print("Biletul nu a fost găsit!")


def attach(self, observer):
    self.observers.append(observer)


def detach(self, observer):
    self.observers.remove(observer)


def notify(self, action):
    for observer in self.observers:
        observer.update(action)

#Factory

class Ticket:
    def __init__(self, id, title):
        self.id = id
        self.title = title


class MovieTicket(Ticket):
    def __init__(self, id, title, movie_name):
        super().__init__(id, title)
        self.movie_name = movie_name


class ConcertTicket(Ticket):
    def __init__(self, id, title, artist):
        super().__init__(id, title)
        self.artist = artist


class TicketFactory:
    @staticmethod
    def createTicket(ticket_type, id, title, **kwargs):
        if ticket_type == "movie":
            movie_name = kwargs.get("movie_name")
            return MovieTicket(id, title, movie_name)
        elif ticket_type == "concert":
            artist = kwargs.get("artist")
            return ConcertTicket(id, title, artist)
        else:
            return None

#Adapter

class TicketLibrary:
    def buyTicket(self, ticket_id):
        print("Bilet cumpărat din bibliotecă:", ticket_id)


class TicketAdapter(Ticket):
    def __init__(self, ticket_id):
        super().__init__(ticket_id, "Bilet adapter")
        self.ticket_library = TicketLibrary()

    def buyTicket(self):
        self.ticket_library.buyTicket(self.id)
        print("Bilet cumpărat din adapter:", self.id)

#Decorator

class PriorityTicketDecorator(Ticket):
    def __init__(self, ticket):
        super().__init__(ticket.id, ticket.title + " / VIP")
        self.ticket = ticket
        self.movie_name = ticket.movie_name

    def getTicketInfo(self):
        self.ticket.getTicketInfo()
        print("Bilet prioritar")

#Observer

class Observer(ABC):
    @abstractmethod
    def update(self, action):
        pass


class TicketSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, action):
        for observer in self.observers:
            observer.update(action)


class TicketObserver(Observer):
    def update(self, action):
        print("Observator notificat cu acțiunea:", action)
        messagebox.showinfo("Notificare", f"Observator notificat cu acțiunea: {action}")

#Strategy

class TicketDisplayStrategy:
    def displayInfo(self, ticket):
        pass


class MovieTicketDisplayStrategy(TicketDisplayStrategy):
    def displayInfo(self, ticket):
        print("Bilet film:")
        print("ID:", ticket.id)
        print("Titlu:", ticket.title)
        print("Film:", ticket.movie_name)


class ConcertTicketDisplayStrategy(TicketDisplayStrategy):
    def displayInfo(self, ticket):
        print("Bilet concert:")
        print("ID:", ticket.id)
        print("Titlu:", ticket.title)
        print("Artist:", ticket.artist)


class TicketInfoContext:
    def __init__(self, display_strategy):
        self.display_strategy = display_strategy

    def setDisplayStrategy(self, display_strategy):
        self.display_strategy = display_strategy

    def displayTicketInfo(self, ticket):
        self.display_strategy.displayInfo(ticket)


class TicketApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistem de gestionare a biletelor")
        self.geometry("500x600")

        self.ticket_manager = TicketManager.getInstance()
        self.ticket_subject = TicketSubject()
        self.ticket_info_context = TicketInfoContext(MovieTicketDisplayStrategy())

        self.ticket_subject.attach(TicketObserver())  # Atașarea observatorilor la subiect

        self.create_widgets()

        self.client_interface = ClientWindow(self, self.ticket_subject)
        self.client_interface.withdraw()

    def create_widgets(self):
        self.message_label = tk.Label(self, text="")
        self.message_label.pack(pady=10)

        ticket_id_frame = tk.Frame(self)
        ticket_id_frame.pack(pady=5)
        ticket_id_label = tk.Label(ticket_id_frame, text="Ticket ID:")
        ticket_id_label.pack(side="left")
        self.ticket_id_entry = tk.Entry(ticket_id_frame)
        self.ticket_id_entry.pack(side="left")

        ticket_title_frame = tk.Frame(self)
        ticket_title_frame.pack(pady=5)
        ticket_title_label = tk.Label(ticket_title_frame, text="Ticket Name:")
        ticket_title_label.pack(side="left")
        self.ticket_title_entry = tk.Entry(ticket_title_frame)
        self.ticket_title_entry.pack(side="left")

        ticket_types = ["movie", "concert"]
        self.ticket_type_entry = tk.StringVar(self)
        self.ticket_type_entry.set("Ticket type")
        self.ticket_type_dropdown = tk.OptionMenu(self, self.ticket_type_entry, *ticket_types)
        self.ticket_type_dropdown.pack(pady=5)

        movie_name_frame = tk.Frame(self)
        movie_name_frame.pack(pady=5)
        movie_name_label = tk.Label(movie_name_frame, text="Movie Name:")
        movie_name_label.pack(side="left")
        self.movie_name_entry = tk.Entry(movie_name_frame)
        self.movie_name_entry.pack(side="left")

        artist_frame = tk.Frame(self)
        artist_frame.pack(pady=5)
        artist_label = tk.Label(artist_frame, text="Artist Name:")
        artist_label.pack(side="left")
        self.artist_entry = tk.Entry(artist_frame)
        self.artist_entry.pack(side="left")

        self.add_ticket_button = tk.Button(self, text="Adaugă Bilet", command=self.add_ticket)
        self.add_ticket_button.pack(pady=5)

        self.get_ticket_button = tk.Button(self, text="Obține Bilet", command=self.get_ticket)
        self.get_ticket_button.pack(pady=5)

        self.delete_ticket_button = tk.Button(self, text="Șterge Bilet", command=self.delete_ticket)
        self.delete_ticket_button.pack(pady=5)

        self.activate_decorator_button = tk.Button(self, text="Activează VIP", command=self.activate_decorator)
        self.activate_decorator_button.pack(pady=5)

        self.switch_interface_button = tk.Button(self, text="Interfață Client", command=self.switch_interface)
        self.switch_interface_button.pack(pady=5)

    def add_ticket(self):
        ticket_id = self.ticket_id_entry.get()
        ticket_title = self.ticket_title_entry.get()
        ticket_type = self.ticket_type_entry.get()

        if ticket_type == "movie":
            movie_name = self.movie_name_entry.get()
            ticket = TicketFactory.createTicket(ticket_type, ticket_id, ticket_title, movie_name=movie_name)
        elif ticket_type == "concert":
            artist = self.artist_entry.get()
            ticket = TicketFactory.createTicket(ticket_type, ticket_id, ticket_title, artist=artist)
        else:
            messagebox.showerror("Eroare", "Selectați un tip de bilet valid!")
            return

        self.ticket_manager.addTicket(ticket)
        self.ticket_subject.notify("Bilet adăugat")

        messagebox.showinfo("Succes", "Bilet adăugat cu succes!")

        self.clear_entries()

    def get_ticket(self):
        ticket_id = self.ticket_id_entry.get()
        ticket = self.ticket_manager.getTicket(ticket_id)
        if ticket:
            self.ticket_subject.notify("Bilet obținut")
        self.clear_entries()

    def delete_ticket(self):
        ticket_id = self.ticket_id_entry.get()
        self.ticket_manager.deleteTicket(ticket_id)
        self.ticket_subject.notify("Bilet șters")
        self.clear_entries()

    def switch_interface(self):
        self.withdraw()
        self.client_interface.deiconify()

    def activate_decorator(self):
        ticket_id = self.ticket_id_entry.get()
        ticket = self.ticket_manager.getTicket(ticket_id)
        if ticket:
            ticket = PriorityTicketDecorator(ticket)
            self.ticket_info_context.displayTicketInfo(ticket)
        self.clear_entries()


    def clear_entries(self):
        self.ticket_id_entry.delete(0, "end")
        self.ticket_title_entry.delete(0, "end")
        self.movie_name_entry.delete(0, "end")
        self.artist_entry.delete(0, "end")


class ClientWindow(tk.Toplevel):
    def __init__(self, parent, ticket_subject):
        super().__init__(parent)

        self.title("Interfață Client")
        self.geometry("400x400")

        self.ticket_manager = TicketManager.getInstance()
        self.ticket_subject = ticket_subject
        self.create_widgets()

    def create_widgets(self):
        self.message_label = tk.Label(self, text="")
        self.message_label.pack(pady=10)

        ticket_id_frame = tk.Frame(self)
        ticket_id_frame.pack(pady=5)
        ticket_id_label = tk.Label(ticket_id_frame, text="Ticket ID:")
        ticket_id_label.pack(side="left")
        self.ticket_id_entry = tk.Entry(ticket_id_frame)
        self.ticket_id_entry.pack(side="left")

        self.show_ticket_info_button = tk.Button(self, text="Arată Informații Bilet", command=self.show_ticket_info)
        self.show_ticket_info_button.pack(pady=5)

        self.buy_ticket_button = tk.Button(self, text="Cumpără Bilet", command=self.buy_ticket)
        self.buy_ticket_button.pack(pady=5)

        self.go_back_button = tk.Button(self, text="Înapoi", command=self.go_back)
        self.go_back_button.pack(pady=5)


    def show_ticket_info(self):
        ticket_id = self.ticket_id_entry.get()
        ticket = self.ticket_manager.getTicket(ticket_id)
        if ticket:
            ticket_info = f"ID: {ticket.id}\nTitlu: {ticket.title}"

            if isinstance(ticket, MovieTicket):
                ticket_info += f"\nFilm: {ticket.movie_name}"
            elif isinstance(ticket, ConcertTicket):
                ticket_info += f"\nArtist: {ticket.artist}"

            self.message_label.configure(text=ticket_info)
        self.clear_entries()


    def buy_ticket(self):
        ticket_id = self.ticket_id_entry.get()
        ticket = self.ticket_manager.getTicket(ticket_id)
        if ticket:
            if isinstance(ticket, TicketAdapter):
                ticket.buyTicket()
                self.master.ticket_subject.notify("Bilet cumpărat")  # Adăugați această linie
                messagebox.showinfo("Succes", "Bilet cumpărat cu succes!")
            else:
                messagebox.showinfo("Succes", "Bilet cumpărat cu succes!")
        self.clear_entries()



    def go_back(self):
        self.withdraw()  # Ascunde fereastra curentă
        self.master.deiconify()  # Face vizibilă fereastra principală


    def clear_entries(self):
        self.ticket_id_entry.delete(0, "end")


if __name__ == "__main__":
    ticket_app = TicketApp()
    ticket_app.mainloop()
