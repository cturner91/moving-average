import random
from typing import List
import unittest

import matplotlib.pyplot as plt

from timer import time_me


N_REPEATS = 1


@time_me(N_REPEATS)
def simple(data: List[float], period: int):
    '''The simplest and probably slowest implementation'''
    results = []
    for i in range(period, len(data)+1):
        sample = data[i-period:i]
        results.append(max(sample))
    return results


@time_me(N_REPEATS)
def push_pop(data: List[float], period: int):
    '''Not slicing the original array each time - update with each subsequent value'''
    sample = list(data[:period])
    
    results = []
    for i in range(period, len(data)):
        results.append(max(sample))

        del sample[0]
        sample.append(data[i])

    results.append(max(sample))
    return results


@time_me(N_REPEATS)
def rotating_sample(data: List[float], period: int):
    '''Same as push and pop but updating a single array'''
    sample = data[:period]
    idx_sample = -1
    
    results = []
    for idx_data in range(period, len(data)):
        results.append(max(sample))

        idx_sample += 1
        if idx_sample >= period:
            idx_sample = 0
        sample[idx_sample] = data[idx_data]

    results.append(max(sample))
    return results


@time_me(N_REPEATS)
def updates(data: List[float], period: int):
    maximum = max(data[:period])
    
    results = [maximum]
    max_updates, max_slices = 0, 0
    for i in range(period, len(data)):
        drop_value = data[i-period]
        new_value = data[i]
        if new_value > maximum:
            max_updates += 1
            maximum = new_value
        elif drop_value == maximum:
            max_slices += 1
            maximum = max(data[i-period:period])

        results.append(maximum)

    print(max_updates, max_slices)
    return results



@time_me(N_REPEATS)
def updates_with_secondary(data: List[float], period: int):
    values = sorted(data[:period])
    maximum, secondary = values[-1], values[-2]
    
    results = [maximum]
    max_updates, max_slices, secondary_updates = 0, 0, 0
    for i in range(period, len(data)):
        drop_value = data[i-period]
        new_value = data[i]
        if new_value > maximum:
            max_updates += 1
            secondary = maximum
            maximum = new_value
        elif secondary is not None and new_value > secondary:
            secondary = new_value
        elif drop_value == maximum:
            maximum = secondary
            secondary = None

        results.append(maximum)

    print(max_updates, max_slices)
    return results

class TestCases(unittest.TestCase):

    # def setUp(self):
    #     self.results_10_3 = [2, 3, 4, 5, 6, 7, 8, 9]
    #     self.results_10_5 = [4, 5, 6, 7, 8, 9]

    #     self.results_20_3 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    #     self.results_20_5 = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    # def test_simple(self):
    #     data = range(10)
    #     self.assertListEqual(simple(data, 3)[0], self.results_10_3)
    #     self.assertListEqual(simple(data, 5)[0], self.results_10_5)

    #     data = range(20)
    #     self.assertListEqual(simple(data, 3)[0], self.results_20_3)
    #     self.assertListEqual(simple(data, 5)[0], self.results_20_5)

    # def test_push_pop(self):
    #     data = range(10)
    #     self.assertListEqual(push_pop(data, 3)[0], self.results_10_3)
    #     self.assertListEqual(push_pop(data, 5)[0], self.results_10_5)

    #     data = range(20)
    #     self.assertListEqual(push_pop(data, 3)[0], self.results_20_3)
    #     self.assertListEqual(push_pop(data, 5)[0], self.results_20_5)

    # def test_rotating_sample(self):
    #     data = range(10)
    #     self.assertListEqual(rotating_sample(list(data), 3)[0], self.results_10_3)
    #     self.assertListEqual(rotating_sample(list(data), 5)[0], self.results_10_5)

    #     data = range(20)
    #     self.assertListEqual(rotating_sample(list(data), 3)[0], self.results_20_3)
    #     self.assertListEqual(rotating_sample(list(data), 5)[0], self.results_20_5)

    # def test_updates(self):
    #     data = range(10)
    #     self.assertListEqual(updates(data, 3)[0], self.results_10_3)
    #     self.assertListEqual(updates(data, 5)[0], self.results_10_5)

    #     data = range(20)
    #     self.assertListEqual(updates(data, 3)[0], self.results_20_3)
    #     self.assertListEqual(updates(data, 5)[0], self.results_20_5)

    # def test_visual(self):
    #     random.seed(32)
    #     func, period = simple, 10
    #     data = [random.random()*2.0 + (i/30)**2 for i in range(50)]
    #     aggregated = func(data, period)[0]

    #     plt.figure()
    #     plt.scatter(range(len(data)), data, alpha=0.5, label='data')
    #     plt.plot([i+period for i in range(len(aggregated))], aggregated, label='aggregated')

    #     plt.grid(True, linestyle='--')
    #     plt.legend()

    #     plt.savefig('visualisation.png')
    #     plt.close('all')

    def test_performance(self):
        random.seed(32)
        data = [i/10 + random.random() for i in range(200_000)]

        results = []
        for func in (simple, push_pop, rotating_sample, updates):
            for period in range(20, 201, 20):
                _, time_taken = func(data, period)
                results.append((func.__name__, period, time_taken))
        
        # plot results - altogether
        plt.figure()
        for key in ('simple', 'push_pop', 'rotating_sample', 'updates'):
            x = [x[1] for x in results if x[0] == key]
            y = [x[2] for x in results if x[0] == key]
            plt.plot(x, y, label=key)

        plt.xlabel('Averaging period')
        plt.ylabel('Avg time taken (s)')
        plt.title('Comparing techniques to calculate a moving maximum')

        plt.grid(True, linestyle='--')
        plt.legend()

        plt.savefig('results.png')
        plt.close('all')

        # plot results - individually
        for key in ('simple', 'push_pop', 'rotating_sample', 'updates'):
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
