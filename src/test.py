import math
from time import perf_counter
from typing import Callable, List, Optional, Tuple
import numpy as np
from matplotlib import pyplot as plt
from pearson import (
    pearson_corr_basic,
    pearson_corr_tensor,
    scipy_pearsonr_corr,
)
from helper import random_list


def test(
    base: Optional[float] = None,
    samples: Optional[int] = 50,
    max_size: Optional[int] = 100000,
    functions: List[Callable[[List[float], List[float]], float]] = [
        pearson_corr_basic,
        pearson_corr_tensor,
        scipy_pearsonr_corr,
    ],
    std_cutoff: float = float('1e-10'),
    time_cutoff: float = 5,
    show_time: bool = True,
    show_results: bool = False,
    input_range: Tuple[float, float] = (-1, 1),
) -> None:
    error = ValueError(
        'Not enough arguments provided to determine the test sizes. Include at'
        ' least two of base, samples, or max_size.'
    )

    missing = sum([base is None, samples is None, max_size is None])
    if missing > 1:
        raise error
    elif missing == 0 or base is None:
        base = max_size ** (1 / samples)
    elif samples is None:
        samples = math.ceil(math.log(max_size, base))

    test_sizes = [math.ceil(base ** n) for n in range(2, samples + 1)]
    test_data = (
        (random_list(length, *input_range), random_list(length, *input_range))
        for length in test_sizes
    )

    print(f'Testing with {functions = }')
    stds = []
    times = []
    for index, (x, y) in enumerate(test_data):
        results = []
        pass_times = []
        for f in functions:
            start = perf_counter()
            result = f(x, y)
            end = perf_counter()
            pass_times.append(end - start)
            results.append(result)

        times.append(pass_times)
        std = np.std(results)
        stds.append(std)
        print(f'Pass {index + 1}/{samples}, {std = }')
        if show_results:
            print(f'{results = }')
        if sum(pass_times) > time_cutoff:
            print(
                f'Time limit of {time_cutoff} seconds reached. Last pass took'
                f' {sum(pass_times)} seconds. Aborting after'
                f' {index + 1} passes.'
            )
            test_sizes = test_sizes[: index + 1]
            break

    max_std = max(stds)
    if max_std < std_cutoff:
        print(f'Test passed! {max_std=} < {std_cutoff=}')
    else:
        print(f'Test failed! {max_std=} > {std_cutoff=}')

    if not show_time:
        return

    labels = [f.__name__ for f in functions]

    print(f'At max input size of {test_sizes[-1]}:')
    for label, time in zip(labels, times[-1]):
        print(f'    {label} took {time} seconds')

    _, ax = plt.subplots()
    for index, time in enumerate(zip(*times)):
        label = functions[index].__name__
        ax.plot(test_sizes, time, label=label)
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Time')
    ax.set_title('Time of functions given input size')
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.legend()

    print('Press enter to show time graph... ')
    input()

    plt.show()


if __name__ == '__main__':
    test()