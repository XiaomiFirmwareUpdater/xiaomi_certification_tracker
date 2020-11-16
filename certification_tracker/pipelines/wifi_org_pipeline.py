from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.wifi_org import Item
from certification_tracker.database.tables.wifi_org import create_table
from certification_tracker.database.utils import table_exists


class WifiOrgPipeline:
    def __init__(self):
        self.session = None
        self.table = "wifi_org"

    def open_spider(self, spider):
        if not table_exists(self.table):
            create_table(self.table)
            metadata.create_all(engine)
        session: sessionmaker = sessionmaker(bind=engine)
        self.session: Session = session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        device = item.get('device').strip('\xa0')
        model = item.get('model').strip('\xa0')
        category = item.get('category').strip('\xa0')
        date = item.get('date').strip('\xa0')
        certification = item.get('certification')

        # temporary code foe updating certificate url after wi-fi.org website is updated on 16-11-2020
        # old = self.session.query(Item).filter_by(model=model).filter_by(category=category).filter_by(
        #     date=date).filter_by(device=device).first()
        # if old:
        #     if old.certification != certification:
        #         old.certification = certification
        #         self.session.commit()

        if self.session.query(Item).filter_by(model=model).filter_by(category=category).count() < 1:
            self.session.add(
                Item(device=device,
                     model=model,
                     category=category,
                     date=date,
                     certification=certification)
            )

            telegram_bot.send_telegram_message(
                f"*New Wi-Fi Alliance Certificate added!*\n\n"
                f"*Name:* {device}\n"
                f"*Model:* {model}\n"
                f"*Type:* {category}\n"
                f"*Date:* {date}\n"
                f"*Certification:* [Here]({certification})\n"
            )

        self.session.commit()
        return item
