import sqlite3
from client import get

db_conn = sqlite3.connect('gpsDB.db')
db_c = db_conn.cursor()
print("Open SQLite3 success")

local_time = get_localTime()
gpggs_message = get_gpggsMessage()

db_c.execute("INSERT INTO GPS (ID,GPS,time) VALUES (, gpggs_message,local_time)")