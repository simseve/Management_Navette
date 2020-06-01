import sqlite3
import pytz
import datetime
import uuid
# import db_func

from sqlite3 import Error

db = sqlite3.connect("test.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
c = db.cursor()

# Creating tables

c.execute("CREATE TABLE IF NOT EXISTS vehicles (vehicle_id TEXT PRIMARY KEY, time TIMESTAMP NOT NULL, "
          "make TEXT NOT NULL, operator TEXT, plate TEXT NOT NULL, description TEXT)" )

c.execute("CREATE TABLE IF NOT EXISTS days_of_service (day_id TEXT PRIMARY KEY, "
          "time TIMESTAMP NOT NULL, day TEXT NOT NULL, description TEXT)")

c.execute("CREATE TABLE IF NOT EXISTS buses (bus_id TEXT PRIMARY KEY, "
          "time TIMESTAMP TEXT NOT NULL, bus_name TEXT NOT NULL, departure_time TEXT NOT NULL, "
          "max_seats INTEGER NOT NULL, vehicle_id TEXT NOT NULL, description TEXT)")

c.execute("CREATE TABLE IF NOT EXISTS pilots (pilot_id TEXT PRIMARY KEY, "
          "time TIMESTAMP NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL, "
          "nick_name TEXT, email TEXT NOT NULL,phone TEXT, description TEXT)")

c.execute("CREATE TABLE IF NOT EXISTS schedule_bus (day_id TEXT, bus_id TEXT)")

c.execute("CREATE TABLE IF NOT EXISTS schedule_pilots (bus_id TEXT, pilot_id TEXT)")


# Creating views
c.execute("CREATE VIEW IF NOT EXISTS display_bus_composition AS SELECT vehicles.make, vehicles.plate ,buses.bus_name, "
          "buses.departure_time, pilots.nick_name, buses.bus_id, pilots.pilot_id  FROM schedule_pilots "
          "INNER JOIN buses ON buses.bus_id = schedule_pilots.bus_id INNER JOIN pilots ON "
          "pilots.pilot_id = schedule_pilots.pilot_id INNER JOIN vehicles ON buses.vehicle_id = vehicles.vehicle_id")

c.execute("CREATE VIEW IF NOT EXISTS display_day_composition AS SELECT days_of_service.day, "
          "buses.bus_name, schedule_bus.day_id, schedule_bus.bus_id FROM schedule_bus INNER JOIN days_of_service ON "
          "days_of_service.day_id = schedule_bus.day_id INNER JOIN buses ON buses.bus_id = schedule_bus.bus_id")

c.execute("CREATE VIEW IF NOT EXISTS grand_summary AS SELECT display_day_composition.day, "
          "display_bus_composition.departure_time, display_bus_composition.make, display_bus_composition.plate,  "
          "display_bus_composition.nick_name FROM display_day_composition "
          "INNER JOIN display_bus_composition ON display_bus_composition.bus_id = display_day_composition.bus_id")


class CreateVehicles:
    def __init__(self, make, operator, plate, vehicle_description):
        self.make = make
        self.operator = operator
        self.plate = plate
        self.vehicle_description = vehicle_description
        self.unique_vehicle_id = str(uuid.uuid1())
        vehicle_creation_time = current_time()

        c.execute("INSERT INTO vehicles (vehicle_id, time, make, operator, plate, description)"
                  " VALUES (?, ?, ?, ?, ?, ?)", (self.unique_vehicle_id, vehicle_creation_time, self.make,
                                                       self.operator, self.plate, self.vehicle_description))
        db.commit()


class DayOfService:
    """ This class represent a day when buses will be scheduled

    Attributes:
        date: the date of the day when the service will be operational

    Methods:
        _add_bus: add a Bus to the schedule
        _cancel_bus: remove a Bus from the schedule
        display_day_schedule: Display the schedule of a day
    """

    def __init__(self, date, day_description=''):
        self.date = date
        self.buses = []
        self.day_description = day_description
        self.unique_day_id = str(uuid.uuid1())
        day_creation_time = current_time()

        # TODO: Check that name does not exist in database and ask to provide a new name
        c.execute("INSERT INTO days_of_service (day_id, time, day, description) VALUES (?, ?, ?, ?)",
                  (self.unique_day_id, day_creation_time, self.date, self.day_description))
        db.commit()

    def add_bus(self, bus_id):
        """ Add a Bus to a day when the service is operational """
        self.buses.append(bus_id.unique_bus_id)

        c.execute("INSERT INTO schedule_bus (day_id, bus_id)"
                  " VALUES (?, ?)", (self.unique_day_id, bus_id.unique_bus_id))
        db.commit()

    def _cancel_bus(self, bus_name):
        """ Cancel a Bus from a day when the service is operational """
        if bus_name in self.buses:
            self.buses.remove(bus_name)
        else:
            print("The bus is not found in daily schedule")
            return False

    def display_day_schedule(self):
        """ Display all the buses listed in a day """
        print("\n\n\n")
        if len(self.buses) > 0:
            print("=" * 80)
            print("This are all the buses we have on {}".format(self.date))
            for i in range(len(self.buses)):
                print(self.buses[i].bus_name + "\t\t" + self.buses[i].time)
        else:
            print("\t\tNo bus are scheduled")
        print("=" * 80)


class Bus:
    """ This class represent a Bus.

    Attributes:
        bus_name {string}: the name of the line.
        time: the time of departure
        max_seats: max number of seats

    Methods:
        _add_person: Load a passenger onto the bus
        _offload_person: Offload a person from the bus
        join_day: Add the bus to the day of service
        signoout: cancel a bus service from a certain date
        display_bus_composition: print out the passenger list
    """

    def __init__(self, bus_name, departure_time, max_seats, vehicle_id, bus_description=''):
        self.people = []
        self.departure_time = departure_time
        self.bus_description = bus_description
        self.vehicle_id = vehicle_id
        self.bus_name = bus_name
        self.max_seats = max_seats
        self.current_seats = max_seats
        self.unique_bus_id = str(uuid.uuid1())

        bus_creation_time = current_time()

        # TODO: Check that name does not exist in database and ask to provide a new name
        c.execute("INSERT INTO buses (bus_id, time, departure_time, bus_name, max_seats, vehicle_id, description) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (self.unique_bus_id, bus_creation_time, self.departure_time, self.bus_name, self.max_seats,
                   self.vehicle_id, self.bus_description))

        db.commit()

    def _add_person(self, person):
        self.people.append(person)
        c.execute("INSERT INTO schedule_pilots (bus_id, pilot_id)"
                  " VALUES (?, ?)", (self.unique_bus_id, person.unique_pilot_id))
        db.commit()

    def _offload_person(self, person):
        if person in self.people:
            self.people.remove(person)
        else:
            print("Pilot does not exist")
            return False

    def join_day(self, day):
        self.day = day
        day.add_bus(self)
        print("Bus {} with ID {} has joined {} with id {}".format(self.bus_name, self.unique_bus_id,
                                                                  self.day.date, day.unique_day_id))

    def signout(self, day):
        self.day = day
        if day._cancel_bus(self):
            print("Bus {} has been cancelled on {}".format(self.bus_name, self.day.date))

    def display_bus_composition(self):
        print("\n\n\n")
        print("=" * 80)
        print("This is the composition for bus {}".format(self.bus_name))
        if len(self.people) > 0:
            for i in range(len(self.people)):
                print(self.people[i].name)
        else:
            print("\t\tThe bus hasn't got any passengers")
        print("=" * 80)

    def reschedule(self, new_time: str):
        self.time = new_time


