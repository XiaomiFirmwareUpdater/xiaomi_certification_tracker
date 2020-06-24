from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.miit import Item
from certification_tracker.database.tables.miit import create_table
from certification_tracker.database.utils import table_exists


class MiitPipeline:
    def __init__(self):
        self.session = None
        self.table = "miit"

    def open_spider(self, spider):
        if not table_exists(self.table):
            create_table(self.table)
            metadata.create_all(engine)
        session: sessionmaker = sessionmaker(bind=engine)
        self.session: Session = session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        device = item.get('device')
        model = item.get('model')
        category = item.get('category')
        date = item.get('date')
        certification = item.get('certification')

        if not device and not model:
            return item

        if self.session.query(Item).filter_by(model=model).filter_by(
                device=device).filter_by(certification=certification).count() < 1:
            self.session.add(
                Item(device=device, model=model,
                     category=category, date=date,
                     certification=certification)
            )

            message = f"*New MIIT Certificate added!*\n\n" \
                      f"*Name:* {device}\n" \
                      f"*Model:* {model}\n" \
                      f"*Type:* {category}\n"
            if date:
                message += f"*Date:* {date}\n"
            message += f"*Certification:* {certification}\n"
            telegram_bot.send_telegram_message(message)

        self.session.commit()
        return item
