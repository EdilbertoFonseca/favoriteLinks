# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 - 2026 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

-------------------------------------------------------------------------
AI DISCLOSURE / NOTA DE IA:
This project utilizes AI for code refactoring and logic suggestions.
All AI-generated code was manually reviewed and tested by the author.
-------------------------------------------------------------------------

Created on: 11/04/2024.
"""

import json
import os
import re
import socket
import sys
from json.decoder import JSONDecodeError
from urllib.error import URLError
from urllib.request import urlopen

import addonHandler
from api import getClipData
from logHandler import log

from .jsonConfig import jsonConfig
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

	# Regular expression that matches http/https/ftp URLs and bare www. addresses.
	# Inspired by the URL pattern used in Link Manager by Abdallah Hader:
	# https://github.com/abdallah-hader/linkManager
	_URL_RE = re.compile(r"(?:(?:https?|ftp)://\S+|www\.\S+)")
	_URL_STRIP_CHARS = '\'.,[]{}:;"'

	def __init__(self):
		self.jsonFilePath = jsonConfig.getCurrentJsonPath()
		self.data = {}
		log.debug(f"[{ourAddon.name}] LinkManager initialized. JSON path: '{self.jsonFilePath}'")
		self.loadJson()

	@classmethod
	def empty(cls):
		"""
		Creates a fully initialised but empty LinkManager without loading the
		JSON file. Use this as a safe fallback when the normal constructor fails
		(e.g. corrupt JSON at startup) so that all expected attributes are
		present and a later reload attempt can still succeed.

		Returns:
			LinkManager: An instance with an empty data dict and a valid
				json_file_path.
		"""
		instance = cls.__new__(cls)
		instance.jsonFilePath = jsonConfig.getCurrentJsonPath()
		instance.data = {}
		return instance

	def loadJson(self):
		"""
		It loads the JSON file data to the memory and ensures that the structure is clean.
		"""
		try:
			with open(self.jsonFilePath, 'r', encoding='utf-8') as file:
				rawData = json.load(file)

			cleanData = {}
			for category, links in rawData.items():
				validLinks = []
				if isinstance(links, list):
					for link in links:
						if isinstance(link, list) and len(link) == 2:
							title, url = link
							if title and url:
								validLinks.append([title, url])
				cleanData[category] = validLinks

			self.data = cleanData
			self.sortCategories()

		except FileNotFoundError:
			self.data = {}
			self.saveLinks()
		except JSONDecodeError:
			self.data = {}
			log.warning("JSON file is corrupt, loading empty data: %s", self.jsonFilePath)
			self.saveLinks()

	def saveLinks(self):
		"""
		Saves memory data to the JSON file.
		"""
		try:
			with open(self.jsonFilePath, 'w', encoding='utf-8') as file:
				json.dump(self.data, file, indent=4, ensure_ascii=False)
		except Exception as e:
			raise Exception(_("Error saving the links: {}").format(e))

	def addCategory(self, category: str):
		"""
		Adds a new category.
		"""
		if not category.strip():
			raise ValueError(_("The category name cannot be empty!"))
		if category in self.data:
			raise ValueError(_("The category already exists!"))
		self.data[category] = []
		self.sortCategories()
		self.saveLinks()

	def getTitleFromURL(self, url: str) -> str:
		"""
		Get the title of a web page from your URL.
		"""
		try:
			with urlopen(url, timeout=5) as response:
				soup = BeautifulSoup(response, 'html.parser')
				titleTag = soup.find('title')
				if titleTag:
					title = titleTag.get_text().strip()
					return UnicodeDammit(title).unicode_markup
				return _("Unknown title")
		except (URLError, socket.timeout) as e:
			log.error(f"Error retrieving the page title for '{url}': {e}")
			raise URLError(_("Failed to get title. Please enter one manually."))

	def addLinkToCategory(self, category: str, title: str, url: str):
		"""
		Adds a link to an existing category.
		"""
		if category not in self.data:
			self.data[category] = []

		if any(link[1] == url for link in self.data[category]):
			raise ValueError(_("The link already exists in the category!"))

		self.data[category].append([title, url])
		self.data[category].sort(key=lambda x: x[0].lower())
		self.saveLinks()

	def editLinkInCategory(self, category: str, oldTitle: str, newTitle: str, newURL: str):
		"""
		Edit an existing link in a category.
		"""
		if category not in self.data:
			raise KeyError(_("Category does not exist."))

		for link in self.data[category]:
			if link[0] == oldTitle:
				link[0] = newTitle
				link[1] = newURL
				break
		else:
			raise ValueError(_("Link not found to edit."))

		self.data[category].sort(key=lambda x: x[0].lower())
		self.saveLinks()

	def removeLinkFromCategory(self, category: str, title: str):
		"""
		Removes a link from a category.
		"""
		if category not in self.data:
			return

		self.data[category] = [link for link in self.data[category] if link[0] != title]
		self.saveLinks()

	def editCategoryName(self, oldName: str, newName: str):
		"""
		Rename a category.
		"""
		if not newName.strip():
			raise ValueError(_("The category name cannot be empty!"))
		if newName in self.data:
			raise ValueError(_("A category with this name already exists!"))
		if oldName not in self.data:
			raise KeyError(_("Old category name not found."))

		self.data[newName] = self.data.pop(oldName)
		self.sortCategories()
		self.saveLinks()

	def deleteCategory(self, category: str):
		"""
		Delete a category and all your links.
		"""
		if category in self.data:
			del self.data[category]
			self.saveLinks()

	def getURLFromClipboard(self) -> str:
		"""
		Obtains a valid URL of the transfer area.
		"""
		try:
			clipboardData = getClipData()
			if clipboardData and self.isValidURL(clipboardData):
				return clipboardData
		except OSError as e:
			log.error("Error accessing the clipboard: {}".format(e))
		return ""

	def isValidURL(self, url: str) -> bool:
		return validators.url(url)

	def mergeLinks(self, importedData: dict):
		"""
		It mixes imported data with existing links.
		"""
		if not isinstance(importedData, dict):
			raise ValueError(_("The imported data must be a dictionary with categories as keys."))

		for category, links in importedData.items():
			if not isinstance(links, list) or not all(isinstance(link, list) and len(link) == 2 for link in links):
				raise ValueError(_("The links in the category '{}' must be lists containing [title, url].".format(category)))

			if category in self.data:
				existingURLS = {link[1] for link in self.data[category]}
				for title, url in links:
					if url not in existingURLS:
						self.data[category].append([title, url])
			else:
				self.data[category] = links

		self.sortCategories()
		self.saveLinks()

	def exportLinks(self, exportPath: str):
		"""
		Export all links to a JSON file.
		"""
		try:
			with open(exportPath, 'w', encoding='utf-8') as file:
				json.dump(self.data, file, indent=4, ensure_ascii=False)
		except Exception as e:
			raise Exception(_("Error exporting the links: {}".format(e)))

	def importLinks(self, importPath: str):
		"""
		Import links from a JSON file.
		"""
		try:
			with open(importPath, 'r', encoding='utf-8') as file:
				importedData = json.load(file)
			self.mergeLinks(importedData)
		except FileNotFoundError:
			raise FileNotFoundError(_("File not found: {}".format(importPath)))
		except JSONDecodeError:
			raise ValueError(_("Error decoding JSON from file: {}".format(importPath)))
		except Exception as e:
			raise Exception(_("Unexpected error importing the links: {}".format(e)))

	@staticmethod
	def extract_urls_from_text(text):
		"""
		Extracts all URLs found in an arbitrary text string using a regular
		expression. Useful for parsing clipboard content that may contain
		URLs embedded inside sentences.

		Inspired by the URL extraction pattern used in Link Manager by
		Abdallah Hader: https://github.com/abdallah-hader/linkManager

		Args:
			text (str): The text to search for URLs.

		Returns:
			list: A list of URL strings found in the text. May be empty.
		"""
		return [s.strip(LinkManager._URL_STRIP_CHARS) for s in LinkManager._URL_RE.findall(text)]

	def is_internet_connected(self, host='8.8.8.8', port=53, timeout=3) -> bool:
		"""
		Check if there is connection to the internet.
		"""
		try:
			socket.create_connection((host, port), timeout=timeout)
			return True
		except (socket.timeout, socket.gaierror, ConnectionRefusedError, OSError):
			return False

	def sortAllLinksAndSave(self):
		"""
		Order all links in all categories.
		"""
		for category, links in self.data.items():
			self.data[category] = sorted(links, key=lambda x: x[0].lower())
		self.saveLinks()

	def sortCategories(self):
		"""
		Order the categories in alphabetical order.
		"""
		self.data = {key: self.data[key] for key in sorted(self.data.keys(), key=str.lower)}
