import sqlite3
import uuid
import pytz
import datetime


db = sqlite3.connect("data.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
c = db.cursor()


class Bus:
    """ This class represent a Bus.

    Attributes:
        bus_name (string): the name of the line.
        time (str): the time of departure in local time
        max_seats (integer): max number of seats
        vehicle (object): The Vehicle object
        bus_description (str): a free field for a description

    Methods:
        add_person: Load a passenger onto the bus
        offload_person: Offload a passenger from the bus
        join_day: Add the bus to the day of service
        sign_out: Remove a bus service from a certain date
        display_bus_composition: print out the passenger list
        reschedule: Reschedule the timpe of departure to a new time
    """

    @staticmethod
    def current_time():
        return pytz.utc.localize(datetime.datetime.now())

    def __init__(self, bus_name, departure_time, max_seats, vehicle, bus_description=''):
        self.people = []
        self.departure_time = departure_time
        self.bus_description = bus_description
        self.vehicle = vehicle
        self.bus_name = bus_name
        self.max_seats = max_seats
        self.current_seats = max_seats
        self.unique_bus_id = str(uuid.uuid1())

        bus_creation_time = Bus.current_time()

        # TODO 2 or more buses with same vehicle_id cannot leave at same time
        c.execute("INSERT INTO buses (bus_id, time, departure_time, bus_name, max_seats, vehicle_id, description) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (self.unique_bus_id, bus_creation_time, self.departure_time, self.bus_name, self.max_seats,
                   self.vehicle.unique_vehicle_id, self.bus_description))

        db.commit()

    def add_person(self, person):
        self.people.append(person)
        c.execute("INSERT INTO schedule_pilots (bus_id, pilot_id)"
                  " VALUES (?, ?)", (self.unique_bus_id, person.unique_pilot_id))
        db.commit()

    def offload_person(self, person):
        # add a select to verify that exists
        c.execute("DELETE FROM schedule_pilots WHERE pilot_id = ?", (person.unique_pilot_id, ))
        db.commit()
        # if person in self.people:
        #     self.people.remove(person)
        # else:
        #     print("Pilot does not exist")
        #     return False

    def join_day(self, day):
        self.day = day
        day.add_bus(self)
        print("Bus {} with ID {} has joined {} with id {}".format(self.bus_name, self.unique_bus_id,
                                                                  self.day.date, day.unique_day_id))
    def sign_out(self, day):
        self.day = day
        day.cancel_bus(self)

    def display_bus_composition(self):
        c.execute("SELECT make, plate, departure_time, nick_name FROM display_bus_composition "
                  "WHERE (bus_id = ?)", (self.unique_bus_id, ))
        row = c.fetchall()
        if row:
            print("I have found {} pilots on {}".format(len(row), self.bus_name))
            for x in row:
                t1, t2, t3, t4 = x
                print("Bus {} with plate {} due at {} has got pilot {} confirmed".format(t1, t2, t3, t4))
        else:
            print("No bus are scheduled")

    def reschedule(self, new_time: str):
        self.time = new_time
        c.execute("UPDATE buses SET departure_time = ? WHERE bus_id = ?", (self.time, self.unique_bus_id))
