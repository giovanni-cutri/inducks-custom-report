# FUNCTION draw plots  barplot piechart




import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    os.mkdir("report")
except FileExistsError:
    pass

df = pd.read_json("collection.json")

df = df.fillna("")

top_appearances = df.loc[df.appearances.str.len() != 0, "appearances"].value_counts()[:10]

top_individual_appearances = df.loc[df["appearances"] != "", "appearances"].str.split(", ").explode().value_counts()[:10]

top_writers = df.loc[df.writing.str.len() != 0, "writing"].value_counts()[:10]

top_artists = df.loc[df.art.str.len() != 0, "art"].value_counts()[:10]

top_years = df.loc[df["date"] != "", "date"].str.split("-")[0].explode().value_counts()[:10]

print(top_years)
input()

sns.set(rc={"figure.figsize":(20,8.27)})
top_appearances_plot = sns.barplot(x = top_appearances.values, y = top_appearances.index, orient = "h").set(title = "Top ten appearances", xlabel = None, ylabel = None)
plt.tight_layout()
plt.savefig("report/top_appearances_bar_plot.png")

plt.figure(clear=True)

labels = top_appearances.index
sizes = top_appearances.values / top_appearances.values.sum() * 100
plt.pie(sizes, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
plt.title("Top ten appearances")
plt.tight_layout()
plt.savefig("report/top_appearances_pie_chart.png")

plt.figure(clear=True)

sns.set(rc={"figure.figsize":(20,8.27)})
top_individual_appearances_plot = sns.barplot(x = top_individual_appearances.values, y = top_individual_appearances.index, orient = "h").set(title = "Top ten individual appearances", xlabel = None, ylabel = None)
plt.tight_layout()
plt.savefig("report/top_individual_appearances__bar_plot.png")

plt.figure(clear=True)

labels = top_individual_appearances.index
sizes = top_individual_appearances.values / top_individual_appearances.values.sum() * 100
plt.pie(sizes, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
plt.title("Top ten individual_appearances")
plt.tight_layout()
plt.savefig("report/top_individual_appearances_pie_chart.png")

plt.figure(clear=True)

sns.set(rc={"figure.figsize":(20,8.27)})
top_writers_plot = sns.barplot(x = top_writers.values, y = top_writers.index, orient = "h").set(title = "Top ten writers", xlabel = None, ylabel = None)
plt.tight_layout()
plt.savefig("report/top_writers_bar_plot.png")

plt.figure(clear=True)

labels = top_writers.index
sizes = top_writers.values / top_writers.values.sum() * 100
plt.pie(sizes, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
plt.title("Top ten writers")
plt.tight_layout()
plt.savefig("report/top_writers_pie_chart.png")

plt.figure(clear=True)

sns.set(rc={"figure.figsize":(20,8.27)})
top_artists_plot = sns.barplot(x = top_artists.values, y = top_artists.index, orient = "h").set(title = "Top ten artists", xlabel = None, ylabel = None)
plt.tight_layout()
plt.savefig("report/top_artists_bar_plot.png")

plt.figure(clear=True)

labels = top_artists.index
sizes = top_artists.values / top_artists.values.sum() * 100
plt.pie(sizes, textprops = {"color":"w"})
labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
plt.title("Top ten artists")
plt.tight_layout()
plt.savefig("report/top_artists_pie_chart.png")