import pandas as pd
import joblib
from scipy.spatial.distance import pdist, squareform
from itertools import combinations
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from io import BytesIO
from ast import literal_eval  # Importar literal_eval para convertir las cadenas de texto a listas


def copy_csv(csv):
    df = pd.read_csv(csv)
    df_copia = df.copy()
    return df, df_copia

def parse_lists(cell):
    try:
        return literal_eval(cell)
    except (ValueError, SyntaxError):
        return cell


def transformar_lista(lista):
    if len(lista) > 0:
        return lista  
    else:
        return lista + [0]   

def ajustar_longitud_columnas_con_listas(df_total):
    columnas_con_listas = ['Muon_pt', 'Muon_eta', 'Muon_phi', 'Muon_mass', 'Muon_charge', 'Muon_dxy', 
                           'Muon_dxyErr', 'Muon_dz', 'Muon_dzErr', 'Muon_pfRelIso03_all', 
                           'Muon_pfRelIso04_all', 'Electron_pt', 'Electron_eta', 'Electron_phi', 
                           'Electron_mass', 'Electron_charge', 'Electron_dxy', 'Electron_dxyErr', 
                           'Electron_dz', 'Electron_dzErr', 'Electron_pfRelIso03_all']

    # Aplicar la función de ajuste de longitud a cada columna con listas
    for columna in columnas_con_listas:
        df_total[columna] = df_total[columna].apply(transformar_lista)

    return df_total

def calcular_medias_para_columnas_con_listas(df_total):
    df_total1 = df_total.copy()
    columnas_con_listas = ['Muon_pt', 'Muon_eta', 'Muon_phi', 'Muon_mass', 'Muon_charge', 'Muon_dxy', 
                           'Muon_dxyErr', 'Muon_dz', 'Muon_dzErr', 'Muon_pfRelIso03_all', 
                           'Muon_pfRelIso04_all', 'Electron_pt', 'Electron_eta', 'Electron_phi', 
                           'Electron_mass', 'Electron_charge', 'Electron_dxy', 'Electron_dxyErr', 
                           'Electron_dz', 'Electron_dzErr', 'Electron_pfRelIso03_all']
    # Iterar sobre las filas del DataFrame original
    for index, row in df_total1.iterrows():
        for column in columnas_con_listas:
            if isinstance(row[column], list):  # Verificar si la columna contiene una lista
                # Calcular la media de los valores en la lista
                mean_value = sum(row[column]) / len(row[column])
                # Actualizar el valor en el DataFrame original con la media
                df_total1.at[index, column] = mean_value
    return df_total1


def predecir_y_filtrar(df_total1, modelo_path1):
    # Carga el modelo de árbol de decisión desde el archivo
    modelo1 = joblib.load(modelo_path1)
    print(df_total1.columns)
    # Realiza predicciones en el DataFrame
    predicciones1 = modelo1.predict(df_total1)

    # Agrega las predicciones al DataFrame
    df_total1['Origin'] = predicciones1
    
    # Filtra el DataFrame basado en la columna de predicciones y el valor especificado
    df_filtrado1 = df_total1[df_total1['Origin'] == 0]
    
    return df_filtrado1

def seleccionar_por_indices(df_total_final, df_filtrado):
    # Obtener los índices filtrados del DataFrame filtrado
    indices_filtrados = df_filtrado.index
    
    # Seleccionar las filas correspondientes en el DataFrame original usando los índices filtrados
    df_seleccionado = df_total_final.loc[indices_filtrados]
    
    # Reiniciar los índices del DataFrame seleccionado
    df_seleccionado = df_seleccionado.reset_index(drop=True)
    
    return df_seleccionado

   

#Reconstrucción de los dos candidatos a bosón Z a partir de los 4 leptones del mismo tipo
def reconstruct_samekind(array):    
    z_mass = 91.2
    idx = np.zeros((2, 2), dtype=int)
    #Genera todas los pares de combinaciones posibles con el número de electrones que hay que serán 4
    pairs = list(combinations(range(len(array['Electron_pt'][0])), 2)) 
    z_idx = [] #lista donde guardar los índices de cada fila para crear una nueva columna en el dataframe
    for pt, eta, phi, mass, charge in zip(array['Electron_pt'],array['Electron_eta'],array['Electron_phi'],array['Electron_mass'],array['Electron_charge']): 
        # Encuentra el primer par de leptones con la masa invariante más cercana a la masa del bosón Z
        best_mass = -1
        for i1, i2 in pairs:
            if charge[i1] != charge[i2]:
               # Calcular componentes de energía y momento lineal para cada lepton
                energy1 = np.sqrt((pt[i1]*np.cosh(eta[i1]))**2 + mass[i1]**2)
                energy2 = np.sqrt((pt[i2]*np.cosh(eta[i2]))**2 + mass[i2]**2)
                px1 = pt[i1] * np.cos(phi[i1])
                py1 = pt[i1] * np.sin(phi[i1])
                pz1 = pt[i1] * np.sinh(eta[i1])
                px2 = pt[i2] * np.cos(phi[i2])
                py2 = pt[i2] * np.sin(phi[i2])
                pz2 = pt[i2] * np.sinh(eta[i2])

                # Calcular la masa invariante
                this_mass = np.sqrt((energy1 + energy2)**2 - (px1 + px2)**2 - (py1 + py2)**2 - (pz1 + pz2)**2)
                if np.abs(z_mass - this_mass) < np.abs(z_mass - best_mass):
                    best_mass = this_mass
                    best_i1, best_i2 = i1, i2
        
        idx[0] = [best_i1, best_i2]
        # Reconstrucción del segundo bosón Z a partir del par de leptones restantes
        remaining_indices = [i for i in range(4) if i != best_i1 and i != best_i2]
        idx[1] = remaining_indices
        z_idx.append(idx.copy())
    return z_idx

