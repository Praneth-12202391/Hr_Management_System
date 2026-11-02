import sqlite3

conn = sqlite3.connect(r'D:\H2\MAnaging Portal\backend\data\talentpulse.db')
cursor = conn.cursor()

cursor.execute('PRAGMA table_info(users);')
cols = [row[1] for row in cursor.fetchall()]
print('Current columns in users table:', cols)

if 'initial_password' not in cols:
    cursor.execute('ALTER TABLE users ADD COLUMN initial_password VARCHAR(255);')
    print('Added initial_password column.')

cursor.execute("UPDATE users SET initial_password = 'Superadmin123!' WHERE role = 'superadmin';")
cursor.execute("UPDATE users SET initial_password = 'Admin123!' WHERE role = 'admin';")
cursor.execute("UPDATE users SET initial_password = 'Hr123!' WHERE role = 'hr';")
cursor.execute("UPDATE users SET initial_password = 'Manager123!' WHERE role = 'manager';")
cursor.execute("UPDATE users SET initial_password = 'Employee123!' WHERE role = 'employee';")
conn.commit()

cursor.execute('SELECT email, role, initial_password FROM users LIMIT 6;')
for row in cursor.fetchall():
    print(row)
conn.close()
