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

    stories_length = get_stories_length(df)

    appearances = df.loc[df.appearances.str.len() != 0, "appearances"].value_counts()
    individual_appearances = df.loc[df["appearances"] != "", "appearances"].str.split(", ").explode().value_counts()
    writers = df.loc[df.writing.str.len() != 0, "writing"].value_counts()
    artists = df.loc[df.art.str.len() != 0, "art"].value_counts()
    years = df.loc[df["date"] != "", "date"].dt.strftime("%Y").value_counts()

    decades = get_decades(df)

    data = {
        "stories_length": stories_length,
        "appearances": appearances,
        "individual_appearances": individual_appearances,
        "writers": writers,
        "artists": artists,
        "years": years,
        "decades": decades
    }

    return data


def get_stories_length(df):

    df = df[~df.pages.str.contains("/")].iloc[:, [1,2]] # some pages contain a slash, like 7 7/8
    df["pages"] = df["pages"].astype(int)
    df = df.sort_values(by = ["pages"], ascending=False)
    df["title"] = df["title"].str.replace("$", "'$'") # replace dollar signs with the letter "s" (they are usually used as a wordplay with Uncle Scrooge and matplotlib interprets that symbol as math text, causing issues)
    stories_length = pd.Series(df["pages"].values, index=df["title"], name="pages")    # convert page number from str to int

    return stories_length


def get_decades(df):

    decades = []
    years = df["date"].dt.strftime("%Y")
    for year in years:
        if str(year).isnumeric():
            decade = str(year)[:3] + "0"
            decades.append(decade)
    decades = dict(sorted(Counter(decades).items(), key = lambda x: x[1], reverse=True))
    decades = pd.Series(decades, name="count")
    decades.index.name = "decade"

    return decades


def write_data(data):

    print("Writing data in CSV format...")

    for title in data:
        data[title].to_csv(f"report/csv/{title}.csv", index=True, header=True)


def draw_plots(data):

    print("Drawing plots...")

    for title in data:

        data[title] = data[title].iloc[:10]

        # Barplot
        sns.set(rc={"figure.figsize":(20,8.27)})
        plot = sns.barplot(x = data[title].values, y = data[title].index, orient = "h").set(title = "Top " + title.title().replace('_', ' '), xlabel = None, ylabel = None)
        plt.tight_layout()
        plt.savefig(f"report/plots/top_{title}_bar_plot.png")

        plt.figure(clear=True)
    
        if title != "stories_length":   # pie chart has no meaning for this stat
            # Pie chart
            labels = data[title].index
            sizes = data[title].values / data[title].values.sum() * 100
            plt.pie(sizes, textprops = {"color":"w"})
            labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
            plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
            plt.title("Top " + title.title().replace('_', ' '))
            plt.tight_layout()
            plt.savefig(f"report/plots/top_{title}_pie_chart.png")

            plt.figure(clear=True)


if __name__ == "__main__":
    main()
