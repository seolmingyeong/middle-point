import sqlite3


DB_NAME = "meeting.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            room_id TEXT PRIMARY KEY
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id TEXT,
            nickname TEXT,
            available_dates TEXT,
            location_name TEXT,
            lat REAL,
            lng REAL,
            transport TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def create_room(room_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO rooms (room_id) VALUES (?)",
        (room_id,)
    )

    conn.commit()
    conn.close()


def room_exists(room_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM rooms WHERE room_id=?",
        (room_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_user(
    room_id,
    nickname,
    available_dates,
    location_name,
    lat,
    lng,
    transport
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # 같은 닉네임 기존 데이터 삭제

    cursor.execute(
        """
        DELETE FROM users
        WHERE room_id=?
        AND nickname=?
        """,
        (room_id, nickname)
    )

    cursor.execute(
        """
        INSERT INTO users (
            room_id,
            nickname,
            available_dates,
            location_name,
            lat,
            lng,
            transport
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            room_id,
            nickname,
            available_dates,
            location_name,
            lat,
            lng,
            transport
        )
    )

    conn.commit()
    conn.close()


def get_room_users(room_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE room_id=?",
        (room_id,)
    )

    users = cursor.fetchall()

    conn.close()

    return users