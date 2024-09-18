import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sqlitecloud

st.set_page_config(page_title="RaceIntel🏎️", layout="wide", page_icon="🏁" )
pagebg = """
<style> 
[data-testid="stAppViewContainer"]{
        background: rgb(249,119,119);
        background: radial-gradient(circle, rgba(249,119,119,1) 0%, rgba(90,0,0,1) 61%, rgba(2,0,36,1) 100%);
}
</style>
"""
headerbg="""
<style> 
[data-testid="stHeader"]{
        background: rgb(249,119,119);
        background: radial-gradient(circle, rgba(249,119,119,1) 0%, rgba(90,0,0,1) 61%, rgba(2,0,36,1) 100%);
}
</style>
"""


# Mostrar el DataFrame estilizado usando st.write

st.markdown(pagebg, unsafe_allow_html=True)
st.markdown(headerbg, unsafe_allow_html=True)
SQLiteCloud_connectionstring= "sqlitecloud://cqzdwoclsz.sqlite.cloud:8860?apikey=8ZBRx9VjOUr3L8r7arbcH8X27UpFfHwvq7qiaULwWdE"
conn = sqlitecloud.connect(SQLiteCloud_connectionstring)
cursor = conn.execute("USE DATABASE Formula1.db")
@st.cache_data
def generate_dataset():
    query = f"""
    select re.raceId,re.driverId,re.constructorId,ra.year, ra.round, re.grid, re.laps, 
    cs.points as constructortotalpoints, cs.position as constructorposition, ds.points as drivertotalpoints, 
    ds.position as driverposition,re.points as currentracepoints,re.position as currentraceposition,
    re.statusId, s.status, ra.year - substr(d.dob, 1, 4) as age
    from results re join qualifying q on re.raceId=q.raceId
    and re.constructorId= q.constructorId
    and re.driverId= q.driverId
    join races ra on ra.raceId= re.raceId
    join constructor_standings cs on cs.raceId= re.raceId and cs.constructorId= re.constructorId
    join driver_standings ds on ds.raceId = re.raceId and ds.driverId= re.driverId
    join status s on s.statusId= re.statusId
    join drivers d on d.driverId=re.driverId
"""
    cursor = conn.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=["raceId","driverId","constructorId","year","round","grid","laps","constructortotalpoints","constructorposition","drivertotalpoints", "driverposition",'currentracepoints','currentraceposition','statusId','status','age'])
    return df

#cargar datos
df = generate_dataset()
df=df[df['year'] == df['year'].max()]
df = df[df['driverId'] != 860]
# Title
st.title("RaceIntel🏎️")


# Load the model
model = joblib.load("model/modelF1.pkl")

st.header('Bienvenido a la Aplicación de Predicción de Resultados de Fórmula 1')


def prediction(driverId):
    input_data = buscarDriver(driverId) 
    prediction = model.predict(input_data)
    return prediction[0]
    
# funciones para obtener datos
def buscarDriver(driverId):
    consulta = df.loc[(df['driverId'] == driverId) & (df['raceId'] == df['raceId'].max())]
    consulta.drop(['raceId', 'currentraceposition','status'], axis=1, inplace=True)
    return consulta
@st.cache_resource
def prediction_button(driverId , year,round , grid , lap, driverposition, currentracepoints):
     # New dataset with the input data
    constructorId= buscarDrivers(driverId, 'constructorId')
    constructortotalpoints= buscarDrivers(driverId, 'constructorPoints')
    constructorposition= buscarDrivers(driverId, 'constructorPosition')
    drivertotalpoints=buscarDrivers(driverId, 'driverPoints')
    statusId= buscarDrivers(driverId, 'status')
    age= buscarDrivers(driverId, 'age')
    input_data = pd.DataFrame([[driverId ,constructorId, year,round , grid , lap, constructortotalpoints, constructorposition, drivertotalpoints, driverposition, currentracepoints,statusId, age]], 
                                    columns=['driverId', 'constructorId', 'year', 'round', 'grid', 'laps',
                                            'constructortotalpoints', 'constructorposition', 'drivertotalpoints',
                                            'driverposition', 'currentracepoints','statusId', 'age'])
    
     # Make the prediction
    prediction = model.predict(input_data)

    return prediction[0]
    
# funciones para obtener datos
def buscarDrivers(driverId, param):
    consulta = df.loc[(df['driverId'] == driverId) & (df['raceId'] == df['raceId'].max())]
    if param == 'age':
        return consulta['age']
    elif param == 'driverPoints':
        return consulta['drivertotalpoints']
    elif param == 'position':
        return consulta['driverposition']
    elif param == 'status':
        return consulta['statusId']
    elif param == 'currentRacePoints':
        return consulta['currentracepoints']
    elif param =='constructorId':
        return consulta['constructorId']
    elif param == 'constructorPoints':
        return consulta['constructortotalpoints']
    elif param == 'constructorPosition':
        return consulta['constructorposition']
