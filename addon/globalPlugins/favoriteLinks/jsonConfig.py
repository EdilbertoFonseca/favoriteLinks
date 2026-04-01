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

Created on: 26/05/2025
"""

import os

import config
from logHandler import log

# Assuming ourAddon is defined in varsConfig.py and imported via __init__.py
# For this file to work standalone or be imported, we'll define a dummy ourAddon if not present
# This is a safety measure; in typical NVDA addon structure, ourAddon is available globally or via specific imports.
try:
	from .varsConfig import ourAddon
except ImportError:
	# Fallback for testing or if varsConfig.py is not in the same direct import path
	# In a real NVDA addon, ourAddon comes from addonHandler.getCodeAddon()
	class DummyAddon:
		name = "favoriteLinks" # Use the actual addon name
	ourAddon = DummyAddon()
	log.warning("Could not import 'ourAddon' from varsConfig.py. Using a dummy Addon object.")

class JsonConfig:

	def __init__(self, defaultPath):
		self.defaultPath = defaultPath
		self.browserPath = ""
		self.firstJsonFile = defaultPath
		self.altJsonFile = ""
		self.indexJson = 0
		self.loadConfig()

	def loadConfig(self):
		try:
			# Get the current configuration for the addon
			conf = config.conf[ourAddon.name]

			# Load the index for the selected path
			self.indexJson = int(conf.get("xx", 0))

			# Load the primary and alternate paths
			self.firstJsonFile = conf.get("path", self.defaultPath)
			self.altJsonFile = conf.get("altPath", "") # altPath can legitimately be empty
			self.browserPath = conf.get("browserPath", "")  # Carrega caminho do navegador

			# Ensure first_json_file is never empty, fallback to default_path if it somehow became empty
			if not self.firstJsonFile:
				self.firstJsonFile = self.defaultPath

			log.debug(f"[{ourAddon.name}] JsonConfig loaded: index={self.indexJson}, primary='{self.firstJsonFile}', alternate='{self.altJsonFile}'")

		except ValueError:
			log.error(f"[{ourAddon.name}] Invalid value for JSON index in configuration, using default: {self.defaultPath}")
			self.browserPath = ""
			self.firstJsonFile = self.defaultPath
			self.altJsonFile = ""
			self.indexJson = 0
		except KeyError:
			log.warning(f"[{ourAddon.name}] JSON configuration not found, initializing with default paths.")
			self.firstJsonFile = self.defaultPath
			self.altJsonFile = ""
			self.indexJson = 0
		except Exception as e:
			log.error(f"[{ourAddon.name}] Unexpected error loading JSON config: {e}")
			self.browserPath = ""
			self.firstJsonFile = self.defaultPath
			self.altJsonFile = ""
			self.indexJson = 0


	def saveConfig(self):
		config.conf[ourAddon.name]["browserPath"] = self.browserPath
		config.conf[ourAddon.name]["path"] = self.firstJsonFile
		config.conf[ourAddon.name]["altPath"] = self.altJsonFile
		config.conf[ourAddon.name]["xx"] = str(self.indexJson)
		log.debug(f"[{ourAddon.name}] JsonConfig saved: index={self.indexJson}, primary='{self.firstJsonFile}', alternate='{self.altJsonFile}'")

	def setJsonPath(self, newPath, isFirst=True):
		"""Sets the primary or alternate JSON file path."""
		if isFirst:
			self.firstJsonFile = newPath
		else:
			self.altJsonFile = newPath
		log.debug(f"[{ourAddon.name}] JsonConfig path set: {'primary' if isFirst else 'alternate'} to '{newPath}'")


	def getCurrentJsonPath(self):
		"""Returns the currently active JSON file path based on the index."""
		currentPath = self.firstJsonFile if self.indexJson == 0 else self.altJsonFile
		if not currentPath: # Fallback in case the selected path is unexpectedly empty
			log.warning(f"[{ourAddon.name}] Current JSON path is empty, falling back to default: {self.defaultPath}")
			return self.defaultPath
		return currentPath

	def updateJsonFilePath(self, newPath):
		"""
		Updates the internal JSON path and handles file renaming if necessary.
		"""
		oldActivePath = self.getCurrentJsonPath()
		
		# Update the path based on the current selection index
		if self.indexJson == 0:
			self.setJsonPath(newPath, isFirst=True)
		else:
			self.setJsonPath(newPath, isFirst=False)

		# Check if renaming is needed (if old path exists, new path doesn't, and paths are different)
		if os.path.exists(oldActivePath) and not os.path.exists(newPath) and oldActivePath != newPath:
			try:
				import shutil
				shutil.move(oldActivePath, newPath)
				log.info(f"[{ourAddon.name}] Renamed JSON file from '{oldActivePath}' to '{newPath}'")
			except Exception as e:
				log.error(f"[{ourAddon.name}] Error renaming JSON file from '{oldActivePath}' to '{newPath}': {e}")
		else:
			log.info(f"[{ourAddon.name}] JSON file path updated to '{newPath}'. No rename needed or file already exists/didn't exist.")


# Global instance of the JSON configuration manager
# This path should ideally be in a user-specific data directory, but
# using os.path.dirname(__file__) ensures it's relative to the addon.
jsonConfig = JsonConfig(defaultPath=os.path.join(os.path.dirname(__file__), "favorite_links.json"))
