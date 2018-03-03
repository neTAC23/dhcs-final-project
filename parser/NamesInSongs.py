import os
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
from more_itertools import unique_everseen

def read_name_lists(input_path):
    names = []
    file = open(input_path, 'r+', encoding='utf8')
    for name in file:
        names.append(name.strip())
    return names


def get_name_sex(name):
    if name in bible_male:
        if name in bible_female:
            return "BU"     # Bible Unisex
        else:
            return "BM"     # Bible Male
    elif name in bible_female:
        return "BF"         # Bible Female
    elif name in males:
        if name in females:
            return "U"
        else:
            return "M"
    elif name in females:
        return "F"
    else:
        return "X"


def find_sex_from_song(lines):
    sex = "U"
    for line in lines:
        data = line.split()
        if len(data) > 6:
            found = data[5]
            if found == "feminine":
                if sex == "U" or sex == "F":
                    sex = "F"
                if sex == "M":
                    sex = "U"
                    break
            if found == "masculine":
                if sex == "U" or sex == "M":
                    sex = "M"
                if sex == "F":
                    sex = "U"
                    break
    return sex


def get_data_from_json(singer, title):
    for song in songs_data:
        if song['singer'] == singer and song['title'] == title:
            url = song['url']
            year = song['year']
            return url, year


def make_query(name):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT ?personLabel ?sex_or_genderLabel
    WHERE {
      ?person wdt:P31 wd:Q5.
      ?person ?label """ + "\"" + name + "\"" """@he.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
      OPTIONAL { ?person wdt:P21 ?sex_or_gender. }
    }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    sex = ""
    for result in results["results"]["bindings"]:
        sex = result["sex_or_genderLabel"]["value"] if 'sex_or_genderLabel' in result else ""
    return sex


def get_singer_sex(singer):
    if singer in artists:
        return artists[singer]
    else:
        sex = make_query(singer)
        artists[singer] = sex
        return sex


def write_to_csv(name, singer, title, sex, url, year, singer_sex):
    if sex == 'U':
        spamwriter_males.writerow([name, singer, title, sex, url, year, singer_sex])
        spamwriter_females.writerow([name, singer, title, sex, url, year, singer_sex])
    elif sex == 'BU':
        spamwriter_bible_males.writerow([name, singer, title, sex, url, year, singer_sex])
        spamwriter_bible_females.writerow([name, singer, title, sex, url, year, singer_sex])
    elif sex == 'M':
        spamwriter_males.writerow([name, singer, title, sex, url, year, singer_sex])
    elif sex == 'F':
        spamwriter_females.writerow([name, singer, title, sex, url, year, singer_sex])
    elif sex == 'BM':
        spamwriter_bible_males.writerow([name, singer, title, sex, url, year, singer_sex])
    elif sex == 'BF':
        spamwriter_bible_females.writerow([name, singer, title, sex, url, year, singer_sex])



def get_names_and_info(input_path):
    bible = False
    for file in os.listdir(input_path):
        print(file)
        if file.lower().endswith('.txt'):
            file_path = os.path.join(input_path, file)
            tagged_file = open(file_path, 'r+', encoding='utf8')
            lines = tagged_file.readlines()
            for i, line in enumerate(lines):
                data = line.split()
                if len(data) > 10:
                    ner = data[10].strip()
                    if ner == "I_PERS":
                        name = data[1].strip()
                        sex = get_name_sex(name)
                        if sex == "X":
                            continue
                        elif sex == "BU" or sex == "U":
                            if sex == "BU":
                                bible = True
                            if i < 2:
                                sex = find_sex_from_song(lines[0:5])
                            elif i > len(lines)-3:
                                sex = find_sex_from_song(lines[i-2:len(lines)])
                            else:
                                sex = find_sex_from_song(lines[i-2:i+3])

                            if bible:
                                sex == "B"+sex
                        file_data = file.split("_")
                        singer = file_data[0]
                        title = "_".join(file_data[-2:])[:-4]
                        url, year = get_data_from_json(singer, title)
                        singer_sex = get_singer_sex(singer)
                        write_to_csv(name, singer, title, sex, url, year, singer_sex)



bible_male = read_name_lists("C:/Users/Neta/Documents/semester7/dhcs/Digital-Humanities-Final-Project/names_lists/Biblical_males.txt")
bible_female = read_name_lists("C:/Users/Neta/Documents/semester7/dhcs/Digital-Humanities-Final-Project/names_lists/Biblical_females.txt")
males = read_name_lists("C:/Users/Neta/Documents/semester7/dhcs/Digital-Humanities-Final-Project/names_lists/Males.txt")
females = read_name_lists("C:/Users/Neta/Documents/semester7/dhcs/Digital-Humanities-Final-Project/names_lists/Females.txt")
json_file = open("merged_file.json", "r+", encoding='utf8')
json_data = json.load(json_file)
songs_data = json_data['songs']
artists = {}
input = 'D:/bgu/dhcs-final-project/all_tagged_songs'
males_csv = open("csvs/males.csv", 'a', newline='', encoding='utf8')
females_csv = open("csvs/females.csv", 'a', newline='', encoding='utf8')
bible_males_csv = open("csvs/bible_males.csv", 'a', newline='', encoding='utf8')
bible_females_csv = open("csvs/bible_females.csv", 'a', newline='', encoding='utf8')

spamwriter_males = csv.writer(males_csv, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter_males.writerow(['name', 'singer', 'title', 'sex', 'url', 'year', 'singer_sex'])

spamwriter_females = csv.writer(females_csv, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter_females.writerow(['name', 'singer', 'title', 'sex', 'url', 'year', 'singer_sex'])

spamwriter_bible_males = csv.writer(bible_males_csv, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter_bible_males.writerow(['name', 'singer', 'title', 'sex', 'url', 'year', 'singer_sex'])

spamwriter_bible_females = csv.writer(bible_females_csv, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
spamwriter_bible_females.writerow(['name', 'singer', 'title', 'sex', 'url', 'year', 'singer_sex'])


get_names_and_info(input)
for file in os.listdir("csvs"):
    file_path = os.path.join("csvs", file)
    with open(file_path,'r', encoding='utf8') as f, open('temp.csv','w', encoding='utf8') as out_file:
        out_file.writelines(unique_everseen(f))
    f.close()
    os.remove(file_path)
    out_file.close()
    os.rename('temp.csv', file_path)

json_file.close()
males_csv.close()
females_csv.close()
bible_males_csv.close()
bible_females_csv.close()