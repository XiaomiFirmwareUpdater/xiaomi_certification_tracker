from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.bluetooth import Item
from certification_tracker.database.tables.bluetooth import create_table
from certification_tracker.database.utils import table_exists


class BluetoothPipeline:
    def __init__(self):
        self.session = None
        self.table = "bluetooth"

    def open_spider(self, spider):
        if not table_exists(self.table):
            create_table(self.table)
            metadata.create_all(engine)
        session: sessionmaker = sessionmaker(bind=engine)
        self.session: Session = session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        name = item.get('name')
        items = item.get('items')
        certification = item.get('certification')
        category = item.get('type')
        date = item.get('date')

        if self.session.query(Item).filter_by(items=items).filter_by(
                certification=certification).count() < 1:
            self.session.add(
                Item(name=name, items=items,
                     certification=certification,
                     type=category, date=date)
            )

            message = f"*New Bluetooth Launch Studio Certificate added!*\n\n"
            if name:
                message += f"*Name:* {name}\n"
            message += f"*Models:* {items}\n" \
                       f"*Certification:* [Here]({certification})\n" \
                       f"*Date:* {date}\n"
            telegram_bot.send_telegram_message(message)

        self.session.commit()
        return item
