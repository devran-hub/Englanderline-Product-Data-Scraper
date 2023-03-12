import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd


class EnglanderSpider(CrawlSpider):
    name = 'englander'
    allowed_domains = ['englanderline.com']
    start_urls = ['https://englanderline.com/']
    rules = (
        Rule(LinkExtractor(deny='product')),
        Rule(LinkExtractor(allow='product/'), callback='parse_item'),


    )
    liste = list()

    def parse_item(self, response):

        for i in response.css('.wpb_text_column.wpb_content_element div.wpb_wrapper span::text').getall():
            if 'tock' in i:
                stock = i

        strsp = str()

        for x in response.css('tr'):
            title = x.css('th ::text').get()
            ct = x.css('td ::text').getall()[0]
            strsp += f'{title}: {ct}\n'

        taglist = response.css(
            '.product-term.product-term--display-name ::text').getall()
        tagstr = str()
        for x in taglist[1:len(taglist) - 1]:
            tagstr += x
        imagy = response.css('.wp-post-image::attr(src)').get()
        EnglanderSpider.liste.append([response.css('h1.product_title.entry-title::text').get().replace('\t', ''), response.css('meta[name*=twitter][name*=data1]::attr(content)').get(), tagstr, response.css('#tab-description p::text').get(), strsp, response.xpath(
            "//*[contains(text(), 'In-Stock')]//text()").get(), response.css('meta[name*=twitter][name*=data2]::attr(content)').get(), '=IMAGE(\"{}\")'.format(imagy)])
        df = pd.DataFrame(EnglanderSpider.liste, columns=['name', 'price','tags', 'description',
                                                          'specifications', 'stock', 'stock situation', 'image'])
        df.to_excel('res.xlsx')
        content = {

            'name': response.css('h1.product_title.entry-title::text').get().replace('\t', ''),
            'price': response.css('meta[name*=twitter][name*=data1]::attr(content)').get(),
            'tags': tagstr,
            'description': response.css('#tab-description p::text').get(),
            'specifications': strsp,
            'stock': response.xpath("//*[contains(text(), 'In-Stock')]//text()").get(),
            'stock situation': response.css('meta[name*=twitter][name*=data2]::attr(content)').get(),
            'image': '=IMAGE(\"{}\")'.format(imagy)
        }
        yield content
