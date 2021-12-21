# BinanceTR-Python-Client
Mini python library to use BinanceTr API

## Usage
Clone the repo and move files to your project.
    git clone https://github.com/eyusufatik/BinanceTR-Python-Client.git

Import the library.

```python
from APIClient import *
```

Create the client object.

```python
client = APIClient("__API_KEY__", "__API_SECRET__")
```

(Note: You should store your api-key and api-secret in environment variables, if you plan to upload your project on any platform)

* Let's see the completed BUY and SELL transactions for BTCUSDT parity on our account.

  ```python
  response = client.get_orders("BTC_USDT", Orders.Closed, OrderSide.Both)

  print(response) # respsone["data"]["list"] to print only the orders
  ```

* Send order for BTCUSDT parity.
  ```python
  try:
    buy_response = client.place_order("BTC_USDT", OrderType.Limit, OrderSide.Buy, 1, 39000)
    print(buy_response)
  except Exception as e:
    print(e)
   ```
* For other use cases take a look at the APIClient.py file.
