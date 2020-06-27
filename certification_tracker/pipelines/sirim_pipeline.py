from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.sirim import Item
from certification_tracker.database.tables.sirim import create_table
from certification_tracker.database.utils import table_exists


class SirimPipeline:
    def __init__(self):
        self.session = None
        self.table = "sirim"

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
        category = item.get('category')
        certification = item.get('certification')
        date = item.get('date')
        description = item.get('description')

        if self.session.query(Item).filter_by(model=model).filter_by(
                description=description).filter_by(category=category).count() < 1:
            self.session.add(
                Item(model=model,
                     category=category,
                     certification=certification,
                     description=description,
                     date=date)
            )

            message = f"*New SIRIM Certificate added!*\n\n" \
                      f"*Model:* {model}\n" \
                      f"*Description:* `{description}`\n" \
                      f"*Type:* {category}\n" \
                      f"*Certification:* {certification}\n" \
                      f"*Date:* {date}\n"
            telegram_bot.send_telegram_message(message)

        self.session.commit()
        return item
