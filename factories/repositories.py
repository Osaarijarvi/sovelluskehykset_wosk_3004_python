
# repositories/factories.py

from repositories.users_sqlite_repository import UsersSQLiteRepository

# nyt tietokantayhteys tulee factory funktiolle parametrina
def create_users_repository(con):


    # ja se välitetään construct injection-mekanismilla UsersSQLiteRepository-luokalle
    return UsersSQLiteRepository(con)