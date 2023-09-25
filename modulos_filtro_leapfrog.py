# importar librerias
import numpy as np
import pandas as pd
# openpyxl


# lectura del archivo .xlsx
def leer_archivo_xlsx(ruta,archivo):
    data = pd.read_excel(ruta + archivo + '.xlsx')
    return data


# renombrar columnas
# la finalidad es que en data_tmp se almacene con estas nuevas columnas
def renombrar_columnas(data):
    # arreglo de nuevos nombres [0,1,2,...]
    nuevos_nombres = {columna: f'{indice}' for indice, columna in enumerate(data.columns)}
    # cambiando la cabecera
    data = data.rename(columns=nuevos_nombres)
    # nuevos nombres en el data_tmp
    data_tmp = data.iloc[ : ,0:3]
    data_tmp = data_tmp.rename(columns={'0': 'punto_X', '1': 'punto_Y', '2': 'punto_Z'})
    # retorno de la data renombrada
    return data_tmp


def n_registros(data_tmp):
    #tam_origen = data_tmp.shape[0]
    return data_tmp.shape[0]
    #print(f'Tamanio de origen = {tam_origen}')


# puntos medios
def puntos_medios(data_tmp):

    tam_origen = n_registros(data_tmp=data_tmp)

    puntos_medios = pd.DataFrame()

    for i in range(0,tam_origen-1):
        x_medio = round((data_tmp.iloc[i,0] + data_tmp.iloc[i+1,0])/2,5)
        #print(x_medio)
        y_medio = round((data_tmp.iloc[i,1] + data_tmp.iloc[i+1,1])/2,5)
        #print(y_medio)

        nuevo_registro = {'punto_X': x_medio, 'punto_Y': y_medio}
        
        
        # Añadir el nuevo registro usando concat
        puntos_medios = pd.concat([puntos_medios, pd.DataFrame([nuevo_registro])], ignore_index=True)   

    data_result = pd.DataFrame()

    # Asegurarse de que ambos DataFrames tengan la misma longitud
    tam_minimo = min(len(data_tmp), len(puntos_medios))
    dataframe1 = data_tmp[:tam_minimo]
    dataframe2 = puntos_medios[:tam_minimo]

    for i in range (tam_minimo):
        registro_a = {'punto_X': dataframe1.iloc[i,0], 'punto_Y': dataframe1.iloc[i,1]}
        registro_b = {'punto_X': dataframe2.iloc[i,0], 'punto_Y': dataframe2.iloc[i,1]}

        data_result = pd.concat([data_result, pd.DataFrame([registro_a])], ignore_index=True)
        data_result = pd.concat([data_result, pd.DataFrame([registro_b])], ignore_index=True)

    ultimo_registro = {'punto_X': data_tmp.iloc[tam_origen-1,0], 'punto_Y': data_tmp.iloc[tam_origen-1,1]}
    data_result = pd.concat([data_result, pd.DataFrame([ultimo_registro])], ignore_index=True)

    data_tmp = data_result

    return data_tmp


'''
def intercalar_dataFrames(data_tmp, puntos_medios):
    tam_origen = n_registros(data_tmp=data_tmp)

    data_result = pd.DataFrame()
    # Asegurarse de que ambos DataFrames tengan la misma longitud
    tam_minimo = min(len(data_tmp), len(puntos_medios))
    dataframe1 = data_tmp[:tam_minimo]
    dataframe2 = puntos_medios[:tam_minimo]

    #print(f'tam_minimo = {tam_minimo}')


    for i in range (tam_minimo):
        registro_a = {'punto_X': dataframe1.iloc[i,0], 'punto_Y': dataframe1.iloc[i,1]}
        registro_b = {'punto_X': dataframe2.iloc[i,0], 'punto_Y': dataframe2.iloc[i,1]}

        data_result = pd.concat([data_result, pd.DataFrame([registro_a])], ignore_index=True)
        data_result = pd.concat([data_result, pd.DataFrame([registro_b])], ignore_index=True)

    ultimo_registro = {'punto_X': data_tmp.iloc[tam_origen-1,0], 'punto_Y': data_tmp.iloc[tam_origen-1,1]}
    data_result = pd.concat([data_result, pd.DataFrame([ultimo_registro])], ignore_index=True)

    data_tmp = data_result
    
    return data_tmp
    #data_result
'''

def query_der_izq(de_derecha_a_izquierda, eje_x, eje_y_normal, x_maximo):
    query_de_der_a_izq = '(  '
    
    for i in range(0,len(de_derecha_a_izquierda)-1):

        if eje_x.iloc[i,0] < eje_x.iloc[i+1,0]:
            max_de_x_der_izq = eje_x.iloc[i,0]
            indice_de_que_se_usara = i
        else:
            max_de_x_der_izq = eje_x.iloc[i+1,0]
            indice_de_que_se_usara = i+1

        query_de_der_a_izq = query_de_der_a_izq + f'[y] >= {eje_y_normal.iloc[i,0]} and [y] <= {eje_y_normal.iloc[i+1,0]} and [x] >= {max_de_x_der_izq} and [x] <= {x_maximo}'
        if i+1 != len(de_derecha_a_izquierda)-1:
            query_de_der_a_izq = query_de_der_a_izq + '\nor '
        else:
            query_de_der_a_izq = query_de_der_a_izq + '  )'
    
    return query_de_der_a_izq    
    #print(query_de_der_a_izq)


