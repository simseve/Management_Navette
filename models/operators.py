import sqlite3
import uuid
import pytz
import datetime

try:
    db = sqlite3.connect("data.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
    c = db.cursor()
except sqlite3.Error as error:
    print("Error while connecting to SQLite 3", error)


class Operator:
    """ This class represent a bus Operator as the company owner

    Attributes:
        company_name (str): name of the owner company
        nick_name (str): easy to remember name associated with the operator
        email (str): email of the operator
        phone (str): phone number
        description (str): a field for a description of the operator
        username (str): username of the pilot
        password: pw of the pilot

    Methods:
        join_bus: add a pilot to a specific bus
        offload_from_bus: remove a pilot from a specific bus
    """

    @staticmethod
    def current_time():
        return pytz.utc.localize(datetime.datetime.now())

    def __init__(self, company_name, nick_name, email, phone='', description='', username='', password=''):
        self.company_name = company_name
        self.nick_name = nick_name
        self.email = email
        self.phone = phone
        self.operator_description = description
        self.unique_operator_id = str(uuid.uuid1())
        self.username = username
        self.password = password

        operator_creation_time = Operator.current_time()

        c.execute("SELECT * FROM operators WHERE email=? OR username=?", (self.email, self.username))
        row = c.fetchone()
        if row:
            print("Operator's Username or Email already present in database")
        else:
            c.execute("INSERT INTO operators (operator_id, time, company_name, nick_name, email, phone, description,"
                      " username, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.unique_operator_id,
                                                                                  operator_creation_time, self.company_name,
                                                                                  self.nick_name, self.email, self.phone,
                                                                                  self.operator_description, self.username,
                                                                                  self.password))
            db.commit()
