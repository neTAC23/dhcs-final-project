import os
import csv
import operator
import json


def count_names_per_year_and_file(file):
    dict = {}
    file_path = os.path.join("csvs", file)
    spamReader = csv.reader(open(file_path, newline='', encoding='utf8'), delimiter='\t',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in spamReader:
        if len(row) > 5:
            year = row[5]
            if not year == 'year':
                if not year == '0':
                    year = year[1:-2]
                year = int(year)
                if year in dict:
                    dict[year] += 1
                else:
                    dict[year] = 1
    return dict


def count_names_per_year():
    for file in os.listdir("csvs"):
        d = count_names_per_year_and_file(file)
        if file == 'males.csv':
            males_per_year = d
        elif file == 'females.csv':
            females_per_year = d
        elif file == 'bible_males.csv':
            bible_males_per_year = d
        elif file == 'bible_females.csv':
            bible_females_per_year = d
    return get_all_years_and_write_data_to_csv(males_per_year, females_per_year, bible_males_per_year, bible_females_per_year)


def get_all_years_and_write_data_to_csv(males, females, bible_males, bible_females):
    names_per_year = open("names_per_year.csv", 'a', newline='', encoding='utf8')
    spamwriter = csv.writer(names_per_year, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['year','male', 'bible_male', 'female', 'bible_female'])
    keys = set(males.keys())
    keys = keys.union(set(females.keys()))
    keys = keys.union(set(bible_males.keys()))
    keys = keys.union(set(bible_females.keys()))
    keys = sorted(keys)
    for year in keys:
        males_year = males[year] if year in males else 0
        females_year = females[year] if year in females else 0
        bible_males_year = bible_males[year] if year in bible_males else 0
        bible_females_year = bible_females[year] if year in bible_females else 0
        spamwriter.writerow([year,males_year, bible_males_year, females_year, bible_females_year])
    return keys


def find_popular_names(years):
    years_to_names = {}
    names = {}
    for year in years:
        years_to_names[year] = {}
    for file in os.listdir("csvs"):
        file_path = os.path.join("csvs", file)
        spamReader = csv.reader(open(file_path, newline='', encoding='utf8'), delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in spamReader:
            if len(row) > 5:
                name_song = row[0]
                year_song = row[5]
                if not year_song == 'year':
                    if not year_song == '0':
                        year_song = year_song[1:-2]
                    year_song = int(year_song)
                    if name_song in years_to_names[year_song]:
                        years_to_names[year_song][name_song] += 1
                    else: years_to_names[year_song][name_song] = 1
                    if name_song in names:
                        names[name_song] += 1
                    else: names[name_song] = 1
    #top_names = open("top_names.txt", 'a', encoding='utf8')
    top_names = {}
    popular_names = open("popular_names.csv", 'a', newline='', encoding='utf8')
    spamwriter = csv.writer(popular_names, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['name', '#occurances'])
    for year in years_to_names:
        sorted_year = sorted(years_to_names[year].items(), key=operator.itemgetter(1))
        top5 = sorted_year[-5:]
        top5_values = []
        for i in top5:
            top5_values.append(i[0])
        top_names[year] = top5_values
    for name in names:
        spamwriter.writerow([name, names[name]])
    #top_names.close()
    with open("top_names.json", 'w+', encoding='utf8') as outfile:
        json.dump(top_names, outfile, ensure_ascii=False)
    popular_names.close()


def do_males_sing_about_females():
    male_songs = 0
    female_songs = 0
    male_songs_about_females = 0
    female_songs_about_males = 0
    for file in os.listdir("csvs"):
        file_path = os.path.join("csvs", file)
        spamReader = csv.reader(open(file_path, newline='', encoding='utf8'), delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if file == "bible_males.csv" or file == "males.csv":
            for row in spamReader:
                if len(row) > 6:
                    singer_sex = row[6]
                    if singer_sex == 'male':
                        male_songs += 1
                    elif singer_sex == 'female':
                        female_songs += 1
                        female_songs_about_males += 1
        elif file == "bible_females.csv" or file == "females.csv":
            for row in spamReader:
                if len(row) > 6:
                    singer_sex = row[6]
                    if singer_sex == 'male':
                        male_songs += 1
                        male_songs_about_females += 1
                    elif singer_sex == 'female':
                        female_songs += 1
    males_songs_about_females_percentage = male_songs_about_females/male_songs
    females_songs_about_males_percentage = female_songs_about_males/female_songs
    print(males_songs_about_females_percentage)
    print(females_songs_about_males_percentage)


def get_letter_num(name):
    letter = name[0]
    num = ord(letter)
    if num < 1498: #aleph-yud
        num = num - 1488
    elif num == 1499:
        num = 10
    elif num > 1499 and num < 1505:
        num = num/2
        num = num-739
    elif num == 1505 or num == 1506:
        num = num-1491
    elif num == 1508 or num == 1510:
        num = num/2
        num = num-738
    elif num > 1510:
        num -= 1493
    return int(num)


def create_names_dict():
    letter_names = {}
    for i in range(22):
        letter_names[i] = {}

    for file in os.listdir("csvs"):
        file_path = os.path.join("csvs", file)
        spamReader = csv.reader(open(file_path, newline='', encoding='utf8'), delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in spamReader:
            if len(row) > 5 and not row[0] == 'name':
                name = row[0]
                singer = row[1]
                song = row[2]
                url = row[4]
                song_key = singer+"_"+song
                letter_num = get_letter_num(name)
                if name in letter_names[letter_num]:
                    songs = letter_names[letter_num][name]
                    if song_key in songs:
                        continue
                    else:
                        songs[song_key] = url
                else:
                    letter_names[letter_num][name] = {}
                    songs = letter_names[letter_num][name]
                    songs[song_key] = url
    with open("names.json", 'w+', encoding='utf8') as outfile:
        json.dump(letter_names, outfile, ensure_ascii=False)


years = count_names_per_year()
years = sorted(years, reverse=True)
find_popular_names(years)
do_males_sing_about_females()
create_names_dict()
