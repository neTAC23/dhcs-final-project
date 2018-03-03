import os
import json


def split_long_files(input_path):
    for file in os.listdir(input_path):
        print(file)
        if file.lower().endswith('.txt'):
            filepath = os.path.join(input_path, file)
            clean_file(filepath, input_path)
            with open(filepath, "r+", encoding='utf8') as text_file:
                word_count, i = 0, 0
                lines = []
                flag = False
                for line in text_file:
                    lines.append(line)
                    word_count += len(line.split())
                    if word_count > 90:
                        flag = True
                        name = os.path.basename(file) + "_" + str(i) + ".txt"
                        f = open(os.path.join(input_path, "newfiles", name), 'a', encoding='utf8')
                        for l in lines:
                            f.write(l)
                        f.close()
                        lines = []
                        word_count = 0
                        i += 1
                if flag:
                    if word_count > 0:
                        name = os.path.basename(file) + "_" + str(i) + ".txt"
                        f = open(os.path.join(input_path, "newfiles", name), 'a', encoding='utf8')
                        for l in lines:
                            f.write(l)
                        f.close()
                    text_file.close()
                    os.remove(filepath)


def clean_file(file_path, path):
    with open(file_path, "r+", encoding='utf8') as old_file:
        new_file_path = os.path.join(path, "temp.txt")
        with open(new_file_path, "a", encoding="utf8") as new_file:
            for line in old_file:
                new_file.write(line.replace("\\", " ").replace("/", " ").replace("|", " ").replace("~", " "))
        old_file.close()
        new_file.close()
        os.remove(file_path)
        os.rename(new_file_path, file_path)


def split_long_lines(input_path):
    for file in os.listdir(input_path):
        print(file)
        flag = False
        if file.lower().endswith('.txt'):
            filepath = os.path.join(input_path, file)
            with open(filepath, "r+", encoding='utf8') as text_file:
                word_count, i = 0, 0
                num_files = 0
                words = []
                lines = []
                flag = False
                for line in text_file:
                    if len(text_file.readlines()) == 0 and len(line.split()) > 90:
                        flag = True
                        print("here")
                        words = line.split()
                        word_count = len(words)
                        num_files = int(word_count/90)+1
                        for i in range(num_files):
                            words_to_write = words[i*90: (i+1)*90]
                            text = " ".join(words_to_write)
                            lines.append(text)
                        print(lines)
            if(flag):
                text_file.close()
                os.remove(filepath)
                file_not_numbered = file[0:-5]
                for i in range(num_files):
                    print(file)
                    file = file_not_numbered+str(i)+".txt"
                    filepath = os.path.join(input_path, file)
                    f = open(filepath, 'a', encoding='utf8')
                    f.write(lines[i])
                    f.close()


def merge_splitted_files(input_path):
    for file in os.listdir(input_path):
        base_name = file[0:-6]
        print(base_name)
        file_path = os.path.join(input_path, base_name)
        old_file = open(os.path.join(input_path, file), "r", encoding='utf8')
        with open(file_path, "a+", encoding='utf8') as text_file:
            for line in old_file:
                text_file.write(line)
            old_file.close()
            os.remove(os.path.join(input_path, file))
            text_file.close()


def merge_json(input_path):
    data = {}
    data['songs'] = []
    for f in os.listdir(input_path):
        file_path = os.path.join(input_path, f)
        with open(file_path, "r+", encoding='utf8') as infile:
            data['songs'].extend(json.load(infile)['songs'])

    file_path = os.path.join(input_path, "merged_file.json")
    with open(file_path, 'w+', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

#input_path = 'C:/Users/Neta/Documents/semester7/dhcs/Digital-Humanities-Final-Project/tagger/lyrics/newfiles'
#split_long_lines(input_path)
merge_splitted_files('C:/Users/Neta/Documents/semester7/dhcs/Digital-Humanities-Final-Project/tagger/taggedlyrics/newfiles')