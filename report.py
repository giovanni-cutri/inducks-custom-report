import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    df = set_up()
    data = calculate(df)
    draw_plots(data)


def set_up():

    try:
        os.mkdir("report")
    except FileExistsError:
        pass
    
    df = pd.read_json("collection.json")
    df = df.fillna("")

    return df


def calculate(df):

    top_appearances = df.loc[df.appearances.str.len() != 0, "appearances"].value_counts()[:10]
    top_individual_appearances = df.loc[df["appearances"] != "", "appearances"].str.split(", ").explode().value_counts()[:10]
    top_writers = df.loc[df.writing.str.len() != 0, "writing"].value_counts()[:10]
    top_artists = df.loc[df.art.str.len() != 0, "art"].value_counts()[:10]
    top_years = df.loc[df.art.str.len() != 0, "art"].value_counts()[:10]
    #top_years = df.loc[df["date"] != "", "date"].str.split("-")[0].explode().value_counts()[:10]

    #print(top_years)
    #input()
    #DECADES

    data = {
        "top_appearances": top_appearances,
        "top_individual_appearances": top_individual_appearances,
        "top_writers": top_writers,
        "top_artists": top_artists,
        "top_years": top_years
    }

    return data


def draw_plots(data):

    for title in data:

        # Barplot
        sns.set(rc={"figure.figsize":(20,8.27)})
        plot = sns.barplot(x = data[title].values, y = data[title].index, orient = "h").set(title = title.title().replace('_', ' '), xlabel = None, ylabel = None)
        plt.tight_layout()
        plt.savefig(f"report/{title}_bar_plot.png")

        plt.figure(clear=True)

        # Pie chart
        labels = data[title].index
        sizes = data[title].values / data[title].values.sum() * 100
        plt.pie(sizes, textprops = {"color":"w"})
        labels = [f"{l} - {s:0.1f}%" for l, s in zip(labels, sizes)]
        plt.legend(labels = labels, bbox_to_anchor = (1.6,1), loc = "best")
        plt.title(title.title().replace('_', ' '))
        plt.tight_layout()
        plt.savefig(f"report/{title}_pie_chart.png")

        plt.figure(clear=True)


if __name__ == "__main__":
    main()
