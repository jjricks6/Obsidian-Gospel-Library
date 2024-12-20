import requests
import re
from bs4 import BeautifulSoup
import os
import json
from progressbar import progressbar

# Single chapter books don't need to be put in a book folder
SINGLE_CHAPTER_BOOKS = ["Enos", "Jarom", "Omni", "Words of Mormon", "4 Nephi", "Obadiah", "Philemon", "2 John", "3 John", "Jude", "Joseph Smith—Matthew", "Joseph Smith—History", "Articles of Faith", "Testimony of Three Witnesses", "Testimony of Eight Witnesses", "Title Page", "Title Page of the Book of Mormon", "Introduction", "Testimony of the Prophet Joseph Smith", "Brief Explanation about the Book of Mormon"]
BOOK_LOOKUP_TABLE = {
        # Old Testament
        "gen": "Genesis",
        "ex": "Exodus",
        "lev": "Leviticus",
        "num": "Numbers",
        "deut": "Deuteronomy",
        "josh": "Joshua",
        "judg": "Judges",
        "ruth": "Ruth",
        "1-sam": "1 Samuel",
        "2-sam": "2 Samuel",
        "1-kgs": "1 Kings",
        "2-kgs": "2 Kings",
        "1-chr": "1 Chronicles",
        "2-chr": "2 Chronicles",
        "ezra": "Ezra",
        "neh": "Nehemiah",
        "esth": "Esther",
        "job": "Job",
        "ps": "Psalms",
        "prov": "Proverbs",
        "eccl": "Ecclesiastes",
        "song": "Song of Solomon",
        "isa": "Isaiah",
        "jer": "Jeremiah",
        "lam": "Lamentations",
        "ezek": "Ezekiel",
        "dan": "Daniel",
        "hosea": "Hosea",
        "joel": "Joel",
        "amos": "Amos",
        "obad": "Obadiah",
        "jonah": "Jonah",
        "micah": "Micah",
        "nahum": "Nahum",
        "hab": "Habakkuk",
        "zeph": "Zephaniah",
        "hag": "Haggai",
        "zech": "Zechariah",
        "mal": "Malachi",
        # New Testament
        "matt": "Matthew",
        "mark": "Mark",
        "luke": "Luke",
        "john": "John",
        "acts": "Acts",
        "rom": "Romans",
        "1-cor": "1 Corinthians",
        "2-cor": "2 Corinthians",
        "gal": "Galations",
        "eph": "Ephesians",
        "philip": "Philippians",
        "col": "Colossians",
        "1-thes": "1 Thessalonians",
        "2-thes": "2 Thessalonians",
        "1-tim": "1 Timothy",
        "2-tim": "2 Timothy",
        "titus": "Titus",
        "philem": "Philemon",
        "heb": "Hebrews",
        "james": "James",
        "1-pet": "1 Peter",
        "2-pet": "2 Peter",
        "1-jn": "1 John",
        "2-jn": "2 John",
        "3-jn": "3 John",
        "jude": "Jude",
        "rev": "Revelation",
        # Book of Mormon
        "bofm-title": "Title Page of the Book of Mormon",
        "introduction": "Introduction",
        "three": "Testimony of Three Witnesses",
        "eight": "Testimony of Eight Witnesses",
        "js": "Testimony of the Prophet Joseph Smith",
        "explanation": "Breif Explanation about the Book of Mormon",
        "1-ne": "1 Nephi",
        "2-ne": "2 Nephi",
        "jacob": "Jacob",
        "enos": "Enos",
        "jarom": "Jarom",
        "omni": "Omni",
        "w-of-m": "Words of Mormon",
        "mosiah": "Mosiah",
        "alma": "Alma",
        "hel": "Helaman",
        "3-ne": "3 Nephi",
        "4-ne": "4 Nephi",
        "morm": "Mormon",
        "ether": "Ether",
        "moro": "Moroni",
        "pronunciation": "Book of Mormon Pronunciation Guide",
        "reference": "Reference Guide to the Book of Mormon",
        # Doctrine and Covenants
        "dc": "Doctrine and Covenants",
        "od": "Official Declaration",
        # Pearl of Great Price
        "moses": "Moses",
        "abr": "Abraham",
        "js-m": "Joseph Smith—Matthew",
        "js-h": "Joseph Smith—History",
        "a-of-f": "Articles of Faith",
        # Study Helps
        "tg": "Topical Guide",
        "bd": "Bible Dictionary",
        "gs": "Guide to the Scriptures",
        "triple-index": "Index to the Triple Combination",
        "jst-gen": "JST, Genesis",
        "jst-ex": "JST, Exodus",
        "jst-deut": "JST, Deuteronomy",
        "jst-1-sam": "JST, 1 Samuel",
        "jst-2-sam": "JST, 2 Samuel",
        "jst-1-chr": "JST, 1 Chronicles",
        "jst-2-chr": "JST, 2 Chronicles",
        "jst-ps": "JST, Psalms",
        "jst-isa": "JST, Isaiah",
        "jst-jer": "JST, Jeremiah",
        "jst-amos": "JST, Amos",
        "jst-matt": "JST, Matthew",
        "jst-mark": "JST, Mark",
        "jst-luke": "JST, Luke",
        "jst-john": "JST, John",
        "jst-acts": "JST, Acts",
        "jst-rom": "JST, Romans",
        "jst-1-cor": "JST, 1 Corinthians",
        "jst-2-cor": "JST, 2 Corinthians",
        "jst-gal": "JST, Galatians",
        "jst-eph": "JST, Ephesians",
        "jst-col": "JST, Colossians",
        "jst-1-thes": "JST, 1 Thessalonians",
        "jst-2-thes": "JST, 2 Thessalonians",
        "jst-1-tim": "JST, 1 Timothy",
        "jst-heb": "JST, Hebrews",
        "jst-james": "JST, James",
        "jst-1-pet": "JST, 1 Peter",
        "jst-2-pet": "JST, 2 Peter",
        "jst-1-jn": "JST, 1 John",
        "jst-rev": "JST, Revelation"
        }
