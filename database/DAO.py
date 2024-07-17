from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getChromosomes():
        conn=DBConnect.get_connection()
        result=[]
        query="""select distinct g.Chromosome  
from genes g 
where g.Chromosome >0"""
        cursor=conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(row['Chromosome'])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnections():
        conn = DBConnect.get_connection()
        result = []
        query = """select distinct t.c, t.c2, sum(t.Expression_corr) as tot
from (
select g.Chromosome as c,g2.Chromosome as c2, i.*
from interactions i , genes g, genes g2 
where i.GeneID1 =g.GeneID and i.GeneID2 =g2.GeneID and g.Chromosome!=g2.Chromosome and g.Chromosome!=0 and g2.Chromosome!=0 
group by g.Chromosome, g2.Chromosome, g.GeneID,g2.GeneID  
order by g2.Chromosome , g.Chromosome) t
group by t.c, t.c2"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append((row['c'],row["c2"], row["tot"]))
        cursor.close()
        conn.close()
        return result
