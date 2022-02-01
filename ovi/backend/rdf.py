from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDF

PEOPLE = "people/"
MEDIA_CREATIONS = "mediaCreations/"
APP_USERS = "users/"
CATEGORIES = "categories/"
COUNTRIES = "countries/"


def create_uri_from_name(name):
    name = name.replace(":", "-")
    return f'''http://example.org/{name.replace(" ","")}'''


def create_users_uri_from_name(name):
    name = name.replace(":", "-")
    return f'''http://example.org/{APP_USERS}{name.replace(" ","")}'''


def create_movie_uri_from_name(name):
    name = name.replace(":", "-")
    return f'''http://example.org/{MEDIA_CREATIONS}{name.replace(" ","")}'''


watched = URIRef(create_uri_from_name("watched"))
g = None
with open('fisier.txt', 'r', encoding="utf8") as file:
    read_data = file.read().replace('\n', '')
    g = Graph().parse(format='ttl', data=read_data)
    g.add((watched, RDF.type, RDF.Property))


def freeSparql(query):
    return g.query(query)


def addUser(username):
    uri = create_users_uri_from_name(username)
    user_ref = URIRef(uri)
    g.add((user_ref, RDF.type, FOAF.Person))
    g.add((user_ref, FOAF.name, Literal(username)))


def addFriend(username, friend_username):
    username_ref = URIRef(create_users_uri_from_name(username))
    friend_ref = URIRef(create_users_uri_from_name(friend_username))
    g.add((username_ref, FOAF.knows, friend_ref))


def addMovie(username, movie_name):
    username_ref = URIRef(create_users_uri_from_name(username))
    movie_ref = URIRef(create_movie_uri_from_name(movie_name))
    g.add((username_ref, watched, movie_ref))


def getMovie(movie_name):
    movie_uri = create_movie_uri_from_name(movie_name)
    movie_query = f'''
    SELECT ?director ?movie WHERE {{
        ?movie rdf:type ?type.
        ?movie sch:director ?directors.
        ?directors rdf:first ?director
        FILTER (
            (?type = sch:Movie || ?type = sch:TVSeries) &&
            ?movie = <{movie_uri}>
        )
    }}
    '''
    return g.query(movie_query)


def getWatchedByFriends(username):
    user_uri = create_users_uri_from_name(username)
    query = f'''
    select ?friend ?movie where 
    {{
        ?user rdf:type foaf:Person.
    

        ?user foaf:knows ?friend.
        ?friend <http://example.org/watched> ?movie.


        ?movie rdf:type ?movieType

        FILTER 
        (
            (?movieType = sch:Movie || ?movieType = sch:TVSeries) &&
            ?user = <{user_uri}>
        )
    }}
    '''
    return g.query(query)
