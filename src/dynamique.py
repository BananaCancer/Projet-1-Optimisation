import copy
from typing import Dict, List, Union

import numpy as np
import pandas as pd


MIN_DEBIT = 0
MAX_DEBIT = 160
PAS_DEBIT = 5


Q_TOTAL = 	540 # doit être multiple de PAS_DEBIT sinon erreur

NIVEAU_AMONT = 	137.89

NB_TURBINE = 5

# L’élévation avale en fonction du débit totat	
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
puissance_turbine_1 = [1.1018, -0.04866, -0.03187, 0.002182, 0.003308,    0    , -1.2771*10**(-5), 3.683*10**(-5),     0   ,     0   ]

# turbine 2             p00  |    x    |    y    |   x^2   |   x*y   |   y^2   |       x^3       |      x^2*y     |  x*y^2  |   y^3   |
puissance_turbine_2 = [0.6987, -0.17500, -0.02011, 0.003632, 0.004154,    0    , -1.6988*10**(-5), 3.5401*10**(-5),     0   ,     0   ]

# turbine 3             p00  |    x    |    y    |       x^2       |   x*y    |   y^2   |       x^3      |     x^2*y     |  x*y^2  |   y^3   |
puissance_turbine_3 = [0.7799,  0.1995 , -0.02261, -3.519*10**(-5) , -0.001695,     0   , -9.338*10**(-5), 7.235*10**(-5),     0   ,     0   ]

# turbine 4             p00    |    x    |    y    |   x^2   |   x*y   |   y^2   |        x^3      |       x^2*y     |  x*y^2  |   y^3   |
puissance_turbine_4 = [20.2212 , -0.4586, -0.577700, 0.004886, 0.011510,     0   , -1.8820*10**(-5),   1.379*10**(-5),     0   ,     0   ]

# turbine 5             p00  |    x    |    y    |   x^2   |   x*y   |   y^2   |        x^3      |       x^2*y     |  x*y^2  |   y^3   |
puissance_turbine_5 = [1.9786, 0.004009, -0.05699, 0.001064, 0.005456,     0   ,  -8.162*10**(-5),   2.849*10**(-5),     0   ,     0   ]
		










def calculer_chute_nette(debit_turbine: Union[int,float]) -> Union[int,float]:

  # Vérifier si le débit est dans la plage admissible
  if debit_turbine < MIN_DEBIT or debit_turbine > MAX_DEBIT:
    raise ValueError(f"Le débit doit être compris entre {MIN_DEBIT} et {MAX_DEBIT} m³/s.")

  # Déterminer l'élévation avale en fonction du débit total
  elevation_avale = elevation_avale_en_fonction_du_debit_total[0] * Q_TOTAL**2 + \
                    elevation_avale_en_fonction_du_debit_total[1] * Q_TOTAL + \
                    elevation_avale_en_fonction_du_debit_total[2]

  # Calculer la chute nette
  chute_nette = NIVEAU_AMONT - elevation_avale - (0.5 * (10**-5) * (debit_turbine**2))

  return chute_nette


  
def list_turbine_restant(nb_turbine: int = 5) -> Dict[int,List[int]]:
  result: Dict[int,List[int]] = {}
  result[1] = [Q_TOTAL]

  for i in range(2,nb_turbine+1):
    debit_restant_max = MAX_DEBIT*(nb_turbine-i+1) if MAX_DEBIT*(nb_turbine-i+1) < Q_TOTAL else Q_TOTAL
    debit_restant_max = round(debit_restant_max,2)

    debit_restant_min = Q_TOTAL - MAX_DEBIT*(i-1) if (Q_TOTAL - MAX_DEBIT*(i-1)) > 0 else 0
    debit_restant_min = round(debit_restant_min,2)

    debit_restant = list(np.arange(debit_restant_min,debit_restant_max+PAS_DEBIT,PAS_DEBIT))
    debit_restant = [value for value in debit_restant if value < debit_restant_max]
    debit_restant.append(debit_restant_max)
    result[i]= debit_restant

  return result

def list_debit_turbine():
   """
   return Debit de la turbine possible
   """
   max_for_turbine = Q_TOTAL if MAX_DEBIT>Q_TOTAL else MAX_DEBIT
   debit_turbine = list(np.arange(MIN_DEBIT,max_for_turbine+PAS_DEBIT,PAS_DEBIT))
   debit_turbine[-1] = max_for_turbine
   return debit_turbine


