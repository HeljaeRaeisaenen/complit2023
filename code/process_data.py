import matplotlib.pyplot as plt
import json

subforums = {}
per_hour = {} #n of instances of swearing per hour
total_per_hour = {} #n of tokens (words posted) per hour
fractions = {} # swears/all per hour

with open('../data/concordances.json', 'r', encoding='utf-8') as f:
    for row in f:
        c = json.loads(row)
        if c['hour'] not in per_hour:
            per_hour[c['hour']] = 0
        per_hour[c['hour']] += 1

        if c['subforum'] not in subforums:
            subforums[c['subforum']] = {}
        if c['hour'] not in subforums[c['subforum']]:
            subforums[c['subforum']][c['hour']] = []
        subforums[c['subforum']][c['hour']].append(c['word'])

        if c['subforum'] == "Kommentaattori":
            print(c)

        #for cat in c["categories"]:
        #    if cat not in subforums:
        #        subforums[cat] = {}
        #    if c['hour'] not in subforums[cat]:
        #        subforums[cat][c['hour']] = []    
        #    subforums[cat][c['hour']].append(c['word'])

k,f = subforums["Kommentaattori"]
print(subforums["Kommentaattori"]["23"], subforums["Kommentaattori"]["18"])
quit()

with open('../data/count_all/all_S24.json', 'r', encoding='utf-8') as f:
    all = json.loads(f.read())

    for h,n in all["corpora"]["S24"]["absolute"].items():
        if h[:2] not in total_per_hour:
            total_per_hour[h[:2]] = 0
        total_per_hour[h[:2]] += int(n) 

for h,n in total_per_hour.items():
    fractions[h] = (per_hour[h] / n)

h = list(fractions.keys())
n = list(fractions.values())

# Plot all swear words across all Suomi24 forums:
n = list(map(lambda x: round(x*100, 3),n))
ticks = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]

plt.bar(h, n, color='blue', edgecolor='black')
plt.yticks(ticks)
plt.xlabel("Hour of the day")
plt.ylabel("% of all posted words")
plt.title("Percentage of swear words in forum posts per hour")

plt.savefig("../data/figures/total_words_barplot.png")
#plt.show()
