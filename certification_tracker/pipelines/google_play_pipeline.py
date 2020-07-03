from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.google_play import Item
from certification_tracker.database.tables.google_play import create_table
from certification_tracker.database.utils import table_exists


class GooglePlayPipeline:
    def __init__(self):
        self.session = None
        self.table = "google_play"

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
        codename = item.get('codename')
        model = item.get('model')

        if self.session.query(Item).filter_by(name=name).filter_by(
                codename=codename).filter_by(model=model).count() < 1:
            self.session.add(
                Item(name=name,
                     codename=codename,
                     model=model)
            )

            message = f"*New Google Play Certificate added!*\n\n" \
                      f"*Name:* {name}\n" \
                      f"*Codename:* {codename}\n" \
                      f"*Model:* {model}\n"
            telegram_bot.send_telegram_message(message)

            self.session.commit()
        return item
