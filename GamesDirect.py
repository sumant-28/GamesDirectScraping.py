import requests
import json
import dataset
from itertools import chain

class GamesDirect():

  def __init__(self, baseurl):
    self.baseurl = baseurl

  def jsondownload(self, page):
    r = requests.get(self.baseurl + f'page={page}', timeout=5)
    if r.status_code != 200:
      print('Bad Status Code: ', r.status_code)
    if len(r.json()['products']) > 0:
      data = r.json()['products']
      return data
    else:
      return

  def jsonparse(self, jsondata):
    products = []
    for prod in jsondata:
      mainid = prod['id']
      title = prod['title']
      published_at = prod['published_at']
      created_at = prod['created_at']
      updated_at = prod['updated_at']
      vendor = prod['vendor']
      product_type = prod['product_type']
      for i in prod['variants']:
        item = {
          'id': mainid,
          'title': title,
          'published_at': published_at,
          'product_type': product_type,
          'varid': i['id'],
          'vartitle': i['title'],
          'sku': i['sku'],
          'price': i['price'],
          'available': i['available'],
          'created_at': i['created_at'],
          'updated_at': i['updated_at'],
          'compare_at_price': i['compare_at_price'],
          'product_id': i['product_id']
        }
        products.append(item)
    return products

def main():
  inventory = GamesDirect('https://www.gamesdirectltd.com/products.json?limit=250&')
  results = []
  for page in range(1,8):
    data = inventory.jsondownload(page)
    print('Getting page: ', page)
    try:
      results.append(inventory.jsonparse(data))
    except:
      print(f'Completed, total pages =  {page - 1}')
      break
  return results

if __name__ == '__main__':
  db = dataset.connect('sqlite:///inventory.db')
  table = db.create_table('GamesDirect', primary_id='varid')
  products = main()
  totals = [item for j in products for item in j]
  
  for k in totals:
    if not table.find_one(varid=k['varid']):
      table.insert(k)
      # print('New Inventory Item: ', k)
    else:
      True # print('no change')
  

  newproducts = list(chain(*products))
  newdatabase = [l for l in newproducts if l['product_type'] == 'CONSOLE']
  db = dataset.connect('sqlite:///newdatabase.db')
  tables2 = db['newdatabase']
  for m in newdatabase:
    if not tables2.find_one(varid=m['varid']):
      tables2.insert(m)
      print('New Console Item ', m)
    else:
      print('No Change')
    

