__author__ = 'wangxiangpeng'
import scrapy
class DmozSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = [
        #"http://www.imdb.com/title/tt1504320/reviews?start=620"
        #"http://www.imdb.com/title/tt0110912/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2398042102&pf_rd_r=013Q4630FNQ1CTDP48V4&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_tt_5"
        "http://www.imdb.com/chart/top?ref_=nv_mv_250_6"
    ]

    def parse_review(self, response):
        #extract reviews
        i = 0
        divs = response.xpath('//*[@id="tn15content"]/p')
        for p in divs:  # extracts all <p> inside
            rawContent = p.extract()
            if rawContent.startswith("<p><"):
                continue
            rawContent = ''
            for text in p.xpath("./text()"):
                rawContent += text.extract() + '\n'
            filename = response.url.split("/")[-2] + response.url.split("/")[-1] + str(i) + '.txt'
            with open(filename, 'wb') as f:
                f.write(rawContent.encode('utf-8'))
            i = i + 1
        #extract next url
        next_href_list = response.xpath('///a/img[@alt="[Next]"]/parent::*/@href')
        if len(next_href_list) > 0:
            href = next_href_list[0]
            url = response.urljoin(href.extract())
            return scrapy.Request(url, callback=self.parse_review)

    def parse_movie(self, response):
        elements = response.xpath('//*[@id="quicklinksMainSection"]/a[text() = "USER REVIEWS"]/@href')
        if len(elements) > 0:
            href = elements[0]
            url = response.urljoin(href.extract())
            return scrapy.Request(url, callback=self.parse_review)

    def parse(self, response):
        elements = response.xpath('//*[@id="main"]/div/span/div/div/div[2]/table/tbody/tr/td[2]/a/@href')
        for i in range(0, 90):
            url = response.urljoin(elements[i].extract())
            yield scrapy.Request(url, callback=self.parse_movie)
        
