class DayOfService:
    def __init__(self, date):
        self.date = date
        self.buses = []

    def add_bus(self, bus_name):
        self.buses.append(bus_name)

    def display_day_schedule(self):
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
    def __init__(self, bus_id, time, max_seats):
        self.people = []
        self.time = time
        self.bus_id = bus_id
        self.max_seats = max_seats
        self.current_seats = max_seats

    def add_person(self, person):
        self.people.append(person)

    def offload_person(self, person):
        if person in self.people:
            self.people.remove(person)
        else:
            print("Pilot does not exist")
            return False

    def join_day(self, day):
        self.day = day
        day.add_bus(self)
        print("Bus {} has joined {}".format(self.bus_id, self.day.date))

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

class Pilot:
    def __init__(self, name):
        self.name = name

    def join_bus(self, bus):
        self.bus = bus
        if self.bus.current_seats > 0:
            self.bus.current_seats -= 1
            bus.add_person(self)
            print("\n\nPilot {} has joined bus {}".format(self.name, self.bus.bus_id))
        else:
            print("\n\nThe bus {} is full and pilot {} is not added".format(self.bus.bus_id, self.name))

    def offload_from_bus(self, bus):
        self.bus = bus
        self.bus.current_seats += 1
        a = bus.offload_person(self)
        if a is not False:
            print("\n\nPilot {} has been offloaded from bus {}".format(self.name, self.bus.bus_id))

