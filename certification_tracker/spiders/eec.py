# -*- coding: utf-8 -*-
import re
from datetime import datetime
from urllib.parse import quote

from scrapy import Spider, Request, Selector


class EecSpider(Spider):
    name = 'eec'
    allowed_domains = ['portal.eaeunion.org']
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-CDAC-LOCALE': 'ru-ru',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://portal.eaeunion.org',
        'Connection': 'keep-alive',
        'Referer': 'https://portal.eaeunion.org/sites/odata/_layouts/15/Portal.EEC.Registry.Ui/DirectoryForm.aspx?ViewId=859ec98d-f4fe-423a-b6bc-d01b53fd4b7c&ListId=0e3ead06-5475-466a-a340-6f69c01b5687&ItemId=232',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
    data = 'viewName=regui.SPLIST_TABLE_VIEW&parameters=' + quote(
        f'''<p><parameter name="list" value="d84d16d7-2cc9-4cff-a13b-530f96889dbc"/><parameter name="view" value="859ec98d-f4fe-423a-b6bc-d01b53fd4b7c"/><parameter name="itemUrl" value="/sites/odata/_layouts/15/Portal.EEC.Registry.UI/DisplayForm.aspx"/><parameter name="query" value="&lt;And&gt;&lt;Contains&gt;&lt;FieldRef Name=&quot;tmp_RegisterNotificationsCryptographicMeans_Manufacturer&quot;/&gt;&lt;Value Type=&quot;Text&quot; &gt;&lt;![CDATA[Xiaomi]]&gt;&lt;/Value&gt;&lt;/Contains&gt;&lt;And&gt;&lt;Or&gt;&lt;Leq&gt;&lt;FieldRef Name='StartDate'/&gt;&lt;Value Type='DateTime' IncludeTimeValue='False'&gt;{now}&lt;/Value&gt;&lt;/Leq&gt;&lt;IsNull&gt;&lt;FieldRef Name='StartDate'/&gt;&lt;/IsNull&gt;&lt;/Or&gt;&lt;Or&gt;&lt;Geq&gt;&lt;FieldRef Name='EndDate'/&gt;&lt;Value Type='DateTime' IncludeTimeValue='False'&gt;{now}&lt;/Value&gt;&lt;/Geq&gt;&lt;IsNull&gt;&lt;FieldRef Name='EndDate'/&gt;&lt;/IsNull&gt;&lt;/Or&gt;&lt;/And&gt;&lt;/And&gt;"/><parameter name="filter" value="[object Object]"/><parameter name="paginginfo" value="Paged=TRUE&amp;p_ID=58236"/><parameter name="pagenumber" value="0"/></p>''')

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.eec_pipeline.EecPipeline': 400
        }
    }

    def start_requests(self):
        yield Request(
            method="POST",
            url="https://portal.eaeunion.org/sites/odata/_layouts/CDAC.Web/"
                "XmlSourceBrockerService.asmx/getViewXmlContentFriendly",
            headers=self.headers,
            body=self.data,
            callback=self.parse
        )

    def parse(self, response):
        content = re.sub(r'<\?xml.*\s<QueryResults.*', '', response.text)
        content = re.sub(r'</QueryResults>.*', '', content)
        content = Selector(text=content)
        items = content.xpath('//tbody/tr')
        for item in items:
            model_info = item.xpath('.//td[contains(@name,"_NAME")]/div/text()').get()
            brand = re.search(r'(?:&quot;|«)(\w+)(?:&quot;|»)', model_info)
            brand = brand.group(1) if brand else ""
            _item = re.search(r'(?:модели|модель): (.*)', model_info)
            _item = _item.group(1).replace('.', '') if _item else model_info
            yield {
                'brand': brand,
                'item': _item,
                'certification': 'https://portal.eaeunion.org' + item.xpath('.//@data-href').get(),
                'date': datetime.strptime(
                    item.xpath('.//td[contains(@name,"_PUBLICATIONDATE")]/div/text()').get(),
                    "%d.%m.%Y %H:%M").strftime("%Y-%m-%d")
            }
