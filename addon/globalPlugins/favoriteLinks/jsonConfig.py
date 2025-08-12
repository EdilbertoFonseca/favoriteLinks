# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 26/05/2025
"""

import os

import addonHandler
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

	def __init__(self, default_path):
		self.default_path = default_path
		self.browser_path = ""
		self.first_json_file = default_path
		self.alt_json_file = ""
		self.index_json = 0
		self.load_config()

	def load_config(self):
		try:
			# Get the current configuration for the addon
			conf = config.conf[ourAddon.name]

			# Load the index for the selected path
			self.index_json = int(conf.get("xx", 0))

			# Load the primary and alternate paths
			self.first_json_file = conf.get("path", self.default_path)
			self.alt_json_file = conf.get("altPath", "") # altPath can legitimately be empty
			self.browser_path = conf.get("browserPath", "")  # Carrega caminho do navegador

			# Ensure first_json_file is never empty, fallback to default_path if it somehow became empty
			if not self.first_json_file:
				self.first_json_file = self.default_path

			log.debug(f"[{ourAddon.name}] JsonConfig loaded: index={self.index_json}, primary='{self.first_json_file}', alternate='{self.alt_json_file}'")

		except ValueError:
			log.error(f"[{ourAddon.name}] Invalid value for JSON index in configuration, using default: {self.default_path}")
			self.browser_path = ""
			self.first_json_file = self.default_path
			self.alt_json_file = ""
			self.index_json = 0
		except KeyError:
			log.warning(f"[{ourAddon.name}] JSON configuration not found, initializing with default paths.")
			self.first_json_file = self.default_path
			self.alt_json_file = ""
			self.index_json = 0
		except Exception as e:
			log.error(f"[{ourAddon.name}] Unexpected error loading JSON config: {e}")
			self.browser_path = ""
			self.first_json_file = self.default_path
			self.alt_json_file = ""
			self.index_json = 0


	def save_config(self):
		config.conf[ourAddon.name]["browserPath"] = self.browser_path
		config.conf[ourAddon.name]["path"] = self.first_json_file
		config.conf[ourAddon.name]["altPath"] = self.alt_json_file
		config.conf[ourAddon.name]["xx"] = str(self.index_json)
		log.debug(f"[{ourAddon.name}] JsonConfig saved: index={self.index_json}, primary='{self.first_json_file}', alternate='{self.alt_json_file}'")

	def set_json_path(self, new_path, is_first=True):
		"""Sets the primary or alternate JSON file path."""
		if is_first:
			self.first_json_file = new_path
		else:
			self.alt_json_file = new_path
		log.debug(f"[{ourAddon.name}] JsonConfig path set: {'primary' if is_first else 'alternate'} to '{new_path}'")


	def get_current_json_path(self):
		"""Returns the currently active JSON file path based on the index."""
		current_path = self.first_json_file if self.index_json == 0 else self.alt_json_file
		if not current_path: # Fallback in case the selected path is unexpectedly empty
			log.warning(f"[{ourAddon.name}] Current JSON path is empty, falling back to default: {self.default_path}")
			return self.default_path
		return current_path

	def update_json_file_path(self, new_path):
		"""
		Updates the internal JSON path and handles file renaming if necessary.
		"""
		old_active_path = self.get_current_json_path()
		
		# Update the path based on the current selection index
		if self.index_json == 0:
			self.set_json_path(new_path, is_first=True)
		else:
			self.set_json_path(new_path, is_first=False)

		# Check if renaming is needed (if old path exists, new path doesn't, and paths are different)
		if os.path.exists(old_active_path) and not os.path.exists(new_path) and old_active_path != new_path:
			try:
				import shutil
				shutil.move(old_active_path, new_path)
				log.info(f"[{ourAddon.name}] Renamed JSON file from '{old_active_path}' to '{new_path}'")
			except Exception as e:
				log.error(f"[{ourAddon.name}] Error renaming JSON file from '{old_active_path}' to '{new_path}': {e}")
		else:
			log.info(f"[{ourAddon.name}] JSON file path updated to '{new_path}'. No rename needed or file already exists/didn't exist.")


# Global instance of the JSON configuration manager
# This path should ideally be in a user-specific data directory, but
# using os.path.dirname(__file__) ensures it's relative to the addon.
json_config = JsonConfig(default_path=os.path.join(os.path.dirname(__file__), "favorite_links.json"))
