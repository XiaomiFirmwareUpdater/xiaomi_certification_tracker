from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.gcf import Item
from certification_tracker.database.tables.gcf import create_table
from certification_tracker.database.utils import table_exists


class GCFPipeline:
    def __init__(self):
        self.session = None
        self.table = "gcf"

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
        device = item.get('device')
        date = item.get('date')
        certification = item.get('certification')

        if self.session.query(Item).filter_by(model=model).count() < 1:
            self.session.add(
                Item(model=model,
                     device=device,
                     date=date,
                     certification=certification)
            )

            telegram_bot.send_telegram_message(
                f"*New Global Certification Forum Certificate added!*\n\n"
                f"*Model:* {model}\n"
                f"*Device:* {device}\n"
                f"*Date:* {date}\n"
                f"*Certification*: [Here]({certification})\n")

        self.session.commit()
        return item
