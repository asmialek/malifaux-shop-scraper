# %% [markdown]
# # Malifaux Scapper

# %% [markdown]
# ## Initialization

# %%
import tabulate
import requests as r
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def check_retailer(url, i):
    try:
        raw_page = r.get(f"{url}{i}").content
    except:
        raw_page = r.get(f"{url}{i}", verify=False).content
    soup = bs(raw_page, "html.parser")
    return soup

# %% [markdown]
# ## Functions

# %%
def find_items(url, range_max, product_tag, name_tag, availability_tag, availability_string):
    last_page_contents = None
    available_products_list = set()
    for i in range(1,range_max):
        soup = check_retailer(url, i)
        products = soup.find_all(class_=product_tag)
        if products == last_page_contents or products == None: break
        for product in products:
            name = product.find(class_=name_tag).text
            print(name)
            try:
                availability = availability_string in product.find(class_=availability_tag).text
            except AttributeError:
                continue
            if availability:
                available_products_list.add(name.strip())
            print('Page:', i, end='\r')
        last_page_contents = products
    return available_products_list

# %%
def find_items_szopgracz(url, product_tag, name_tag, availability_tag, availability_string):
    available_products_list = set()
    soup = check_retailer(url, '')
    products = soup.find_all(class_=product_tag)
    for product in products:
        name = product.find(class_=name_tag).text
        availability = bool(product.find(class_=availability_tag))
        if not availability:
            available_products_list.add(name.strip())
    return available_products_list

# %%
def find_items_allegro():
    driver = webdriver.Chrome(ChromeDriverManager().install())  
    html = driver.page_source
    soup = bs(html, "html.parser")
    product_list = []
    for i in range(1,30):
        new_products = 0
        driver.get(f"https://allegro.pl/kategoria/bitewne-inne-systemy-6059?string=malifaux&p={i}")
        html = driver.page_source
        soup = bs(html, "html.parser")
        products = soup.find_all(class_='mgn2_14 m9qz_yp meqh_en mpof_z0 mqu1_16 m6ax_n4 mp4t_0 m3h2_0 mryx_0 munh_0 mj7a_4')
        for product in products:
            name = product.text
            if name not in product_list:
                # print(name)
                product_list.append(name)
                new_products += 1
        print('Page:', i, end='\r')
        if new_products == 0: break
    
    return product_list

# %%
def used_items_allegro():
    driver = webdriver.Chrome(ChromeDriverManager().install())  
    html = driver.page_source
    soup = bs(html, "html.parser")
    product_list = []
    for i in range(1,30):
        new_products = 0
        driver.get(f"https://allegro.pl/listing?string=malifaux&stan=używane")
        html = driver.page_source
        soup = bs(html, "html.parser")
        products = soup.find_all(class_='mgn2_14 m9qz_yp meqh_en mpof_z0 mqu1_16 m6ax_n4 mp4t_0 m3h2_0 mryx_0 munh_0 mj7a_4')
        for product in products:
            name = product.text
            if name not in product_list:
                # print(name)
                product_list.append(name)
                new_products += 1 
            product_list.append(name)
        print('Page:', i, end='\r')
        if new_products == 0: break
    
    return product_list

# %%
def find_items_levi():
    driver = webdriver.Chrome(ChromeDriverManager().install())  
    last_page_contents = None
    available_products_list = set()
    
    html = driver.page_source
    soup = bs(html, "html.parser")
    for i in range(1,30):
        driver.get(f"https://levisuel.com/fr/4-malifaux?page={i}")
        html = driver.page_source
        soup = bs(html, "html.parser")
        products = soup.find_all(class_='product-miniature js-product-miniature')
        if products == last_page_contents or products == None: break
        for product in products:
            name = product.find(class_='h3 product-title').text
            try:
                availability = 'Ajouter' in product.find(class_='add-to-cart').text
            except AttributeError:
                continue
            if availability:
                available_products_list.add(name.strip())
        print('Page:', i, end='\r')
    
        last_page_contents = products
    return available_products_list

# %%
def find_items_fire():
    driver = webdriver.Chrome(ChromeDriverManager().install())  
    available_products_list = set()
    
    html = driver.page_source
    soup = bs(html, "html.parser")
    driver.get(f"https://www.firestormgames.co.uk/wargames-miniatures/malifaux")
    html = driver.page_source
    soup = bs(html, "html.parser")
    products = soup.find_all(class_='item-inner')
    for product in products:
        name = product.find(class_='title match-height').text
        try:
            availability = 'Now' in product.find(class_='banner alert alert-info').text
        except AttributeError:
            continue
        if availability:
            available_products_list.add(name.strip())
    
    return available_products_list

