import requests, bs4, sys, json, os

BASE_URL = "https://inducks.org/"


def main ():
    username = input("Enter your Inducks username: ")
    collection_url = BASE_URL + f"browsecollec.php?user={username}&pg=0"
    issues = get_issues(collection_url)
    stories = get_stories(issues)
    info = get_info(stories)
    dump(username, info)
    print("Done.")


def get_issues(url):
    res = requests.get(url)
    if "This user has not made his collection public." in res.text:
        sys.exit("Could not find your collection. Make sure that its visibility is set to public and that you have typed your username correctly.")
    print("Getting issues...")
    issues = []
    while True:
        soup = bs4.BeautifulSoup(res.text, "lxml")
        issues_elems = soup.select("a[href^='issue']")
        if not issues_elems:
            break
        for issue_elem in issues_elems:
            issue_url = BASE_URL + issue_elem.attrs["href"]
            issues.append(issue_url)
        url = url.rsplit("=", 1)[0] + "=" + str(int(url.rsplit("=", 1)[1]) + 1)
        res = requests.get(url)
    return issues


def get_stories(issues):
    print("Getting stories...")
    stories = []
    for issue in issues:
        res = requests.get(issue)
        soup = bs4.BeautifulSoup(res.text, "lxml")
        stories_elems = soup.select("tr.normal a[href^='story']")
        for story_elem in stories_elems:
            story_url = BASE_URL + story_elem.attrs["href"]
            stories.append(story_url)
    stories = list(dict.fromkeys(stories))  # remove duplicates
    return stories


def get_info(stories):
    print("Getting info...")
    info = []
    for story in stories:
        res = requests.get(story)
        soup = bs4.BeautifulSoup(res.text, "lxml")
        title = get_title(soup)
        pages = get_pages(soup)
        appearances = get_appearances(soup)
        writing = get_writing(soup)
        art = get_art(soup)
        date = get_date(soup)
        story_dict = {
            "url": story,
            "title": title,
            "pages": pages,
            "appearances": appearances,
            "writing": writing,
            "art": art,
            "date": date
        } 
        info.append(story_dict)
    return info


def get_title(soup):
    try:
        title = soup.select("i")[0].getText()
    except IndexError:
        title = soup.select("h1")[0].getText()
    return title


def get_pages(soup):
    dts = soup.select("dt")
    for dt in dts:
        if dt.getText() == "Pages":
            dd = dt.find_all_next("dd")[0]
            pages = dd.getText()
            return pages


def get_appearances(soup):
    dts = soup.select("dt")
    for dt in dts:
        if dt.getText() == "Appearances":
            dd = dt.find_all_next("dd")[0]
            appearances = []
            for elem in dd.children:
                try:
                    if elem.attrs["href"]:
                        if elem.getText() != "picture":
                            appearances.append(elem.getText())
                except (AttributeError, KeyError):
                    continue
            appearances = ', '.join(appearances)
            return appearances


def get_writing(soup):
    dts = soup.select("dt")
    for dt in dts:
        if dt.getText() == "Writing":
            dd = dt.find_all_next("dd")[0]
            writing = []
            for elem in dd.children:
                try:
                    if elem.attrs["href"]:
                        writing.append(elem.getText())
                except (AttributeError, KeyError):
                    continue
            writing = ', '.join(writing)
            return writing


def get_art(soup):
    dts = soup.select("dt")
    for dt in dts:
        if dt.getText() == "Art (pencil and ink)" or dt.getText() == "Pencils":
            dd = dt.find_all_next("dd")[0]
            art = []
            for elem in dd.children:
                try:
                    if elem.attrs["href"]:
                        art.append(elem.getText())
                except (AttributeError, KeyError):
                    continue
            art = ', '.join(art)
            return art


def get_date(soup):
    dts = soup.select("dt")
    for dt in dts:
        if dt.getText() == "Date of first publication":
            try:
                dd = dt.find_all_next("dd")[0]
            except IndexError:
                return None
            try:
                date = dd.findChildren("time")[0].attrs["datetime"]
            except IndexError:  
                date = dd.findChildren("a")[0].getText()
            
            return date
        

def dump(username, info):
    print("Dumping info...")
    path = os.path.join(os.getcwd(), "report", username.lower().replace(" ", "_"))
    os.makedirs(path)
    file = os.path.join(path, "collection.json")
    with open(file, "w", encoding="utf-8") as output:
        json.dump(info, output)


if __name__ == "__main__":
    main()
