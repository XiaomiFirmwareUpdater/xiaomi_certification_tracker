from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.xiaomi_certification.database import engine, metadata
from certification_tracker.xiaomi_certification.database.models.nbtc import Item
from certification_tracker.xiaomi_certification.database.tables.nbtc import create_table
from certification_tracker.xiaomi_certification.database.utils import table_exists


class NbtcPipeline:
    def __init__(self):
        self.session = None
        self.table = "nbtc"

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
        device = item.get('device')
        certification = item.get('certification')
        link = item.get('link')

        if self.session.query(Item).filter_by(model=model).filter_by(certification=certification).count() < 1:
            self.session.add(
                Item(brand=brand,
                     device=device, model=model,
                     certification=certification,
                     link=link)
            )

            telegram_bot.send_telegram_message(
                f"*New NTBC Certificate added!*\n\n"
                f"*Brand:* {brand}\n"
                f"*Device:* {device}\n"
                f"*Model:* {model}\n"
                f"*Certification:* [{certification}]({link})\n"
            )

        self.session.commit()
        return item
