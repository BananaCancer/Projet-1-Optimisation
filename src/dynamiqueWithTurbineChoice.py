import copy
from typing import Dict, List, Union

import numpy as np
import pandas as pd

MIN_DEBIT = 0
MAX_DEBIT = 160
PAS_DEBIT = 5


# Paramètres



# L’élévation avale en fonction du débit total
# f(x) = p1*x^2 + p2*x + p3	

elevation_avale_en_fonction_du_debit_total = [-1.453*10**(-6), 0.007022, 99.9812] # [p1, p2, p3] 

# puissance turbine 1 = 1.1018 − 0.0487x − 0.0319y + 0.0022x2 + 0.0033xy
# puissance turbine 2 = 0.6987 − 0.1750x − 0.0201y + 0.0036x2 + 0.0042xy − 1.6988 × 10−5x3 + 3.5401 × 10−5x2y
# puissance turbine 3 = 0.7799 + 0.1995x − 0.0226y − 0.0017xy + 0.0001x2y 
# puissance turbine 4 = 0.2212 − 0.0487x − 0.0319y + 0.0022x2 + 0.0033xy

# La puissance produite en fonction de la hauteur de chute nette et du débit turbiné
# f(x,y) = p00 + p10*x + p01*y + p20*x^2 + p11*x*y + p02*y^2 + p30*x^3 + p21*x^2*y + p12*x*y^2 + p03*y^3 + p40*x^4 + p31*x^3*y + p22*x^2*y^2 + p13*x*y^3 + p04*y^4

# x : debit
# y : Chute nette

# turbine 1             p00  |    x    |    y    |   x^2   |   x*y   |   y^2   |       x^3       |      x^2*y    |  x*y^2  |   y^3   |                   
puissance_turbine_1 = [1.1018, -0.04866, -0.03187, 0.002182, 0.003308,    0    , -1.2771e-05, 3.683e-05,     0   ,     0   ]

# turbine 2             p00  |    x    |    y    |   x^2   |   x*y   |   y^2   |       x^3       |      x^2*y     |  x*y^2  |   y^3   |
puissance_turbine_2 = [0.6987, -0.175, -0.02011, 0.003632, 0.004154,    0    , -1.6988e-05, 3.5401e-05,     0   ,     0   ]

# turbine 3             p00  |    x    |    y    |       x^2       |   x*y    |   y^2   |       x^3      |     x^2*y     |  x*y^2  |   y^3   |
puissance_turbine_3 = [0.7799,  0.1995 , -0.02261, -3.519e-05 , -0.001695,     0   , -9.338e-06, 7.235e-05,     0   ,     0   ]

# turbine 4             p00    |    x    |    y    |   x^2   |   x*y   |   y^2   |        x^3      |       x^2*y     |  x*y^2  |   y^3   |
puissance_turbine_4 = [20.2212 , -0.4586, -0.5777, 0.004886, 0.01151,     0   , -1.882e-05,   1.379e-05,     0   ,     0   ]

# turbine 5             p00  |    x    |    y    |   x^2   |   x*y   |   y^2   |        x^3      |       x^2*y     |  x*y^2  |   y^3   |
puissance_turbine_5 = [1.9786, 0.004009, -0.05699, 0.001064, 0.005456,     0   ,  -8.162e-06,   2.849e-05,     0   ,     0   ]
		

ARRAY_COEFFICIENTS_TURBINES = [puissance_turbine_1, puissance_turbine_2, puissance_turbine_3, puissance_turbine_4, puissance_turbine_5]








def calculer_chute_nette(debit_turbine: Union[int,float],
                         q_total: int,
                         niveau_amont: float) -> Union[int,float]:
  # Vérifier si le débit est dans la plage admissible
  if debit_turbine < MIN_DEBIT or debit_turbine > MAX_DEBIT:
    raise ValueError(f"Le débit doit être compris entre {MIN_DEBIT} et {MAX_DEBIT} m³/s.")

  # Déterminer l'élévation avale en fonction du débit total
  elevation_avale = elevation_avale_en_fonction_du_debit_total[0] * q_total**2 + \
                    elevation_avale_en_fonction_du_debit_total[1] * q_total + \
                    elevation_avale_en_fonction_du_debit_total[2]

  # Calculer la chute nette
  chute_nette = niveau_amont - elevation_avale - (0.5 * (10**-5) * (debit_turbine**2))

  return chute_nette


  
def getListeEtatsParTurbine(turbines: list,
                            q_total: int) -> Dict[int,List[int]]:
  nb_turbines = len(turbines)
  result: Dict[int,List[int]] = {}
  result[turbines[0]] = [q_total]

  for i, turbine in enumerate(turbines[1:]):
    # Débit max restant: Max débit * nb turbines restantes 
    # ou QTot si Max débit * nb turbines restantes > Qtot
    debit_restant_max = MAX_DEBIT*(nb_turbines-i-1) if MAX_DEBIT*(nb_turbines-i-1) < q_total else q_total
    debit_restant_max = round(debit_restant_max,2)

    # Débit min restant: Débit total - DébitMax * Nb turbines avant (ou 0)
    debit_restant_min = q_total - MAX_DEBIT*(i+1) if (q_total - MAX_DEBIT*(i+1)) > 0 else 0
    debit_restant_min = round(debit_restant_min,2)

    debit_restant = list(np.arange(debit_restant_min,
                                   debit_restant_max,
                                   PAS_DEBIT))

    debit_restant.append(debit_restant_max)
    result[turbine]= debit_restant
  return result

