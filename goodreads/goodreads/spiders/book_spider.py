import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['goodreads.com']
    start_urls = ['https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once']

    def parse(self, response):
        books = response.css('tr[itemtype="http://schema.org/Book"]')
        for book in books:
            avg_rating = float(book.css('.minirating::text').get().split('avg')[0].strip())
            rating_number = int(book.css('.minirating::text').get().split(' ')[-2].strip().replace(',', ''))

            yield {
                'title': book.css('span[role="heading"]::text').get(),
                'author': book.css('.authorName span::text').get(),
                'rating': avg_rating,
                'votes': rating_number
            }
        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
