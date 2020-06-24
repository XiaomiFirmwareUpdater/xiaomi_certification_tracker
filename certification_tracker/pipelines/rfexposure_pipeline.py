from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.rfexposure import Item
from certification_tracker.database.tables.rfexposure import create_table
from certification_tracker.database.utils import table_exists


class RfExposurePipeline:
    def __init__(self):
        self.session = None
        self.table = "rfexposure"

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
        region = item.get('region')

        if self.session.query(Item).filter_by(model=model).filter_by(region=region).count() < 1:
            self.session.add(
                Item(device=device,
                     device_id=item.get('device_id'),
                     model=item.get('model'),
                     region=region)
            )

            telegram_bot.send_telegram_message(
                f"*New Xiaomi device RF Exposure information Added to Mi {region} website!*\n\n"
                f"*Device Name:* {device}\n"
                f"*Device Model:* {model}\n"
            )

        self.session.commit()
        return item
