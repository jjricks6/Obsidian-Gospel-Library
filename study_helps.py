import requests
import re
from bs4 import BeautifulSoup
import os
import json
from progressbar import progressbar

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
SINGLE_CHAPTER_BOOKS = ["Enos", "Jarom", "Omni", "Words of Mormon", "4 Nephi", "Obadiah", "Philemon", "2 John", "3 John", "Jude", "Joseph Smith—Matthew", "Joseph Smith—History", "Articles of Faith", "Testimony of Three Witnesses", "Testimony of Eight Witnesses", "Title Page", "Title Page of the Book of Mormon", "Introduction", "Testimony of the Prophet Joseph Smith", "Brief Explanation about the Book of Mormon"]


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
def scrape(collection, entry):
    url = f'https://www.churchofjesuschrist.org/study/scriptures/{collection}/{entry}?lang=eng'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Uncomment for debugging
        # with open('scraped_page.html', 'w', encoding='utf-8') as file:
        #     file.write(str(soup))
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return soup

def generate_markdown(collection, entry):
    try:
        soup = scrape(collection, entry)
    except Exception as e:
        print(e)
    markdown_output = []

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

    # Extract additional headings, paragraphs, and sections
    body = soup.find("div", class_="body-block")
    if body:
        for element in body.find_all(["h2", "h3", "p", "a"], recursive=True):
            if element.name == "h2":
                markdown_output.append(f"## {element.get_text(strip=True)}")
            elif element.name == "h3":
                markdown_output.append(f"### {element.get_text(strip=True)}")
            elif element.name == "p":
                entry_text = clean_text(element.get_text())
                links = element.find_all("a", class_="scripture-ref")

                offset = 0
                for link in links:
                    link_text = clean_text(link.get_text())
                    obsidian_link = create_obsidian_link(link_text, link)

                    # Find the next occurrence of the link text after the current offset
                    match_index = entry_text.find(link_text, offset)
                    if match_index != -1:
                        # Replace the matched text with the Obsidian link
                        entry_text = (
                            entry_text[:match_index] +
                            obsidian_link +
                            entry_text[match_index + len(link_text):]
                        )
                        # Update the offset to the end of the newly inserted link
                        offset = match_index + len(obsidian_link)
                
                markdown_output.append(f" {entry_text}")

    markdown_output.append(nav_bar)

    if collection == "bd":
        entry = bible_dictionary_entries[entry]
    elif collection == "gs":
        entry = guide_to_the_scriptures_entries[entry]
    elif collection == "tg":
        entry = topical_guide_entries[entry]
    elif collection == "triple-index":
        entry = index_to_the_triple_combination_entries[entry]

    # Save Markdown content to file
    output_path = f"{COLLECTION_LOOKUP_TABLE[collection]}/{entry}.md"
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Write Markdown to file
    markdown_result = "\n\n".join(markdown_output)
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(markdown_result)

if __name__ == '__main__':
    for entry in progressbar(bible_dictionary_entries, redirect_stdout=True):
        try:
            generate_markdown("bd", entry)
        except:
            pass
    for entry in progressbar(guide_to_the_scriptures_entries, redirect_stdout=True):
        try:
            generate_markdown("gs", entry)
        except:
            pass
    for entry in progressbar(index_to_the_triple_combination_entries, redirect_stdout=True):
        try:
            generate_markdown("triple-index", entry)
        except:
            pass
    for entry in progressbar(topical_guide_entries, redirect_stdout=True):
        try:
            generate_markdown("tg", entry)
        except:
            pass
    print('done')
