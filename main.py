import sys

new_path = '/Users/n87557/Documents/Metodologia de capital/DECT/bin'

if new_path not in sys.path:
    sys.path.append(new_path)

import credit
from scenario import scenarios
import pandas as pd
import numpy as np

cor_credit = pd.read_excel("/Users/n87557/Documents/Metodologia de capital/DECT/data/cor_credit_drivers.xlsx")
sensi = pd.read_excel("/Users/n87557/Documents/Metodologia de capital/DECT/data/TB_SENSIB_corr.xlsx")

x = scenarios(cor_credit, sensi)
x.generate(10000)

tb_ru = pd.read_excel("/Users/n87557/Documents/Metodologia de capital/DECT/data/TB_PD_RU_All.xlsx")

tb_ru = pd.merge(tb_ru, x.rnd)

tb_ru = tb_ru.assign(
  cpd = lambda x: credit.cond_pd_retail(x.PD, x.Rho, x.CWI)
)

tb_ru = tb_ru.assign(
  loss = lambda x: credit.loss(x.cpd, x.EAD, x.LGD)
)

# total capital

tb_ru.loss.sum()

# by segment / country

# by country

# by segment

# diversification by segment

# diversification by country

# total diversification
