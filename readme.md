# Favorite Links

* **Author**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Creation Date**: 11/04/2024
* **License**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introduction

The **FavoriteLinks** add-on is a tool that allows you to manage favorite links in an organized and efficient manner. With it, you can save, edit, and remove links in a categorized list. Its intuitive interface offers comprehensive features, such as adding new links, editing titles, removing unwanted links, and managing categories. When you open the add-on, you have quick access to your favorite links and can open a selected link directly in your browser.

> Note: The FavoriteLinks add-on was developed with the help of ChatGPT for creating some functions and optimization; it was also used for code organization.

## Installation

Follow the instructions below to install the Favorite Links add-on in NVDA:

1. **Download the add-on installation file**: Obtain the file from the NVDA Add-ons Store.
   **Note**: If the add-on is downloaded from the store, installation will occur automatically. Otherwise, follow the instructions below.
2. **Install the add-on**: Press Enter on the downloaded add-on file.
3. **Follow the on-screen instructions**: Complete the installation as directed.
4. **Restart NVDA**: It is necessary to restart to activate the add-on.
5. **Check the installation**: Press `NVDA+N` to open the NVDA menu, go to "Tools," and check if Favorite Links is listed.

## Configuration

You can select a different location from the default one to save your link file. To do this, access the NVDA menu, go to Preferences, Settings, and under Settings, select the Favorite Links category. Then, choose a different folder using the "Select or add a directory" button.

## Usage

### Accessing the Add-on

Press `Alt+Windows+K` or use the NVDA menu `NVDA+N` > Tools > Favorite Links to open the add-on.

### Main Interface

The displayed dialog will have two main fields:

1. **Category**: A combo box where you can choose the desired category.
2. **Link List**: Here, the links corresponding to the selected category will be displayed.

### Available Actions

To access options for working with links and categories, you can use the NVDA Context Menu (application key).

### Category

When positioned in the category combo box, the following options are displayed:

* **Add Category**: Allows you to add a category to the list.
* **Edit Category**: Allows renaming an existing category.
* **Remove Category**: Allows you to delete a category and all links associated with it.
* **Export Links**: Allows exporting the saved links and categories to a json file.
* **Import Links**: Allows importing previously saved links and categories from a json file.

### Link List

When positioned in the link list, the following options are displayed:

* **Open Link**: Opens the selected link in the system's default browser.
  **Note**: Pressing Enter on the selected link opens it in the system's default browser.
* **Add Link**: Allows you to add a new link by providing its URL and category.
  **Note**: The title is automatically obtained. When the title cannot be obtained, a dialog will appear for you to manually add the title.
* **Edit Link**: Allows you to edit the title of an existing link and its URL.
* **Remove Link**: Allows you to remove a link from the list.
* **Export Links**: Allows exporting the saved links and categories to a json file.
* **Import Links**: Allows importing previously saved links and categories from a json file.
* **Sort Links**: Allows sorting the links in alphabetical order.

### Shortcuts

Some options are available through direct shortcuts in the interface:

* **Open link, `alt+O`**: Opens the selected link in the system's default browser.
  **Note**: Pressing Enter on the selected link opens it in the system's default browser.
* **Add link, `alt+A`**: Allows you to add a new link by providing its URL and category.
  **Note**: The title is automatically obtained. When the title cannot be obtained, a dialog will appear for you to manually add the title.
* **Edit link, `alt+E` or `F2`**: Allows you to edit the title of an existing link and its URL.
* **Delete link, `alt+L` or `del`**: Allows you to remove a link from the list.
* **Add category, `alt+G`**: Allows you to add a category to the list.
* **Exit, `alt+X`**: Closes the dialog. You can also use the `Escape` key or `Alt+F4`.

## Add New Link Dialog

1. **Category**: A combo box where you can choose the desired category.
2. **Field for adding the link URL**: A text box where you can paste the URL.
   **Note**: If you have already copied the URL, it will be automatically placed in the edit box.
3. **OK, `alt+O`**: Adds the link to the list.
   **Note**: The title is automatically obtained. When the title cannot be obtained, a dialog will appear for you to manually add the title.
4. **Cancel, `alt+C`**: Closes the dialog. You can also use the `Escape` key or Alt+F4.

## Edit Link Dialog

1. **Category**: A combo box where you can choose the desired category.
   Selecting another category will save the link in the newly selected category.
2. **Field for editing the URL title**: A text box where you can edit the title associated with the URL.
3. **Field for editing the URL**: A text box where you can edit the URL.
4. **OK, `Alt+O`**: Saves the changes made.
5. **Cancel, `Alt+C`**: Closes the dialog. You can also use the `Escape` key or `Alt+F4`.

## Acknowledgments

I would like to thank Rue Fontes and Ângelo Abrantes for testing and suggestions to improve this project, and Marlon Brandão de Sousa for generously sharing his workflow, which was crucial for the efficiency and quality of the project.

### Translators

* **Arabic** by Ahmed Bakr.
* **Portuguese (Brazil)** by Edilberto Fonseca.
* **Russian (Russia)** by Valentin Kupriyanov.
* **Turkish (Turkey)** by Umut KORKMAZ.
* **Ukrainian (Ukraine)** by Heorhii Halas.
