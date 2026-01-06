# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 11/04/2024.
"""

import json
import os
import socket
import sys
from json.decoder import JSONDecodeError
from urllib.error import URLError
from urllib.request import urlopen

import addonHandler
from api import getClipData
from logHandler import log

from .jsonConfig import json_config
from .varsConfig import ourAddon, addonPath

# Initialize translation support
addonHandler.initTranslation()

# Add the lib/ folder to sys.path (only once)
libPath = os.path.join(addonPath, "lib")
if libPath not in sys.path:
	sys.path.insert(0, libPath)

try:
	import validators
	from bs4 import BeautifulSoup
	from bs4.dammit import UnicodeDammit
except ImportError as e:
	log.error(f"[{ourAddon}] Error when importing libraries: {e}")
	raise ImportError(_("Missing required libraries: validators, BeautifulSoup e UnicodeDammit"))


class LinkManager:

	def __init__(self):
		self.json_file_path = json_config.get_current_json_path()
		self.data = {}
		log.debug(f"[{ourAddon.name}] LinkManager inicializado. Caminho do JSON: '{self.json_file_path}'")
		self.load_json()

	def load_json(self):
		"""
		It loads the JSON file data to the memory and ensures that the structure is clean.
		"""
		try:
			with open(self.json_file_path, 'r', encoding='utf-8') as file:
				raw_data = json.load(file)

			clean_data = {}
			for category, links in raw_data.items():
				valid_links = []
				if isinstance(links, list):
					for link in links:
						if isinstance(link, list) and len(link) == 2:
							title, url = link
							if title and url:
								valid_links.append([title, url])
				clean_data[category] = valid_links

			self.data = clean_data
			self.sort_categories()

		except FileNotFoundError:
			self.data = {}
			self.save_links()
		except JSONDecodeError:
			self.data = {}
			self.save_links()
			raise JSONDecodeError(_("Error decoding the JSON. Check the file content."), doc='', pos=0)

	def save_links(self):
		"""
		Saves memory data to the JSON file.
		"""
		try:
			with open(self.json_file_path, 'w', encoding='utf-8') as file:
				json.dump(self.data, file, indent=4, ensure_ascii=False)
		except Exception as e:
			raise Exception(_("Error saving the links: {}").format(e))

	def add_category(self, category: str):
		"""
		Adds a new category.
		"""
		if not category.strip():
			raise ValueError(_("The category name cannot be empty!"))
		if category in self.data:
			raise ValueError(_("The category already exists!"))
		self.data[category] = []
		self.sort_categories()
		self.save_links()

	def get_title_from_url(self, url: str) -> str:
		"""
		Get the title of a web page from your URL.
		"""
		try:
			with urlopen(url, timeout=5) as response:
				soup = BeautifulSoup(response, 'html.parser')
				title_tag = soup.find('title')
				if title_tag:
					title = title_tag.get_text().strip()
					return UnicodeDammit(title).unicode_markup
				return _("Unknown title")
		except (URLError, socket.timeout) as e:
			log.error(f"Error retrieving the page title for '{url}': {e}")
			raise URLError(_("Failed to get title. Please enter one manually."))

	def add_link_to_category(self, category: str, title: str, url: str):
		"""
		Adds a link to an existing category.
		"""
		if category not in self.data:
			self.data[category] = []
		
		if any(link[1] == url for link in self.data[category]):
			raise ValueError(_("The link already exists in the category!"))
		
		self.data[category].append([title, url])
		self.data[category].sort(key=lambda x: x[0].lower())
		self.save_links()

	def edit_link_in_category(self, category: str, old_title: str, new_title: str, new_url: str):
		"""
		Edit an existing link in a category.
		"""
		if category not in self.data:
			raise KeyError(_("Category does not exist."))
		
		for link in self.data[category]:
			if link[0] == old_title:
				link[0] = new_title
				link[1] = new_url
				break
		else:
			raise ValueError(_("Link not found to edit."))

		self.data[category].sort(key=lambda x: x[0].lower())
		self.save_links()

	def remove_link_from_category(self, category: str, title: str):
		"""
		Removes a link from a category.
		"""
		if category not in self.data:
			return

		self.data[category] = [link for link in self.data[category] if link[0] != title]
		self.save_links()

	def edit_category_name(self, old_name: str, new_name: str):
		"""
		Rename a category.
		"""
		if not new_name.strip():
			raise ValueError(_("The category name cannot be empty!"))
		if new_name in self.data:
			raise ValueError(_("A category with this name already exists!"))
		if old_name not in self.data:
			raise KeyError(_("Old category name not found."))

		self.data[new_name] = self.data.pop(old_name)
		self.sort_categories()
		self.save_links()

	def delete_category(self, category: str):
		"""
		Delete a category and all your links.
		"""
		if category in self.data:
			del self.data[category]
			self.save_links()

	def get_url_from_clipboard(self) -> str:
		"""
		Obtains a valid URL of the transfer area.
		"""
		try:
			clipboard_data = getClipData()
			if clipboard_data and self.is_valid_url(clipboard_data):
				return clipboard_data
		except OSError as e:
			log.error("Error accessing the clipboard: {}".format(e))
		return ""

	def is_valid_url(self, url: str) -> bool:
		return validators.url(url)

	def merge_links(self, imported_data: dict):
		"""
		It mixes imported data with existing links.
		"""
		if not isinstance(imported_data, dict):
			raise ValueError(_("The imported data must be a dictionary with categories as keys."))

		for category, links in imported_data.items():
			if not isinstance(links, list) or not all(isinstance(link, list) and len(link) == 2 for link in links):
				raise ValueError(_("The links in the category '{}' must be lists containing [title, url].".format(category)))

			if category in self.data:
				existing_urls = {link[1] for link in self.data[category]}
				for title, url in links:
					if url not in existing_urls:
						self.data[category].append([title, url])
			else:
				self.data[category] = links

		self.sort_categories()
		self.save_links()

	def export_links(self, export_path: str):
		"""
		Export all links to a JSON file.
		"""
		try:
			with open(export_path, 'w', encoding='utf-8') as file:
				json.dump(self.data, file, indent=4, ensure_ascii=False)
		except Exception as e:
			raise Exception(_("Error exporting the links: {}".format(e)))

	def import_links(self, import_path: str):
		"""
		Import links from a JSON file.
		"""
		try:
			with open(import_path, 'r', encoding='utf-8') as file:
				imported_data = json.load(file)
			self.merge_links(imported_data)
		except FileNotFoundError:
			raise FileNotFoundError(_("File not found: {}".format(import_path)))
		except JSONDecodeError:
			raise ValueError(_("Error decoding JSON from file: {}".format(import_path)))
		except Exception as e:
			raise Exception(_("Unexpected error importing the links: {}".format(e)))

	def is_internet_connected(self, host='8.8.8.8', port=53, timeout=3) -> bool:
		"""
		Check if there is connection to the internet.
		"""
		try:
			socket.create_connection((host, port), timeout=timeout)
			return True
		except (socket.timeout, socket.gaierror, ConnectionRefusedError, OSError):
			return False

	def sort_all_links_and_save(self):
		"""
		Order all links in all categories.
		"""
		for category, links in self.data.items():
			self.data[category] = sorted(links, key=lambda x: x[0].lower())
		self.save_links()

	def sort_categories(self):
		"""
		Order the categories in alphabetical order.
		"""
		self.data = {key: self.data[key] for key in sorted(self.data.keys(), key=str.lower)}
