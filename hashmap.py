# Hashmap class
class HashMap:

    # O(n)
    def __init__(self):
        self.hash_counter = 0
        self.hash_counter_index = 0
        self.map = []
        for i in range(10):
            self.map.append([])

    # Used to create in iterator to iterate over a hashmap along side the next method
    # O(1)
    def __iter__(self):
        return self

    # Used when iterating over the hashmap along side an iterator
    # O(1)
    def __next__(self):
        if self.hash_counter < 10:
            self.hash_counter += 1
        elif self.hash_counter == 10 and self.hash_counter_index == 3:
            self.hash_counter = 1
            self.hash_counter_index = 0
        else:
            self.hash_counter = 1
            self.hash_counter_index += 1
        value = self._get_hash(self.hash_counter)
        index = self.hash_counter_index
        next_v = self.map[value][index][1]
        return next_v

    def _get_hash(self, key):
        return int(key) % len(self.map)

    # O(n)
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    # O(n)
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        else:
            return None

    # O(n)
    def delete(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

# # Test
# h = HashMap()
# h.add(1, 'test')
# h.add(2, 'test2')
# h.add(3, 'test3')
# h.add(4, 'test4')
# h.add(5, 'test5')
# h.add(6, 'test6')
# h.add(7, 'test6')
# h.add(8, 'test6')
# h.add(9, 'test6')
# h.add(10, 'test6')
# h.add(11, 'test6')
# # h.print()
# print(h.get(2))