CHAPTER_COUNTS = {
        "ot": {
            "gen": "50",
            "ex": "40",
            "lev": "27",
            "num": "36",
            "deut": "34",
            "josh": "24",
            "judg": "21",
            "ruth": "4",
            "1-sam": "31",
            "2-sam": "24",
            "1-kgs": "22",
            "2-kgs": "25",
            "1-chr": "29",
            "2-chr": "36",
            "ezra": "10",
            "neh": "13",
            "esth": "10",
            "job": "42",
            "ps": "150",
            "prov": "31",
            "eccl": "12",
            "song": "8",
            "isa": "66",
            "jer": "52",
            "lam": "5",
            "ezek": "48",
            "dan": "12",
            "hosea": "14",
            "joel": "3",
            "amos": "9",
            "obad": "1",
            "jonah": "4",
            "micah": "7",
            "nahum": "3",
            "hab": "3",
            "zeph": "3",
            "hag": "2",
            "zech": "14",
            "mal": "4"
        },
        "nt": {
            "matt": "28",
            "mark": "16",
            "luke": "24",
            "john": "21",
            "acts": "28",
            "rom": "16",
            "1-cor": "16",
            "2-cor": "13",
            "gal": "6",
            "eph": "6",
            "philip": "4",
            "col": "4",
            "1-thes": "5",
            "2-thes": "3",
            "1-tim": "6",
            "2-tim": "4",
            "titus": "3",
            "philem": "1",
            "heb": "13",
            "james": "5",
            "1-pet": "5",
            "2-pet": "3",
            "1-jn": "5",
            "2-jn": "1",
            "3-jn": "1",
            "jude": "1",
            "rev": "22"
        },
        "bofm": {
            "1-ne": "22",
            "2-ne": "33",
            "jacob": "7",
            "enos": "1",
            "jarom": "1",
            "omni": "1",
            "w-of-m": "1",
            "mosiah": "29",
            "alma": "63",
            "hel": "16",
            "3-ne": "30",
            "4-ne": "1",
            "morm": "9",
            "ether": "15",
            "moro": "10"
        },
        "dc-testament": {
            "dc": "138",
            "od": "2"
        },
        "pgp": {
            "moses": "8",
            "abr": "5", 
            "js-m": "1",
            "js-h": "1",
            "a-of-f": "1"
        },
        "jst": {
            "jst-gen": {
                "1-8": "JST, Genesis 1-8",
                "9": "JST, Genesis 9",
                "14": "JST, Genesis 14",
                "15": "JST, Genesis 15",
                "17": "JST, Genesis 17",
                "19": "JST, Genesis 19",
                "21": "JST, Genesis 21",
                "48": "JST, Genesis 48",
                "50": "JST, Genesis 50"
            },
            "jst-ex": {
                "4": "JST, Exodus 4",
                "18": "JST, Exodus 18",
                "22": "JST, Exodus 22",
                "32": "JST, Exodus 32",
                "33": "JST, Exodus 33",
                "34": "JST, Exodus 34"
            },
            "jst-deut": {
                "10": "JST, Deuteronomy"
            },
            "jst-1-sam": {
                "16": "JST, 1 Samuel"
            },
            "jst-2-sam": {
                "12": "JST, 2 Samuel"
            },
            "jst-1-chr": {
                "21": "JST, 1 Chronicles"
            },
            "jst-2-chr": {
                "18": "JST, 2 Chronicles"
            },
            "jst-ps": {
                "11": "JST, Psalm 11",
                "14": "JST, Psalm 14",
                "24": "JST, Psalm 24",
                "109": "JST, Psalm 109"
            },
            "jst-isa": {
                "29": "JST, Isaiah 29",
                "42": "JST, Isaiah 42"
            },
            "jst-jer": {
                "26": "JST, Jeremiah"
            },
            "jst-amos": {
                "7": "JST, Amos"
            },
            "jst-matt": {
                "3": "JST, Matthew 3",
                "4": "JST, Matthew 4",
                "5": "JST, Matthew 5",
                "6": "JST, Matthew 6",
                "7": "JST, Matthew 7",
                "9": "JST, Matthew 9",
                "11": "JST, Matthew 11",
                "12": "JST, Matthew 12",
                "13": "JST, Matthew 13",
                "16": "JST, Matthew 16",
                "17": "JST, Matthew 17",
                "18": "JST, Matthew 18",
                "19": "JST, Matthew 19",
                "21": "JST, Matthew 21",
                "23": "JST, Matthew 23",
                "26": "JST, Matthew 26",
                "27": "JST, Matthew 27"
            },
            "jst-mark": {
                "2": "JST, Mark 2",
                "3": "JST, Mark 3",
                "7": "JST, Mark 7",
                "8": "JST, Mark 8",
                "9": "JST, Mark 9",
                "12": "JST, Mark 12",
                "14": "JST, Mark 14",
                "16": "JST, Mark 16"
            },
            "jst-luke": {
                "1": "JST, Luke 1",
                "2": "JST, Luke 2",
                "3": "JST, Luke 3",
                "6": "JST, Luke 6",
                "9": "JST, Luke 9",
                "11": "JST, Luke 12",
                "14": "JST, Luke 14",
                "16": "JST, Luke 16",
                "17": "JST, Luke 17",
                "18": "JST, Luke 18",
                "21": "JST, Luke 21",
                "23": "JST, Luke 23",
                "24": "JST, Luke 24"
            },
            "jst-john": {
                "1": "JST, John 1",
                "4": "JST, John 4",
                "6": "JST, John 6",
                "13": "JST, John 13",
                "14": "JST, John 14"
            },
            "jst-acts": {
                "9": "JST, Acts 9",
                "22": "JST, Acts 22"
            },
            "jst-rom": {
                "3": "JST, Romans 3",
                "4": "JST, Romans 4",
                "7": "JST, Romans 7",
                "8": "JST, Romans 8",
                "13": "JST, Romans 13"
            },
            "jst-1-cor": {
                "7": "JST, 1 Corinthians 7",
                "15": "JST, 1 Corinthians 15"
            },
            "jst-2-cor": {
                "5": "JST, 2 Corinthians"
            },
            "jst-gal": {
                "3": "JST, Galations"
            },
            "jst-eph": {
                "4": "JST, Ephesians"
            },
            "jst-col": {
                "2": "JST, Colossians"
            },
            "jst-1-thes": {
                "4": "JST, 1 Thessalonians"
            },
            "jst-2-thes": {
                "2": "JST, 2 Thessalonians"
            },
            "jst-1-tim": {
                "2": "JST, 1 Timothy 2",
                "3": "JST, 1 Timothy 3",
                "6": "JST, 1 Timothy 6"
            },
            "jst-heb": {
                "1": "JST, Hebrews 1",
                "4": "JST, Hebrews 4",
                "6": "JST, Hebrews 6",
                "7": "JST, Hebrews 7",
                "11": "JST, Hebrews 11"
            },
            "jst-james": {
                "1": "JST, James 1",
                "2": "JST, James 2"
            },
            "jst-1-pet": {
                "3": "JST, 1 Peter 3",
                "4": "JST, 1 Peter 4"
            },
            "jst-2-pet": {
                "3": "JST, 2 Peter"
            },
            "jst-1-jn": {
                "2": "JST, 1 John 2",
                "3": "JST, 1 John 3",
                "4": "JST, 1 John 4"
            },
            "jst-rev": {
                "1": "JST, Revelation 1",
                "2": "JST, Revelation 2",
                "5": "JST, Revelation 5",
                "12": "JST, Revelation 12",
                "19": "JST, Revelation 19"
            }
        }
    }