def calcular_energia_momento(pt, eta, phi, mass):
    px = pt * np.cos(phi)
    py = pt * np.sin(phi)
    pz = pt * np.sinh(eta)
    energy = np.sqrt(px**2 + py**2 + pz**2 + mass**2)
    return energy, px, py, pz

# Función para crear los cuadrivectores a partir de las componentes de energía y momento
def crear_cuadrivector(energy, px, py, pz):
    return np.array([energy, px, py, pz])

def calcular_masa_invariante(cuadrivector):
    energy = cuadrivector[0]
    momentum_modulus_squared = np.sum(cuadrivector[1:]**2)
    invariant_mass_squared = energy**2 - momentum_modulus_squared
    invariant_mass = np.sqrt(invariant_mass_squared)
    return invariant_mass

# Función principal para calcular los cuadrivectores de las partículas
def z_fourvectors_samekind(z_idx, array):
    lista_z_fourvecs = []
    z_mass = 91.2
    for fila in range(len(z_idx)):
        pt = array['Electron_pt'][fila]
        eta = array['Electron_eta'][fila]
        phi = array['Electron_phi'][fila]
        mass = array['Electron_mass'][fila]
        z_fourvecs = np.zeros((2, 4))  # Crear arreglo para almacenar cuadrivectores
        for i in range(2):
            i1 = z_idx[fila][i][0]
            i2 = z_idx[fila][i][1]
            energy1, px1, py1, pz1 = calcular_energia_momento(pt[i1], eta[i1], phi[i1], mass[i1])
            energy2, px2, py2, pz2 = calcular_energia_momento(pt[i2], eta[i2], phi[i2], mass[i2])
            cuadrivector = crear_cuadrivector(energy1 + energy2, px1 + px2, py1 + py2, pz1 + pz2)
            z_fourvecs[i] = cuadrivector

        # Ordenar cuadrivectores según proximidad a la masa del bosón Z
        if abs(calcular_masa_invariante(z_fourvecs[0]) - z_mass) < abs(calcular_masa_invariante(z_fourvecs[1]) - z_mass):
            lista_z_fourvecs.append(z_fourvecs)
        else:
            z_fourvecs = z_fourvecs[::-1]
            lista_z_fourvecs.append(z_fourvecs)

    return lista_z_fourvecs

def z_fourvectors_2el2mu(array):
    lista_z_fourvecs = [] #lista para meter cada cuadruvetcor de cada fila. Habrá dos por fila por cada par de electrones
    z_mass = 91.2
    for fila in range(0,len(array)):
        el_pt = array['Electron_pt'][fila]   
        el_eta = array['Electron_eta'][fila]   
        el_phi = array['Electron_phi'][fila]   
        el_mass = array['Electron_mass'][fila]   
        mu_pt = array['Muon_pt'][fila]   
        mu_eta = array['Muon_eta'][fila]   
        mu_phi = array['Muon_phi'][fila]   
        mu_mass = array['Muon_mass'][fila]  
        z_fourvecs = np.zeros((2,), dtype=object)
        i1 = 0 #índice primer electrón
        i2 = 1 #índice segundo electrón
        i3 = 0 #índice primer muón
        i4 = 1 #índice segundo muón
        if len(el_pt)>1 and len(el_eta)>1 and len(el_phi)>1 and len(el_mass)>1 and len(mu_pt)>1 and len(mu_eta)>1 and len(mu_phi)>1 and len(mu_mass)>1:
            energy_e1, px_e1, py_e1, pz_e1 = calcular_energia_momento(el_pt[i1], el_eta[i1], el_phi[i1], el_mass[i1]) 
            energy_e2, px_e2, py_e2, pz_e2 = calcular_energia_momento(el_pt[i2], el_eta[i2], el_phi[i2], el_mass[i2])
            energy_m1, px_m1, py_m1, pz_m1 = calcular_energia_momento(mu_pt[i3], mu_eta[i3], mu_phi[i3], mu_mass[i3])
            energy_m2, px_m2, py_m2, pz_m2 = calcular_energia_momento(mu_pt[i4], mu_eta[i4], mu_phi[i4], mu_mass[i4])
        
            p1 = crear_cuadrivector(energy_e1, px_e1, py_e1, pz_e1)
            p2 = crear_cuadrivector(energy_e2, px_e2, py_e2, pz_e2)
            p3 = crear_cuadrivector(energy_m1, px_m1, py_m1, pz_m1)
            p4 = crear_cuadrivector(energy_m2, px_m2, py_m2, pz_m2)
            
            z_fourvecs = [p1 + p2, p3 + p4]
        
            if abs(calcular_masa_invariante(z_fourvecs[0]) - z_mass) < abs(calcular_masa_invariante(z_fourvecs[1]) - z_mass):
                lista_z_fourvecs.append(z_fourvecs)
            else:
                z_fourvecs = z_fourvecs[::-1]
                lista_z_fourvecs.append(z_fourvecs)
        else: 
            lista_z_fourvecs.append(np.array([[0,0,0,0],[0,0,0,0]]))
    return lista_z_fourvecs

