'''
Python数据结构: Bag_ADT
ADT: Abstact Data Type
'''


class Bag:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self._items = list()

    def add(self, item):
        try:
            if len(self._items) >= self.capacity:
                raise Exception('The bag is full!')
            self._items.append(item)
        except Exception as e:
            print(e)

    def remove(self, item):
        self._items.remove(item)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        for item in self._items:
            yield item
