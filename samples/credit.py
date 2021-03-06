import numpy as np
import scipy.stats


def cond_pd_retail(PD, rho, CWI):
  return scipy.stats.norm.cdf((scipy.stats.norm.ppf(PD) - np.sqrt(rho) * CWI) / np.sqrt(1 - rho))

# def cond_pd_wholesale(PD, rho, CWI):
#   return scipy.stats.norm.cdf((scipy.stats.norm.ppf(PD) - sqrt(rho) * CWI) / sqrt(1 - rho))

def loss(cond_pd, EAD, LGD):
  return cond_pd * EAD * LGD

