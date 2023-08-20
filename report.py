import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


def main():
    df = set_up()
    data = calculate(df)
    write_data(data)
    draw_plots(data)
    print("Done.")


def set_up():

    try:
        os.makedirs(os.path.join(os.getcwd(), "report", "csv"))
    except FileExistsError:
        pass

    try:
        os.makedirs(os.path.join(os.getcwd(), "report", "plots"))
    except FileExistsError:
        pass

    print("Getting data...")
    
    df = pd.read_json("collection.json")
    df = df.fillna("")

    return df


def calculate(df):

    print("Calculating stats...")

    longest_stories = get_longest_stories(df)

    top_appearances = df.loc[df.appearances.str.len() != 0, "appearances"].value_counts()[:10]
    top_individual_appearances = df.loc[df["appearances"] != "", "appearances"].str.split(", ").explode().value_counts()[:10]
    top_writers = df.loc[df.writing.str.len() != 0, "writing"].value_counts()[:10]
    top_artists = df.loc[df.art.str.len() != 0, "art"].value_counts()[:10]
    top_years = df.loc[df["date"] != "", "date"].dt.strftime("%Y").value_counts()[:10]

    top_decades = get_decades(df)

    data = {
        "longest_stories": longest_stories,
        "top_appearances": top_appearances,
        "top_individual_appearances": top_individual_appearances,
        "top_writers": top_writers,
        "top_artists": top_artists,
        "top_years": top_years,
        "top_decades": top_decades
    }

    return data


def get_longest_stories(df):

    df = df[~df.pages.str.contains("/")].iloc[:, [1,2]] # some pages contain a slash, like 7 7/8
    df["pages"] = df["pages"].astype(int)
    df = df.sort_values(by = ["pages"], ascending=False).head(10)
    df["title"] = df["title"].str.replace("$", "'$'") # replace dollar signs with the letter "s" (they are usually used as a wordplay with Uncle Scrooge and matplotlib interprets that symbol as math text, causing issues)
    longest_stories = pd.Series(df["pages"].values, index=df["title"], name="pages")    # convert page number from str to int

    return longest_stories


def get_decades(df):

    decades = []
    years = df["date"].dt.strftime("%Y")
    for year in years:
        if str(year).isnumeric():
            decade = str(year)[:3] + "0"
            decades.append(decade)
    top_decades = dict(sorted(Counter(decades).items(), key = lambda x: x[1], reverse=True))
    top_decades = pd.Series(top_decades, name="count")
    top_decades.index.name = "decade"

    return top_decades


def write_data(data):

    print("Writing data in CSV format...")

    for title in data:
        data[title].to_csv(f"report/csv/{title}.csv", index=True, header=True)


def draw_plots(data):

    print("Drawing plots...")

    for title in data:

        # Barplot
        sns.set(rc={"figure.figsize":(20,8.27)})
        plot = sns.barplot(x = data[title].values, y = data[title].index, orient = "h").set(title = title.title().replace('_', ' '), xlabel = None, ylabel = None)
        plt.tight_layout()
        plt.savefig(f"report/plots/{title}_bar_plot.png")

        plt.figure(clear=True)
    
        if title != "longest_stories":   # pie chart has no meaning for this stat
            # Pie chart
            labels = data[title].index
            sizes = data[title].values / data[title].values.sum() * 100
            plt.pie(sizes, textprops = {"color":"w"})
            labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
            plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
            plt.title(title.title().replace('_', ' '))
            plt.tight_layout()
            plt.savefig(f"report/plots/{title}_pie_chart.png")

            plt.figure(clear=True)


if __name__ == "__main__":
    main()
