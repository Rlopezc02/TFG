from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Body, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import shutil
import pandas as pd
from back import copy_csv, parse_lists, transformar_lista, ajustar_longitud_columnas_con_listas, calcular_medias_para_columnas_con_listas, predecir_y_filtrar, seleccionar_por_indices, reconstruct_samekind, calcular_energia_momento, crear_cuadrivector, calcular_masa_invariante, z_fourvectors_samekind, z_fourvectors_2el2mu, Higgs_fourvec, masas, seleccionar_columnas, bookHistogram, writeHistogram, main1, main2, main

load_dotenv()

app = FastAPI()

# Importar funciones necesarias

# Configurar CORS
origins = [
    "http://localhost:5173",  # Agrega aquí la URL de tu front-end si es diferente 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "¡Hola, bienvenido a tu API FastAPI con integración de backend!"}

@app.post('/upload-file')
async def upload_file(file: str = Form(...)):
    if file != './Run2012B_DoubleElectron.csv':
        raise HTTPException(status_code=415, detail="Tipo de archivo no soportado. Por favor, suba un archivo CSV.")

    try:
        # # Guardar temporalmente el archivo
        # temp_file_path = f"temp_{file}"
        # with open(temp_file_path, "wb") as buffer:
        #     shutil.copyfileobj(file.file, buffer)

        df, df_copia = copy_csv(file)
        for col in df.columns:  
            df[col] = df[col].apply(parse_lists)  # Aplicar la función parse_lists a cada celda de cada columna
        for col in df_copia.columns:  
            df_copia[col] = df_copia[col].apply(parse_lists)  # Aplicar la función parse_lists a cada celda de cada columna
        df_total = ajustar_longitud_columnas_con_listas(df)
        df_total1 = calcular_medias_para_columnas_con_listas(df_total)
        df_total2 = calcular_medias_para_columnas_con_listas(df_total)
        df_filtrado1 = predecir_y_filtrar(df_total1, 'modelo_arbol_decision3.pkl')
        df_filtrado2 = predecir_y_filtrar(df_total2, 'modelo_arbol_decision4.pkl')
        df_seleccionado1 = seleccionar_por_indices(df_copia, df_filtrado1)
        df_seleccionado2 = seleccionar_por_indices(df_copia, df_filtrado2)
        z_idx = reconstruct_samekind(df_seleccionado1)
        lista_z_fourvecs1 = z_fourvectors_samekind(z_idx, df_seleccionado1)
        lista_z_fourvecs2 = z_fourvectors_2el2mu(df_seleccionado2)
        df_seleccionado1['z_fourvecs'] = lista_z_fourvecs1
        df_seleccionado2['z_fourvecs'] = lista_z_fourvecs2
        fourvec1 = Higgs_fourvec(df_seleccionado1)
        fourvec2 = Higgs_fourvec(df_seleccionado2)
        df_seleccionado1['Higgs_fourvec'] = fourvec1
        df_seleccionado2['Higgs_fourvec'] = fourvec2
        Higgs_mass1, Z1_mass1, Z2_mass1 = masas(df_seleccionado1)
        Higgs_mass2, Z1_mass2, Z2_mass2 = masas(df_seleccionado2)
        df_seleccionado1['Higgs_mass'] = Higgs_mass1
        df_seleccionado1['Z1_mass'] = Z1_mass1
        df_seleccionado1['Z2_mass'] = Z2_mass1
        df_seleccionado2['Higgs_mass'] = Higgs_mass2
        df_seleccionado2['Z1_mass'] = Z1_mass2
        df_seleccionado2['Z2_mass'] = Z2_mass2
        df_seleccionado1 = seleccionar_columnas(df_seleccionado1)
        df_seleccionado2 = seleccionar_columnas(df_seleccionado2)

        ranges = {
            "Higgs_mass": (36, 70, 180),
            "Z1_mass": (36, 40, 160),
            "Z2_mass": (36, 12, 160)
        }

        main1(df_seleccionado1)
        main2(df_seleccionado2)

        variable_labels = {
            "Higgs_mass": "Mass 4 leptons / GeV",
            "Z1_mass": "Mass Z_{1} / GeV",
            "Z2_mass": "Mass Z_{2} / GeV",
        }

        images_base64 = main()

        # # Eliminar el archivo temporal
        # os.remove(temp_file_path)

        return JSONResponse(content={"mensaje": "Archivo CSV procesado correctamente", "imagenes": images_base64})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la imagen: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000) 

