from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), ''))

import label_image


if __name__ == '__main__':

    top_ranks, labels, results, evaluation_time = label_image.check()

    highest_rank = top_ranks[0]
    most_relevant_value = results[highest_rank] * 100
    most_relevant_name = labels[highest_rank]

    if most_relevant_value >= 70:
        print('\nEvaluation time: {0:.3f}s\n'.format(evaluation_time))
        print('The entered image is "' + most_relevant_name + '"\n')