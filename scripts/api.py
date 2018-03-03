from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), ''))

import label_image


if __name__ == '__main__':

    label_image.check()
