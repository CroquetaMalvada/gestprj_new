from django.db import connection

def generaPkProjecte():
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(ID_PROJECTE)+1 FROM gestprj.dbo.PROJECTES")
        row = cursor.fetchone()
        return row[0]

def generaPkOrganisme():
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(ID_ORGANISME)+1 FROM gestprj.dbo.T_ORGANISMES")
        row = cursor.fetchone()
        return row[0]