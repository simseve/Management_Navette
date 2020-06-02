import sqlite3
import uuid
import pytz
import datetime


try:
    db = sqlite3.connect("data.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
    c = db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to SQLite 3", error)


class DayOfService:
    """ This class represent a day when buses will be scheduled

    Attributes:
        date (str): the date of the day when the service will be operational
        day_description (str):  a description of the day when Bus will be circulating

    Methods:
        add_bus: add a Bus to the schedule
        cancel_bus: remove a Bus from the schedule
        display_day_schedule: Display the schedule of a day
    """

    @staticmethod
    def current_time():
        return pytz.utc.localize(datetime.datetime.now())

    def __init__(self, date, day_description=''):
        self.date = date
        self.buses = []
        self.day_description = day_description
        self.unique_day_id = str(uuid.uuid1())
        day_creation_time = DayOfService.current_time()

        c.execute("SELECT * FROM days_of_service WHERE day=?", (self.date,))
        row = c.fetchone()
        if row:
            print("Day of service already present in database")
        else:
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
            print("The day schedule is EMPTY")

