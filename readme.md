# Favorite Links

* **Author**: Edilberto Fonseca ([edilberto.fonseca@outlook.com](mailto:edilberto.fonseca@outlook.com))
* **Creation Date**: 04/11/2024
* **License**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## 📌 Introduction

The **FavoriteLinks** add-on is a tool that allows you to manage your favorite links in an organized and efficient way. With it, you can save, edit, and remove links in a categorized list. Its intuitive interface provides full functionality such as adding new links, editing titles, removing unwanted entries, and managing categories.

When you open the add-on, you get quick access to your favorite links and can open any selected link directly in your default browser.

> **Note**: The FavoriteLinks add-on was developed with the help of ChatGPT, used both for creating some functions and for code organization and optimization.

## 💾 Installation

Follow the steps below to install the **FavoriteLinks** add-on in NVDA:

1. **Download the installation file**: You can get it from the NVDA Add-on Store.

   > **Note**: If downloaded from the store, installation will be automatic. Otherwise, follow the next steps.

2. **Install the add-on**: Press `Enter` on the downloaded `.nvda-addon` file.

3. **Follow the on-screen instructions**: Complete the installation as directed.

4. **Restart NVDA**: Restarting is necessary to activate the add-on.

5. **Verify installation**: Press `NVDA+N`, go to *Tools*, and check if **Favorite Links** is listed.

## ⚙️ Configuration

You can choose a custom location to save your links file:

1. Open the NVDA menu: `NVDA+N` > *Preferences* > *Settings*.
2. From the category list, select **Favorite Links**.
3. Click the **"Select or add a directory"** button to define a new save folder.

## 🚀 Usage

### Accessing the Add-on

* Press `Alt+Windows+K`, or
* Go to `NVDA+N` > *Tools* > *Favorite Links*

### Main Interface

The main interface has two key fields:

1. **Category**: A combo box with the existing categories.
2. **Link List**: Displays the links associated with the selected category.

### Available Actions

Use the **context menu** (application key) while focused on one of the lists to access more options.

#### Category Options

* **Add Category**: Creates a new category.
* **Edit Category**: Renames the selected category.
* **Remove Category**: Deletes the category and its associated links.
* **Export Links**: Saves links and categories to a `.json` file.
* **Import Links**: Loads links and categories from a `.json` file.

#### Link List Options

* **Open Link**: Opens the link in the default browser.

   > Pressing `Enter` also opens the selected link.

* **Add Link**: Allows you to insert a new URL and assign a category.

   > The title is retrieved automatically. If it can't be retrieved, you can enter it manually.

* **Edit Link**: Edits the title and URL of an existing link.

* **Remove Link**: Deletes the selected link.

* **Export/Import Links**: Same as in the category section.

* **Sort Links**: Sorts the links alphabetically.

### ⌨️ Shortcuts

The following shortcuts are available:

| Action               | Shortcut                   |
| -------------------- | -------------------------- |
| Open Link            | `Alt+B`                    |
| Add Link             | `Alt+A`                    |
| Edit Link            | `Alt+E` or `F2`            |
| Delete Link          | `Alt+L` or `Del`           |
| Add Category         | `Alt+D`                    |
| Exit                 | `Alt+S`, `Esc`, or `Alt+F4`|

## ➕ "Add New Link" Dialog

1. **Category**: Select the desired category.
2. **URL**: Paste or type the link address.

   > If a URL is already copied to the clipboard, it will be automatically inserted.
3. **OK (`Alt+O`)**: Adds the link.

   > The title is retrieved automatically. If it can't be retrieved, you can enter it manually.
4. **Cancel (`Alt+C`)**: Closes the dialog (`Esc` or `Alt+F4` also work).

## 📝 "Edit Link" Dialog

1. **Category**: Changing the category will move the link to the new category.
2. **Title**: Edit the link title.
3. **URL**: Edit the link address.
4. **OK (`Alt+O`)**: Saves the changes.
5. **Cancel (`Alt+C`)**: Closes without saving (`Esc` or `Alt+F4` also work).

## 🙏 Acknowledgments

Special thanks to **Rue Fontes** and **Ângelo Abrantes** for the tests and valuable suggestions that significantly improved this project.

Also, thank you to **Marlon Brandão de Sousa** for generously sharing his workflow, which was crucial for ensuring the project's efficiency and quality.

## 🌍 Translators

* 🇸🇦 **Arabic** — Ahmed Bakr
* 🇧🇷 **Portuguese (Brazil)** — Edilberto Fonseca
* 🇵🇹 **Portuguese (Portugal)** — Edilberto Fonseca
* 🇷🇺 **Russian (Russia)** — Valentin Kupriyanov
* 🇹🇷 **Turkish (Turkey)** — Umut KORKMAZ
* 🇺🇦 **Ukrainian (Ukraine)** — Heorhii Halas
