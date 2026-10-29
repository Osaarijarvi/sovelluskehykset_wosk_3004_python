
# repositories/users_sqlite_repository.py

from models import User


class UsersSQLiteRepository:

    def __init__(self, con):
        self.connection = con

    def all(self):

        cur = self.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        users_list = []

        for user in users:
            users_list.append(User(user[1], user[2], user[3], user[0]))
        return users_list

    def get_by_id(self, _id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (_id,))
        user = cursor.fetchone()
        cursor.close()
        if user is None:
            return None
        return User(user[1], user[2], user[3], user[0])

    def _add(self, first_name, last_name, username):

        cur = self.connection.cursor()
        cur.execute("INSERT INTO users(first_name, last_name, username) VALUES(?, ?, ?)",
                    (first_name, last_name, username))
        self.connection.commit()
        _id = cur.lastrowid
        cur.close()

        return User(first_name, last_name, username, _id)

    def _update(self, first_name, last_name, username, _id):
        user = self.get_by_id(_id)
        # jos käyttäjää ei löydy, ei päivitetä mitään
        if user is None:
            return None

        cur = self.connection.cursor()
        cur.execute("UPDATE users SET first_name = ?, last_name = ?, username = ? WHERE id = ?",
                    (first_name, last_name, username, _id))
        self.connection.commit()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        cur.close()

        return user

    def save(self, first_name, last_name, username, user_id=None):

        if user_id is None:
            return self._add(first_name, last_name, username)

        else:
            return self._update(first_name, last_name, username, user_id)

    def remove_by_id(self, _id):
        cur = self.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (_id,))
        self.connection.commit()
        rows_affected = cur.rowcount
        cur.close()
        return rows_affected == 1