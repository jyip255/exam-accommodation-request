import sqlite3

conn = sqlite3.connect('exam_requests.db')

conn.execute("ALTER TABLE examrequest DELETE COLUMN DATE")

conn.commit()
conn.close()