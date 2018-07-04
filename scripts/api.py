from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), ''))

from label_image import check


def detectTrafficSign (index):
    signsDec ={
        "00000": "120 km sign",
        "00001": "30 km sign",
        "00002": "50 km sign",
        "00003": "60 km sign",
        "00004": "70 km sign",
        "00005": "80 km sign",
        "00006": "80 km sign",
        "00007": "100 km sign",
        "00008": "120 km sign",
        "00009": "narrow path sign",
        "00010": "narrow path sign",
        "00011": "blocked road sign",
        "00012": "30 km sign",
        "00013": "watch your back sign",
        "00014": "Stop sign",
        "00015": "do nothing sign",
        "00016": "truck road sign",
        "00017": "wrong direction sign",
        "00018": "don't stop sign",
        "00019": "turn right sign",
        "00020": "70 km sign",
        "00021": "80 km sign",
        "00022": "30 km sign",
        "00023": "30 km sign",
        "00024": "30 km sign",
        "00025": "30 km sign",
        "00026": "30 km sign",
        "00027": "people passing sign",
        "00028": "30 km sign",
        "00029": "30 km sign",
        "00030": "30 km sign",
        "00031": "30 km sign",
        "00032": "70 km sign",
        "00033": "80 km sign",
        "00034": "30 km sign",
        "00035": "30 km sign",
        "00036": "30 km sign",
        "00037": "30 km sign",
        "00038": "30 km sign",
        "00039": "30 km sign",
        "00040": "30 km sign",
        "00041": "30 km sign",
        "00042": "30 km sign",
    }
    image = '../data/cropped'+str(index)+'.png'
    top_ranks, labels, results, evaluation_time = check(image)

    highest_rank = top_ranks[0]
    most_relevant_value = results[highest_rank] * 100
    most_relevant_name = labels[highest_rank]
    signName = signsDec[most_relevant_name]
    
    print(most_relevant_name,most_relevant_value)

    if most_relevant_value >= 50:
        print('\nEvaluation time: {0:.3f}s\n'.format(evaluation_time))
        print('The entered image is "' + signName + '"\n')
        return signName
    else: 
        return 'no sign'