from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.certipedia import Item
from certification_tracker.database.tables.certipedia import create_table
from certification_tracker.database.utils import table_exists


class CertipediaPipeline:
    def __init__(self):
        self.session = None
        self.table = "certipedia"

    def open_spider(self, spider):
        if not table_exists(self.table):
            create_table(self.table)
            metadata.create_all(engine)
        session: sessionmaker = sessionmaker(bind=engine)
        self.session: Session = session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        models = item.get('models')
        certification = item.get('certification')
        link = item.get('link')

        if self.session.query(Item).filter_by(models=models).count() < 1:
            self.session.add(
                Item(models=models,
                     certification=certification,
                     link=link)
            )

            message = f"*New Certipedia Certificate added!*\n\n" \
                      f"*Models:* {models}\n" \
                      f"*Certification:* [{certification}]({link})\n"
            telegram_bot.send_telegram_message(message)

            self.session.commit()
        return item
