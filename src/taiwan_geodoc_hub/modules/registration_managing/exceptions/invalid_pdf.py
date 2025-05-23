class InvalidPDF(Exception):
    def __iter__(self):
        yield "name", __class__.__name__
