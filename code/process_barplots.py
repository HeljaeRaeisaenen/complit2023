import matplotlib.pyplot as plt
import numpy as np
import json

hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]

subforums = {}
per_hour = {} #n of instances of swearing per hour
total_per_hour = {} #n of tokens (words posted) per hour
total_fractions = {} # swears/all per hour

# data0 contains the S24 corpus concordances, data contains the total all conclusive
with open('../data0/concordances.json', 'r', encoding='utf-8') as f:
    for row in f:
        c = json.loads(row)
        if c['hour'] not in per_hour:
            per_hour[c['hour']] = 0
        per_hour[c['hour']] += 1

        if c['subforum'] not in subforums:
            subforums[c['subforum']] = {}
        # ensure all subforums have all hours, even if theres' been 0 posts in that hour
        for hour in hours:
            if hour not in subforums[c['subforum']]:
                subforums[c['subforum']][hour] = 0
        subforums[c['subforum']][c['hour']] += 1



with open('../data0/count_all/all_S24.json', 'r', encoding='utf-8') as f:
    all = json.loads(f.read())

    for h,n in all["total"]["absolute"].items():
        if h[:2] not in total_per_hour:
            total_per_hour[h[:2]] = 0
        total_per_hour[h[:2]] += int(n) 

for h,n in total_per_hour.items():
    total_fractions[h] = round(per_hour[h] / n * 100, n)

# Plot all swear words across all Suomi24 forums:
    
h = list(total_fractions.keys())
n = list(total_fractions.values())

ticks = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]

plt.bar(h, n, color='violet')
plt.yticks(ticks)
plt.xlabel("Hour of the day")
plt.ylabel("% of all posted words")
plt.title("Percentage of swear words in forum posts per hour")

plt.savefig("../data/figures/total_words_barplot.png")


# Plot swearwords showing different subforums separately:

sub_fractions = {}
subforums_counts_per_hour = {}
unwanted_subs = ["Tori", "Kommentaattori", "Suomi24", "var cname = 0;  category name"]
for key,s in subforums.items():
    fractions = {}
    for hour,n in total_per_hour.items():
        fractions[hour] = round(s[hour]/n * 100, 3)

    sub_fractions[key] = fractions

    if key in unwanted_subs:
        continue
    subforums_counts_per_hour[key] = np.array(list(fractions.values()))

width = 0.85
fig, ax = plt.subplots()
bottom = np.zeros(24)
ax.set_yticks(ticks)

for subforum, count in subforums_counts_per_hour.items():
    p = ax.bar(hours, count, width, label=subforum, bottom=bottom)
    bottom += count


ax.set_title('Percentage of swear words by subforum')
ax.legend(bbox_to_anchor=(0.97, 0.97))
plt.xlabel("Hour of the day")
plt.ylabel("% of all posted words")

plt.savefig("../data/figures/subforums_barplot.png")
plt.show()