# %%
def create_shop_dict(allegro=True, abroad=True):
    shops_dict = {}

    print('\ngraal')
    graal = find_items('https://sklep-graal.pl/pl/c/Malifaux-3rd/474/', 30, 'product-inner-wrap', 'productname', 'addtobasket', 'Do koszyka')
    shops_dict['graal'] = graal

    print('\nbolter')
    bolter = find_items('https://bolter.pl/pl/c/MALIFAUX-3ed./1211/', 30, 'product-inner-wrap', 'productname', 'addtobasket', 'Do koszyka')
    shops_dict['bolter'] = bolter

    print('\nstrefa')
    strefamtg = find_items('https://strefamtg.pl/2596-malifaux-3ed?page=', 30, 'product-miniature__container', 'product-miniature__title', 'product-quantities', 'dostępna')
    shops_dict['strefa'] = strefamtg

    print('\nszop')
    szopgracz = find_items_szopgracz('https://shopgracz.pl/298-malifaux', 'item-product', 'product_name', 's_soon', 'niedostępny')
    shops_dict['szop'] = szopgracz

    print('\ngnom')
    gnom = find_items('https://gnom-sklep.pl/pl/menu/malifaux-261.html?filter_price=&filter_availability=y?counter=', 10, 'product', 'product__name', 'product__name', '')
    shops_dict['gnom'] = gnom

    if allegro:
        print('\nallegro')
        allegro = find_items_allegro()
        shops_dict['allegro'] = allegro

    if abroad:
        print('\nlevisuel')
        levi = find_items_levi()
        shops_dict['levi'] = levi

        print('\nminiatur')
        miniatur = find_items('https://www.miniaturicum.de/3rd-Edition?availability=1&seite=', 30, 'productbox-inner', 'productbox-title', 'price-note', '')
        shops_dict['miniatur'] = miniatur

        print('\nfirestorm')
        firestorm = find_items_fire()
        shops_dict['firestorm'] = firestorm
    
    return shops_dict

# %%
def generate_table(item_list, shops_dict):
    table_rows = []
    for item in item_list:
        table_row = []
        for shop in shops_dict:
            for product in shops_dict[shop]:
                if item.upper() in product.upper():
                    table_row.append('X')
                    break
            else:
                if item == '---------------------':
                    table_row.append('-'*len(shop))
                else:
                    table_row.append('-')
        table_rows.append([item.title(), *table_row])
    print(tabulate.tabulate(table_rows, headers=['box', *shops_dict.keys()], tablefmt="pretty"))

# %%
def main(item_list):
    shops_dict = create_shop_dict()
    generate_table(item_list, shops_dict)

# %% [markdown]
# ## Dictionary generation

# %%
shops_dict = create_shop_dict()

# %%
shops_dict

# %% [markdown]
# ## Table generation

# %%
item_list = ['Tara Core Box',
             'Forward and Back',
             'Servants of the Void',
             'Beyond Time',
             '---------------------',
             'KAERIS CORE BOX',
             'BURNING BRIDGES',
             'Mechanical Rider',
             'Center Stage',
             'CRACK IN THE FOUNDATION',
             'EMBRACE THE EMBER',
             '---------------------',
             'LADY JUSTICE CORE BOX',
             'WAKE THE DEAD',
             '---------------------',
             'VON SCHILL CORE BOX',
             'BETWEEN THE LEY LINES',
             'CUTTING-EDGE TECHNOLOGY',
             '---------------------',
             'LEVETICUS CORE BOX',
             'NECROPUNKS',
             'DESOLATION',
             'ASHES AND DUST',
             'MARLENA WEBSTER',
             '---------------------',
             'HOFFMAN CORE BOX',
             'SUPPORT STAFF',
             'KEEPING THE PEACE',
             '---------------------',
             'Intrepid Fate',
             '---------------------',
             'Ravencroft Core Box',
             'Invisible Ink',
             'Living Soulstones',
             '---------------------',
             'Lord Cooper Core Box',

             ]

generate_table(item_list, shops_dict)


