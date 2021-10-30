# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
import logging
from showspider import settings

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ShowspiderPipeline:
    def __init__(self) -> None:
        self.connection = pymysql.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
        self.connection.ping(reconnect=True)
        with self.connection as conn:
            with conn.cursor() as cursor:
                try:
                    sql = "select * from search_show where id = %s"
                    cursor.execute(sql, (item["id"],))
                    result = cursor.fetchone()
                    if result is not None:
                        sql = """update search_show set title=%s,url=%s,date=%s,
                            time=%s,venue=%s,artist=%s,post=%s,source=%s where id=%s"""
                        cursor.execute(sql, (item['title'], item['url'], item['date'], 
                            item['time'], item['venue'], item['artist'], item['post'], item['source'], item['id']))
                    else:
                        sql = """insert into search_show(id,title,url,date,time,venue,artist,post,source)
                            value (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        cursor.execute(sql, (item['id'], item['title'], item['url'], 
                            item['date'], item['time'], item['venue'], item['artist'], item['post'], item['source']))
                    conn.commit()
                except Exception as e:
                    logging.error(e)
                return item