COLLECTION_LOOKUP_TABLE = {
    "ot": "Old Testament",
    "nt": "New Testament",
    "bofm": "Book of Mormon",
    "dc-testament": "Doctrine and Covenants",
    "pgp": "Pearl of Great Price",
    "gs": "Study Helps/Guide to the Scriptures",
    "tg": "Study Helps/Topical Guide",
    "bd": "Study Helps/Bible Dictionary",
    "triple-index": "Study Helps/Index to the Triple Combination",
    "jst": "Study Helps/Joseph Smith Translation Appendix",
    "bible-chron": "Study Helps/Bible Chronology",
    "harmony": "Study Helps/Harmony of the Gospels"
}

with open("study-helps-lookup-files/bible_dictionary.json", "r") as json_file:
    bible_dictionary_entries = json.load(json_file)

with open("study-helps-lookup-files/guide_to_the_scriptures.json", "r") as json_file:
    guide_to_the_scriptures_entries = json.load(json_file)

with open("study-helps-lookup-files/index_to_the_triple_combination.json", "r") as json_file:
    index_to_the_triple_combination_entries = json.load(json_file)

with open("study-helps-lookup-files/topical_guide.json", "r") as json_file:
    topical_guide_entries = json.load(json_file)

# Clean odd characters in the text
def clean_text(text):
    text = text.replace("Â ", " ").replace("â", "—").replace("â", "'").replace("&amp;", "&").replace("â", "-").replace("â", '"').replace("â", '"').replace("Â¶", "¶").replace("â¦", "...").replace("Ã¦", "æ")
    return text

