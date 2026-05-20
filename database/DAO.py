from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select DISTINCT(t.year)
                    from teams t
                    where t.year >= 1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select *
                    from teams t 
                    where t.year = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalariesofTeam(year, idMapTeams):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select t.ID , t.teamCode, sum(s.salary) as totSalary
                    from salaries s, teams t, appearances a 
                    where s.`year` = t.`year` and t.`year` = a.`year` and a.`year` = %s
                    and a.teamID = t.ID and a.playerID = s.playerID
                    group by t.ID , t.teamCode"""

        cursor.execute(query, (year,))

        mapSalary = {}

        for row in cursor:
            mapSalary[idMapTeams[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return mapSalary
