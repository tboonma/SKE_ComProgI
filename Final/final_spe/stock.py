class Stock:
    def __init__(self, item, amount=0, price=0):
        self.__item = item
        self.__amount = amount
        self.__price = price
    
    @property
    def amount(self):
        return self.__amount
    
    @amount.setter
    def amount(self, value):
        self.__amount = value
    
    @property
    def price(self):
        return self.__price

    def __str__(self):
        return f"({self.__item.item_id},{self.__item.item_type},{self.__item.item_color},{self.__amount},{self.__price})"