def find_the_max_puissance(df_tableau_this_turbine: pd.DataFrame,
                           number_of_this_turbine: int) -> pd.DataFrame:
  xn = f"X{number_of_this_turbine}"
  fn = f"F{number_of_this_turbine}"

  for debit_restant in df_tableau_this_turbine.index:
    # Filter out non-numeric values and convert to float
    numeric_values = df_tableau_this_turbine.loc[debit_restant, df_tableau_this_turbine.columns.difference([fn, xn])]
    numeric_values = numeric_values.apply(pd.to_numeric, errors='coerce')
    numeric_values = numeric_values.dropna()  # Drop NaN values

    if not numeric_values.empty:
      max_value = numeric_values.max()
      max_column = numeric_values.idxmax()
      df_tableau_this_turbine.at[debit_restant, fn] = max_value
      df_tableau_this_turbine.at[debit_restant, xn] = max_column
  
  return df_tableau_this_turbine


def create_df_tableau_for_each_turbine(nb_turbine: int,
                                       debit_restant: Dict[int,List[int]],
                                       turbine_possible: List[int]):
  
  result = {}
  for i in range(1,nb_turbine,1):
    df = pd.DataFrame(index=debit_restant.get(i), columns=turbine_possible)
    result[i] = df
  result[nb_turbine] = pd.DataFrame(index=debit_restant.get(nb_turbine), columns=[])
  return result


def calcule_puissance_tableau_first(df_tableau_this_turbine: pd.DataFrame,
                                    formule_puissance_turbine: list,
                                    number_of_this_turbine: int = 5) -> pd.DataFrame: 
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
  xn = f"X{number_of_this_turbine}"
  fn = f"F{number_of_this_turbine}"

  df_tableau_this_turbine[xn] = None  # Create a column 'X5' with None values
  df_tableau_this_turbine[fn] = None  # Create a column 'F5' with None values
  for debit_restant in df_tableau_this_turbine.index:
    debit_turbine = debit_restant

    df_tableau_this_turbine.loc[debit_restant, xn] = debit_restant
    
    chute_nette = calculer_chute_nette(debit_turbine=debit_turbine)
    puissance = formule_puissance_turbine[0] + \
                formule_puissance_turbine[1] * debit_turbine +\
                formule_puissance_turbine[2] * chute_nette + \
                formule_puissance_turbine[3] * debit_turbine**2 +\
                formule_puissance_turbine[4] * debit_turbine * chute_nette +\
                formule_puissance_turbine[5] * chute_nette**2 +\
                formule_puissance_turbine[6] * debit_turbine**3 +\
                formule_puissance_turbine[7] * debit_turbine**2*chute_nette  +\
                formule_puissance_turbine[8] * debit_turbine*chute_nette**2  +\
                formule_puissance_turbine[9] * chute_nette**3 
    df_tableau_this_turbine.loc[debit_restant, fn] = puissance

  return df_tableau_this_turbine



def calcule_puissance_tableau_middle(df_tableau_this_turbine: pd.DataFrame,
                                     df_tableau_before_turbine: pd.DataFrame,
                                     formule_puissance_turbine: list,
                                     number_of_this_turbine: int) -> pd.DataFrame: 
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
  xn = f"X{number_of_this_turbine}"
  fn = f"F{number_of_this_turbine}"

  debit_restant_max_for_turbine_after = MAX_DEBIT*(NB_TURBINE-number_of_this_turbine) if MAX_DEBIT*(NB_TURBINE-number_of_this_turbine) < Q_TOTAL else Q_TOTAL
  debit_turbine_columns = df_tableau_this_turbine.columns

  df_tableau_this_turbine[xn] = None  
  df_tableau_this_turbine[fn] = None  
  
  for debit_restant in df_tableau_this_turbine.index:
    for debit_turbine in debit_turbine_columns:
      chute_nette = calculer_chute_nette(debit_turbine=debit_turbine)

      debit_for_turbine_after = debit_restant-debit_turbine
      if debit_for_turbine_after < 0 or debit_for_turbine_after > debit_restant_max_for_turbine_after:
        df_tableau_this_turbine.loc[debit_restant, debit_turbine] = "-"
        debit_for_turbine_after = None

      if debit_for_turbine_after != None:
        puissance_add = df_tableau_before_turbine.loc[debit_for_turbine_after, f"F{number_of_this_turbine+1}"]
        # print(f"{debit_restant}-{debit_turbine} : {puissance_add}")

        puissance = formule_puissance_turbine[0] + \
                    formule_puissance_turbine[1] * debit_turbine +\
                    formule_puissance_turbine[2] * chute_nette + \
                    formule_puissance_turbine[3] * debit_turbine**2 +\
                    formule_puissance_turbine[4] * debit_turbine * chute_nette +\
                    formule_puissance_turbine[5] * chute_nette**2 +\
                    formule_puissance_turbine[6] * debit_turbine**3 +\
                    formule_puissance_turbine[7] * debit_turbine**2*chute_nette  +\
                    formule_puissance_turbine[8] * debit_turbine*chute_nette**2  +\
                    formule_puissance_turbine[9] * chute_nette**3 +\
                    puissance_add
        
        df_tableau_this_turbine.loc[debit_restant, debit_turbine] = puissance
  
    df_tableau_this_turbine = find_the_max_puissance(df_tableau_this_turbine=df_tableau_this_turbine,
                                                    number_of_this_turbine=number_of_this_turbine)
    
  return df_tableau_this_turbine


