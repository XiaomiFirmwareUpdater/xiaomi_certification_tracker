from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.sertifikasi import Item
from certification_tracker.database.tables.sertifikasi import create_table
from certification_tracker.database.utils import table_exists


class SertifikasiPipeline:
    def __init__(self):
        self.session = None
        self.table = "sertifikasi"

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
        model = item.get('model')
        description = item.get('description')
        certification = item.get('certification')

        if self.session.query(Item).filter_by(certification=certification).filter_by(
                model=model).filter_by(description=description).count() < 1:
            self.session.add(
                Item(name=name,
                     model=model,
                     description=description,
                     certification=certification)
            )

            telegram_bot.send_telegram_message(
                f"*New POSTEL Certificate added!*\n\n"
                f"*Name:* {name}\n"
                f"*Model:* {model}\n"
                f"*Description:* {description}\n"
                f"*Certification:* {certification}\n"
            )

        self.session.commit()
        return item
