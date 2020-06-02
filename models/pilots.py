import sqlite3
import uuid
import pytz
import datetime

db = sqlite3.connect("data.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
c = db.cursor()


class Pilot:
    """ This class represent a passenger (in this app is a paraglider pilot).

    Attributes:
        first_name (str): first name of the passenger
        last_name (str): last name of the passenger
        email (str): email of the passenger
        nick_name (str): nick name of the passenger
        phone (str): phone number of the passenger
        description (str): description of the passenger
        username (str): username of the pilot
        password: pw of the pilot
    Methods:
        join_bus: add a pilot to a specific bus
        offload_from_bus: remove a pilot from a specific bus
    """

    @staticmethod
    def current_time():
        return pytz.utc.localize(datetime.datetime.now())

    def __init__(self, first_name, last_name, email, nick_name='', phone='', description='', username='', password=''):
        self.first_name = first_name
        self.last_name = last_name
        self.nick_name = nick_name
        self.email = email
        self.phone = phone
        self.pilot_description = description
        self.unique_pilot_id = str(uuid.uuid1())
        self.username = username
        self.password = password

        pilot_creation_time = Pilot.current_time()

        # TODO: Check that email does not exist in database and ask to provide a new name
        c.execute("INSERT INTO pilots (pilot_id, time, first_name, last_name, nick_name, email, phone, description,"
                  " username, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (self.unique_pilot_id, pilot_creation_time, self.first_name, self.last_name, self.nick_name,
                   self.email, self.phone, self.pilot_description, self.username, self.password))
        db.commit()

    def join_bus(self, bus):
        self.bus = bus
        if self.bus.current_seats > 0:
            self.bus.current_seats -= 1
            bus.add_person(self)
            print("Pilot {} with ID {} has joined bus {} with ID {}".
                  format(self.unique_pilot_id, self.nick_name, self.bus.bus_name, bus.unique_bus_id))
        else:
            print("The bus {} is full and pilot {} is not added".format(self.bus.bus_name, self.nick_name))

    def offload_from_bus(self, bus):
        self.bus = bus
        self.bus.current_seats += 1
        bus.offload_person(self)
        print("Pilot {} has been offloaded from bus {}".format(self.last_name, self.bus.bus_name))



