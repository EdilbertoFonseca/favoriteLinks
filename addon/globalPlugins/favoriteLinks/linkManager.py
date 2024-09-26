# -*- coding: UTF-8 -*-

# Description: Module for Business Logic
# Author: Edilberto Fonseca.
# Date of creation: 11/04/2024.

# import the necessary modules.
import json
import logging
from json.decoder import JSONDecodeError
from urllib.error import URLError
from urllib.request import urlopen

import addonHandler
import api
import requests
import ui
import wx

from .configPanel import dirJsonFile
from .lib import validators
from .lib.bs4 import BeautifulSoup, UnicodeDammit

# Configure the logger instance for the current module, allowing logging of log messages.
logger = logging.getLogger(__name__)

# To start the translation process
addonHandler.initTranslation()


class LinkManager:

	def __init__(self, json_file_path=dirJsonFile):
		self.json_file_path = json_file_path
		self.data = {}

	def load_json(self, ui_instance=None):
		"""
		Loads JSON data from a file and updates the UI (if provided).
		This function attempts to load JSON data from the file specified by
		`self.json_file_path`. If successful, the data is stored in the
		`self.data` attribute and the categories are populated into the
		`ui_instance.category` combobox (if provided).

		Args:
		ui_instance (object, optional): A reference to a UI object that has
			attributes `category` (a combobox) and potentially `onCategorySelected`
			(a callback function). Defaults to None.

		Returns:
		None

		Raises:
		FileNotFoundError: If the JSON file is not found.
		json.JSONDecodeError: If the JSON data is invalid.

		Excepetion Handling:
		- In case of `FileNotFoundError`, an empty dictionary is assigned to
		`self.data` and the links are saved using `self.save_links()`.
		- In case of `json.JSONDecodeError`, if `ui_instance` is provided, a message
		is displayed indicating an error decoding the JSON data. The links are
		also saved using `self.save_links()`.
		"""

		try:
			with open(self.json_file_path, 'r') as file:
				self.data = json.load(file)
			self.sort_categories()
			if ui_instance:
				ui_instance.category.Clear()
				categories = list(self.data.keys())
				ui_instance.category.AppendItems(categories)
				if categories:
					ui_instance.category.SetSelection(0)
					if hasattr(ui_instance, 'onCategorySelected') and callable(getattr(ui_instance, 'onCategorySelected')):
						ui_instance.onCategorySelected(None)
		except FileNotFoundError:
			self.data = {}
			self.save_links()
		except json.JSONDecodeError:
			if ui_instance:
				ui_instance.show_message(_("Error decoding JSON. Check the file contents."))
			self.save_links()

	def save_links(self):
		"""
		Saves the links and categories in a json file.

		Raises:
			Exception: Returns an error message with the code.
		"""
		try:
			with open(self.json_file_path, 'w') as file:
				json.dump(self.data, file, indent=4)
		except Exception as e:
			raise Exception(_(f"Error saving links: {e}"))

	def add_category(self, category):
		"""
		Adds a new category to the system.

		Arg	s:
			category (str): The name of the new category to add.

		Raises:
			ValueError: If the category already exists in the system.
		"""
		if category in self.data:
			raise ValueError(_("Category already exists!"))
		self.data[category] = []  # Initialize the category as an empty list
		self.save_links()  # Save the data after adding the new category

	def get_title_from_url(self, url):
		"""
		Gets the title of a web page from the URL.

		Args:
			url (str):The URL of the web page from which the title will be taken.

		Returns:
			str:The page title.

		Raises:
			Exception:If an error occurs when accessing the URL or trying to extract the title.
		"""
		try:
			with urlopen(url) as response:
				soup = BeautifulSoup(response, 'html.parser')
				title = soup.find('title').get_text().strip()
				return UnicodeDammit(title).unicode_markup
		except URLError as e:
			ui.message(f"Error fetching title: {e}")
			return self.prompt_for_title(url)

	def prompt_for_title(self, url):
		"""
			Prompts the user to enter a title for the given URL.
			Opens a dialog box for the user to enter the title manually.

					Parameters:
			- url (str): OURL for which the title is requested.

			Returns:
			- str:The title entered by the user or 'Unknown Title' if the user cancels.
			"""

		title = _("Enter a title for the URL:")
		caption = _("Unknown Title for URL")

		# Creates a dialog box to request the title
		dlg = wx.TextEntryDialog(None, title, caption, value="")
		if dlg.ShowModal() == wx.ID_OK:
			user_input = dlg.GetValue()
			dlg.Destroy()
			return user_input.strip() if user_input else _("Unknown Title")
		else:
			dlg.Destroy()
			return _("Unknown Title")

	def add_link_to_category(self, category, title, url):
		"""
		Adds a link to a specific category.

		Args:
			category (str):The name of the category where the link will be added.
			title (str): The title of the link.
			url (str):The URL of the link.

		Raises:
			ValueError: If the link already exists in the category.
		"""
		if category in self.data:
			if not any(link[1] == url for link in self.data[category]):
				self.data[category].append([title, url])
			else:
				raise ValueError(_("Link already exists in the category!"))
		else:
			self.data[category] = [[title, url]]

	def edit_link_in_category(self, category, old_title, new_title, new_url):
		"""
		Edit a specific link within a category.

		Args:
			category (str):The name of the category where the link will be edited.
			old_title (str):The current title of the link to be edited.
			new_title (str):The new link title.
			new_url (str): The new link URL.
		"""
		if category in self.data:
			for link in self.data[category]:
				if link[0] == old_title:
					link[0] = new_title
					link[1] = new_url
					break

	def remove_link_from_category(self, category, title):
		"""
		Removes a specific link from a category.

		Args:
			category (str): The name of the category from which the link will be removed.
			title (str): The title of the link to be removed.
		"""
		if category in self.data:
			self.data[category] = [link for link in self.data[category] if link[0] != title]

	def edit_category_name(self, old_name, new_name):
		"""
		Edit the name of an existing category.

		Args:
			old_name (str): The current name of the category.
			new_name (str): The new name for the category.
		"""
		if old_name in self.data:
			self.data[new_name] = self.data.pop(old_name)

	def delete_category(self, category):
		"""
		Removes a specific category from the system.

		Args:
			category (str): The name of the category to remove.
		"""

		if category in self.data:
			del self.data[category]

	def get_url_from_clipboard(self):
		"""
		Gets a valid URL from the clipboard.

		Returns:
			str: Valid clipboard URL if available, otherwise an empty string.
		"""

		try:
			clipboard_data = api.getClipData()
			if clipboard_data and self.is_valid_url(clipboard_data):
				return clipboard_data
		except OSError as e:
			print(f"Error accessing clipboard: {e}")
		return ""

	def is_valid_url(self, url):
		"""
		Checks whether the provided URL is valid.

		Args:
			url (str): The URL to check.

		Returns:
			bool: True if the URL is valid, otherwise False.
		"""

		return validators.url(url)

	def merge_links(self, imported_data):
		"""
		Merges the imported links with the existing links in the system.

		Args:
			imported_data (dict): Imported data containing links to merge.
			The dictionary should have categories as keys
			and lists of (title, url) pairs as values.

		Raises:
			ValueError: If the imported data format is invalid.
		"""

		if not isinstance(imported_data, dict):
			raise ValueError("The imported_data must be a dictionary with categories as keys.")

		for category, links in imported_data.items():
			if not isinstance(links, list) or not all(isinstance(link, list) and len(link) == 2 for link in links):
				raise ValueError(f"The links for category '{category}' must be a list of [title, url] pairs.")

			if category in self.data:
				existing_urls = {link[1] for link in self.data[category]}
				for title, url in links:
					if url not in existing_urls:
						self.data[category].append([title, url])
			else:
				self.data[category] = links

	def export_links(self, export_path):
		"""
		Exports saved links to a specified JSON file.

		Args:
			export_path (str):The path of the JSON file where the links will be exported.

		Raises:
			Exception:If an error occurs while exporting the links.
		"""

		try:
			with open(export_path, 'w') as file:
				json.dump(self.data, file, indent=4)
		except Exception as e:
			raise Exception(f"Error exporting links: {e}")

	def import_links(self, import_path):
		"""
		Imports links from a specified JSON file and merges with existing links.

		Args:
			import_path (str): The path of the JSON file to be imported.

		Raises:
			FileNotFoundError: If the specified file does not exist.
			JSONDecodeError: If there is an error decoding the JSON data.
			Exception: For other exceptions that might occur.
		"""

		try:
			with open(import_path, 'r') as file:
				imported_data = json.load(file)
			self.merge_links(imported_data)
			self.save_links()
		except FileNotFoundError as e:
			raise FileNotFoundError(f"The file at {import_path} was not found: {e}")
		except JSONDecodeError as e:
			raise JSONDecodeError(f"Error decoding JSON from the file at {import_path}: {e}")
		except Exception as e:
			raise Exception(f"An unexpected error occurred while importing links: {e}")

	def is_internet_connected(self, url="http://www.google.com", timeout=5):
		"""
		Checks if there is an active internet connection.
		This function tries to send a GET request to a specified URL to determine if there is an active internet
		connection. By default, it checks the connection to http://www.google.com with a timeout of 5 seconds.

		Parameters:
		- url (str): The URL to test the internet connection (default is "http://www.google.com").
		- timeout (int): The maximum time in seconds to wait for a response (default is 5 seconds).

		Returns:
		- bool: True if the internet connection is active, False otherwise.
		"""

		try:
			response = requests.get(url, timeout=timeout)
			return response.status_code == 200
		except (requests.ConnectionError, requests.Timeout):
			return False

	def sort_json(self):
		"""
		Loads and sorts the contents of the JSON file.

		The function loads data from the JSON file, sorts the links in each category in order
		alphabetically based on the title (first element of each link), and saves the data
		sorted back into the JSON file.
				"""

		with open(self.json_file_path, 'r') as file:
			data = json.load(file)
		# Iterate over the categories and order the links within each category
		for category, links in data.items():
			# Sort links alphabetically based on title (first element of each link)
			data[category] = sorted(links, key=lambda x: x[0].lower())
		# Save sorted data back to JSON file
		with open(self.json_file_path, "w") as file:
			json.dump(data, file, indent=4)

	def sort_categories(self):
		"""
		Sorts the categories in alphabetical order.
		"""
		self.data = {key: self.data[key] for key in sorted(self.data.keys(), key=str.lower)}
