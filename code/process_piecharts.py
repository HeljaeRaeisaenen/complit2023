import matplotlib.pyplot as plt
import numpy as np
import json

cat_list = ['insult', 'common', 'censored', 'body', 'religious', 'weak', 'women', 'men', 'slur']
hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]

categories = {}
categories_per_subforum = {}
swears_per_hour = {}

for cat in cat_list:
    categories[cat] = 0

for h in hours:
    swears_per_hour[h] = 0

categories_per_hour = {}
for c in cat_list:
    categories_per_hour[c] = {}

with open('../data/concordances.json', 'r', encoding='utf-8') as f:
    for row in f:
        c = json.loads(row)

        if c['subforum'] not in categories_per_subforum:
            categories_per_subforum[c['subforum']] = {}


        for cat in c['categories']:
            categories[cat] += 1
            swears_per_hour[c['hour']] += 1

            if cat not in categories_per_subforum[c['subforum']]:
                for cat2 in cat_list:
                    categories_per_subforum[c['subforum']][cat2] = 0
            categories_per_subforum[c['subforum']][cat] += 1

            if c['hour'] not in categories_per_hour[cat]:
                for h in hours:
                    categories_per_hour[cat][h] = 0
            categories_per_hour[cat][c['hour']] += 1

for key,sub in categories_per_subforum.items():
    if key in ["Tori", "Kommentaattori", "Suomi24", "var cname = 0;  category name"]:
        continue
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


for h,n in swears_per_hour.items():
    for c in categories_per_hour.values():
        c[h] = c[h] / n * 100

width = 0.85
fig, ax = plt.subplots()
bottom = np.zeros(24)

for category, count in categories_per_hour.items():
    p = ax.bar(hours, list(count.values()), width, label=category, bottom=bottom)
    bottom += list(count.values())


ax.set_title('Percentage of swear words by category')
ax.legend(bbox_to_anchor=(0.97, 0.97))
plt.xlabel("Hour of the day")
plt.ylabel("% of all posted swears")

plt.savefig("../data/figures/categories_barplot.png")
plt.show()

