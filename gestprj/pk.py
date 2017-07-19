from django.db import connection

def generaPkProjecte():# Ojo al nombre de la bdd!!
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(ID_PROJECTE)+1 FROM gestprj_v4.dbo.PROJECTES")
        row = cursor.fetchone()
        return row[0]

def generaPkOrganisme():
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(ID_ORGANISME)+1 FROM gestprj_v4.dbo.T_ORGANISMES")
        row = cursor.fetchone()
        return row[0]