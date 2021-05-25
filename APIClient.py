import requests
import HelperFunctions
from enum import Enum


class Orders(Enum):
    All = -1
    Open = 1
    Closed = 2


class OrderSide(Enum):
    Buy = 0
    Sell = 1
    Both = ""


class OrderType(Enum):
    Limit = 1
    Market = 2
    Stop_Limit = 4


class APIClient:
    time_url = "https://www.trbinance.com/open/v1/common/time"
    symbols_url = "https://www.trbinance.com/open/v1/common/symbols"
    order_book_url = "https://www.trbinance.com/open/v1/market/depth"
    recent_trades_url = "https://api.binance.cc/api/v3/trades"
    account_information_url = "https://www.trbinance.com/open/v1/account/spot"
    asset_information_url = "https://www.trbinance.com/open/v1/account/spot/asset"
    orders_url = "https://www.trbinance.com/open/v1/orders"
    cancel_order_url = "https://www.trbinance.com/open/v1/orders/cancel"

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret

    def test_connection(self):
        """
        Tests connection by pinging the time endpoint.
        """

        response = self.__send_unauthorized_request__(self.time_url)
        return response

    def get_symbols(self):
        """
        :return: Tokens/coins listen on the exchange as a dict
        """

        response = self.__send_unauthorized_request__(self.symbols_url)
        return response

    def get_order_book(self, symbol, limit=100):
        """
        :param symbol: Should be in the form of COIN_FIAT e.g. BTC_USDT
        :param limit: Depth wanted
        :return: Order book for given coin/token as a dict
        """

        parameters = {"symbol": symbol, "limit": limit}
        response = self.__send_authorized_request__("GET", self.order_book_url, parameters)
        return response

    def get_account_info(self):
        """
        :return: Account information as a dict
        """

        response = self.__send_authorized_request__("GET", self.account_information_url)
        return response

    def get_recent_trades(self, symbol, limit=500):
        """
        :param symbol: Should be in the form of COINFIAT e.g. BTCUSD
        :param limit: Amount of trades wanted
        :return: Returns recent trades as a dict
        """

        parameters = {"symbol": symbol, "limit": limit}
        response = self.__send_unauthorized_request__(self.recent_trades_url, parameters)
        return response

    def get_asset_information(self, name):
        """
        :param name: Particular asset wanted, if left empty returns whole wallet
        :return: Asset info in your wallet as a dict
        """

        parameters = {"asset": name}
        response = self.__send_authorized_request__("GET", self.asset_information_url, parameters)
        return response

    def get_all_open_orders(self, symbol="", limit=100):
        """
        :param symbol: Coin/token wanted, if left empty returns all open orders. Should be in the form of COIN_FIAT
        :param limit:
        :return: Open orders as a dict
        """

        response = self.get_orders(symbol, Orders.Open, OrderSide.Both, limit)
        return response

    def get_all_closed_orders(self, symbol="", limit=100):
        """
        :param symbol: Coin/token wanted, if left empty returns all closed orders. Should be in the form of COIN_FIAT
        :param limit:
        :return: Closed orders as a dict
        """

        response = self.get_orders(symbol, Orders.Closed, OrderSide.Both, limit)
        return response

    def get_orders(self, symbol, order_type=Orders.All, order_side=OrderSide.Both, limit=100):
        """
        :param symbol: Coin/token wanted, if left empty, returns all  orders. Should be in the form of COIN_FIAT
        :param order_type: Should be Orders.All or Orders.Open or Orders.Closed, Orders.All is default
        :param order_side: Should be OrderSide.Both or OrderSide.Buy or OrderSide.Sell, OrderSide.Both is default
        :param limit:
        :return: Orders as a dict
        """

        parameters = {"symbol": symbol, "type": order_type.value, "side": order_side.value, "limit": limit}
        response = self.__send_authorized_request__("GET", self.orders_url, parameters)
        return response

    def place_order(self, symbol, order_type, order_side, quantity, price=""):
        """
        Places an order of any type
        
        :param symbol: e.g. BTC_USDT
        :param order_type: OrderType.Limit or OrderType.Market or OrderType.Stop_Limit
        :param order_side: OrderSide.Buy or OrderSide.Sell
        :param quantity: Desired amount of coin/token
        :param price: Desired price. Leave empty for market orders.
        :return: Returns server response
        """
        if order_type == OrderType.Market and price != "":
            raise Exception("Market orders shouldn't include price ")
        else:
            parameters = {"symbol": symbol, "type": order_type.value, "side": order_side.value, "quantity": quantity,
                          "price": price}
            response = self.__send_authorized_request__("POST", self.orders_url, parameters)
            return response

    def cancel_order(self, order_ID):
        """
        Cancels an order with given ID
        
        :param order_ID: Order ID as a string
        :return: Returns server response
        """
        parameters = {"orderId": order_ID}
        response = self.__send_authorized_request__("POST", self.cancel_order_url, parameters)
        return response

    def __send_authorized_request__(self, method, url, parameters=None):
        try:
            url_extension = HelperFunctions.create_query(parameters)
            if method == "GET":
                if url_extension == "":
                    url += "?" + "signature=" + HelperFunctions.get_signature(self.api_secret, url_extension)
                else:
                    url += "?" + url_extension + "&" + "signature=" + HelperFunctions.get_signature(
                        self.api_secret, url_extension)
                response = requests.get(url, headers={"X-MBX-APIKEY": self.api_key})
                return response.json()
            elif method == "POST":
                parameters["signature"] = HelperFunctions.get_signature(self.api_secret, url_extension)
                response = requests.post(url, headers={"X-MBX-APIKEY": self.api_key}, data=parameters)
                return response.json()
        except Exception as e:
            print(e)

    def __send_unauthorized_request__(self, url, parameters=None):
        try:
            if parameters is not None:
                url_extension = "?" + HelperFunctions.create_query(parameters, False)
                url += url_extension
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(e)
