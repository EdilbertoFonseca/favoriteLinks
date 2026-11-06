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
import shutil

import config
import globalVars
from logHandler import log

from .varsConfig import getAddonConf

# Safely obtain ourAddon instance or fallback to a dummy object for standalone environments
try:
	from .varsConfig import ourAddon
except ImportError:

	class DummyAddon:
		name = "favoriteLinks"

	ourAddon = DummyAddon()
	log.warning("Could not import 'ourAddon' from varsConfig.py. Using a dummy Addon object.")


class JsonConfig:
	"""
	Manages the JSON configuration file paths and browser settings for the addon.
	Handles directory creation, path fallbacks, and safe file operations.
	"""

	def __init__(self, defaultPath: str):
		self.defaultPath = defaultPath
		self.browserPath = ""
		self.firstJsonFile = defaultPath
		self.altJsonFile = ""
		self.indexJson = 0

		# Ensure default directory exists upon initialization
		self.ensureDirectoryExists(self.defaultPath)
		self.loadConfig()

		# Check if the loaded path points to the obsolete addon folder and update it
		self._migrateLegacyConfigPath()

	def _migrateLegacyConfigPath(self) -> None:
		"""
		Detects if the configured primary JSON path points to the legacy addon directory.
		If detected, updates the configuration path to the new user directory and cleans up
		any empty legacy files.
		"""
		addonDirMarker = os.path.join("addons", ourAddon.name)

		# Check if the active primary path resides inside the installed addon directory
		if self.firstJsonFile and addonDirMarker in self.firstJsonFile:
			legacyPath = self.firstJsonFile
			log.info(
				f"[{ourAddon.name}] Legacy addon path detected in configuration: '{legacyPath}'. "
				f"Migrating setting to default user path: '{self.defaultPath}'",
			)

			# 1. Update the internal state to the new default path
			self.firstJsonFile = self.defaultPath

			# 2. Persist the updated configuration to nvda.ini
			self.saveConfig()

			# 3. Clean up the empty/obsolete file left in the addon directory if it exists
			if os.path.isfile(legacyPath):
				try:
					os.remove(legacyPath)
					log.info(f"[{ourAddon.name}] Removed obsolete JSON file at '{legacyPath}'")
				except Exception as e:
					log.error(f"[{ourAddon.name}] Failed to remove obsolete file '{legacyPath}': {e}")

	def ensureDirectoryExists(self, filePath: str) -> None:
		"""
		Ensures that the parent directory for a given file path exists on the filesystem.
		Creates intermediate directories if they are missing.
		"""
		if not filePath:
			return

		directoryPath = os.path.dirname(filePath)
		if directoryPath and not os.path.exists(directoryPath):
			try:
				os.makedirs(directoryPath, exist_ok=True)
				log.info(f"[{ourAddon.name}] Created directory structure: '{directoryPath}'")
			except Exception as e:
				log.error(f"[{ourAddon.name}] Failed to create directory '{directoryPath}': {e}")

	def loadConfig(self) -> None:
		"""Loads addon configuration values from NVDA's primary configuration manager."""
		try:
			conf = config.conf[ourAddon.name]

			self.indexJson = int(conf.get("xx", 0))
			self.firstJsonFile = conf.get("path", self.defaultPath)
			self.altJsonFile = conf.get("altPath", "")
			self.browserPath = conf.get("browserPath", "")

			# Fallback to default path if stored path is empty
			if not self.firstJsonFile:
				self.firstJsonFile = self.defaultPath

			log.debug(
				f"[{ourAddon.name}] JsonConfig loaded: index={self.indexJson}, "
				f"primary='{self.firstJsonFile}', alternate='{self.altJsonFile}'",
			)

		except ValueError:
			log.error(
				f"[{ourAddon.name}] Invalid value for JSON index in configuration. Falling back to default.",
			)
			self._resetToDefaults()
		except KeyError:
			log.warning(f"[{ourAddon.name}] Addon section not found in configuration. Initializing defaults.")
			self._resetToDefaults()
		except Exception as e:
			log.error(f"[{ourAddon.name}] Unexpected error loading JSON configuration: {e}")
			self._resetToDefaults()

	def _resetToDefaults(self) -> None:
		"""Resets internal state variables to default values."""
		self.browserPath = ""
		self.firstJsonFile = self.defaultPath
		self.altJsonFile = ""
		self.indexJson = 0

	def saveConfig(self) -> None:
		"""Saves active paths and settings into NVDA's configuration state."""
		addonConf = getAddonConf()
		addonConf["browserPath"] = self.browserPath
		addonConf["path"] = self.firstJsonFile
		addonConf["altPath"] = self.altJsonFile
		addonConf["xx"] = str(self.indexJson)

		log.debug(
			f"[{ourAddon.name}] JsonConfig saved: index={self.indexJson}, "
			f"primary='{self.firstJsonFile}', alternate='{self.altJsonFile}'",
		)

	def setJsonPath(self, newPath: str, isFirst: bool = True) -> None:
		"""Sets the primary or alternate JSON file path."""
		if isFirst:
			self.firstJsonFile = newPath
		else:
			self.altJsonFile = newPath

		log.debug(
			f"[{ourAddon.name}] JsonConfig path set: {'primary' if isFirst else 'alternate'} -> '{newPath}'",
		)

	def getCurrentJsonPath(self) -> str:
		"""Returns the active JSON path based on the selected index."""
		currentPath = self.firstJsonFile if self.indexJson == 0 else self.altJsonFile
		if not currentPath:
			log.warning(
				f"[{ourAddon.name}] Active JSON path is empty. Falling back to default: '{self.defaultPath}'",
			)
			return self.defaultPath
		return currentPath

	def updateJsonFilePath(self, newPath: str) -> None:
		"""
		Updates the active JSON file path, ensuring destination directories exist
		and moving the original file if necessary.
		"""
		oldActivePath = self.getCurrentJsonPath()

		# Ensure destination parent folder exists before performing updates/moves
		self.ensureDirectoryExists(newPath)

		if self.indexJson == 0:
			self.setJsonPath(newPath, isFirst=True)
		else:
			self.setJsonPath(newPath, isFirst=False)

		# Move file if the old file exists, new file doesn't exist, and paths differ
		if os.path.exists(oldActivePath) and not os.path.exists(newPath) and oldActivePath != newPath:
			try:
				shutil.move(oldActivePath, newPath)
				log.info(f"[{ourAddon.name}] Moved JSON file from '{oldActivePath}' to '{newPath}'")
			except Exception as e:
				log.error(
					f"[{ourAddon.name}] Error moving JSON file from '{oldActivePath}' to '{newPath}': {e}",
				)
		else:
			log.info(
				f"[{ourAddon.name}] JSON file path updated to '{newPath}'. No file movement required.",
			)


# Calculate default user configuration directory for the addon
DEFAULT_JSON_DIRECTORY = os.path.join(str(globalVars.appArgs.configPath), "favoriteLinks")
DEFAULT_JSON_FILE_PATH = os.path.join(DEFAULT_JSON_DIRECTORY, "favorite_links.json")

# Instantiate the singleton instance exposed to configPanel and other modules
JSON_CONFIG = JsonConfig(defaultPath=DEFAULT_JSON_FILE_PATH)
