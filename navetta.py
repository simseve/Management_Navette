from modules import *

# We open a day eg 29/05/2020 for operations
today = DayOfService("29/05/2020", "Today is a beautiful day")
vehicle1 = CreateVehicles("Toyota Hyace", "Vito", "AZ 989 GH", "A beaten Truck")
vehicle2 = CreateVehicles("For Transit", "Vito", "YY 389 HH", "A tough Truck")

bus1 = Bus("Linea 1", "10:00", 4, vehicle1.unique_vehicle_id, "This line is best")
bus2 = Bus("Linea 2", "12:00", 4, vehicle2.unique_vehicle_id, "This line is kind of good")
bus3 = Bus("Linea 3", "08:00", 4, vehicle1.unique_vehicle_id, "This line is for amateur")


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
pilot6.join_bus(bus3)

pilot4.join_bus(bus3)
pilot5.join_bus(bus3)
pilot1.join_bus(bus3)


tomorrow = DayOfService("01/06/2020", "Tomorrow is not a very sunny day")

# # Display the schedule of a single day
# today.display_day_schedule()
#
# # Load pilots into the bus on a specific time
# pilot1.join_bus(bus1)
# pilot2.join_bus(bus1)
# pilot3.join_bus(bus1)
# pilot4.join_bus(bus1)
#
# # Display the current composition status of the navetta
# bus1.display_bus_composition()
#
# # Add a new pilot to the navetta (exceed max seats)
# pilot5.join_bus(bus1)
# bus1.display_bus_composition()
#
# # Offload an existing pilot from the navetta
# pilot4.offload_from_bus(bus1)
# bus1.display_bus_composition()
#
# # Add a new pilot to the navetta
# pilot5.join_bus(bus1)
# bus1.display_bus_composition()
#
# # Try to offload a use tha is not currently on the navetta
# pilot4.offload_from_bus(bus1)
# bus1.display_bus_composition()
#
# # Offload all
# pilot1.offload_from_bus(bus1)
# pilot2.offload_from_bus(bus1)
# pilot3.offload_from_bus(bus1)
# pilot5.offload_from_bus(bus1)
#
# # Display bus composition
# bus1.display_bus_composition()
#
# # Cancel a Navetta in a specific day
# bus1.signout(today)
#
# # Display the schedule of a single day
# today.display_day_schedule()
#
# # Cancel a navetta
# # bus1.signout(today)
#
# bus2.reschedule("10:25")
# bus2.display_bus_composition()
# today.display_day_schedule()
#
#
