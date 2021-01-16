from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.tuvsud import Item
from certification_tracker.database.tables.tuvsud import create_table
from certification_tracker.database.utils import table_exists


class TuvsudPipeline:
    def __init__(self):
        self.session = None
        self.table = "tuvsud"

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
        category = item.get('category') or ""
        certification = item.get('certification')
        date = item.get('date')

        if self.session.query(Item).filter_by(category=category).filter_by(
                models=models).count() < 1:
            self.session.add(
                Item(models=models,
                     category=category,
                     certification=certification,
                     date=date)
            )

            telegram_bot.send_telegram_message(
                f"*New TÜV SÜD Certificate added!*\n\n"
                f"*Models:* {models}\n"
                f"*Type:* {category}\n"
                f"*Certification:* {certification}\n"
                f"*Date:* {date}\n"
            )

        self.session.commit()
        return item
