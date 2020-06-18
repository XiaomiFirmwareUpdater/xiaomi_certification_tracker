from sqlalchemy.orm import sessionmaker

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
        self.session = session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        if self.session.query(Item).filter_by(device=item.get('device')).count() < 1:
            self.session.add(
                Item(device=item.get('device'),
                     certification=item.get('certificate'),
                     region=item.get('region'))
            )
            self.session.commit()
        return item
