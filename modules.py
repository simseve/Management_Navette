from db_func import *
import pytz
import datetime
import uuid


class CreateVehicles:
    def __init__(self, operator, make, plate, vehicle_description):
        self.make = make
        self.plate = plate
        self.vehicle_description = vehicle_description
        self.unique_vehicle_id = str(uuid.uuid1())
        self.operator = operator
        vehicle_creation_time = current_time()

        c.execute("INSERT INTO vehicles (vehicle_id, time, make, operator, plate, description)"
                  " VALUES (?, ?, ?, ?, ?, ?)", (self.unique_vehicle_id, vehicle_creation_time, self.make,
                                                 self.operator.unique_operator_id, self.plate, self.vehicle_description))
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

    def add_bus(self, bus):
        """ Add a Bus to a day when the service is operational """
        self.buses.append(bus.unique_bus_id)

        c.execute("INSERT INTO schedule_bus (day_id, bus_id)"
                  " VALUES (?, ?)", (self.unique_day_id, bus.unique_bus_id))
        db.commit()

    def cancel_bus(self, bus):
        """ Cancel a Bus from a day when the service is operational """
        c.execute("DELETE FROM buses WHERE bus_id = ?", (bus.unique_bus_id, ))
        db.commit()

    def display_day_schedule(self):
        """ Display all the buses listed in a day """
        c.execute("SELECT day, departure_time, make, plate, count(nick_name) FROM grand_summary "
                  "WHERE (day = ?) GROUP BY day, departure_time, make, plate", (self.date, ))
        row = c.fetchall()
        if row:
            print("I have found {} buses on {}".format(len(row), self.date))
            for x in row:
                t1, t2, t3, t4, t5 = x
                print("On date {} at {} the bus {} {} with {} passengers is set for departure".format(t1, t2, t3, t4, t5))
        else:
            print("The bus is not scheduled, not sure why you want to cancel")


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

    def __init__(self, bus_name, departure_time, max_seats, vehicle, bus_description=''):
        self.people = []
        self.departure_time = departure_time
        self.bus_description = bus_description
        self.vehicle = vehicle
        self.bus_name = bus_name
        self.max_seats = max_seats
        self.current_seats = max_seats
        self.unique_bus_id = str(uuid.uuid1())

        bus_creation_time = current_time()

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
    def signout(self, day):
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

        # TODO: Check that email does not exist in database and ask to provide a new name
        c.execute("INSERT INTO pilots (pilot_id, time, first_name, last_name, nick_name, email, phone, description)"
                  " VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (self.unique_pilot_id, pilot_creation_time, self.first_name,
                                                       self.last_name, self.nick_name, self.email, self.phone,
                                                       self.pilot_description))
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


class Operator:
    """ This class represent a Person (in this app is a paraglider pilot).

    Attributes:
        name: name of the pilot

    Methods:
        join_bus: add a pilot to a specific bus
        offload_from_bus: remove a pilot from a specific bus
    """

    def __init__(self, company_name, nick_name, email, phone='', description=''):
        self.company_name = company_name
        self.nick_name = nick_name
        self.email = email
        self.phone = phone
        self.operator_description = description
        self.unique_operator_id = str(uuid.uuid1())

        operator_creation_time = current_time()

        # TODO: Check that email does not exist in database and ask to provide a new name
        c.execute("INSERT INTO operators (operator_id, time, company_name, nick_name, email, phone, description)"
                  " VALUES (?, ?, ?, ?, ?, ?, ?)", (self.unique_operator_id, operator_creation_time, self.company_name,
                                                       self.nick_name, self.email, self.phone,
                                                       self.operator_description))
        db.commit()


def current_time():
    return pytz.utc.localize(datetime.datetime.now())
