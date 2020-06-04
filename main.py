from models.buses import *
from models.day_of_service import *
from models.operators import *
from models.pilots import *
from models.vehicles import *

# We open a day eg 29/05/2020 for operations
today = DayOfService("29/05/2020", "Today is a beautiful day")

# Create an operator eg Vito
operator1 = Operator("VLLM", "Vito", "Vito@email.com", "+390768050877", "A good guy", "operator1_username",
                     "operator2_password")

vehicle1 = Vehicles(operator1, "Toyota Hyace", "AZ 989 GH", "A beaten Truck")
vehicle2 = Vehicles(operator1, "For Transit", "YY 389 HH", "A tough Truck")

bus1 = Bus("Linea 1", "08:00", 4, vehicle1, "This line is best")
bus2 = Bus("Linea 2", "10:00", 4, vehicle2, "This line is kind of good")
bus3 = Bus("Linea 3", "14:00", 4, vehicle1, "This line is for amateur")


pilot1 = Pilot("Simone", "Severini", "email_1@email.com", "Seve", "+41768050877", "Users created manually",
               "pilot1_username", "pilot1_password")
pilot2 = Pilot("Giorgio", "Mauri",  "email_2@email.com", "Giorgiuz", "+41768050877", "Users created manually",
               "pilot2_username", "pilot2_password")
pilot3 = Pilot("Ezio", "Rossi",  "email_3@email.com", "Scintilla", "+41768050877", "Users created manually",
               "pilot3_username", "pilot3_password")
pilot4 = Pilot("Matteo", "Evangelista", "email_4@email.com", "Anoressico", "+41768050877",
               "Users created manually", "pilot4_username", "pilot4_password")
pilot5 = Pilot("Luca", "Fatebenefratelli", "email_5@email.com", "Inaffidabile", "+41768050877",
               "Users created manually", "pilot5_username", "pilot5_password")
pilot6 = Pilot("Giulia", "Enrici", "email_6@email.com", "Finto Svizzero", "+41768050877",
               "Users created manually", "pilot6_username", "pilot6_password")

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

# bus1.sign_out(today)
# today.display_day_schedule()

bus1.offload_person(pilot1)
bus1.display_bus_composition()


tomorrow = DayOfService("01/06/2020", "Tomorrow is not a very sunny day")

db.close()
