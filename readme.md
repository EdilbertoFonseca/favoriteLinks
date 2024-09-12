# Favorite Links

* **Author**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Creation Date**: 11/04/2024
* **License**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introduction

The **FavoriteLinks** add-on is a tool that allows you to manage favorite links in an organized and efficient manner. With it, you can save, edit, and remove links in a categorized list. Its intuitive interface provides comprehensive functionalities, such as adding new links, editing titles, removing unwanted links, and managing categories. Upon opening the add-on, you have quick access to your favorite links and can open a selected link directly in your browser.

> Note: The FavoriteLinks add-on was developed with the assistance of ChatGPT for creating some functions and optimizing performance; it was also used for organizing the code.

## Installation

Follow the instructions below to install the Favorite Links add-on in NVDA:

1. **Download the add-on installation file**: Obtain the file from the NVDA Add-ons Store.
   > **Note**: If the add-on is downloaded from the store, installation will occur automatically. Otherwise, follow the instructions below.
2. **Install the add-on**: Press Enter on the downloaded add-on file.
3. **Follow the on-screen instructions**: Complete the installation according to the provided guidelines.
4. **Restart NVDA**: It is necessary to restart to activate the add-on.
5. **Verify the installation**: Press `NVDA+N` to open the NVDA menu, go to "Tools," and check if Favorite Links is listed.

## Configuration

You can select a different location from the default to save your links file. To do this, simply access the NVDA menu, go to Preferences, Settings, and in Settings, select the Favorite Links category. Then, choose a different folder using the “Select or add a directory” button.

## Usage

### Accessing the Add-on

Press `Alt+Windows+K` or use the NVDA menu `NVDA+N` > Tools > Favorite Links to open the add-on.

### Main Interface

The displayed dialog will have two main fields:

1. **Category**: A combo box where you can choose the desired category.
2. **Links List**: Here, the links corresponding to the selected category will be displayed.

### Available Actions

To access options for working with links and categories, you can use the NVDA Context Menu (Application key).

### Category

When positioned in the category combo box, the following options are displayed:

* **Add Category**: Allows adding a category to the list.
* **Edit Category**: Allows renaming an existing category.
* **Remove Category**: Allows deleting a category and all links associated with it.
* **Export Links**: Allows exporting the saved links and categories to a JSON file.
* **Import Links**: Allows importing previously saved links and categories from a JSON file.

### Links List

When positioned in the links list, the following options are displayed:

* **Open Link**: Opens the selected link in the system’s default browser.
  > Note: Pressing Enter on the selected link will open it in the system’s default browser.
* **Add Link**: Allows adding a new link by specifying its URL and category.
  > **Note**: The title is automatically obtained. If the title cannot be obtained, a dialog will appear for you to manually enter the title.
* **Edit Link**: Allows editing the title of an existing link and its URL.
* **Remove Link**: Allows removing a link from the list.
* **Export Links**: Allows exporting the saved links and categories to a JSON file.
* **Import Links**: Allows importing previously saved links and categories from a JSON file.
* **Sort Links**: Allows sorting the links in alphabetical order.

### Shortcuts

Some options are available through direct shortcuts in the interface. They are:

* **Open Link, `alt+B`**: Opens the selected link in the system’s default browser.
  > **Note**: Pressing Enter on the selected link will open it in the system’s default browser.
* **Add Link, `alt+A`**: Allows adding a new link by specifying its URL and category.
  > **Note**: The title is automatically obtained. If the title cannot be obtained, a dialog will appear for you to manually enter the title.
* **Edit Link, `alt+E`**: Allows editing the title of an existing link and its URL.
* **Delete Link, `alt+L`**: Allows removing a link from the list.
* **Add Category, `alt+D`**: Allows adding a category to the list.
* **Exit, `alt+S`**: Closes the dialog. You can also use the "Escape" key or Alt+F4.

## Add New Link Dialog

1. **Category**: A combo box where you can choose the desired category.
2. **Link URL Field**: A text box where you can paste the URL.
   > **Note**: If you have already copied the URL, it will be automatically placed in the text box.
3. **OK, `alt+O`**: Adds the link to the list.
   > **Note**: The title is automatically obtained. If the title cannot be obtained, a dialog will appear for you to manually enter the title.
4. **Cancel, `alt+C`**: Closes the dialog. You can also use the "Escape" key or Alt+F4.

## Acknowledgements

I thank Rue Fontes and Ângelo Abrantes for testing and suggestions to improve this project, and Marlon Brandão de Sousa for generously sharing his workflow, which was crucial for the efficiency and quality of the project.

### Translators

* **Arabic** by Ahmed Bakr.
* **Portuguese (Brazil)** by Edilberto Fonseca.
* **Turkish (Turkey)** by Umut KORKMAZ.
* **Ukrainian (Ukraine)** by Heorhii Halas.
