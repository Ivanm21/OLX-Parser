
class Add:

    href = None
    Id = None
    href= None
    promoted = None
    published_from_mobile = False
    price = 0
    currency = ''
    negotiable = False
    text = None
    add_title = None
    district = None
    phone_number = None
    addType = None
    rooms = None
    rent_type = None
    date = None
    number = None
    image_links = None

    def __init__(self, href):
        start = href.find('ID')
        end = href.find('.html')
        if start & end is not None:
            self.Id = href[start + 2: end]

        self.href = href


    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

