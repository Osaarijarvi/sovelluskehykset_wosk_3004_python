
# decorators/users_repository.py

import functools
import sqlite3
from contextlib import closing

from factories.repositories import create_users_repository


def get_users_repository(route_handler_func):
    # @functools.wraps säilyttää alkuperäisen funktion nimen.
    # Ilman tätä jokainen koristeltu funktio olisi nimeltään "wrapper" ja Flask kaatuisi
    # virheeseen: "View function mapping is overwriting an existing endpoint function"
    @functools.wraps(route_handler_func)
    def wrapper(*args, **kwargs):


        # avataan tietokantayhteys tässä.
        # closing sulkee yhteyden, kun with-lohkosta poistutaan
        with closing(sqlite3.connect("tuntiharjoitus1.db")) as con:

            # annetaan con-muuttuja factorylle parametrina
            users_repository = create_users_repository(con)

            return route_handler_func(users_repository, *args, **kwargs)
    # muista wrapper funktio pitää palauttaa dekoraattorin lopussa, mutta ilman sulkuja
    return wrapper