import sqlite3

from custom_exceptions.not_found_exception import NotFoundException


class User:
    def __init__(self, firstname, lastname, username, _id=None):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self._id = _id



    @staticmethod
    def get_all():
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            cur.close()
            users_list = []
            # Huomaa, että model classin metodi ei palauta hakutulosta suoraan json-formaatissa
            # Meidän pitää pystyä käyttämään samaa koodia riippumatta siitä,
            # haluaako käyttäjä vastauksen html, json- tai xml-formaatissa

            # Jos päättäisimme responsen formaatin modelissa,
            # joutuisimme tekemään uuden model-luokan metodin eri
            # dataformaateille.
            # Modelin tehtävä ei ole päättää tästä.
            # MODEL TOIMII TIETOMALLINA ja DATA ACCESS LAYERINÄ
            # ELI TULKKINA CONTROLLERIN JA TIETOKANNAN VÄLISSÄ

            for user in users:
                users_list.append(User(user[1], user[2], user[3], _id=user[0]))

            return users_list

    def save(self):
        if self._id is None:
            self._insert()
        else:
            self._update()

    @staticmethod
    def get_by_id(_id):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (_id,))
            existing_user = cur.fetchone()
            if existing_user is None:
                raise NotFoundException()
            return User(existing_user[1], existing_user[2], existing_user[3], _id=existing_user[0])

    @staticmethod
    def delete_by_id(_id):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE id = ?", (_id,))
            con.commit()
            row_count = cur.rowcount
            cur.close()
            return row_count

    def remove(self):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE id = ?", (self._id,))
            con.commit()
            cur.close()



    def _update(self):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET first_name = ?, last_name = ?, username = ?  WHERE id = ?",
                        (self.firstname, self.lastname, self.username, self._id))
            con.commit()
            cur.close()

    def _insert(self):
        with sqlite3.connect("tuntiharjoitus1.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO users(first_name, last_name, username) VALUES(?, ?, ?)",
                        (self.firstname, self.lastname, self.username))
            con.commit()
            self._id = cur.lastrowid
            cur.close()


    # JSON-tyyppimuunnoksia ei pitäisi tehdä modelissa,
    # koska model on malli datasta ja data access layer
    # controllerin tehtävä on hoitaa responsen parsiminen
    # TÄMÄ ON VAIN ESIMERKKI
    @staticmethod
    def list_to_json(users_list):
        json_list = []
        for user in users_list:
            json_list.append(user.to_json())
        return json_list

    # JSON-tyyppimuunnoksia ei pitäisi tehdä modelissa,
    # koska model on malli datasta ja data access layer
    # controllerin tehtävä on hoitaa responsen parsiminen
    # TÄMÄ ON VAIN ESIMERKKI
    def to_json(self):
        return {'id': self._id, 'firstname': self.firstname, 'lastname': self.lastname, 'username': self.username}

    @property
    def id(self):
        return self._id
