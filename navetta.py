from modules import *

# Open up a day for scheduling Navette
today = DayOfService("29/05/2020")

# Create how many navette we plan to schedule in a day and at what time. Specify also max number of seats
bus1 = Bus("Linea 1", "10:00", 4)
bus2 = Bus("Linea 2", "12:00", 4)
bus3 = Bus("Linea 3", "16:00", 4)

# Create pilots
pilot1 = Pilot("Simone")
pilot2 = Pilot("Giorgio")
pilot3 = Pilot("Musica")
pilot4 = Pilot("Giulia")
pilot5 = Pilot("Nicole")
pilot6 = Pilot("Carol")

# Schedule Navette to a specific day
bus1.join_day(today)
bus2.join_day(today)
bus3.join_day(today)

# Display the schedule of a single day
today.display_day_schedule()

# Load pilots into the bus on a specific time
pilot1.join_bus(bus1)
pilot2.join_bus(bus1)
pilot3.join_bus(bus1)
pilot4.join_bus(bus1)

# Display the current compsition status of the navetta
bus1.display_bus_composition()

# Add a new pilot to the navetta (exceed max seats)
pilot5.join_bus(bus1)
bus1.display_bus_composition()

# Offload an existing pilot from the navetta
pilot4.offload_from_bus(bus1)
bus1.display_bus_composition()

# Add a new pilot to the navetta
pilot5.join_bus(bus1)
bus1.display_bus_composition()

# Try to offload a use tha is not currently on the navetta
pilot4.offload_from_bus(bus1)
bus1.display_bus_composition()

# Offload all
pilot1.offload_from_bus(bus1)
pilot2.offload_from_bus(bus1)
pilot3.offload_from_bus(bus1)
pilot5.offload_from_bus(bus1)

# Display bus composition
bus1.display_bus_composition()
