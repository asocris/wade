from operator import truediv
from rdflib import Graph
from enum import Enum
import csv

class CSV_Columns(Enum):
    SHOW_ID = 0
    TYPE = 1
    TITLE = 2
    DIRECTOR = 3
    CAST = 4
    COUNTRY = 5
    DATE_ADDED = 6
    RELEASE_YEAR = 7
    RATING = 8
    DURATION = 9
    LISTED_IN = 10
    DESCRIPTION = 11

#used for mapping dates which were in a kind of weird format
MONTHS_DICT = {"january" : 1, "february" : 2, "march" : 3, "april" : 4, "may" : 5, "june" : 6, 
                "july" : 7, "august" : 8, "september" : 9, "october" : 10, "november" : 11, "december" : 12}

TV_SHOW = "TV Show"
MOVIE = "Movie"

#using this dictionary to make sure we do not define an actor twice
CREATED_URIS = {}

base_rdf_schema = '''
@base <http://example.org/>.
@prefix sch: <https://schema.org/>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix dbo: <http://dbpedia.org/ontology/>.
@prefix fb: <https://facebook.com/>.

'''


#Input: string
#Output: an example.org based uri containing that name
def create_uri_from_name(name):
    name = name.replace(":","-")    
    return f'''<#{name.replace(" ","")}>'''

#template method to define a director
def define_director(director_name):
    base_text = f'''{create_uri_from_name(director_name)} rdf:type sch:Person;
                      foaf:name "{director_name}".'''
    return base_text

#template method to define an director
def define_actor(actor_name):
    base_text = f'''{create_uri_from_name(actor_name)} rdf:type sch:Person;
                      foaf:name "{actor_name}".'''
    return base_text

#template method to define a country
def define_country(country_name):
    base_text = f'''{create_uri_from_name(country_name)} rdf:type sch:Country;
                      foaf:name "{country_name}".'''
    return base_text

#template method to define a netflix category
def define_netflix_category(category_name):
    base_text = f'''{create_uri_from_name(category_name)} rdf:type dbo:Genre;
                      foaf:name "{category_name}".'''
    return base_text

#method to bring the "Date Added" column from CSV in a standard format
def transform_date_added(date_string):

    if date_string == "":
        return ""

    result_date = ""
    year = 2
    day = 1
    month = 0
    clean_string = date_string.replace(",","").lower().strip()
    dates_array = clean_string.split(" ")
    result_date = dates_array[year] + "-" + str(MONTHS_DICT.get(dates_array[month])) + "-" + dates_array[day]
    return result_date

#template method for creating a media record with all its actors, directors etc.
def create_media(media_type, media_name, actors_list, directors_list, countries, date_added_on_netflix, date_created, duration, genres_list, description):

    if media_type == TV_SHOW:
        media_type = "TVSeries"
    else:
        media_type = "Movie"

    base_text = f'''{create_uri_from_name(media_name)} rdf:type sch:{media_type};
                   sch:name "{media_name}";
                   sch:actor {actors_list};
                   sch:director {directors_list};
                   sch:countryOfOrigin {countries};
                   sch:datePublished "{date_added_on_netflix}T00:00:0+01:00"^^xsd:dateTime;
                   sch:dateCreated "{date_created}T00:00:00+01:00"^^xsd:dateTime;
                   sch:duration {duration};
                   sch:genre {genres_list};
                   rdfs:comment  "{description}". '''
    return base_text

#the CSV contains "columns" defined as a list (eg. actors). Our parser returns it as a string. In order to further create all the records inside, we need to convert the string to a list
def list_from_csv_list(items_string):  
    items_list = items_string.strip().split(",")
    return list(map( lambda item : item.strip(), items_list))

# given a list of names, a RDF list of URIs is returned. We need this in order, for example, to attach a movie its list of actors    
def uri_string_from_list(items_list):   
    result = "( "
    for item in items_list:       
        if item != "":
         result = result + create_uri_from_name(item) + " "
    return result + " )"

#we use this in order to avoid adding duplicates
def ontology_already_contains_name(name):    
    global CREATED_URIS

    uri = create_uri_from_name(name)    
    if uri in CREATED_URIS.keys():
        return True
    else:
        CREATED_URIS[uri] = True
        return False 
    
