import matplotlib.pyplot as plt
import json

cat_list = ['insult', 'common', 'censored', 'body', 'religious', 'weak', 'women', 'men', 'slur']
categories = {}
categories_per_subforum = {}

for cat in cat_list:
    categories[cat] = 0

# data0 contains the S24 corpus concordances, data contains the total all conclusive
with open('../data0/concordances.json', 'r', encoding='utf-8') as f:
    for row in f:
        c = json.loads(row)

        if c['subforum'] not in categories_per_subforum:
            categories_per_subforum[c['subforum']] = {}


        for cat in c["categories"]:
            categories[cat] += 1

            if cat not in categories_per_subforum[c['subforum']]:
                for cat2 in cat_list:
                    categories_per_subforum[c['subforum']][cat2] = 0
            categories_per_subforum[c['subforum']][cat] += 1


for key,sub in categories_per_subforum.items():
    if key in ["Tori", "Kommentaattori", "Suomi24", "var cname = 0;  category name"]:
        continue
    print(sub, type(sub))
    labels = list(sub.keys())
    sizes = list(sub.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%.0f%%')
    
    fig.suptitle(f'{key}', fontsize=16)

    fig.savefig(f"../data/figures/piechart_{key}.png")

    fig.clf()
    ax.cla()
    plt.close()


labels = list(categories.keys())
sizes = list(categories.values())
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%.0f%%')

fig.suptitle(f'All of Suomi24', fontsize=16)

fig.savefig(f"../data/figures/piechart_all.png")