driver = {
    1: 'Lewis Hamilton',
    4: 'Fernando Alonso',
    807: 'Nico Hülkenberg',
    815: 'Sergio Pérez',
    817: 'Daniel Ricciardo',
    822: 'Valtteri Bottas',
    825: 'Kevin Magnussen',
    830: 'Max Verstappen',
    832: 'Carlos Sainz',
    839: 'Esteban Ocon',
    840: 'Lance Stroll',
    842: 'Pierre Gasly',
    844: 'Charles Leclerc',
    846: 'Lando Norris',
    847: 'George Russell',
    848: 'Alexander Albon',
    852: 'Yuki Tsunoda',
    855: 'Guanyu Zhou',
    857: 'Oscar Piastri',
    858: 'Logan Sargeant'
}
drivers = {
    'Lewis Hamilton': 1,
    'Fernando Alonso': 4,
    'Nico Hülkenberg':807,
    'Sergio Pérez': 815,
    'Daniel Ricciardo': 817,
    'Valtteri Bottas': 822,
    'Kevin Magnussen': 825,
    'Max Verstappen':830,
    'Carlos Sainz':832,
    'Esteban Ocon': 839,
    'Lance Stroll': 840,
    'Pierre Gasly': 842,
    'Charles Leclerc': 844,
    'Lando Norris': 846,
    'George Russell': 847,
    'Alexander Albon': 848,
    'Yuki Tsunoda': 852,
    'Guanyu Zhou': 855,
    'Oscar Piastri': 857,
    'Logan Sargeant': 858
}
col1, col2 = st.columns(2)
with col1:
     st.markdown("""
    Esta aplicación te permite predecir la posición final de un piloto en una carrera de Fórmula 1 utilizando datos clave de su rendimiento reciente. Basándonos en los datos de la última carrera y otros factores relacionados con el rendimiento del piloto, la aplicación genera una predicción sobre en qué posición puede terminar.

    ### ¿Cómo usar la aplicación?
    1. Ingresa los siguientes valores para el piloto que deseas analizar:
    - **Nombre del Piloto**: Este es el código único que identifica al piloto.
    - **Ronda**: Es el número de la carrera en la temporada actual.
    - **Posición en la Parrilla**: La posición inicial del piloto en la ultima carrera.
    - **Vueltas en la última carrera**: El número de vueltas que el piloto completó en la última carrera.
    - **Puntos actuales**: Los puntos que el piloto ha acumulado en la temporada actual.
    - **Posición global actual**: La posición actual del piloto en la clasificación general.
                         
    2. Haz clic en el botón **"Predecir"** y obtendrás una predicción de la **posición final** en la que el piloto podría terminar en su próxima carrera.
    """)
    # st.markdown("""
    #             Esta aplicación te permite predecir la posición de los 10 primeros
    #             puestos en la siguiente carrera de Fórmula 1 utilizando datos clave de su rendimiento reciente. 
    #             Basándonos en los datos de la última carrera y otros factores relacionados con el rendimiento del piloto,
    #             la aplicación genera una tabla con la predicción y la probabilidad de que quede en ese puesto.
    # """)
with col2:
    tab1, tab2 = st.tabs(["Predicción de un Piloto", "Predicción de los 10 primeros"])
    with tab1:
        driverId= st.selectbox('Conductor:',('Lewis Hamilton','Fernando Alonso','Nico Hülkenberg','Sergio Pérez','Daniel Ricciardo','Valtteri Bottas','Kevin Magnussen','Max Verstappen','Carlos Sainz','Esteban Ocon','Lance Stroll','Pierre Gasly',
            'Charles Leclerc','Lando Norris','George Russell','Alexander Albon','Yuki Tsunoda','Guanyu Zhou','Oscar Piastri','Logan Sargeant'))
        # constructorId=st.radio('Escuderia:',('McLaren','Williams','Ferrari','Red Bull','Kick Sauber','Aston Martin','Mercedes','Haas F1 Team','Alpine','RB'))
        year= 2024
        round= st.slider('Ronda:', 1, 22, disabled=False)
        grid= st.slider('Pocision de salida:', 1, 21, disabled=False)
        laps= st.slider('Vueltas en la ultima carrera', 40, 80, disabled=False)
        currentracepoints = st.slider('Puntos actuales:', 0, 25, disabled=False)
        driverposition = st.slider('Posicion global actual:', 1, 20, disabled=False)



        # Button to make the prediction
        if st.button("Predict"):
            name= driverId
            driverId = drivers[driverId]
            result = prediction_button(driverId , year,round , grid , laps, driverposition, currentracepoints)
            if result >21: 
                st.write(f"El conductor {name} no terminará la carrera")
            else:
                st.write(f"El conductor {name} terminará en la posición {result}")

    with tab2:    
        df_pred = pd.DataFrame(columns=['driverId', 'prediction'])
        rows_list = []
        for driver_id in df['driverId'].unique():
            # Paso 2: Pasar el driverId a la función prediction
            pred = prediction(driver_id)
            # Crear una nueva fila con el driverId y la predicción
            prob = model.predict_proba(buscarDriver(driver_id))[0][1]
            new_row = pd.DataFrame({'Piloto': [driver.get(driver_id)],'Prediccion': [pred],'Probabilidad': [prob*100]})
            # Añadir la nueva fila a la lista de filas
            rows_list.append(new_row)

        # Concatenar todas las filas en un DataFrame final
        df_pred = pd.concat(rows_list, ignore_index=True)
        df_pred= df_pred.sort_values(by='Prediccion', ascending=True).head(10)
        ## transparencia del la fondo de la tabla
        df_styled = df_pred.style.set_properties(**{
        'background-color': 'rgba(0, 0, 0, 0)',
        'color': 'white',
        'border': '1px solid white'
        })
        st.write(df_styled.to_html(), unsafe_allow_html=True)  
