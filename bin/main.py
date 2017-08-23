import sys

new_path = '/Users/n87557/Documents/Metodologia de capital/DECT/bin'

if new_path not in sys.path:
    sys.path.append(new_path)

import credit
from scenario import scenarios
import pandas as pd
import numpy as np

cor_credit = pd.read_excel("/Users/n87557/Documents/Metodologia de capital/DECT/data/cor_credit_drivers.xlsx")
sensi = pd.read_excel("/Users/n87557/Documents/Metodologia de capital/DECT/data/Sensib.xlsx")

x = scenarios(cor_credit, sensi)
x.generate(10000)


