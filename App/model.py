"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """
import config
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria.
"""


# -----------------------------------------------------
# API del TAD Catalogo de películas.
# -----------------------------------------------------
def new_catalog():
    """ Inicializa el catálogo de películas

    Crea una lista vacia para guardar todas las películas.

    Se crean indices (Maps) por los siguientes criterios:
    id películas

    Retorna el catálogo inicializado.
    """
    catalog = {
        'details': lt.newList('SINGLE_LINKED'),
        'casting': lt.newList('SINGLE_LINKED'),
        #'producer_companies': mp.newMap(1000, maptype='PROBING', loadfactor=2, comparefunction=compare_ids)
        #'producer_companies': mp.newMap(200, maptype='PROBING', loadfactor=10, comparefunction=compare_ids)
        #'producer_companies': mp.newMap(4000, maptype='PROBING', loadfactor=0.5, comparefunction=compare_ids), 
        'movies_ids': mp.newMap(5000, maptype='PROBING', loadfactor=0.4, comparefunction=compare_ids),
        'production_companies': mp.newMap(1000, maptype='PROBING', loadfactor=0.4, comparefunction=compare_producers),
        'actors_id' : mp.newMap(4000, maptype='PROBING', loadfactor=0.5, comparefunction=compare_actors),
        'actors': mp.newMap(4000, maptype='PROBING', loadfactor=0.5, comparefunction=compare_actors)
    }
    return catalog


def new_producer(name):
    """
    Crea una nueva estructura para modelar las películas de una compañia de producción
    y su promedio de ratings
    """
    producer = {'name': name, 'movies': lt.newList('SINGLE_LINKED', compare_producers), 'average_rating': 0}
    return producer

def new_actor(name):
    """
    Crea una nueva estructura para modelar las películas de un director
    y su promedio de ratings
    """
    actor = {name: 'name',
                'actor_id': lt.newList('SINGLE_LINKED', compare_ids),
                'total_movies':0,
                'movies': lt.newList('SINGLE_LINKED', compare_actors),
                'average_rating': 0.0}
    return actor

# Funciones para agregar información al catálogo.
def add_details(catalog, movie):
    """
    Esta función adiciona detalles a la lista de películas,
    adicionalmente los guarda en un Map usando como llave su id.
    """
    lt.addLast(catalog['details'], movie)
    mp.put(catalog['movies_ids'], movie['id'], movie)

    
def add_movie(catalog, movie):
    """
    Esta funcion adiciona una película a la lista de películas,
    adicionalmente lo guarda en un Map usando como llave su id.
    Finalmente crea una entrada en el Map de productoras, para indicar que este
    la película hace parte de la productora-
    """
    lt.addLast(catalog['details'],catalog['casting'], movie)
    mp.put(catalog['movies_ids'], movie['production_companies'], movie['actors'], movie)

def add_actor(catalog, actor):
    lt.addLast(catalog['casting'], actor)
    mp.put(catalog['actors'], actor['actor1_name'], actor)
    mp.put(catalog['actors'], actor['actor2_name'], actor)
    mp.put(catalog['actors'], actor['actor3_name'], actor)
    mp.put(catalog['actors'], actor['actor4_name'], actor)
    mp.put(catalog['actors'], actor['actor5_name'], actor)
    mp.put(catalog['actors_id'], actor['id'], actor)

def add_movie_production_companies(catalog, producer_name, movie):
    producers = catalog['production_companies']
    existproducer = mp.contains(producers, producer_name)  
    if existproducer:
        entry = mp.get(producers, producer_name)
        producer = me.getValue(entry)
    else:
        producer = new_producer(producer_name)
        mp.put(producers, producer_name, producer)
    lt.addLast(producer['movies'], movie)
    # Producer vote average.
    producer_avg = producer['average_rating']
    movie_avg = movie['vote_average']
    if producer_avg == 0.0:
        producer['average_rating'] = float(movie_avg)
    else:
        producer['average_rating'] = (producer_avg + float(movie_avg)) / 2

def add_movie_actors(catalog, actor, actors_id):
    actors = catalog['actors']
    movies = catalog['movies_ids']
    existactor = mp.contains(actors, actor)
    movie_id = actors_id['id']
    if existactor:
        entry = mp.get(actors, actor)
        entry2 = mp.get(movies, movie_id) 
        Aactor = me.getValue(entry)
        movie = me.getValue(entry2)
    else:
        Aactor = new_actor(actor)
        movie = new_actor(actor)
        entry2 = mp.get(movies, movie_id) 
        movie = me.getValue(entry2)
        mp.put(actors, actor, Aactor)
    lt.addLast(Aactor['actor_id'], actors_id['id'])
    lt.addLast(Aactor['movies'], movie)
    Aactor['total_movies'] += 1
    # Director vote average.
    actor_avg = Aactor['average_rating']
    movie_av = mp.get(movies, movie_id)
    movie_avg = movie_av['value']['vote_average']
    if actor_avg == 0.0:
        Aactor['average_rating'] = float(movie_avg)
    else:
        Aactor['average_rating'] = (actor_avg + float(movie_avg)) / 2


# ==============================
# Funciones de consulta
# ==============================

def details_size(catalog):
    # Número de detalles en el catálogo.
    return lt.size(catalog['details'])


def casting_size(catalog):
    # Número de elencos en el catálogo.
    return lt.size(catalog['casting'])


def show_movie_data(catalog, index):
    el = lt.getElement(catalog['details'], catalog['casting'], index)
    return (f'- {el["title"]}:'
            + f'\n   con un puntaje promedio de {el["vote_average"]} y un total de {el["vote_count"]} votaciones,'
            + f'\n   fue estrenada en {el["release_date"]} en el idioma "{el["original_language"]}".')


def show_producer_data(producer):
    """
    Imprime las películas de una productara.
    """
    if producer:
        print('Productora de cine encontrada: ' + producer['name'])
        print('Promedio: ' + str(producer['average_rating']))
        print('Total de películas: ' + str(lt.size(producer['movies'])))
        iterator = it.newIterator(producer['movies'])
        while it.hasNext(iterator):
            movie = it.next(iterator)
            print('Título: ' + movie['title'] + ' | Vote Average: ' + movie['vote_average'])
    else:
        print('No se encontró la productora')

def show_actor_data(actor):
    """
    Imprime las películas de un director
    """
    if actor:
        print('Actor de cine encontrado: ' + actor['name'].strip())
        print('Promedio: ' + str(actor['average_rating']))
        print('Total de películas: ' + str(lt.size(actor['movies'])))
        print('Director con mas participaciones: '+ actor['colab'])
        iterator = it.newIterator(actor['movies'])
        while it.hasNext(iterator):
            movie = it.next(iterator)
            print('Título: ' + movie['title'] + ' | Vote Average: ' + movie['vote_average'])
    else:
        print('No se encontró el actor')


def total_average(lista):
    total = lt.size(lista)
    votes = 0
    for i in range(lt.size(lista)):
        movie = lt.getElement(lista, i)
        votes += float(movie)
    total_vote_average = votes / total
    return round(total_vote_average, 1)


def get_movie_producer(catalog, producer_name):
    """
    Retorna las películas a partir del nombre de la productora
    """
    producer = mp.get(catalog['production_companies'], producer_name)
    if producer:
        return me.getValue(producer)
    return None

def get_movie_actor(catalog, actor_name):
    """
    Retorna las películas a partir del nombre del director
    """
    actor = mp.get(catalog['actors'], actor_name)
    if actor:
        return me.getValue(actor)
    return None


"""
def productors_movies(catalog,production):
    lista = lt.newList('ARRAYLIST')
    values_average = lt.newList('ARRAYLIST')
    for i in range(lt.size(catalog['details'])):
        file = lt.getElement(catalog['details'],i)
        if production.strip().lower() == file['production_companies'].strip().lower():
            movies = file['title']
            average = file['vote_average']
            lt.addLast(values_average,average)
            lt.addLast(lista,movies)

    for i in range(lt.size(lista)):
        print('-',lt.getElement(lista,i))
           
    average_number = total_average(values_average)
    return average_number, lt.size(lista)

def directors_movies(catalog,production):
    lista = lt.newList('ARRAYLIST')
    values_average = lt.newList('ARRAYLIST')
    for i in range(lt.size(catalog['casting'])):
        file = lt.getElement(catalog['casting'],i)
        if production.strip().lower() == file['directors'].strip().lower():
            movies = file['title']
            average = file['vote_average']
            lt.addLast(values_average,average)
            lt.addLast(lista,movies)

    for i in range(lt.size(lista)):
        print('-',lt.getElement(lista,i))
           
    average_number = total_average(values_average)
    return average_number, lt.size(lista)
"""
# ==============================
# Funciones de Comparacion
# ==============================
def compare_ids(id_, tag):
    entry = me.getKey(tag)
    if int(id_) == int(entry):
        return 0
    elif int(id_) > int(entry):
        return 1
    else:
        return 0


def compare_producers(keyname, producer):
    proentry = me.getKey(producer)
    if keyname == proentry:
        return 0
    elif keyname > proentry:
        return 1
    else:
        return -1

def compare_actors(keyname, producer):
    entry = me.getKey(producer)
    if keyname == entry:
        return 0
    elif keyname > entry:
        return 1
    else:
        -1
    