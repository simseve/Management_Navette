import sqlite3

db = sqlite3.connect("test.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
c = db.cursor()
print("Connected to SQLite")

# Creating tables

c.execute("CREATE TABLE IF NOT EXISTS vehicles (vehicle_id TEXT PRIMARY KEY, time TIMESTAMP NOT NULL, "
          "make TEXT NOT NULL, operator TEXT, plate TEXT NOT NULL, description TEXT)")

c.execute("CREATE TABLE IF NOT EXISTS operators (operator_id TEXT PRIMARY KEY, time TIMESTAMP NOT NULL, "
          "company_name TEXT NOT NULL, nick_name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT, description TEXT)")

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
