import json
import pandas as pd

def cargar_y_aplanar_json(file_path):
    """
    Carga un archivo JSON y aplana los datos utilizando pandas

    Parameters:
    - file_path (str): Ruta del archivo JSON a cargar

    Returns:
    - pd.DataFrame: DataFrame con los datos del archivo JSON aplanado.
    """
    # Lectura del archivo JSON
    with open(file_path, 'r') as file:
        json_file = json.load(file)

    # Aplanar el archivo JSON  
    df = pd.json_normalize(
        json_file,
        record_path=['albums', 'tracks'],
        meta=['artist_id', 'artist_name', 'artist_popularity', ['albums', 'album_id'],
              ['albums', 'album_name'], ['albums', 'album_release_date'], ['albums', 'album_total_tracks']],
        sep='.'
    )

    return df


def cargar_csv(file_path):
    """
    Carga un archivo CSV y lo convierte en un DataFrame

    Parameters:
    - file_path (str): Ruta del archivo CSV a cargar

    Returns:
    - pd.DataFrame: DataFrame con los datos del archivo CSV
    """
    # Lectura del archivo CSV
    df = pd.read_csv(file_path)
    return df


def ajustar_formato_dataframe(df, df_formato):
    """
    Ajusta un DataFrame según un formato dado

    Parameters:
    - df (pd.DataFrame): DataFrame a ajustar
    - df_formato (pd.DataFrame): DataFrame que sirve como formato de referencia

    Returns:
    - pd.DataFrame: DataFrame ajustado
    """

    # Renombrar columnas según el formato
    dic_columns = dict(zip(df.columns, df_formato.columns))
    df.rename(columns=dic_columns, inplace=True)

    # Reemplazar valores vacíos por None en columnas especificadas
    null_differences = ['track_id',
                        'track_name',
                        'audio_features.danceability',
                        'audio_features.acousticness',
                        'audio_features.tempo',
                        'album_name']
    df[null_differences] = df[null_differences].replace('', None)

    # Igualar tipo de datos según el formato
    tipo_datos = df_formato.dtypes
    df = df.astype(tipo_datos)

    return df


def x_to_e(string):
    '''
    Convierte las "x" en un string a "e" para corregir formato de notacion científia

    Parameters:
    - string (str): string a convertir

    Returns:
    - string (str): string convertido
    '''
    # Convertir a string si no lo es
    string = str(string)
    if 'x' in string:
        string = string.replace('x', 'e')
    return string


def ajustar_tipos_de_datos(df, df_formato):
    """
    Ajusta tipos de datos en dos DataFrames

    Parameters:
    - df_formato (pd.DataFrame): DataFrame con el formato de referencia
    - df (pd.DataFrame): DataFrame a ajustar

    Returns:
    - pd.DataFrame: DataFrame ajustado.
    """
    # Ajustar tipo de dato para 'audio_features.instrumentalness'
    df_formato['audio_features.instrumentalness'] = df_formato['audio_features.instrumentalness'].apply(x_to_e).astype(float).round(6)
    df['audio_features.instrumentalness'] = df['audio_features.instrumentalness'].apply(x_to_e).astype(float).round(6)

    # Ajustar tipo de dato para 'explicit'
    df_formato['explicit'] = df_formato['explicit'].replace({'False': False, 'True': True, 'Si': True, 'No': False}).astype(bool)
    df['explicit'] = df['explicit'].replace({'False': False, 'True': True, 'Si': True, 'No': False}).astype(bool)

    # Reemplazar 'Thirteen' con 13 y ajustar tipo de dato para 'album_total_tracks'
    df_formato['album_total_tracks'] = df_formato['album_total_tracks'].replace('Thirteen', 13).astype(int)
    df['album_total_tracks'] = df['album_total_tracks'].replace('Thirteen', 13).astype(int)

    return df, df_formato

def comparar_dataframes(df1, df2):
    """
    Compara dos DataFrames y devuelve un mensaje indicando si son idénticos o no.

    Parameters:
    - df1 (pd.DataFrame): Primer DataFrame
    - df2 (pd.DataFrame): Segundo DataFrame

    Returns:
    - str: Mensaje indicando si los DataFrames son idénticos o no
    """
    if df1.equals(df2):
        return print("Los datasets son idénticos")
    else:
        return print("Los datasets son diferentes")


if __name__ == "__main__":

    # Rutas de los archivos
    json_path = 'taylor_swift_spotify.json'
    csv_path = 'dataset.csv'

    # Cargar archivos
    df_json = cargar_y_aplanar_json(json_path)
    df_csv = cargar_csv(csv_path)

    # Ajustar formato del DataFrame
    df_json = ajustar_formato_dataframe(df_json, df_csv)

    # Ajustar tipos de datos
    df_json, df_csv = ajustar_tipos_de_datos(df_json, df_csv)

    # Comparar DataFrames
    comparar_dataframes(df_json, df_csv)