def list_debit_turbine(q_total: int):
   """
   return Debit de la turbine possible
   """
   max_for_turbine = q_total if MAX_DEBIT > q_total else MAX_DEBIT
   debit_turbine = list(np.arange(MIN_DEBIT,max_for_turbine+PAS_DEBIT,PAS_DEBIT))
   debit_turbine[-1] = max_for_turbine
   return debit_turbine


def find_the_max_puissance(stage: pd.DataFrame,
                           turbineID: int) -> pd.DataFrame:
  xn = f"X{turbineID}"
  fn = f"F{turbineID}"

  for debit_restant in stage.index:
    # Filter out non-numeric values and convert to float
    numeric_values = stage.loc[debit_restant, stage.columns.difference([fn, xn])]
    numeric_values = numeric_values.apply(pd.to_numeric, errors='coerce')
    numeric_values = numeric_values.dropna()  # Drop NaN values

    if not numeric_values.empty:
      max_value = numeric_values.max()
      max_column = numeric_values.idxmax()
      stage.at[debit_restant, fn] = max_value
      stage.at[debit_restant, xn] = max_column
  
  return stage


def createStagesDF(turbines: list,
                   listeEtats: Dict[int,List[int]],
                   debits_possible: List[int]):
  
  result = {}
  for i in turbines[:-1]:
    df = pd.DataFrame(index = listeEtats.get(i), columns = debits_possible)
    result[i] = df
  # La dernière turbine n'a pas de colonnes car on utilise tout le débit possible
  result[turbines[-1]] = pd.DataFrame(index = listeEtats.get(turbines[-1]), 
                                    columns = [])
  return result

def addOptimalResultCols(stage: pd.DataFrame,
                         turbineID: int):
  xn = f"X{turbineID}"
  fn = f"F{turbineID}"
  stage[xn] = None
  stage[fn] = None
  return xn, fn

def powerFunction(debit_turbine: Union[int,float],
                  chute_nette: Union[int,float],
                  coefficients: list):
  return coefficients[0] + \
         coefficients[1] * debit_turbine +\
         coefficients[2] * chute_nette + \
         coefficients[3] * debit_turbine**2 +\
         coefficients[4] * debit_turbine * chute_nette +\
         coefficients[5] * chute_nette**2 +\
         coefficients[6] * debit_turbine**3 +\
         coefficients[7] * debit_turbine**2*chute_nette  +\
         coefficients[8] * debit_turbine*chute_nette**2  +\
         coefficients[9] * chute_nette**3 

def fillLastStage(stage: pd.DataFrame,
                  fonctionPuissance: list,
                  turbineID: int,
                  q_total,
                  niveau_amont) -> pd.DataFrame: 
  """
  debit_restant : lignes
  debit_turbine : columns
  c o l u m n s
  l
  i
  g
  n
  e
  s
  """
  xn, fn = addOptimalResultCols(stage, turbineID)

  for debit_restant in stage.index:
    debit_turbine = debit_restant
    stage.loc[debit_restant, xn] = debit_restant
    
    chute_nette = calculer_chute_nette(debit_turbine, q_total, niveau_amont)
    puissance = powerFunction(debit_turbine, chute_nette, fonctionPuissance)
    stage.loc[debit_restant, fn] = puissance
  return stage



def fillPreviousStages(stage: pd.DataFrame,
                       previousStage: pd.DataFrame,
                       fonctionPuissance: list,
                       turbineID: int,
                       previousTurbineID: int,
                       turbineIndex: int,
                       q_total: int,
                       niveau_amont: float,
                       nb_turbines: int) -> pd.DataFrame: 
  """
  debit_restant : lignes
  debit_turbine : columns
  c o l u m n s
  l
  i
  g
  n
  e
  s
  """
  

  debit_restant_max_for_turbine_after = MAX_DEBIT * (nb_turbines - turbineIndex) if MAX_DEBIT*(nb_turbines - turbineIndex) < q_total else q_total
  debit_turbine_columns = stage.columns
  addOptimalResultCols(stage, turbineID)
  for debit_restant in stage.index:
    for debit_turbine in debit_turbine_columns:
      chute_nette = calculer_chute_nette(debit_turbine, q_total, niveau_amont)

      debit_for_turbine_after = debit_restant-debit_turbine
      if debit_for_turbine_after < 0 or debit_for_turbine_after > debit_restant_max_for_turbine_after:
        stage.loc[debit_restant, debit_turbine] = "-"
        debit_for_turbine_after = None

      if debit_for_turbine_after != None:
        puissance_add = previousStage.loc[debit_for_turbine_after, f"F{previousTurbineID}"]
        
        puissance = puissance_add + powerFunction(debit_turbine, chute_nette, 
                                                  fonctionPuissance)
        
        stage.loc[debit_restant, debit_turbine] = puissance
  
    stage = find_the_max_puissance(stage=stage,
                                                    turbineID=turbineID)
    
  return stage


