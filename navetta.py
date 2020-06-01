from modules import *

# We open a day eg 29/05/2020 for operations
today = DayOfService("29/05/2020", "Today is a beautiful day")
vehicle1 = CreateVehicles("Toyota Hyace", "Vito", "AZ 989 GH", "A beaten Truck")
vehicle2 = CreateVehicles("For Transit", "Vito", "YY 389 HH", "A tough Truck")

bus1 = Bus("Linea 1", "08:00", 4, vehicle1.unique_vehicle_id, "This line is best")
bus2 = Bus("Linea 2", "10:00", 4, vehicle2.unique_vehicle_id, "This line is kind of good")
bus3 = Bus("Linea 3", "14:00", 4, vehicle1.unique_vehicle_id, "This line is for amateur")


pilot1 = Pilot("Simone", "Severini", "severini.simone@gmail.com", "Seve", "+41768050877", "Users created manually")
pilot2 = Pilot("Giorgio", "Mauri",  "severini.simone@gmail.com", "Giorgiuz", "+41768050877", "Users created manually")
pilot3 = Pilot("Ezio", "Rossi",  "severini.simone@gmail.com", "Scintilla", "+41768050877", "Users created manually")
pilot4 = Pilot("Matteo", "Evangelista", "severini.simone@gmail.com", "Anoressico", "+41768050877", "Users created manually")
pilot5 = Pilot("Luca", "Fatebenefratelli", "severini.simone@gmail.com", "Inaffidabile", "+41768050877", "Users created manually")
pilot6 = Pilot("Giulia", "Enrici", "severini.simone@gmail.com", "Finto Svizzero", "+41768050877", "Users created manually")

# Assigning Navette to a day
bus1.join_day(today)
bus2.join_day(today)
bus3.join_day(today)

# Assigning pilots to buses
pilot1.join_bus(bus1)
pilot2.join_bus(bus1)
pilot3.join_bus(bus1)
pilot4.join_bus(bus1)
pilot5.join_bus(bus1)
pilot6.join_bus(bus1)

pilot1.join_bus(bus2)
pilot2.join_bus(bus2)

pilot1.join_bus(bus3)
pilot4.join_bus(bus3)
pilot5.join_bus(bus3)
pilot6.join_bus(bus3)


today.display_day_schedule()
bus1.display_bus_composition()
bus2.display_bus_composition()
bus3.display_bus_composition()

bus1.reschedule("23:30")
today.display_day_schedule()

# bus1.signout(today)
# today.display_day_schedule()

bus1.offload_person(pilot1)
bus1.display_bus_composition()


tomorrow = DayOfService("01/06/2020", "Tomorrow is not a very sunny day")

db.close()
