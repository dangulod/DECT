import numpy as np
import pandas as pd
from math import sqrt

class scenarios:
  
  def f(self, x):
    if (x.split("_")[0] == "SCF"):
      return x.split("_")[1]
    else:
      return x.split("_")[0]
  
  def __init__(self, cor_credit, sensitivities):
    self.cor_credit = cor_credit
    self.n_simul = None
    self.rnd = None
    self.sensitivities = sensitivities.assign(
      IF = list(map(sqrt, round(1 - (sensitivities['GF'] ** 2 + sensitivities['LF'] ** 2),7))), 
      map = list(map(self.f, np.array(sensitivities[sensitivities.columns[0]])))
    )
  
  def generate(self, n_simul):
    self.n_simul = n_simul
    U, s, V = np.linalg.svd(self.cor_credit, full_matrices=True)
    s = np.diag(list(map(sqrt, s)))
    self.rnd = pd.DataFrame(np.dot(np.dot(U, s), np.random.randn(self.cor_credit.shape[1], self.n_simul)).transpose())
    self.rnd.columns = self.cor_credit.columns
    self.rnd = self.rnd.assign(
      index = np.array(range(1, self.n_simul + 1)))
    self.rnd = pd.melt(self. rnd, id_vars=['index', 'GLOBAL'], var_name = 'map', value_name = 'LOCAL')
    self.rnd = pd.merge(self.sensitivities, self.rnd)
    self.rnd = self.rnd.assign(
      idio = np.random.randn(self.n_simul * (self.cor_credit.shape[1] - 1)))
    self.rnd = self.rnd.assign(
      CWI = ((self.rnd['GF'] * self.rnd['GLOBAL']) + (self.rnd['LF'] * self.rnd['LOCAL']) + (self.rnd['IF'] * self.rnd['idio']))) # np.random.randn(self.n_simul * (self.cor_credit.shape[1] - 1))    )
    self.rnd = self.rnd[['equation', 'index', 'CWI']]


