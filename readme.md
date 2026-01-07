# Favorite Links

* **Author**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Creation Date**: 04/11/2024
* **License**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introduction

The **FavoriteLinks** add-on is a tool to manage your favorite links in an organized and efficient way. It allows you to save, edit, and remove links in a categorized list, offering an intuitive interface with features such as adding new links, renaming titles, removing unwanted entries, and managing categories. In addition, the add-on allows importing bookmarks directly from HTML files exported by browsers.

When opening the add-on, you get quick access to your links and can open them directly in the default browser. There is now also support for opening links in a secondary browser, in case you need more flexibility.

## Installation

Follow the steps below to install the **FavoriteLinks** add-on in NVDA:

1. In NVDA, open the **Tools** menu and select **Add-ons Store**.
2. In the **Available Add-ons** tab, navigate to the **Search** field.
3. Search for "favoriteLinks". In the results, press **Enter** or **Apply**, and then choose **Install**.
4. Restart NVDA to apply the changes.

## Configuration

You have full control over where your links are saved and which browser opens them.

1. Access the NVDA menu: `NVDA+N` > *Preferences* > *Settings*.
2. In the list of categories, select **Favorite Links**.

You can choose a custom location to save the links file using the **"Select or add a directory"** button (`Alt+S`).

To define a secondary browser, which can be either installed or portable:

1. Navigate with `Tab` to the **Browser path** field.
2. Use the **"Select browser path"** button (`Alt+N`) to add the executable of the desired browser.

## Usage

### Accessing the Add-on

* Press `Alt+Windows+K`.
* Or access via `NVDA+N` > *Tools* > *Favorite Links*.

### Main Interface

The main interface consists of two main fields, which can be navigated using the `Tab` key:

1. **Category**: A combo box with the existing categories.
2. **Links List**: A list that shows the links associated with the selected category.

Use the **context menu** (applications key) in any of these fields to access additional options.

### Available Actions

#### In the Categories Combo Box

* **Add Category**: Creates a new category.
* **Edit Category**: Renames the selected category.
* **Remove Category**: Deletes the category and all its links.
* **Export Links**: Saves all links and categories to a `.json` file.
* **Import Links**: Loads links and categories from a `.json` file.

#### In the Links List

* **Open Link**: Opens the link in the browser you configured.
    > **Note**: It is necessary to configure the secondary browser beforehand in the settings.
* **Add Link**: Allows inserting a new URL. The title will be obtained automatically, but you can enter it manually if the retrieval fails.
* **Edit Link**: Modifies the title and URL of an existing link.
* **Remove Link**: Deletes the selected link.
* **Export Links** / **Import Links**: Same as the category options.
* **Import HTML Bookmarks**: Imports links from a `.html` file exported by browsers.
* **Sort Links**: Organizes the links of the current category in alphabetical order.

### Import HTML Bookmarks

FavoriteLinks also allows importing bookmarks directly from HTML files, such as those exported by browsers (Chrome, Firefox, Edge, among others).

This feature is useful for migrating your existing bookmarks to the add-on quickly and in an organized way.

#### How to import bookmarks from an HTML file

1. Open the **Favorite Links** add-on.
2. Access the context menu in the **Categories Combo Box** or use the option available in the main menu.
3. Select **Import HTML bookmarks**.
4. Choose the `.html` file exported from your browser.
5. Wait for the links to be processed.

During the import:

* Progress is displayed in a progress bar.
* You can **cancel the operation at any time**.
* NVDA remains responsive throughout the entire process.

#### Organization of imported links

* Imported links are automatically added to the JSON file configured in the add-on preferences.
* By default, bookmarks are inserted into the **“Imported Bookmarks”** category.
* Duplicate links (with the same URL) are not added again.

At the end of the import, a confirmation message is displayed and the add-on interface is updated automatically.

### Shortcuts

| Function | Shortcut |
| :--- | :--- |
| Open Link | `Alt+B` or `Enter` (in the links list) |
| Add Link | `Alt+A` |
| Add Category | `Alt+D` |
| Edit Link | `Alt+E` or `F2` |
| Delete Link | `Alt+L` or `Del` |
| Save URL of the current page | `Shift+Control+D` |
| Show URL of the current page | `Windows+Control+P` Pressing twice copies the URL to the clipboard. |
| Exit | `Alt+S`, `Esc` or `Alt+F4` |

## "Add New Link" Dialog

1. **Category**: Select the desired category.
2. **URL**: Paste or type the link address.
    > If you have already copied a URL, it will be pasted automatically.
3. **OK (`Alt+O`)**: Adds the link.
    > The title will be fetched automatically. If the retrieval fails, you will be able to enter it manually.
4. **Cancel (`Alt+C`)**: Closes the dialog. `Esc` or `Alt+F4` also work.

## "Edit Link" Dialog

1. **Category**: When changing the category here, the link will be moved to the new category.
2. **Title**: Edit the link title.
3. **URL**: Change the link address.
4. **OK (`Alt+O`)**: Saves the changes.
5. **Cancel (`Alt+C`)**: Closes without saving. `Esc` or `Alt+F4` also work.

## Acknowledgements

Special thanks to **Rue Fontes** and **Ângelo Abrantes** for the tests carried out and for the valuable suggestions that significantly contributed to improving this project.

I also thank **Abel Passos** for the contribution with the functionality to import bookmarks from HTML files.

The FavoriteLinks add-on was developed with the assistance of **ChatGPT** and **Google Gemini**, used for creating functions, optimizing and refactoring the code, and improving the documentation.

## 🌍 Translators

* 🇸🇦 **Arabic** — Ahmed Bakr
* 🇧🇷 **Portuguese (Brazil)** — Edilberto Fonseca
* 🇵🇹 **Portuguese (Portugal)** — Edilberto Fonseca
* 🇷🇺 **Russian (Russia)** — Valentin Kupriyanov
* 🇹🇷 **Turkish (Turkey)** — Umut KORKMAZ
* 🇺🇦 **Ukrainian (Ukraine)** — Heorhii Halas
