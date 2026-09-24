import bcrypt
import psycopg2

# Unganisha na database
conn = psycopg2.connect(
    host="dpg-danrpi942hec73fgj0eg-a.frankfurt-postgres.render.com",
    dbname="masterlexicon",
    user="masterlexicon_user",
    password="KTiyEbF5F6KbhQYp3EOB9fD0OSN7UgDb"
)

cur = conn.cursor()

# Futa admin wa zamani
cur.execute("DELETE FROM admin_users;")

# Unda admin mpya kwa bcrypt hash
password = "admin123"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
cur.execute("INSERT INTO admin_users (username, password_hash) VALUES (%s, %s)", ("admin", hashed))

conn.commit()
cur.close()
conn.close()

print("✅ Admin reset successfully!")
