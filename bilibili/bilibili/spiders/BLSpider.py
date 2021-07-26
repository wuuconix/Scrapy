    import scrapy

    class BlspiderSpider(scrapy.Spider):
        name = 'BLSpider'   #spider的名字
        allowed_domains = ['www.bilibili.com']  #允许爬取的域名
        start_urls = ['https://www.bilibili.com/v/popular/rank/all']    #开始url，是b站实时热门榜的url

        def parse(self, response):
            for i in range(100):    #循环一百次，表示爬取一百条记录
                record = {} #每一条记录储存在一个字典dict之中
                record['rank'] = str(i + 1) #record的rank键表示视频当前的排名
                url = "https:" +  response.xpath('//*[@id="app"]/div[2]/div[2]/ul/li[' + str(i + 1) + ']/div[2]/div[2]/a/@href')[0].extract()   #爬取视频的url
                title = response.xpath('//*[@id="app"]/div[2]/div[2]/ul/li[' + str(i + 1) + ']/div[2]/div[2]/a/text()')[0].extract()    #爬取视频的标题
                record['url'] = url    #将url存入字典中
                record['title'] = title
                record['Uploader'] = response.xpath('//*[@id="app"]/div[2]/div[2]/ul/li[' + str (i + 1) + ']/div[2]/div[2]/div[1]/a/span/text()')[0].extract()[17:-15]  #爬取视频的up主名字
                yield scrapy.Request(url, meta= {'record' : record}, callback=self.detail_parse)    #利用生成器，进入视频url中进行双层爬取
        
        def detail_parse(self, response):   #用来爬取第二层的网页，来获得视频的更加具体的信息
            record = response.meta['record']    #利用Request对象的meta传递数据
            record['view'] = response.xpath('//*[@id="viewbox_report"]/div/span/text()')[0].extract()[:-3]  #播放量
            record['BulletScreen'] = response.xpath('//*[@id="viewbox_report"]/div/span[2]/text()')[0].extract()    #弹幕数量
            record['UploadedTime'] = response.xpath('//*[@id="viewbox_report"]/div/span[3]/text()')[0].extract()[2:-5]  #上传时间
            record['ToppestRank'] = response.xpath('//*[@id="viewbox_report"]/div/span[4]/text()')[0].extract()[2:-5]   #最高排行
            record['Star'] = response.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[1]/text()')[0].extract()[0:-5]   #点赞数
            record['Coin'] = response.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[2]/text()')[0].extract()[7:-5]   #硬币数
            record['Collect'] = response.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[3]/text()')[0].extract()[0:-5]    #收藏数
            try:
                Description = response.xpath('//*[@id="v_desc"]/div[2]/span/text()')[0].extract()   #因为有些up主不写简介，在没有简介的情况下，根据xpath会找不到东西，而我用用到了列表操作，会报错，所以这里利用python的异常捕捉。如果发生异常，就将简介内容手动复制为空
            except IndexError:
                Description = ""
            record['Desription'] = Description
            return  record      #返回最终的记录