# a row is a row from the CSV file, defined as a list
def create_rdf_from_row(row):

    global base_rdf_schema 

    media_type = row[1]
    media_name = row[2].replace('"',"").replace("|","") 

    directors = list_from_csv_list(row[3].replace('"',""))
    for director in directors:       
        if director != '' and not ontology_already_contains_name(director):
            base_rdf_schema = base_rdf_schema + "\n" + define_director(director)
    directors_uris_as_string = uri_string_from_list(directors)

    actors = list_from_csv_list(row[4].replace('"',""))
    for actor in actors:        
        if actor != '' and not ontology_already_contains_name(actor):
            base_rdf_schema = base_rdf_schema + "\n" + define_actor(actor)                
    actors_uris_as_string = uri_string_from_list(actors)

    countries = list_from_csv_list(row[5])
    for country in countries:
     if country != '' and not ontology_already_contains_name(country):
       base_rdf_schema = base_rdf_schema + "\n" + define_country(country)

    country_uris_as_string = uri_string_from_list(countries)

    date_added_on_netflix = transform_date_added(row[6])
    date_created = row[7] + "-01-01"

    duration = row[9].split(" ")[0]

    categories = list_from_csv_list(row[10])
    for category in categories:
        if category != '' and not ontology_already_contains_name(category):
            base_rdf_schema = base_rdf_schema + "\n" + define_netflix_category(category)            
    category_uris_as_string = uri_string_from_list(categories)

    description = row[11].replace('"',"")
    base_rdf_schema =  base_rdf_schema + "\n" +  create_media(media_type, media_name, actors_uris_as_string, directors_uris_as_string, country_uris_as_string, date_added_on_netflix, date_created, duration, category_uris_as_string, description )


#with open('netflix_titles.csv', encoding="utf8") as csvfile:
  #  csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
  ##  counter = 0
   # for row in csv_reader:
      # if counter > 0:
        #    create_rdf_from_row(row)                              
       #counter = counter + 1

#print( base_rdf_schema)

base_rdf_schema =  base_rdf_schema + "\n" + '''

fb:BogdanCiubotaru rdf:type sch:Person;
        foaf:name "Bogdan Ciubotaru";
        foaf:accountName "bogdan.ciubotaru";
        foaf:knows ( fb:User1 fb:User2 fb:user3 );
        foaf:watched ( <#DickJohnsonIsDead> <#Blood&Water> ).        

'''

#f = open("fisier.txt", "w", encoding="utf8")
#f.write(base_rdf_schema)
#f.close()

with open('fisier.txt', 'r', encoding="utf8") as file:
    read_data = file.read().replace('\n', '')
    g = Graph().parse(format = 'ttl', data = read_data)

#print(qres)

#print(base_rdf_schema)

#g = Graph().parse(format = 'ttl', data = base_rdf_schema)

sparqlQuery = '''
SELECT ?movie where {
    ?entitatePersoana rdf:type sch:Person;
                    foaf:accountName ?fbAccountName.
    ?entitatePersoana foaf:watched ?movieList.
    ?movieList rdf:rest*/rdf:first ?movie.

    

    FILTER ( ?fbAccountName = "bogdan.ciubotaru"^^xsd:string)
}
                                                 
  '''                  

qres = g.query(sparqlQuery)

for row in qres:
    movie_uri = row.movie
    print (movie_uri)
    query2 = '''
    select ?comentariu where {
         <''' + str(movie_uri) + '''> rdfs:comment ?comentariu.
    }
    '''   
    qres2 = g.query(query2)
    for row2 in qres2:
        print(row2.comentariu)

queryPentruLista = '''
SELECT ?entitateFilm where { 
                    ?entitateFilm rdfs:comment ?commentariu.                                       
                    ?entitateFilm sch:actor ?listaActori                
                                        
                    filter exists 
                        { ?listaActori  rdf:rest*/rdf:first ?actor.
                          ?actor foaf:name "Mary Berry"
                        }
                                                 
                    } 
'''

queryPentruData = '''
SELECT ?entitateFilm where { 
                    ?entitateFilm sch:dateCreated ?data.
                    filter (
                    year(xsd:dateTime(?data))  = 2018 )  
                    }                                                                            
'''
#merge si month()