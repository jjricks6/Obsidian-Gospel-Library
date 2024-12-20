# Obsidian Gospel Library

## Overview
This project brings the [standard works](https://www.churchofjesuschrist.org/study/manual/gospel-topics/standard-works?lang=eng) of [The Church of Jesus Christ of Latter-day Saints](https://www.churchofjesuschrist.org/?lang=eng) into [Obsidian](https://obsidian.md/), a powerful note-taking platform. It offers an intuitive and dynamic way to study the scriptures, combining the complete standard works with preserved links, footnotes, and hover-over previews for a seamless study experience. 

## Key Features
- **Full Standard Works**: All 5 books of the standard works of The Church of Jesus Christ of Latter-day Saints have been translated into Obsidian Markdown format.
- **Study Helps**: The primary Study Help resources have also been translated, including the Bible Dictionary, Topical Guide, Guide to the Scriptures, Index to the Triple Combination, and Jospeh Smith Translation Appendix.
- **Preserved Links**: All links within the documents have been preserved. This includes footnote links within the same page, and links to other documents.
- **Easy Navigation**: Navigate between pages using Obsidian's file browser, open multiple pages using tabs, or navigate to the previosu or next entry in a collection using the navigation links at the top and bottom of each page.
- **Hover-over Previews**: Hover over any link to get an instant preview. Follow a trail of references without ever leaving the page!
- **Take Notes Your Way**: With Obsidian, you can write and format your notes however makes sense for you. You can type notes directly in line, write notes in your own handwriting, highlight text, or even link to your documents, like a study journal or personal talks.

## How to Install
1. [Download Obsidian](https://obsidian.md/download)
2. [Create an Obsidian Vault](https://help.obsidian.md/Getting+started/Create+a+vault)
3. Download the files from this repo
4. Move the desired folders **directly within the root of your Obsidian Vault**. Don't worry! Once they have been placed in root, they can be moved anywhere within your vault - this is to preserve the functionality of the links.

## How to Use
Exactly how you study the scriptures using Obsidain is up to you. I recommend installing any of the useful community plugins listed under `Suggested Plugins and Settings` section of this README. These plugins will enable additional customization options not native to Obsidian, such as colored highlight, colored text, or even inserting hand-written note sections.

Obsidian becomes powerful when you **link** connected ideas. I recommend you organize your notes by adding links between the scriptures and your personal note files. You might consider creating a "Study Journal" folder to contain your notes.

### Reading vs Editing
While reading an open file in Obsidian there are two modes you can switch beteen: Reading and Editing modes. You can switch between modes by clicking on the **pecil** or **book** icon in the top right corner of the open file. 

While in **Reading Mode** you will be able to:
- Hover over links to see a live preview
- Read the text without any markdown formatting to get in the way

However, while in Reading mode you will **not** be able to add text, edit text, or even highlight text in any way. To do that you will need to by in Editing mode.

While in **Editing Mode** you will be able to:
- Modify text
- Highlight text
- Add notes and links

The down side to editing mode is that you have to sort through all the markdown clutter (such as link formatting or CSS style tags) AND you can't preview links. You can however still click on the links to navigate to the linked document.

You can easily switch between the modes by clicking on the mode button in the top right corner of the document. Alternatively, you could open each mode side-by-side (For example, Editing can happen on the left pane, while reading happens on the right pane.)

## Important Note
While in Editing Mode at the end of each verse you will see `^verse-#`. These are called "blockIDs" which are required by Obsidian to link to a specific verse within a page. These need to come at the very end of a paragraph for them to work properly. This means that you can not add text directly *after* the blockID. Doing so will break any link that links to that specific verse. Instead, write your note *before* the blockID, or be sure to start a *new* paragraph for your note. (Writing a note on the immediate next line will include the line as a part of the paragraph, thus breaking the blockID link)

If you choose to use the Highlightr or Colored Text plugins (see Plugins below), this means that the blockID cannot be contained within the highlight or colored text. Doing so will break the verse link (due to the CSS tags). Be sure to end the highlight before the blockID starts.

While in **Reading Mode**, if you can see the blockID at the end of a verse (such as "...Christ should come all men must perish. ^verse-6") then you know the link is broken. Switch to Editing Mode and check for text that may be breaking the link. It is normal to see the blockID at the end of a verse in Editing mode, however. If you don't want to see these blockIDs (except while editing the verse), then follow the directions under the Suggested Plugins and Settings.

## Suggested Plugins and Settings
**Plugins**

To install Obsidian plugins, first go to Settings then select `Turn on community plugins`. Then select `Browse` to browse community plugins.
- **Multi-Color Highlighting**: Install the [Highlightr](https://github.com/chetachiezikeuzor/Highlightr-Plugin) plugin (by chetachi) from the community Plugins to enable the ability to highlight text with multiple colors. Simply highlight the text you wish to highlight, then right click and select Highlight, then select your color. You can also customize the highlight colors within the plugin settings page.
- **Colored Text**: Install the [Colored Text](https://github.com/erincayaz/obsidian-colored-text) plugin (by Erinc Ayaz) from the community plugins to change the color of text. This can be useful as a way of highlighting key words in a verse, or by differentiating your own personal notes written in-line.
- **Hand-Written Notes**: Install the [Ink](https://github.com/daledesilva/obsidian_ink) plugin (by Dale de Silva) to enable writing notes with a stylus (such as an Apple Pencil) between verses.
- **Properly-Ordered Files**: Install the [Custom File Explorer sorting](https://github.com/SebastianMC/obsidian-custom-sort) plugin (by SebastianMC) to enable custom sorting of the files in the file explorer. This will allow you to order the books in the proper order (rather than just alphabetical).

**Settings**
- If you would like the text to display with the same font as the Gospel Library, change the font in the settings under Appearance > Font > Text Font and set it to `Palatino` or `Palatio Linotype`. Change the font size to your preference.
- To hide BlockIDs while in Editing Mode you will need to add a custom CSS snipet to your Obsidian Vault. Go to Settings > Appearance then click "Open snippets folder". Move the `hide-block-ids.css` file from this repo into the folder. Click "Reload Snippets" and enable the `hide-block-ids` snippet. Now the blockID will only appear while editing the verse. Be sure not to modify the blockID or add text on the same line directly after the blockID, or else the blockID will break, and the verse will no longer be able to be linked.
- To remove "spelling errors" on old english words (such as "stirreth", or "sufficeth"), you can either diable spell checking entirely in the settings, or add each word as you encounter it to the dictionary. Do this by right clicking on the word and pushing "Add to dictionary". This will ignore the word from here on out.

## Future Additions

- **General Conference Talks**
- **Come, Follow Me 2025**

---

Created by Jordan Ricks

If you encounter any issues or have ideas for improvement, please share your feedback or contribute via the GitHub repository.

