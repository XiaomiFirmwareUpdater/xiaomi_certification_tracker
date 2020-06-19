from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.xiaomi_certification.database import engine, metadata
from certification_tracker.xiaomi_certification.database.models.fccid import Item
from certification_tracker.xiaomi_certification.database.tables.fccid import create_table
from certification_tracker.xiaomi_certification.database.utils import table_exists


class FccidPipeline:
    def __init__(self):
        self.session = None
        self.table = "fccid"

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
        certification = item.get('certification')

        if self.session.query(Item).filter_by(model=model).count() < 1:
            self.session.add(
                Item(model=model,
                     date=date,
                     certification=certification)
            )

            telegram_bot.send_telegram_message(
                f"*New FCCID Certificate added!*\n\n"
                f"*Model:* {model}\n"
                f"*Date:* {date}\n"
                f"*Certification*: [Here]({certification})\n")

        self.session.commit()
        return item
