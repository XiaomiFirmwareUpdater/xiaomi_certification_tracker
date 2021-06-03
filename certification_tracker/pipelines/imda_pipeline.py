from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.imda import Item
from certification_tracker.database.tables.imda import create_table
from certification_tracker.database.utils import table_exists


class IdmaPipeline:
    def __init__(self):
        self.session = None
        self.table = "imda"

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
        description = item.get('description')

        if self.session.query(Item).filter_by(brand=brand).filter_by(
                model=model).count() < 1:
            self.session.add(
                Item(brand=brand,
                     model=model,
                     description=description)
            )

            telegram_bot.send_telegram_message(
                f"*New IDMA Certificate added!*\n\n"
                f"*Brand:* {brand}\n"
                f"*Model:* {model}\n"
                f"*Description:* {description}\n"
            )

        self.session.commit()
        return item
