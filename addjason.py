import sqlite3

conn = sqlite3.connect('exam_requests.db')

conn.execute("ALTER TABLE examrequest ADD COLUMN FILE_PATH")

conn.commit()
conn.close()
