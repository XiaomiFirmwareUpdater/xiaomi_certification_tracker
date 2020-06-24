from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.tenaa_cert import Item
from certification_tracker.database.tables.tenaa_cert import create_table
from certification_tracker.database.utils import table_exists


class TennaCertPipeline:
    def __init__(self):
        self.session = None
        self.table = "tenaa_cert"

    def open_spider(self, spider):
        if not table_exists(self.table):
            create_table(self.table)
            metadata.create_all(engine)
        session: sessionmaker = sessionmaker(bind=engine)
        self.session: Session = session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        model = item.get('model')
        date = item.get('date')
        photos = item.get('photos')
        certification = item.get('certification')

        if self.session.query(Item).filter_by(model=model).filter_by(
                certification=certification).count() < 1:
            self.session.add(
                Item(model=model,
                     certification=certification,
                     date=date, photos=photos)
            )

            message = f"*New TENAA Certificate added!*\n\n" \
                      f"*Model:* {model}\n" \
                      f"*Date:* {date}\n" \
                      f"*Certification:* {certification}\n"
            if photos:
                message += f"*Photos:* [Here]({photos})\n"
            telegram_bot.send_telegram_message(message)

        self.session.commit()
        return item
