#!/usr/bin/env python3.9

import time
from repetidos import *

for n in [10, 100, 1000, 10000, 100000, 1000000]:
    test = f"nums/nums{n}"
    f = open(test)
    nums = read_data(f)
    t0 = time.process_time()
    m = process(nums)
    t1 = time.process_time()
    print (f"{test+':':18} {t1-t0:f}")