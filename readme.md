# Favorite Links

* **Author**: Edilberto Fonseca <edilberto.fonseca@outlook.com>
* **Creation Date**: 04/11/2024
* **License**: [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.html)

## Introduction

The **FavoriteLinks** add-on is a tool that allows you to manage favorite links in an organized and efficient way. With it, you can save, edit, and remove links in a categorized list. Its intuitive interface offers comprehensive functionalities, such as adding new links, editing titles, removing unwanted links, and managing categories. When you open the add-on, you have quick access to your favorite links and can open a selected link directly in the browser.

Note: The FavoriteLinks add-on was developed with the assistance of ChatGPT for the creation of some functions and optimization, and it was also used for code organization.

## Installation

Follow the instructions below to install the Favorite Links add-on in NVDA:

1. **Download the add-on installation file**: Obtain the file from the Add-ons Store or the official [Favorite Links](https://github.com/EdilbertoFonseca/favoriteLinks/releases/download/2024.2.1/favoriteLinks-2024.2.1.nvda-addon) page.
   **Note**: If the add-on is downloaded from the store, the installation will occur automatically. Otherwise, follow the instructions below.
2. **Install the add-on**: Press Enter on the downloaded add-on file.
3. **Follow the on-screen instructions**: Complete the installation as instructed.
4. **Restart NVDA**: You need to restart NVDA to activate the add-on.
5. **Verify the installation**: Press "NVDA + N" to open the NVDA menu, go to "Tools," and check if Favorite Links is listed.

## Configuration

You can select a different location from the default to save your links file. To do this, access the Favorite Links category in the NVDA menu and choose a different folder using the "Select or add a directory" button.

## Usage

### Accessing the Add-on

Press "Alt+Windows+K" or use the NVDA menu (NVDA+N) > Tools > Favorite Links to open the add-on.

### Main Interface

The displayed dialog will have two main fields:

1. **Category**: A combo box where you can choose the desired category.
2. **Links List**: Here, the links corresponding to the selected category will be displayed.

### Available Actions

To access the options for working with links and categories, you can use the NVDA context menu (application key).

### Category

When positioned in the category combo box, the following options are displayed:

* **Add Category**: Allows you to add a category to the list.
* **Edit Category**: Allows you to rename an existing category.
* **Remove Category**: Allows you to delete a category and all associated links.
* **Export Links**: Allows you to export the links and categories saved in the JSON file.
* **Import Links**: Allows you to import previously saved links and categories from the JSON file.

### Links List

When positioned in the links list, the following options are displayed:

* **Open Link**: Opens the selected link in the system's default browser. **Note**: Pressing Enter on the selected link will open it in the system's default browser.
* **Add Link**: Allows you to add a new link by entering its URL and category.
  **Note**: The title is obtained automatically. When the title cannot be obtained, a dialog will appear for you to add the title manually.
* **Edit Link**: Allows you to edit the title of an existing link and its URL.
* **Remove Link**: Allows you to remove a link from the list.
* **Export Links**: Allows you to export the links and categories saved in the JSON file.
* **Import Links**: Allows you to import previously saved links and categories from the JSON file.
* **Sort Links**: Allows you to sort links in alphabetical order.

## Shortcuts

Some options are available through direct shortcuts in the interface. They are:

* **Open link, Alt+B**: Opens the selected link in the system's default browser.
  **Note**: Pressing Enter on the selected link will open it in the system's default browser.
* **Add link, Alt+A**: Allows you to add a new link by entering its URL and category.
  **Note**: The title is obtained automatically. When the title cannot be obtained, a dialog will appear for you to add the title manually.
* **Edit link, Alt+E**: Allows you to edit the title of an existing link and its URL.
* **Remove link, Alt+L**: Allows you to remove a link from the list.
* **Add category, Alt+D**: Allows you to add a category to the list.
* **Exit, (Alt+S)**: Closes the dialog. You can also use the "Escape" key or Alt+F4.

## Add New Link Dialog

1. **Category**: A combo box where you can choose the desired category.
2. **Field for adding the link URL**: A text box where you can paste the URL.
   **Note**: If you have already copied the URL, it will be automatically placed in the edit box.
3. **OK, Alt+O**: Adds the link to the list.
   **Note**: The title is obtained automatically. When the title cannot be obtained, a dialog will appear for you to add the title manually.
4. **Cancel, Alt+C**: Closes the dialog. You can also use the "Escape" key or Alt+F4.

## Acknowledgements

I would like to thank Rue Fontes and Ângelo Abrantes for their testing and suggestions to improve this project, and Marlon Brandão de Sousa for generously sharing his workflow, which was crucial for the project's efficiency and quality.
