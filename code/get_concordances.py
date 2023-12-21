# Query the Korp API and save the results in a local file

from korp.korp import Korp
import time, csv, json

def main():
    korppi = Korp(service_name="kielipankki")

    corpora = ['S24'] # Suomi24 corpus 2001-2014
    query_words = read_query_words()
    #print(query_words)
    additional_parameters = {
        "show":["word", "lemma", "lemmacomp"],
        "show_struct":["text","text_title","text_sect","text_sub","text_date","text_time", "text_topic_name_top", "text_topic_names_set"]
    }

    hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]

    # Ensure that the file is empty before we begin appending to it:
    with open('../data/concordances.json', 'w', encoding='utf-8') as f:
        f.write('')
    
    start = time.time()
    for word in query_words:
        query = '"' + word[0] + '"'
        print(query)
        print(corpora)

        try:
            number, concordances = korppi.concordance(query, corpora, additional_parameters=additional_parameters) # all_concordances
        except Exception as e:
            if e == KeyboardInterrupt:
                quit()
            else: continue


        results = []
        for c in concordances:
            query.replace('"', '')
            result = {"word":query, "categories":word[1:]}
            #print(c)
            for h in hours:
                if c["structs"]["text_time"][0:2] == h:
                    result["hour"] = h
            result["date"] = c["structs"]["text_date"]
            try:
                result["subforum"] = c["structs"]["text_sect"]
            except: result["subforum"] = c["structs"]["text_topic_name_top"]
            result["title"] = c["structs"]["text_title"]
            result["tokens"] = c["tokens"]

            results.append(result)

        with open('../data/concordances.json', 'a', encoding='utf-8') as f:
            for r in results:
                json.dump(r, f, ensure_ascii=False)
                f.write("\n")


    end = time.time()
    print("Time: ", end-start)


def read_query_words():
    with open('../data/swears-csv.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        result = []
        for row in reader:
            while("" in row):
                row.remove("")
            
            if " " in row[0]:
                parts = row[0].split(" ")
                row[0] = f'("{parts[0]}" "{parts[1]}")'

            result.append(row)
    return result

main()