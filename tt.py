from functools import reduce
from itertools import repeat
import time
import random

SECRET = 'huilo'


class Timer:
    def __init__(self, name='Timer'):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        diff = self.end - self.start
        print(f'{self.name}: {diff} seconds elapsed')


def find_number(n):
    lim = int('9'*(len(str(n)) + 2))
    for q in range(0, lim):
        arr = list(map(lambda x: int(x), list(str(q))))
        res = reduce(lambda x, y: x * y, arr)
        if res == n:
            return q
    return -1


def f(n, inversions):
    bulbs = [False for _ in range(n)]
    for i in inversions:
        for b in range(i-1, n, i):
            bulbs[b] = not bulbs[b]
    #print(bulbs)
    return sum(bulbs)


def calc(expr: str):
    ...

MIN = 1
MAX = 5


def brute(maxx=MAX, mode='lettersonly'):
    from string import ascii_lowercase, digits, ascii_uppercase

    def check_passw(passw):
        if passw != SECRET:
            return False
        return True

    if mode == 'all':
        source = ascii_lowercase + digits + ascii_uppercase
    elif mode == 'lower':
        source = ascii_lowercase + digits
    elif mode == 'lettersonly':
        source = ascii_lowercase
    elif mode == 'digitsonly':
        source = digits
    else:
        raise ValueError('wrong mode')
    length = len(source)
    for step in range(maxx-MIN+1):
        letters = [source[0] for _ in range(step+MIN)]
        for i in range(int(length**(step+MIN+1))):
            part = i % length
            last_char = source[part]
            letters[0] = last_char
            for mul in range(1, step+MIN):
                if i % length**mul == 0:
                    cur_order = source.find(letters[mul])
                    letters[mul] = source[(cur_order+1) % length]
            temp = ''.join(letters)
            if check_passw(temp):
                print('SECRET FOUND:', temp)
                return None
    print(f'SECRET NOT FOUND. {maxx} chars is not enough, increase it')


def ifer():
    it = repeat(0, int(1e8))
    for i in it:
        if i == 0:
            10/10


def tryer():
    it = repeat(0, int(1e8))
    for i in it:
        try:
            10/i
        except Exception as e:
            pass


def perform_brute():
    brute(mode='lettersonly')


def main():
    INPUT = (101 , [19, 2, 7, 13, 40, 23, 16, 45, 9])
    res = f(*INPUT)
    print('RESULT:', res)


if __name__ == "__main__":
    with Timer('IF') as t:
        ifer()
    with Timer('TRY') as t2:
        tryer()