class ScrapNewsCaptchaCatch(Exception):
    def __init__(self, message="Error when scraping news from captcha"):
        self.message = message
        super().__init__(self.message)

class ScrapNewsDownloadImageError(Exception):
    def __init__(self, message="Error when download image from article"):
        self.message = message
        super().__init__(self.message)