# Formats intra-document links within the text
def format_links(text, links):
    # Track the processed text as a list of segments
    processed_text = text
    offset = 0  # Tracks shifts caused by replacements
    
    for link in links:
        href = link["href"]
        marker = link.get_text()
        note_id = re.sub(r"(note)(\d+)", r"\1-\2", link["data-scroll-id"])
        
        # Find the next occurrence of the marker from the current offset
        match_index = processed_text.find(marker, offset)
        
        # If the marker is found, replace it
        if match_index != -1:
            replacement = f"[[#^{note_id}|{marker}]]"
            processed_text = (
                processed_text[:match_index]  # Text before the match
                + replacement                 # Replacement text
                + processed_text[match_index + len(marker):]  # Text after the match
            )
            
            # Update the offset to prevent replacing nested/modified parts
            offset = match_index + len(replacement)
    
    return processed_text

# Creates extra-document links between notes in a standardized fashion
def create_obsidian_link(text, link):
    collection = ""
    book = ""
    chapter = ""
    verse = ""
    entry = ""
    obsidian_link = ["[["]
    output_link = ""

    href = link["href"]
    if len(href.split("/")) >= 4:
        collection_code = href.split("/")[3].split("?")[0]
        collection = COLLECTION_LOOKUP_TABLE[collection_code]
        obsidian_link.append(f"{collection}")
    if collection_code in ["gs", "tg", "bd", "triple-index"]:
        if len(href.split("/")) >= 5:
            entry_code = href.split("/")[4].split("?")[0]
            if collection_code == "gs":
                try:
                    entry = guide_to_the_scriptures_entries[entry_code]
                except Exception as e:
                    print(f"Can't find {entry_code}")
            elif collection_code == "tg":
                try:
                    entry = topical_guide_entries[entry_code]
                except Exception as e:
                    print(f"Can't find {entry_code}")
            elif collection_code == "bd":
                try:
                    entry = bible_dictionary_entries[entry_code]
                except Exception as e:
                    print(f"Can't find {entry_code}")
            elif collection_code == "triple-index":
                try:
                    entry = index_to_the_triple_combination_entries[entry_code]
                except Exception as e:
                    print(f"Can't find {entry_code}")
            obsidian_link.append(f"/{entry}")
        
    else:
        if len(href.split("/")) >= 5:
            book_code = href.split("/")[4].split("?")[0]
            book = BOOK_LOOKUP_TABLE[book_code]
            obsidian_link.append(f"/{book}")
        if book not in SINGLE_CHAPTER_BOOKS and len(href.split("/")) >= 6:
            chapter = href.split("/")[5].split("?")[0].split(".")[0]
            obsidian_link.append(f"/{book} {chapter}")
        if len(href.split("#p")) >= 2:
            verse = href.split("#p")[1]
            obsidian_link.append(f"#^verse-{verse}")

    obsidian_link.append(f"|{text}]]")
    output_link = output_link.join(obsidian_link)

    return output_link

