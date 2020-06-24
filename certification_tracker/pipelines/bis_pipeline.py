from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.bis import Item
from certification_tracker.database.tables.bis import create_table
from certification_tracker.database.utils import table_exists


class BisPipeline:
    def __init__(self):
        self.session = None
        self.table = "bis"

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
        model = item.get('model')
        category = item.get('category')
        certification = item.get('certification')
        date = item.get('date')

        if self.session.query(Item).filter_by(brand=brand).filter_by(
                model=model).filter_by(category=category).count() < 1:
            self.session.add(
                Item(brand=brand,
                     model=model,
                     category=category,
                     certification=certification,
                     date=date)
            )

            telegram_bot.send_telegram_message(
                f"*New BIS Certificate added!*\n\n"
                f"*Brand:* {brand}\n"
                f"*Model:* {model}\n"
                f"*Type:* {category}\n"
                f"*Certification:* {certification}\n"
                f"*Date:* {date}\n"
            )

        self.session.commit()
        return item
