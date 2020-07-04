from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.xsms import Item
from certification_tracker.database.tables.xsms import create_table
from certification_tracker.database.utils import table_exists


class XsmsPipeline:
    def __init__(self):
        self.session = None
        self.table = "xsms"

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

        if self.session.query(Item).filter_by(model=model).count() < 1:
            self.session.add(Item(model=model))

            message = f"*New device added to XSMS Database!*\n\n" \
                      f"*Model:* {model}\n"
            telegram_bot.send_telegram_message(message)

        self.session.commit()
        return item
