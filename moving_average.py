import random
from typing import List
import unittest

import matplotlib.pyplot as plt

from timer import time_me


N_REPEATS = 10


@time_me(N_REPEATS)
def simple(data: List[float], period: int):
    '''The simplest and probably slowest implementation'''
    results = []
    for i in range(period, len(data)):
        sample = data[i-period:i]
        mean = sum(sample) / period
        results.append(mean)
    return results


@time_me(N_REPEATS)
def rotating_sample(data: List[float], period: int):
    '''Not slicing the original array each time - update with each subsequent value'''
    sample = data[:period]
    idx_sample = -1
    
    results = []
    for idx_data in range(period, len(data)):
        mean = sum(sample) / period
        results.append(mean)

        idx_sample += 1
        if idx_sample >= period:
            idx_sample = 0
        sample[idx_sample] = data[idx_data]

    return results


@time_me(N_REPEATS)
def updates(data: List[float], period: int):
    '''Update the mean value wth removing the old and adding the new value'''
    mean = sum(data[:period]) / period
    
    results = [mean]
    for i in range(period+1, len(data)):
        mean = ((mean * period) - data[i-period] + data[i]) / period
        results.append(mean)

    return results


class TestCases(unittest.TestCase):

    def setUp(self):
        self.results_10_3 = [1, 2, 3, 4, 5, 6, 7]
        self.results_10_5 = [2, 3, 4, 5, 6]

        self.results_20_3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        self.results_20_5 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    def test_simple(self):
        data = range(10)
        self.assertListEqual(simple(data, 3)[0], self.results_10_3)
        self.assertListEqual(simple(data, 5)[0], self.results_10_5)

        data = range(20)
        self.assertListEqual(simple(data, 3)[0], self.results_20_3)
        self.assertListEqual(simple(data, 5)[0], self.results_20_5)

    def test_rotating_sample(self):
        data = range(10)
        self.assertListEqual(rotating_sample(list(data), 3)[0], self.results_10_3)
        self.assertListEqual(rotating_sample(list(data), 5)[0], self.results_10_5)

        data = range(20)
        self.assertListEqual(rotating_sample(list(data), 3)[0], self.results_20_3)
        self.assertListEqual(rotating_sample(list(data), 5)[0], self.results_20_5)

    def test_updates(self):
        data = range(10)
        self.assertListEqual(updates(data, 3)[0], self.results_10_3)
        self.assertListEqual(updates(data, 5)[0], self.results_10_5)

        data = range(20)
        self.assertListEqual(updates(data, 3)[0], self.results_20_3)
        self.assertListEqual(updates(data, 5)[0], self.results_20_5)

    def test_performance(self):
        data = [i for i in range(200_000)]

        results = []
        for func in (simple, rotating_sample, updates):
            for period in range(20, 201, 20):
                _, time_taken = func(data, period)
                results.append((func.__name__, period, time_taken))
        
        # plot results - altogether
        plt.figure()
        for key in ('simple', 'rotating_sample', 'updates'):
            x = [x[1] for x in results if x[0] == key]
            y = [x[2] for x in results if x[0] == key]
            plt.plot(x, y, label=key)

        plt.xlabel('Averaging period')
        plt.ylabel('Avg time taken (s)')
        plt.title('Comparing techniques to calculate a moving average')

        plt.grid(True, linestyle='--')
        plt.legend()

        plt.savefig('results.png')
        plt.close('all')

        # plot results - individually
        for key in ('updates', 'rotating_sample', 'simple'):
            plt.figure()
            x = [x[1] for x in results if x[0] == key]
            y = [x[2] for x in results if x[0] == key]
            plt.plot(x, y, label=key)

            plt.xlabel('Averaging period')
            plt.ylabel('Avg time taken (s)')
            plt.title(key)

            plt.grid(True, linestyle='--')

            plt.savefig(f'results-{key}.png')
            plt.close('all')


if __name__ == '__main__':
    unittest.main()