# Scrape the webpage
def scrape(collection, book, chapter):
    url = f'https://www.churchofjesuschrist.org/study/scriptures/{collection}/{book}/{chapter}?lang=eng'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Uncomment for dubugging
        # with open('scraped_page.html', 'w', encoding='utf-8') as file:
        #     file.write(str(soup))
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return soup

def generate_markdown(collection, book, chapter):               
    soup = scrape(collection, book, chapter)
    markdown_output = []

    title = soup.find("h1", id="title1").get_text() if soup.find("h1", id="title1") else ""
    subtitle = soup.find("p", id="subtitle1").get_text() if soup.find("p", id="subtitle1") else ""
    if title:
        markdown_output.append(f"# {clean_text(title)}")
    if subtitle:
        markdown_output.append(f"## {clean_text(subtitle)}")

    intro = soup.find("p", id="intro1").get_text() if soup.find("p", id="intro1") else ""
    if intro:
        markdown_output.append(f"*{clean_text(intro)}*")

    chapter_heading = soup.find("p", id="title_number1").get_text(strip=True) if soup.find("p", id="title_number1") else ""
    if chapter_heading:
        markdown_output.append(f"### {clean_text(chapter_heading)}")
    
    # Generate nav bar
    nav_bar = ""
    previous_chapter = soup.find("span", class_="traversalLink-JrW0G prevLink-c6tNM")
    if previous_chapter and previous_chapter.find("a"):
        previous_chapter_href = previous_chapter.find("a")
        previous_link = create_obsidian_link("Previous Entry", previous_chapter_href)
    else:
        previous_link = None

    next_chapter = soup.find("span", class_="traversalLink-JrW0G nextLink-otfJl")
    if next_chapter and next_chapter.find("a"):
        next_chapter_href = next_chapter.find("a")
        next_link = create_obsidian_link("Next Entry", next_chapter_href)
    else:
        next_link = None
    
    if previous_link:
        nav_bar = nav_bar + f"{previous_link}"
        if next_link:
            nav_bar = nav_bar + "  ||  "
    if next_link:
        nav_bar = nav_bar + f"{next_link}"

    markdown_output.append(nav_bar)
    study_summary = soup.find("p", id="study_summary1").get_text() if soup.find("p", id="study_summary1") else ""
    if study_summary:
        markdown_output.append(f"*{clean_text(study_summary)}*")

    # Extract verses
    verses = soup.find_all("p", class_="verse")
    for verse in verses:
        verse_number = verse.find("span", class_="verse-number").get_text(strip=True)
        verse.find("span", class_="verse-number").decompose()
        verse_text = verse.get_text()

        # Replace links with Obsidian-style links and handle spacing
        links = verse.find_all("a", class_="study-note-ref")
        verse_text = format_links(verse_text, links)
        verse_text.lstrip()
        
        markdown_output.append(f"**{verse_number}**  {clean_text(verse_text)} ^verse-{verse_number}")

    # Add footnotes
    markdown_output.append(f"\n---\n{nav_bar}\n")
    markdown_output.append("**Footnotes**\n")
    footnotes = soup.select("footer.study-notes ul.marker > li ul.marker > li")
    for footnote in footnotes:
        note_id = footnote.get("data-full-marker")
        if not note_id:
            continue  # Skip footnotes with no valid marker

        # Create link-style formatting for footnotes
        footnote_links = footnote.find_all("a", class_="scripture-ref")
        obsidian_links = []
        for link in footnote_links:
            obsidian_links.append(create_obsidian_link(clean_text(link.get_text()), link))
        translations = footnote.find_all("span", {"data-note-category": "trn"})
        for translation in translations:
            obsidian_links.append(clean_text(translation.get_text()))
        jsts = footnote.find_all("span", {"data-note-category": "jst"})
        for jst in jsts:
            obsidian_links.append(clean_text(jst.get_text()))
        ies = footnote.find_all("span", {"data-note-category": "ie"})
        for ie in ies:
            obsidian_links.append(clean_text(ie.get_text()))
        ors = footnote.find_all("span", {"data-note-category": "or"})
        for _or in ors:
            obsidian_links.append(clean_text(_or.get_text()))
        links_formatted = "; ".join(obsidian_links)
        markdown_output.append(f"{note_id}. {links_formatted} ^note-{note_id}")

    # Write Markdown to file
    markdown_result = "\n\n".join(markdown_output)
    
    book_name = BOOK_LOOKUP_TABLE[book]
    file_name = f"{book_name} {chapter}"
    collection_name = clean_text(soup.find("span", class_="bookTitle-XO2nM").get_text(strip=True))
    
    if collection_name == "Joseph Smith Translation Appendix":
        collection_name = "Study Helps/Joseph Smith Translation Appendix"
    
    if book_name in SINGLE_CHAPTER_BOOKS:
        output_path = f"{collection_name}/{book_name}.md"
    else:
        output_path = f"{collection_name}/{book_name}/{file_name}.md"
    
    # Create the directory and write the file
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(markdown_result)


if __name__ == '__main__':
    for collection, books in CHAPTER_COUNTS.items():
        for book, chapter_count in books.items():
            if collection != "jst":
                # For non-JST collections, chapter_count is a string representing the number of chapters
                for chapter in range(1, int(chapter_count) + 1):  # Chapters start from 1
                    generate_markdown(collection, book, chapter)
            else:
                # For the "jst" collection, chapter_count is a nested dictionary
                for chapter, description in chapter_count.items():
                    generate_markdown(collection, book, chapter)
