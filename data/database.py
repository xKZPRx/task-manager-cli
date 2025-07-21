import sqlite3


def create_connection():
    conn = sqlite3.connect("data\\task_manager.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            list_id INTEGER,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (list_id) REFERENCES tasks_lists(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def get_list_id(list_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks_lists WHERE name=?", (list_name,))
    list_id = cursor.fetchone()[0]
    return list_id


def add_list_todb(list_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks_lists (name) VALUES (?)", (list_name,))
    conn.commit()
    conn.close()


def add_task_todb(list_name, task_title):
    conn = create_connection()
    cursor = conn.cursor()
    list_id = get_list_id(list_name)

    cursor.execute("INSERT INTO tasks (list_id, title, completed) VALUES (?, ?, 0)", (list_id, task_title))
    conn.commit()
    conn.close()


def get_lists_names_fromdb():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM tasks_lists")
    result = cursor.fetchall()

    conn.close()
    return[lists_names[0] for lists_names in result]


def get_tasks_titles_fromdb(list_name):
    conn = create_connection()
    cursor = conn.cursor()

    list_id = get_list_id(list_name)

    cursor.execute("SELECT title FROM tasks WHERE list_id=?", (list_id,))
    result = cursor.fetchall()

    conn.close()
    return [tasks_titles[0] for tasks_titles in result]


def remove_list_fromdb(list_name):
    conn = create_connection()
    cursor = conn.cursor()

    list_id = get_list_id(list_name)
    cursor.execute("DELETE FROM tasks_lists WHERE id=?", (list_id,))

    conn.commit()
    conn.close()


def remove_task_fromdb(list_name, task_title):
    conn = create_connection()
    cursor = conn.cursor()

    list_id = get_list_id(list_name)

    cursor.execute("DELETE FROM tasks WHERE list_id=? AND title=?", (list_id, task_title))

    conn.commit()
    conn.close()