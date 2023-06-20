import json
import requests
from time import sleep

qurey = 'meskie/polbuty'
result_per_site = 20
url = f'https://eobuwie.com.pl/t-api/rest/search/eobuwie/v4/search?channel=eobuwie&currency=PLN&locale=pl_PL&limit={result_per_site}&page=1&categories[]={qurey}&select[]=product_active&select[]=product_badge&select[]=manufacturer&select[]=manufacturer_with_collection&select[]=clothes_size&select[]=main_color&select[]=discount&select[]=eco_friendly&select[]=fason&select[]=final_price&select[]=footwear_size&select[]=tegosc&select[]=hot_deal&select[]=images&select[]=model&select[]=nazwa_wyswietlana&select[]=nazwa_wyswietlana_front&select[]=okazja&select[]=price&select[]=producent&select[]=rozmiar_karta_produktu&select[]=product_group_associated&select[]=series_name&select[]=size_type&select[]=index&select[]=action_label&select[]=akcje_marketingowe&select[]=technologie_entity&select[]=url_key&select[]=video_url&select[]=product_color_variants_count&select_locales[]=pl_PL'
headers = []
res = {}

r = requests.get(url=url, headers=headers, timeout=3)

products = json.loads(r.text)['products']
for product in products:
    model = product['values']['model']['value'].split()
    if len(model[-1]) < 5 and len(model) > 2:
        model = model[-2] + ' ' + model[-1]
    else:
        model = model[-1]
    price = product['values']['final_price']['value']['pl_PL']['PLN']['amount']
    prod_url = 'https://eobuwie.com.pl/p/' + product['values']['url_key']['value']['pl_PL']
    res[model] = price, prod_url
    
    print(model, price, prod_url)
sleep(5)
