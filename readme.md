# Favorite Links

* **Author**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Date of Creation**: 04/11/2024
* **License**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introduction

The **FavoriteLinks** add-on is a tool for managing your favorite links in an organized and efficient way. It allows you to save, edit, and remove links in a categorized list, offering an intuitive interface with features such as adding new links, renaming titles, removing unwanted entries, and managing categories.

When you open the add-on, you have quick access to your favorite links and can open them directly in the default browser. Now, there is also support for opening links in a secondary browser, should you need more flexibility.

## Installation

Follow the steps below to install the **FavoriteLinks** add-on on NVDA:

1. In NVDA, open the **Tools** menu and select the **Add-on Store**.
2. In the **Available Add-ons** tab, navigate to the **Search** field.
3. Search for "favoriteLinks". In the results, press **Enter** or **Apply**, and then choose **Install**.
4. Restart NVDA to apply the changes.

## Configuration

You have full control over where your links are saved and the browser that opens them.

1. Access the NVDA menu: `NVDA+N` > *Preferences* > *Settings*.
2. In the categories list, select **Favorite Links**.

You can choose a custom location to save the links file using the **"Select or add a directory"** button (`Alt+S`).

To set a secondary browser, which can be either an installed or a portable one:

1. Navigate with the `Tab` key to the **Browser Path** field.
2. Use the **"Select browser path"** button (`Alt+N`) to add the executable of the desired browser.

## Usage

### Accessing the Add-on

* Press `Alt+Windows+K`.
* Or access it via `NVDA+N` > *Tools* > *Favorite Links*.

### Main Interface

The main interface consists of two primary fields, which can be navigated using the `Tab` key:

1. **Category**: A selection box with existing categories.
2. **Links List**: A list that shows the links associated with the selected category.

Use the **context menu** (applications key) in either of these fields to access additional options.

### Available Actions

#### In the Categories Box

* **Add Category**: Creates a new category.
* **Edit Category**: Renames the selected category.
* **Remove Category**: Deletes the category and all its links.
* **Export Links**: Saves all links and categories to a `.json` file.
* **Import Links**: Loads links and categories from a `.json` file.

#### In the Links List

*** Open link **: Open the link to the browser you configured.
    > **Note**: You must configure the secondary browser beforehand in the settings.

* **Add Link**: Allows you to insert a new URL. The title will be obtained automatically, but you can enter it manually if the search fails.
* **Edit Link**: Modifies the title and URL of an existing link.
* **Remove Link**: Deletes the selected link.
* **Export Links** / **Import Links**: Same as the category options.
* **Sort Links**: Organizes the links in the current category alphabetically.

### Shortcuts

| Function | Shortcut |
| :--- | :--- |
| Open Link | `Alt+B` or`Enter` (on the link list) |
| Add Link | `Alt+A` |
| Add Category | `Alt+D` |
| Edit Link | `Alt+E` or `F2` |
| Delete Link | `Alt+L` or `Del` |
| Save current page URL | `Shift+Control+D` |
| Show current page URL | `NVDA+Control+F4` |
| Exit | `Alt+S`, `Esc` or `Alt+F4` |

## "Add New Link" Dialog

1. **Category**: Select the desired category.
2. **URL**: Paste or type the link address.
    > If you have already copied a URL, it will be pasted automatically.
3. **OK (`Alt+O`)**: Adds the link.
    > The title will be fetched automatically. If the search fails, you can enter it manually.
4. **Cancel (`Alt+C`)**: Closes the dialog. `Esc` or `Alt+F4` also work.

## "Edit Link" Dialog

1. **Category**: By changing the category here, the link will be moved to the new one.
2. **Title**: Edit the link's title.
3. **URL**: Change the link's address.
4. **OK (`Alt+O`)**: Saves the changes.
5. **Cancel (`Alt+C`)**: Closes without saving. `Esc` or `Alt+F4` also work.

## Acknowledgments

A special thanks to **Rue Fontes** and **Ângelo Abrantes** for the testing and valuable suggestions that contributed significantly to the improvement of this project.

The FavoriteLinks add-on was developed with the help of ChatGPT and Google Gemini, which were used for creating functions, optimizing and refactoring the code, and improving the documentation.

## 🌍 Translators

* 🇸🇦 **Arabic** — Ahmed Bakr
* 🇧🇷 **Portuguese (Brazil)** — Edilberto Fonseca
* 🇵🇹 **Portuguese (Portugal)** — Edilberto Fonseca
* 🇷🇺 **Russian (Russia)** — Valentin Kupriyanov
* 🇹🇷 **Turkish (Turkey)** — Umut KORKMAZ
* 🇺🇦 **Ukrainian (Ukraine)** — Heorhii Halas
