from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.xiaomi_certification.database import engine, metadata
from certification_tracker.xiaomi_certification.database.models.tkdn import Item
from certification_tracker.xiaomi_certification.database.tables.tkdn import create_table
from certification_tracker.xiaomi_certification.database.utils import table_exists


class TkdnPipeline:
    def __init__(self):
        self.session = None
        self.table = "tkdn"

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
        certification = item.get('certification')
        reference = item.get('reference')
        date = item.get('date')
        link = item.get('link')

        if self.session.query(Item).filter_by(model=model).filter_by(
                certification=certification).filter_by(date=date).count() < 1:
            self.session.add(
                Item(model=model,
                     certification=certification,
                     reference=reference,
                     date=date,
                     link=link)
            )

            telegram_bot.send_telegram_message(
                f"*New TKDN Certificate added!*\n\n"
                f"*Model:* {model}\n"
                f"*Reference Number:* {reference}\n"
                f"*Date:* {date}\n"
                f"*Certification:* [{certification}]({link})\n"
            )

        self.session.commit()
        return item
