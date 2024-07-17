from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getLocalization():
        conn = DBConnect.get_connection()
        result=[]
        query="""select distinct c.Localization 
from classification c """
        cursor=conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(row["Localization"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni():
        conn = DBConnect.get_connection()
        result = []
        query = """select distinct  t.l1, t.l2, t.Type
from (select c.Localization as l1, c2.Localization as l2 , i.`Type` 
from classification c , interactions i, classification c2 
where i.GeneID1 =c.GeneID and c2.GeneID =i.GeneID2 and c.Localization!=c2.Localization 
order by c.Localization, c2.Localization) t 
order by t.l1, t.l2"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append((row["l1"], row["l2"], row["Type"]))
        cursor.close()
        conn.close()
        return result
