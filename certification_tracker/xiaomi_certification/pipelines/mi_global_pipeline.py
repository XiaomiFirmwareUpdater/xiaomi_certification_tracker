from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.xiaomi_certification.database import engine, metadata
from certification_tracker.xiaomi_certification.database.models.mi_global import Item
from certification_tracker.xiaomi_certification.database.tables.mi_global import create_table
from certification_tracker.xiaomi_certification.database.utils import table_exists


class MiGlobalPipeline:
    def __init__(self):
        self.session = None
        self.table = "mi_global"

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
        region = item.get('region')
        certification = item.get('certification')

        if self.session.query(Item).filter_by(device=device).count() < 1:
            self.session.add(
                Item(device=device,
                     certification=certification,
                     region=region)
            )

            message = f"*New Xiaomi device Added to Mi {region} website!*\n\n*Name:* {device}\n"
            if certification:
                message += f"*Certification*: [Here]({certification})\n"
            telegram_bot.send_telegram_message(message)
        else:
            query = self.session.query(Item).filter(
                Item.device == device).filter(
                Item.region == region).first()
            if query.certification != certification:
                query.certification = certification
                self.session.add(query)

        self.session.commit()
        return item
