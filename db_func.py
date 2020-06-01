import sqlite3


def check_email_duplicate(email):
    db_search = sqlite3.connect("test.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
    s = db_search.cursor()
    s.execute("SELECT * FROM pilots WHERE (email = ?)", (email,))
    row = s.fetchall()
    if row:
        print("Email already exists {} times".format(len(row)))
        return True
    else:
        return False
    db_search.close()


a = check_email_duplicate("severini.simone@gmail.com")

