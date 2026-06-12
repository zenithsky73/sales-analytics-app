import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT,
        jenis_kelamin TEXT,
        jabatan TEXT,
        email TEXT,
        username TEXT UNIQUE,
        password TEXT,
        foto_profil TEXT
    )
    """)

    existing_columns = [
        col[1]
        for col in c.execute(
            "PRAGMA table_info(users)"
        ).fetchall()
    ]

    if "jenis_kelamin" not in existing_columns:
        c.execute(
            "ALTER TABLE users ADD COLUMN jenis_kelamin TEXT"
        )

    if "email" not in existing_columns:
        c.execute(
            "ALTER TABLE users ADD COLUMN email TEXT"
        )

    if "foto_profil" not in existing_columns:
        c.execute(
            "ALTER TABLE users ADD COLUMN foto_profil TEXT"
        )

    conn.commit()
    conn.close()


def register_user(nama, jenis_kelamin, jabatan, email, username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    try:
        c.execute(
            """
            INSERT INTO users
            (nama, jenis_kelamin, jabatan, email, username, password)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                nama,
                jenis_kelamin,
                jabatan,
                email,
                username,
                hash_password(password)
            )
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT nama, jabatan
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = c.fetchone()
    conn.close()

    return user

def get_user_profile(username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT nama, jenis_kelamin, jabatan, email, username, foto_profil
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = c.fetchone()
    conn.close()
    return user


def update_user_profile(nama, jenis_kelamin, jabatan, email, foto_profil, username):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        """
        UPDATE users
        SET nama=?, jenis_kelamin=?, jabatan=?, email=?, foto_profil=?
        WHERE username=?
        """,
        (nama, jenis_kelamin, jabatan, email, foto_profil, username)
    )

    conn.commit()
    conn.close()
    return True

def get_user_profile(username):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT
        nama,
        jenis_kelamin,
        jabatan,
        email,
        username,
        foto_profil
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = c.fetchone()

    conn.close()

    return user

def update_user_profile(
    nama,
    jenis_kelamin,
    jabatan,
    email,
    foto_profil,
    username
):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        """
        UPDATE users
        SET
        nama=?,
        jenis_kelamin=?,
        jabatan=?,
        email=?,
        foto_profil=?
        WHERE username=?
        """,
        (
            nama,
            jenis_kelamin,
            jabatan,
            email,
            foto_profil,
            username
        )
    )

    conn.commit()
    conn.close()
    
def change_password(username, old_password, new_password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT password FROM users
        WHERE username=?
        """,
        (username,)
    )

    user = c.fetchone()

    if not user:
        conn.close()
        return False, "User tidak ditemukan."

    if user[0] != hash_password(old_password):
        conn.close()
        return False, "Password lama salah."

    c.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            hash_password(new_password),
            username
        )
    )

    conn.commit()
    conn.close()

    return True, "Password berhasil diubah."

def verify_user_email(username, email):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        """
        SELECT id
        FROM users
        WHERE username=?
        AND email=?
        """,
        (username, email)
    )

    user = c.fetchone()
    conn.close()

    return user is not None


def reset_user_password(username, new_password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            hash_password(new_password),
            username
        )
    )

    conn.commit()
    conn.close()

    return True