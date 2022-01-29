from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import FOAF, RDF

g = None
with open('fisier.txt', 'r', encoding="utf8") as file:
    read_data = file.read().replace('\n', '')
    g = Graph().parse(format = 'ttl', data = read_data)


def create_uri_from_name(name):
    name = name.replace(":","-")
    return f'''http://example.org/{name.replace(" ","")}'''


def create_movie_uri_from_name(name):
    name = name.replace(":","-")
    return f'''http://example.org/{name.replace(" ","")}'''    

def freeSparql(query):
    return g.query(query)


def addUser(username):
    uri = create_uri_from_name(username)
    user_ref =  URIRef(uri)
    g.add((user_ref, RDF.type, FOAF.Person))
    g.add((user_ref, FOAF.name, Literal(username)))


def addFriend(username, friend_username):
    username_ref = URIRef(create_uri_from_name(username))
    friend_ref = URIRef(create_uri_from_name(friend_username))
    g.add((username_ref, FOAF.knows, friend_ref))
    

def addMovie(username, movie_name):
    username_ref = URIRef(create_uri_from_name(username))
    movie_ref = URIRef(create_movie_uri_from_name(movie_name))
    g.add((username_ref, FOAF.watched, movie_ref))
        