def Higgs_fourvec(array):
    fourvec = []
    for i in range(0, len(array)):
        fourvec.append(array['z_fourvecs'][i][0]+array['z_fourvecs'][i][1])
    return fourvec

def masas(array):
    Higgs_mass = []
    Z1_mass = []
    Z2_mass = []
    for i in range(0, len(array)):
        Higgs_mass.append(calcular_masa_invariante(array['Higgs_fourvec'][i]))
        Z1_mass.append(calcular_masa_invariante(array['z_fourvecs'][i][0]))
        Z2_mass.append(calcular_masa_invariante(array['z_fourvecs'][i][1]))
    return Higgs_mass, Z1_mass, Z2_mass

def seleccionar_columnas(df_seleccionado1):
    # Seleccionar las columnas especificadas en una nueva variable
    df_seleccionado_final = df_seleccionado1[["run", "Higgs_mass", "Z1_mass", "Z2_mass"]]
    return df_seleccionado_final


ranges = {
    "Higgs_mass": (36, 70, 180),
    "Z1_mass": (36, 40, 160),
    "Z2_mass": (36, 12, 160)
}

# Function to book a histogram for a specific variable
def bookHistogram(array, variable, range_):
    return np.histogram(array[variable], bins=range_[variable][0], range=(range_[variable][1], range_[variable][2]))

# Function to write a histogram with a given name to the output file
def writeHistogram(hist, bins, name):
    with open(f"{name}.txt", "w") as f:
        f.write("BinCenter BinContent\n")
        for i in range(len(bins)-1):
            bin_center = (bins[i] + bins[i+1]) / 2
            f.write(f"{bin_center} {hist[i]}\n")


def main1(array):
    print(f">>> Process skimmed sample {'Run2012B_DoubleElectron_filtrado'} and final state {'FourElectrons'}")

    # Load the data
    df = array

    # Book histograms
    histograms = {}
    for variable in ranges.keys():
        histograms[variable] = bookHistogram(df, variable, ranges)

    # Write histograms to output file
    for variable, histogram in histograms.items():
        writeHistogram(histogram[0], histogram[1], f"{'Run2012B_DoubleElectron_filtrado'}_{'FourElectrons'}_{variable}")

def main2(array):
    print(f">>> Process skimmed sample {'Run2012B_DoubleElectron'} and final state {'TwoMuonsTwoElectrons'}")

    # Load the data
    df = array

    # Book histograms
    histograms = {}
    for variable in ranges.keys():
        histograms[variable] = bookHistogram(df, variable, ranges)

    # Write histograms to output file
    for variable, histogram in histograms.items():
        writeHistogram(histogram[0], histogram[1], f"{'Run2012B_DoubleElectron_filtrado'}_{'TwoMuonsTwoElectrons'}_{variable}")

variable_labels = {
    "Higgs_mass": "Mass 4 leptons / GeV",
    "Z1_mass": "Mass Z_{1} / GeV",
    "Z2_mass": "Mass Z_{2} / GeV",
}

def main():
    # Load histograms from the input file
    histograms = {}
    images_base64 = {}
    for final_state, samples in [["FourElectrons", "Run2012B_DoubleElectron_filtrado"], ["TwoMuonsTwoElectrons", "Run2012B_DoubleElectron_filtrado"]]:
        for variable in variable_labels.keys():
            file_name = "{}_{}_{}.txt".format(samples, final_state, variable)
            data = pd.read_csv(file_name, delim_whitespace=True, header=0, names=["BinCenter", "BinContent"])
            histograms[variable] = data

            # Plot histograms
            for variable, data in histograms.items():
                plt.figure()
                plt.hist(data["BinCenter"], bins=10, weights=data["BinContent"], label="Data",color="blue", linewidth=2, alpha=0.2)
                 
              # Plot data points with error bars
                plt.errorbar(data["BinCenter"], data["BinContent"], xerr=np.sqrt(data["BinContent"]), yerr=np.sqrt(data["BinContent"]), fmt='o', color='black', label='Data Points', capsize=4, capthick=1)
                
                plt.xlabel(variable_labels[variable])
                plt.ylabel("N_{Events}")
                plt.title(f"Graph of {variable}")
                plt.legend()
                plt.grid(True)
                
                # Convert plot to base64
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
                images_base64[str(final_state)+str(variable)] = image_base64
                plt.close()
    
    return images_base64
