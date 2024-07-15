from database.DB_connect import DBConnect
from model.chromosone import Chromosone
from model.connection import Connection


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getChromosone():
        conn=DBConnect.get_connection()
        result=[]
        query="""select distinct g.Chromosome as chromosone 
from genes g 
where g.Chromosome !=0"""
        cursor=conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(row["chromosone"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges():
        conn=DBConnect.get_connection()
        result=[]
        query="""select g1.Chromosome as Chromosome1, g2.Chromosome as Chromosome2,i.GeneID1 as gene1, i.GeneID2 as gene2, i.Expression_Corr as corr  
from interactions i ,genes g1, genes g2
where i.GeneID1 =g1.GeneID  and i.GeneID2 =g2.GeneID and g1.Chromosome!=0 and g2.Chromosome!=0 and g1.Chromosome!=g2.Chromosome
group by  g1.Chromosome , g2.Chromosome ,i.GeneID1, i.GeneID2"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(Connection(**row))
        cursor.close()
        conn.close()
        return result