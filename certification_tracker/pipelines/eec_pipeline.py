from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.eec import Item
from certification_tracker.database.tables.eec import create_table
from certification_tracker.database.utils import table_exists


class EecPipeline:
    def __init__(self):
        self.session = None
        self.table = "eec"

    def open_spider(self, spider):
        if not table_exists(self.table):
            create_table(self.table)
            metadata.create_all(engine)
        session: sessionmaker = sessionmaker(bind=engine)
        self.session: Session = session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        brand = item.get('brand')
        _item = item.get('item')
        certification = item.get('certification')
        date = item.get('date')

        if self.session.query(Item).filter_by(item=_item).count() < 1:
            self.session.add(
                Item(brand=brand,
                     item=_item,
                     certification=certification,
                     date=date)
            )

            message = f"*New EEC Certificate added!*\n\n" \
                      f"*Brand:* {brand}\n" \
                      f"*Item:* `{_item}`\n" \
                      f"*Certification:* [Here]({certification})\n" \
                      f"*Date:* {date}\n"
            telegram_bot.send_telegram_message(message)

        self.session.commit()
        return item