def query_izq_der(de_izquierda_a_derecha, eje_x, eje_y_normal, x_minimo):

    query_de_izq_a_der = '(  '
    for i in range(0,len(de_izquierda_a_derecha)-1):

        if eje_x.iloc[de_izquierda_a_derecha[i],0] < eje_x.iloc[de_izquierda_a_derecha[i+1],0]:
            max_de_x_izq_der = eje_x.iloc[de_izquierda_a_derecha[i+1],0]
            indice_de_que_se_usara = i
        else:
            max_de_x_izq_der = eje_x.iloc[de_izquierda_a_derecha[i],0]
            indice_de_que_se_usara = i+1

        query_de_izq_a_der = query_de_izq_a_der + f'[y] <= {eje_y_normal.iloc[de_izquierda_a_derecha[i],0]} and [y] >= {eje_y_normal.iloc[de_izquierda_a_derecha[i+1],0]} and [x] >= {x_minimo} and [x] <= {max_de_x_izq_der}'

        if i+1 != len(de_izquierda_a_derecha)-1:
            query_de_izq_a_der = query_de_izq_a_der + '\nor '
        else:
            query_de_izq_a_der = query_de_izq_a_der + '  )'

    return query_de_izq_a_der
    #print(query_de_izq_a_der)


def funcion_principal(ruta, archivo, cant_puntos, z_minimo, z_maximo):
    data = leer_archivo_xlsx(ruta=ruta, archivo=archivo)

    data_tmp = renombrar_columnas(data)

    # cant puntos = 1, 3, 7, 15
    # [1] = 1 puntos medios
    # [2] = 3 puntos medios
    # [3] = 7 puntos medios

    if cant_puntos!=1 and cant_puntos!=2 and cant_puntos!=3:
        print(f'Error al digital la opcion de cantidad de puntos')
        exit()

    for i in range(0,cant_puntos):
        data_tmp = puntos_medios(data_tmp)

#------------------------------------------------------------------------------------------

    # indices de relacion entre ejes
    data_tmp.loc[:, 'indice'] = np.arange(0, len(data_tmp))
    #data_tmp


    # obtenemos dataFrames para cada eje con su respectivo indice
    eje_x = data_tmp.loc[ : ,['punto_X','indice']]
    eje_y = data_tmp.loc[ : ,['punto_Y','indice']]
    # copia eje_y
    eje_y_normal = data_tmp.loc[ : ,['punto_Y','indice']]
    # copia eje_x que servira para ordenar
    eje_x_sort = data_tmp.loc[ : ,['punto_X','indice']]
    eje_y_sort = data_tmp.loc[ : ,['punto_Y','indice']]


    #ordenamiento de los puntos en los ejes
    eje_y.sort_values(by='punto_Y', ascending=True, inplace=True)

    eje_x_sort.sort_values(by='punto_X', ascending=True, inplace=True)
    eje_y_sort.sort_values(by='punto_Y', ascending=True, inplace=True)

    # reset de los index para cada conjunto de datos
    eje_y.reset_index(drop=True, inplace=True)
    eje_x_sort.reset_index(drop=True, inplace=True)



    # valores resultado
    #y_minimo = eje_y.iloc[0,0]
    #y_maximo = eje_y.iloc[eje_y.shape[0]-1,0]

    y_minimo_indice = eje_y.iloc[0,1]
    y_maximo_indice = eje_y.iloc[eje_y.shape[0]-1,1]

    x_minimo = eje_x_sort.iloc[0,0]
    x_maximo = eje_x_sort.iloc[eje_x_sort.shape[0]-1,0]


    de_derecha_a_izquierda = list(range(y_maximo_indice+1))
    #de_derecha_a_izquierda

    de_izquierda_a_derecha = list(range(y_maximo_indice, data_tmp.shape[0])) + [0]
    #de_izquierda_a_derecha


    # rectangulos reiemman
    q_der_izq = query_der_izq(de_derecha_a_izquierda=de_derecha_a_izquierda, eje_x=eje_x, eje_y_normal=eje_y_normal, x_maximo=x_maximo)
    q_izq_der = query_izq_der(de_izquierda_a_derecha=de_izquierda_a_derecha, eje_x=eje_x, eje_y_normal=eje_y_normal, x_minimo=x_minimo)


    #query_final = '(' + q_der_izq + '\nand\n' + q_izq_der + ')\n and' + '([z] >=' + 3890 + 'and [z] <=' + 3905 +')'
    query_final = f'( {q_der_izq} \nand \n{q_izq_der} ) \nand \n([z] >= {z_minimo} and [z] <= {z_maximo})' 
    
    return query_final


if __name__ == '__main__':

    ruta = '/home/chino/Escritorio/gb/lun_11_set_23/src/'
    archivo = 'ensayo-error'
    cant_puntos = 4
    z_minimo = 3890
    z_maximo = 3905

    resultado = funcion_principal(ruta=ruta,archivo=archivo,cant_puntos=cant_puntos,z_minimo=z_minimo,z_maximo=z_maximo)
    print(resultado)
    
    
