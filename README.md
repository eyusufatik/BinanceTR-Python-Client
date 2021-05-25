# BinanceTR-Python-Client
BinanceTR API'ını kullanmak için mini Python kütüphanesi

## Kullanım
Dosyaları indirip kullanmak istediğiniz yere taşıyın.

    git clone https://github.com/eyusufatik/BinanceTR-Python-Client.git

Daha sonra bir .py dosyasında küütphaneyi import edin.

```python
from APIClient import *
```

Client objesini oluşturun. 


```python
client = APIClient("__API_KEY__", "__API_SECRET__")
```
(Not: API key ve secretınızı dosyanızda string halinde tutmak yerine environment variable olarak tutmanızda fayda var, eğer online bir VCS kullanacaksanız bunların internete düşmesi çok tehlikeli.)

* BTCUSDT paritesinde daha önce yapmış olduğumuz AL ve SAT işlemlerini görelim.

  ```python
  response = client.get_orders("BTC_USDT", Orders.Closed, OrderSide.Both)

  print(response) # respsone["data"]["list"] ile sadece emirleri yazdırabilirsiniz.
  ```

* BTCUSDT paritesinde emir girelim
  ```python
  try:
    buy_response = client.place_order("BTC_USDT", OrderType.Limit, OrderSide.Buy, 1, 39000)
    print(buy_response)
  except Exception as e:
    print(e)
  
  print(response) # respsone["data"]["list"] ile sadece emirleri yazdırabilirsiniz.
