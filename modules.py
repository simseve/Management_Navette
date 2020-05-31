class DayOfService:
    """ This class represent a day when buses will be scheduled

    Attributes:
        date: the date of the day when the service will be operational

    Methods:
        _add_bus: add a Bus to the schedule
        _cancel_bus: remove a Bus from the schedule
        display_day_schedule: Display the schedule of a day
    """

    def __init__(self, date):
        self.date = date
        self.buses = []

    def _add_bus(self, bus_name):
        """ Add a Bus to a day when the service is operational """
        self.buses.append(bus_name)

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
                print(self.buses[i].bus_id + "\t\t" + self.buses[i].time)
        else:
            print("\t\tNo bus are scheduled")
        print("=" * 80)


class Bus:
    """ This class represent a Bus.

    Attributes:
        bus_id {string}: the name of the line.
        time: the time of departure
        max_seats: max number of seats

    Methods:
        _add_person: Load a passenger onto the bus
        _offload_person: Offload a person from the bus
        join_day: Add the bus to the day of service
        signoout: cancel a bus service from a certain date
        display_bus_composition: print out the passenger list
    """

    def __init__(self, bus_id, time, max_seats):
        self.people = []
        self.time = time
        self.bus_id = bus_id
        self.max_seats = max_seats
        self.current_seats = max_seats

    def _add_person(self, person):
        self.people.append(person)

    def _offload_person(self, person):
        if person in self.people:
            self.people.remove(person)
        else:
            print("Pilot does not exist")
            return False

    def join_day(self, day):
        self.day = day
        day._add_bus(self)
        print("Bus {} has joined {}".format(self.bus_id, self.day.date))

    def signout(self, day):
        self.day = day
        if day._cancel_bus(self):
            print("Bus {} has been cancelled on {}".format(self.bus_id, self.day.date))

    def display_bus_composition(self):
        print("\n\n\n")
        print("=" * 80)
        print("This is the composition for bus {}".format(self.bus_id))
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
    def __init__(self, name):
        self.name = name

    def join_bus(self, bus):
        self.bus = bus
        if self.bus.current_seats > 0:
            self.bus.current_seats -= 1
            bus._add_person(self)
            print("\n\nPilot {} has joined bus {}".format(self.name, self.bus.bus_id))
        else:
            print("\n\nThe bus {} is full and pilot {} is not added".format(self.bus.bus_id, self.name))

    def offload_from_bus(self, bus):
        self.bus = bus
        self.bus.current_seats += 1
        if bus._offload_person(self):
            print("\n\nPilot {} has been offloaded from bus {}".format(self.name, self.bus.bus_id))

