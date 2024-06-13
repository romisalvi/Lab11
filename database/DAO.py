from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getColors():
        conn=DBConnect.get_connection()
        result=[]
        cursor=conn.cursor(dictionary=True)
        query="""select distinct g.Product_color
                from go_sales.go_products g
                order by g.Product_color desc
                """
        cursor.execute(query)
        for row in cursor:
            result.append(row["Product_color"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProdottiColorati(color):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                        from go_sales.go_products g
                        where g.Product_color=%s
                        """
        cursor.execute(query,(color,))
        for row in cursor:
            result.append(Product(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges( year, color):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select gds.Product_number as p1, gds2.Product_number as p2 , count(distinct gds2.`Date`) as count
from go_sales.go_daily_sales gds 
join go_sales.go_daily_sales gds2  on gds2.Retailer_code = gds.Retailer_code 
join go_sales.go_products gp on gds.Product_number = gp.Product_number 
join go_sales.go_products gp2 on gds2.Product_number = gp2.Product_number 
where gds2.`Date` = gds.`Date` and year(gds2.`Date`)=%s and gp2.Product_color = %s
	and gp.Product_color = %s and gds2.Product_number < gds.Product_number 
group by gds.Product_number, gds2.Product_number 
                                """
        cursor.execute(query, (year,color,color,))
        for row in cursor:
            result.append((row["p1"],row["p2"], row["count"]))
        cursor.close()
        conn.close()
        return result