def forward_pass(df_tableau_this_turbine : pd.DataFrame,
                 df_tableau_turbine_after :pd.DataFrame,
                 number_to_choose: int) -> pd.DataFrame:
  debit_restant = df_tableau_this_turbine.index[0]
  debit_choose = df_tableau_this_turbine.loc[debit_restant,f"X{number_to_choose-1}"]

  debit_restant_after = debit_restant - debit_choose
  # debit_choose_after = df_tableau_turbine_after.loc[debit_restant_after,f"X{number_to_choose}"]

  final_df = df_tableau_turbine_after.loc[[debit_restant_after]]
  return final_df


if __name__ == "__main__":
  # ====
  debit_restant = list_turbine_restant(nb_turbine=NB_TURBINE)
  # for i in debit_restant.keys():
  #   print(f" {i}: {debit_restant[i][0]} - {debit_restant[i][-1]} => {len(debit_restant[i])}")
  # # ====
  turbine_possible = list_debit_turbine()
  df_tableau = create_df_tableau_for_each_turbine(nb_turbine=NB_TURBINE,
                                                  debit_restant=debit_restant,
                                                  turbine_possible=turbine_possible)



  df_tableau_5 = calcule_puissance_tableau_first(df_tableau_this_turbine=copy.copy(df_tableau[5]),
                                                 formule_puissance_turbine=puissance_turbine_5,
                                                 number_of_this_turbine=5)

  df_tableau_4 = calcule_puissance_tableau_middle(df_tableau_this_turbine=copy.copy(df_tableau[4]),
                                                  df_tableau_before_turbine=copy.copy(df_tableau_5),
                                                  formule_puissance_turbine=puissance_turbine_4,
                                                  number_of_this_turbine=4)

  # print(df_tableau_4[-10:])
  df_tableau_3 = calcule_puissance_tableau_middle(df_tableau_this_turbine=copy.copy(df_tableau[3]),
                                                  df_tableau_before_turbine=copy.copy(df_tableau_4),
                                                  formule_puissance_turbine=puissance_turbine_3,
                                                  number_of_this_turbine=3)
  # print(df_tableau_3[-10:])

  df_tableau_2 = calcule_puissance_tableau_middle(df_tableau_this_turbine=copy.copy(df_tableau[2]),
                                                  df_tableau_before_turbine=copy.copy(df_tableau_3),
                                                  formule_puissance_turbine=puissance_turbine_2,
                                                  number_of_this_turbine=2)
  # print(df_tableau_2[-10:])


  df_tableau_1 = calcule_puissance_tableau_middle(df_tableau_this_turbine=copy.copy(df_tableau[1]),
                                                  df_tableau_before_turbine=copy.copy(df_tableau_2),
                                                  formule_puissance_turbine=puissance_turbine_1,
                                                  number_of_this_turbine=1)
  df_tableau_1_choose = copy.copy(df_tableau_1)

  df_tableau_2_choose = forward_pass(df_tableau_this_turbine=copy.copy(df_tableau_1_choose),
                                      df_tableau_turbine_after=copy.copy(df_tableau_2),
                                      number_to_choose = 2)
  # print(type(df_tableau_2_choose))
  # print(type(df_tableau_1))
  # print(df_tableau_2_choose)
  
  df_tableau_3_choose = forward_pass(df_tableau_this_turbine=copy.copy(df_tableau_2_choose),
                                      df_tableau_turbine_after=copy.copy(df_tableau_3),
                                      number_to_choose = 3)

  
  df_tableau_4_choose = forward_pass(df_tableau_this_turbine=copy.copy(df_tableau_3_choose),
                                      df_tableau_turbine_after=copy.copy(df_tableau_4),
                                      number_to_choose = 4)

  df_tableau_5_choose = forward_pass(df_tableau_this_turbine=copy.copy(df_tableau_4_choose),
                                      df_tableau_turbine_after=copy.copy(df_tableau_5),
                                      number_to_choose = 5)
  
  print(" ========================================= ")
  print(f"turbine 1 : Q1 = {df_tableau_1_choose['X1'].values[0]}")
  print(f"turbine 2 : Q2 = {df_tableau_2_choose['X2'].values[0]}")
  print(f"turbine 3 : Q3 = {df_tableau_3_choose['X3'].values[0]}")
  print(f"turbine 4 : Q4 = {df_tableau_4_choose['X4'].values[0]}")
  print(f"turbine 5 : Q5 = {df_tableau_5_choose['X5'].values[0]}")








  