class Pilot:
    """ This class represent a Person (in this app is a paraglider pilot).

    Attributes:
        name: name of the pilot

    Methods:
        join_bus: add a pilot to a specific bus
        offload_from_bus: remove a pilot from a specific bus
    """

    def __init__(self, first_name, last_name, email, nick_name='', phone='', description=''):
        self.first_name = first_name
        self.last_name = last_name
        self.nick_name = nick_name
        self.email = email
        self.phone = phone
        self.pilot_description = description
        self.unique_pilot_id = str(uuid.uuid1())

        pilot_creation_time = current_time()

        # TODO: Check that name does not exist in database and ask to provide a new name
        c.execute("INSERT INTO pilots (pilot_id, time, first_name, last_name, nick_name, email, phone, description)"
                  " VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (self.unique_pilot_id, pilot_creation_time, self.first_name,
                                                       self.last_name, self.nick_name, self.email, self.phone,
                                                       self.pilot_description))
        db.commit()

    def join_bus(self, bus):
        self.bus = bus
        if self.bus.current_seats > 0:
            self.bus.current_seats -= 1
            bus._add_person(self)
            print("\n\nPilot {} with ID {} has joined bus {} with ID {}".
                  format(self.unique_pilot_id, self.nick_name, self.bus.bus_name, bus.unique_bus_id))

        else:
            print("\n\nThe bus {} is full and pilot {} is not added".format(self.bus.bus_name, self.last_name))

    def offload_from_bus(self, bus):
        self.bus = bus
        self.bus.current_seats += 1
        if bus._offload_person(self):
            print("\n\nPilot {} has been offloaded from bus {}".format(self.last_name, self.bus.bus_name))


def current_time():
    return pytz.utc.localize(datetime.datetime.now())