def forward_pass(stage : pd.DataFrame,
                 df_tableau_turbine_after :pd.DataFrame,
                 number_to_choose: int,
                 prevStageID: int) -> pd.DataFrame:
  debit_restant = stage.index[0]
  debit_choose = stage.loc[debit_restant,f"X{prevStageID}"]

  debit_restant_after = debit_restant - debit_choose
  # debit_choose_after = df_tableau_turbine_after.loc[debit_restant_after,f"X{number_to_choose}"]

  final_df = df_tableau_turbine_after.loc[[debit_restant_after]]
  return final_df

def backwardPass(turbines: list, q_total: int, niveau_amont: float, emptyStages):
  nb_turbines = len(turbines)
  filledStages = {}
  for i, turbineID in enumerate(turbines[::-1]):
    if turbineID == turbines[-1]:
      filledStages[turbineID] = fillLastStage(copy.copy(emptyStages[turbineID]),
                                      ARRAY_COEFFICIENTS_TURBINES[turbineID - 1],
                                      turbineID,
                                      q_total,
                                      niveau_amont)
    else:
      filledStages[turbineID] = fillPreviousStages(copy.copy(emptyStages[turbineID]),
                                           copy.copy(filledStages[prevStage]),
                                           ARRAY_COEFFICIENTS_TURBINES[turbineID - 1],
                                           turbineID,
                                           prevStage,
                                           nb_turbines - i,
                                           q_total,
                                           niveau_amont,
                                           nb_turbines)
    prevStage = turbineID
  return filledStages

def loopForwardPass(turbines, filledStages):
    dfs_choose = {}
    prevStage = turbines[0]
    dfs_choose[prevStage] = copy.copy(filledStages[prevStage])

    for i in turbines[1:]:
      dfs_choose[i] = forward_pass(stage = copy.copy(dfs_choose[prevStage]),
                                 df_tableau_turbine_after = copy.copy(filledStages[i]),
                                 number_to_choose = i,
                                 prevStageID = prevStage)
      prevStage = i
    return dfs_choose

def algo(q_total, niveau_amont, turbines):
  listeEtats = getListeEtatsParTurbine(turbines, q_total)
  debits_possible = list_debit_turbine(q_total)
  emptyStages = createStagesDF(turbines, listeEtats, debits_possible)
  filledStages = backwardPass(turbines, q_total, niveau_amont, emptyStages)
  dfs_choose = loopForwardPass(turbines, filledStages)
  
  return dfs_choose



if __name__ == "__main__":
  q_total = 	580 # doit être multiple de PAS_DEBIT sinon erreur
  niveau_amont = 	137.89
  turbines = [1, 2, 4, 5]
  #algo(q_total, niveau_amont, turbines)
  df = pd. read_excel("data/DataProjet2024.xlsx")
  STARTING_ROW = 2
  ROW_COUNT = 100
  for row in range(STARTING_ROW, STARTING_ROW + ROW_COUNT + 1):
    debit_total = round(df.iloc[row, 2] / 5) * 5
    niveau_amont = df.iloc[row, 5]
    actives_turbines = []
    debits_turbines = {}
    puissances_turbines = {}
    sumPuissance = 0
    sumComputedPuissance = 0
    for i in range(5):
      if int(df.iloc[row, 6 + 2 * i]) != 0:
        actives_turbines.append(i+1)
        debits_turbines[i + 1] = df.iloc[row, 6 + 2 * i]
        puissances_turbines[i + 1] = df.iloc[row, 7 + 2 * i]
        sumPuissance += df.iloc[row, 7 + 2 * i]

    result = algo(debit_total,niveau_amont, actives_turbines)
    sumDifferences = 0
    for i, IDturbine in enumerate(actives_turbines):
      if (i < len(actives_turbines) - 1):
        nextTurbine = actives_turbines[i+1]
        currentPuissance = result[IDturbine]['F' + str(IDturbine)].values[0] - result[nextTurbine]['F'+str(nextTurbine)].values[0]
      else:
        currentPuissance = result[IDturbine]['F' + str(IDturbine)].values[0]
      sumComputedPuissance += currentPuissance
      currentDebit = result[IDturbine]['X'+str(IDturbine)].values[0]
      print(f"Turbine {IDturbine}")
      print(f"Débit utilisé : {debits_turbines[IDturbine]} (réelle) vs {currentDebit} (calculée)")
      print(f"Puissance produite : {puissances_turbines[IDturbine]} (réelle) vs {currentPuissance} (calculée)")
      print(" ========================================= ")
    print(f"Puissance totale produite : {sumPuissance} (réelle) vs {sumComputedPuissance}")
    sumDifferences += sumComputedPuissance - sumPuissance
  print(sumDifferences)
    
    
    
