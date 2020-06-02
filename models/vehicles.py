import sqlite3
import uuid
import pytz
import datetime

db = sqlite3.connect("data.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
c = db.cursor()


class Vehicles:
    """ This class represent a vehicle to transport pilots

    Attributes:
        operator (object): this is a object that represent the company that operates the vehicle
        make (str): The make and model of the vehicle
        plate (str): The plate number of the vehicle
        vehicle_description (str): A free description field

    """

    @staticmethod
    def current_time():
        return pytz.utc.localize(datetime.datetime.now())

    def __init__(self, operator, make, plate, vehicle_description):
        self.make = make
        self.plate = plate
        self.vehicle_description = vehicle_description
        self.unique_vehicle_id = str(uuid.uuid1())
        self.operator = operator

        vehicle_creation_time = Vehicles.current_time()

        c.execute("INSERT INTO vehicles (vehicle_id, time, make, operator, plate, description)"
                  " VALUES (?, ?, ?, ?, ?, ?)", (self.unique_vehicle_id, vehicle_creation_time, self.make,
                                                 self.operator.unique_operator_id, self.plate, self.vehicle_description))
        db.commit()
