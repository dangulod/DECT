import numpy as np
import pandas as pd
from math import sqrt

class scenarios:
  
  """
  Scenarios class are used to generate scenatios through a correlation matrix and the weights to the local and 
  global factor. The correlation is given by singular value decompistion (SVD).
  
  This class is compound by 4 attributes:
    cor_credit - correlation matrix. This attribute must be a DataFrame
    n_simul - number of simulations performed
    rnd - scnenarios
    sensitivities - weights to global & local factor. This attribute must be a DataFrame
    
  The scenarios generated follow a normal standard distribution N(0, 1) because is generated as the lineal combination
  of three normal standard distribution:
  
  This scenarios are commonly known as Credit Worthiness Index (CWI) and its computed as follow:
  
    CWI = beta_global * GF + beta_local * LF + beta_idiosyncratic * IF
  """
  
  def __f(self, x):
    if (x.split("_")[0] == "SCF"):
      return x.split("_")[1]
    else:
      return x.split("_")[0]
  
  def __init__(self, cor_credit, sensitivities):
    
    self.cor_credit = cor_credit
    
    self.n_simul = None
    
    self.rnd = None
    
  # Idiosyncratic factor computation
    
    self.sensitivities = sensitivities.assign(
      IF = list(map(sqrt, round(1 - (sensitivities['GF'] ** 2 + sensitivities['LF'] ** 2),7))), 
      map = list(map(self.__f, np.array(sensitivities[sensitivities.columns[0]])))
    )
  
  def generate(self, n_simul):
    self.n_simul = n_simul
    
    U, s, V = np.linalg.svd(self.cor_credit, full_matrices=True)
    
    s = np.diag(list(map(sqrt, s)))
    
    self.rnd = pd.DataFrame(np.dot(np.dot(U, s), 
                            np.random.randn(self.cor_credit.shape[1], 
                            self.n_simul)).transpose())
    
    self.rnd.columns = self.cor_credit.columns
    
    self.rnd = self.rnd.assign(
      index = np.array(range(1, self.n_simul + 1))
      )
      
    self.rnd = pd.melt(self. rnd, id_vars=['index', 'GLOBAL'], var_name = 'map', value_name = 'LOCAL')
    
    self.rnd = pd.merge(self.sensitivities, self.rnd)
    
    self.rnd = self.rnd.assign(
      idio = np.random.randn(self.rnd.shape[0])
      )
      
    self.rnd = self.rnd.assign(
      CWI = ((self.rnd['GF'] * self.rnd['GLOBAL']) + (self.rnd['LF'] * self.rnd['LOCAL']) + (self.rnd['IF'] * self.rnd['idio']))) 
      
    self.rnd = self.rnd[['equation', 'index', 'CWI']]


