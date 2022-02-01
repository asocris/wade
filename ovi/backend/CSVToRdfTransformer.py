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

PEOPLE = "people/"
MEDIA_CREATIONS = "mediaCreations/"
APP_USERS = "users/"
CATEGORIES = "categories/"
COUNTRIES = "countries/"


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

'''


#Input: string
#Output: an example.org based uri containing that name
def create_uri_from_name(name, category):
    name = name.replace(":","-").replace("|","")    
    return f'''<{category}{name.replace(" ","")}>'''

#template method to define a director
def define_director(director_name):
    global PEOPLE
    base_text = f'''{create_uri_from_name(director_name, PEOPLE)} rdf:type sch:Person;
                      foaf:name "{director_name}".'''
    return base_text

#template method to define an director
def define_actor(actor_name):
    global PEOPLE
    base_text = f'''{create_uri_from_name(actor_name, PEOPLE)} rdf:type sch:Person;
                      foaf:name "{actor_name}".'''
    return base_text

#template method to define a country
def define_country(country_name):
    global COUNTRIES
    base_text = f'''{create_uri_from_name(country_name, COUNTRIES)} rdf:type sch:Country;
                      foaf:name "{country_name}".'''
    return base_text

#template method to define a netflix category
def define_netflix_category(category_name):
    global CATEGORIES
    base_text = f'''{create_uri_from_name(category_name, CATEGORIES)} rdf:type dbo:Genre;
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
def create_media(media_type, media_name, actors_list, directors_list, countries_list, 
                date_added_on_netflix, date_created, duration, genres_list, description):
    global MEDIA_CREATIONS
    if media_type == TV_SHOW:
        media_type = "TVSeries"
    else:
        media_type = "Movie"

    base_text = f'''{create_uri_from_name(media_name, MEDIA_CREATIONS)} rdf:type sch:{media_type};
                   sch:name "{media_name}";
                   sch:actor {actors_list};
                   sch:director {directors_list};
                   sch:countryOfOrigin {countries_list};
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
def uri_string_from_list(items_list, category):   
    result = "( "
    for item in items_list:       
        if item != "":
         result = result + create_uri_from_name(item, category) + " "
    return result + " )"

#we use this in order to avoid adding duplicates
def ontology_already_contains_name(name, category):    
    global CREATED_URIS

    uri = create_uri_from_name(name, category)    
    if uri in CREATED_URIS.keys():
        return True
    else:
        CREATED_URIS[uri] = True
        return False 
    
# a row is a row from the CSV file, defined as a list
def create_rdf_from_row(row):

    global base_rdf_schema 
    global PEOPLE
    global MEDIA_CREATIONS
    global APP_USERS
    global CATEGORIES
    global COUNTRIES

    media_type = row[1]
    media_name = row[2].replace('"',"")

    directors = list_from_csv_list(row[3].replace('"',""))
    for director in directors:       
        if director != '' and not ontology_already_contains_name(director, PEOPLE):
            base_rdf_schema = base_rdf_schema + "\n" + define_director(director)
    directors_uris_as_string = uri_string_from_list(directors, PEOPLE)

    actors = list_from_csv_list(row[4].replace('"',""))
    for actor in actors:        
        if actor != '' and not ontology_already_contains_name(actor, PEOPLE):
            base_rdf_schema = base_rdf_schema + "\n" + define_actor(actor)                
    actors_uris_as_string = uri_string_from_list(actors, PEOPLE)

    countries = list_from_csv_list(row[5])
    for country in countries:
     if country != '' and not ontology_already_contains_name(country, COUNTRIES):
       base_rdf_schema = base_rdf_schema + "\n" + define_country(country)

    country_uris_as_string = uri_string_from_list(countries, COUNTRIES)

    date_added_on_netflix = transform_date_added(row[6])
    date_created = row[7] + "-01-01"

    duration = row[9].split(" ")[0]

    categories = list_from_csv_list(row[10])
    for category in categories:
        if category != '' and not ontology_already_contains_name(category, CATEGORIES):
            base_rdf_schema = base_rdf_schema + "\n" + define_netflix_category(category)            
    category_uris_as_string = uri_string_from_list(categories, CATEGORIES)

    description = row[11].replace('"',"")
    base_rdf_schema =  base_rdf_schema + "\n" +  create_media(media_type, media_name, actors_uris_as_string, directors_uris_as_string, country_uris_as_string, date_added_on_netflix, date_created, duration, category_uris_as_string, description )


with open('netflix_titles.csv', encoding="utf8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    counter = 0
    for row in csv_reader:
       if counter > 0 and counter < 100:
        create_rdf_from_row(row)                              
       counter = counter + 1

print( base_rdf_schema)


f = open("RDFSchema.txt", "w", encoding="utf8")
f.write(base_rdf_schema)
f.close()