import random


class UnpairedException(Exception):
    pass


class WaitingSet(set):
    def remove(self, element):
        try:
            super().remove(element)
        except KeyError:
            pass


class PairedConnections(dict):
    def __init__(self, *args, **kwargs):
        self.waiting = set()
        super().__init__(*args, **kwargs)

    def __delitem__(self, key):
        paired_key = self[key]
        if paired_key is not None:
            try:
                super().__delitem__(paired_key)
            except Exception as e:
                pass
        else:
            self.waiting.remove(key)
        super().__delitem__(key)

    def __setitem__(self, key, value):
        if value is not None:
            try:
                self[value]
            except KeyError as e:
                raise UnpairedException(f"Connection {key}-{value} not paired")
            super().__setitem__(value, key)
        else:
            self.waiting.add(key)
        super().__setitem__(key, value)

    def get_random_conn(self):
        return random.choice(tuple(self.waiting))




def check_code_valid(code):
    '''Checking whether the incoming code is valid or not'''
    if len(code) == 8:
        return True
    return False


conns = PairedConnections()

if __name__ == "__main__":
    conns['one'] = None
    conns['two'] = None
    conns['three'] = None
    print('1:', conns)
    print('\t', conns.waiting)
    conns['two'] = 'one'
    print('2:', conns)
    print('\t', conns.waiting)
    del conns['one']
    print('3:', conns)
    print('\t', conns.waiting)
    del conns['three']
    print('4:', conns)
    print('\t', conns.waiting)
