#!/usr/bin/env python3

import sys
import pandas as pd
import numpy as np
import re

import consistency
import analysisMethods as am

if len(sys.argv) < 2:
    print("Usage: analysis.py <file-to-read>")
    exit()


pd.set_option('max_colwidth',500) # makes data easier to read when printing

try:
    df = pd.read_csv(sys.argv[1], sep='\t', dtype='unicode') # dataframe object representingfull dataset
except FileNotFoundError:
    print(str(sys.argv[1]) + " not found")
    exit()

if not sys.argv[1].endswith("_consistent.tsv"):
    df = consistency.removeInconsistentData(df)
    new_data = open(re.split("(\.)", sys.argv[1])[0] + "_consistent.tsv", "w")
    new_data.write(df.to_csv(index=False, sep='\t'))
    new_data.close()
else:
    df = consistency.getTypesForCleanData(df)

print("")
am.initialAnalysis(df)
print("")
am.additionalAnalysis(df)
print("")
