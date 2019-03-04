import sqlite3
from client import get_localTime, get_gpggsMessage

for i in range(10)
db_conn = sqlite3.connect('gpsDB.db')
db_c = db_conn.cursor()
print("Open SQLite3 success")

local_time = get_localTime()
gpggs_message = get_gpggsMessage()

db_c.execute(
    "INSERT INTO GPS (ID,GPS,time) VALUES (NULL,'%s','%s')" % (gpggs_message, local_time))
db_conn.commit()
print("Insert Success")
db_conn.close()
