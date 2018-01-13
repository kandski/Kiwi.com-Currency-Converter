from sqlalchemy import schema, create_engine, types
from sqlalchemy.sql import select, and_
import aiohttp, asyncio
from forex_python.converter import CurrencyCodes

class StorageAlchemy():
    def __init__(self):
        self.meta = schema.MetaData()
        self.currencies = schema.Table('currencies', self.meta,
                          schema.Column('id', types.Integer, primary_key=True),
                          schema.Column('input', types.String, default=''),
                          schema.Column('output', types.String, default=''),
                          schema.Column('coeficient', types.Float, default=0.0),
                          schema.Column('symbol', types.Unicode, default=u''))

        self.db = create_engine('sqlite:///storage.db', echo=False)
        self.meta.bind = self.db
        self.meta.create_all(checkfirst=True)
        # self.insert_some_data()
        self._fetched = dict()
        self.codes = ["USD", "JPY","BGN","CZK","DKK","EUR","GBP","HUF","PLN",
                      "RON","SEK","CHF","NOK","HRK","RUB","TRY","AUD","BRL",
                      "CAD","CNY","HKD","IDR","ILS","INR","KRW","MXN","MYR",
                      "NZD","PHP","SGD","THB","ZAR"]

        self.symbol = dict()
        c = CurrencyCodes()
        for code in self.codes:
            self.symbol[code] = c.get_symbol(code)

    def get_coeficient(self, in_currency, out_currency):
        connection = self.db.connect()
        table = self.currencies.c
        coefficients = dict()
        if out_currency is not None:
            sel = select([self.currencies], and_(table.input == in_currency,
                                                 table.output == out_currency))
        else:
            sel = select([self.currencies], and_(table.input == in_currency))
        result = connection.execute(sel)
        for row in result:
            coefficients[row[2]] = row[3]

        connection.close()
        return coefficients

    async def fetch(self, client, code):
        async with client.get("http://api.fixer.io/latest?base={}".format(code)) as r:
            self._fetched[code] = await r.json()

        conn = self.db.connect()
        table = self.currencies
        for key, val in self._fetched[code]['rates'].items():
            conn.execute(table.insert(), [dict(input=code, output=key,
                                               coeficient=val,
                                               symbol=self.symbol[code]
                                               )])
        conn.close()

    def update_db(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # drop all tables bcs SQlite does not support upsert
        self.meta.drop_all()
        self.meta.create_all(checkfirst=True)



        with aiohttp.ClientSession(loop=loop) as client:
            tasks = asyncio.wait([self.fetch(client, url) for url in self.codes])
            loop.run_until_complete(tasks)


        return {"database":"was updated"}