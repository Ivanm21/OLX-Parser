import Parser as parser
import Exporter as exporter

address = 'https://www.olx.ua/nedvizhimost/arenda-kvartir/dolgosrochnaya-arenda-kvartir/kiev/'
file = "/Users/Ivanm/Desktop/olx_v3.xlsx"
pages = parser.get_next_page(address)

count = 0
for page_idx,p in enumerate(pages):
    links = parser.get_add_link(p)
    for link_idx, l in enumerate(links):
        add = parser.parse_add(l)
        exporter.writeToExcel(add,file)
        print(page_idx,link_idx,count)
        count += 1

# link = 'https://www.olx.ua/obyavlenie/arenda-3-komn-kvartira-115-kv-m-metro-poznyaki-darnitskiy-rayon-IDwbr4E.html#198eafd9aa;promoted'
# add = parser.parse_add(link)
# print (list(add))

