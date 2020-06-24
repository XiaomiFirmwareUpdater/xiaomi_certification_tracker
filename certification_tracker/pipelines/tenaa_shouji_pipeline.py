from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.tenaa_shouji import Item
from certification_tracker.database.tables.tenaa_shouji import create_table
from certification_tracker.database.utils import table_exists


class TenaaShoujiPipeline:
    def __init__(self):
        self.session = None
        self.table = "tenaa_shouji"

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
        photo = item.get('photo')
        certification = item.get('certification')

        if self.session.query(Item).filter_by(model=model).filter_by(
                certification=certification).count() < 1:
            self.session.add(
                Item(model=model,
                     certification=certification,
                     photo=photo)
            )

            message = f"*New TENAA Shouji Certificate added!*\n\n" \
                      f"*Model:* {model}\n" \
                      f"*Certification:* [Here]({certification})\n"
            if photo:
                message += f"*Photos:* [Here]({photo})\n"
            telegram_bot.send_telegram_message(message)

        self.session.commit()
        return item
