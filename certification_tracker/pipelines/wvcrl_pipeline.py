from sqlalchemy.orm import sessionmaker, Session

from certification_tracker import telegram_bot
from certification_tracker.database import engine, metadata
from certification_tracker.database.models.wvcrl import Item
from certification_tracker.database.tables.wvcrl import create_table
from certification_tracker.database.utils import table_exists


class WvcrlPipeline:
    def __init__(self):
        self.session = None
        self.table = "wvcrl"

    def open_spider(self, spider):
        if not table_exists(self.table):
            create_table(self.table)
            metadata.create_all(engine)
        session: sessionmaker = sessionmaker(bind=engine)
        self.session: Session = session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        manufacturer = item.get('manufacturer')
        model = item.get('model')
        soc = item.get('soc')
        type_ = item.get('type')
        certification = item.get('certification')
        date = item.get('date')
        level = item.get('level')
        method = item.get('method')

        if self.session.query(Item).filter_by(certification=certification).count() < 1:
            self.session.add(
                Item(manufacturer=manufacturer,
                     model=model, soc=soc, type=type_,
                     certification=certification, date=date,
                     level=level, method=method)
            )

            message = f"*Widevine Revocation Tracker device added!*\n\n" \
                      f"*Manufacturer:* `{manufacturer}`\n" \
                      f"*Model:* `{model}`\n" \
                      f"*SoC:* `{soc}`\n" \
                      f"*Type:* `{type_}`\n" \
                      f"*Date:* `{date}`\n" \
                      f"*Level:* `{level}`\n" \
                      f"*Certification:* `{certification}`\n"
            if method:
                message += f"*Method:* `{method}`\n"
            telegram_bot.send_telegram_message(message)

        self.session.commit()
        return item
