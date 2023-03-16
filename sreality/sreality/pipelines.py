# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class SrealityPipeline:
    def __init__(self):
        # Connection Details
        hostname = '0.0.0.0'
        port = '5432'
        username = 'lana'
        password = 'luxonis'
        database = 'estates'
        # Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()
        # Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Estates(
            id serial PRIMARY KEY,
            title text,
            image_urls text
        )
        """)
        print('TABLE estate created!')
        self.cur.execute("""
        DELETE FROM estates *
        """)

    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(""" insert into estates (title, image_urls) values (%s,%s)""", (
            item["title"],
            str(item["image_urls"])
        ))
        ## Execute insert of data into database
        self.connection.commit()
        print('ITEM was processed!')
        return item

    def close_spider(self, spider):
        # Prepare html page for http server
        self.cur.execute("""
        SELECT * FROM estates
        """)
        print("Selecting rows from estate table using cursor.fetchall")
        estate_records = self.cur.fetchall()

        print("Print each row and it's columns values")
        for row in estate_records:
            print("Title = ", row[1], )
            print("Image urls = ", row[2], "\n")

        strTable = "<html><meta charset=\"UTF-8\"><table><tr><th>Estates</th><th> </th></tr>"
        for row in estate_records:
            strRW = "<tr><td>" + row[1] + "</td><td><img src=\"" + row[2] + "\"></td></tr>"
            strTable = strTable + strRW

        strTable = strTable + "</table></html>"

        hs = open("../server/srealityEstates.html", 'w')
        hs.write(strTable)
        hs.close()

        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()