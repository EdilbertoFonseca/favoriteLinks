# -*- coding: UTF-8 -*-

# Description:
# This script is part of a simple contact book add-on for NVDA (NonVisual Desktop Access).
#              It handles the installation process by moving the existing database file to a new location.
#              The script checks if the database file exists in the current configuration path and renames
#              it to ensure compatibility with pending installations.

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2022-2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation: 03/03/2023.

import os

import addonHandler
import config
import globalVars
from gui import messageBox


# Initializes the translation
addonHandler.initTranslation()

# Get the name of the addon defined in the manifest.
ADDON_name = addonHandler.getCodeAddon().manifest["name"]


def onInstall():
	"""
	Moves the add-on's json file to a new location during installation.
	"""
	relativeJsonPath = os.path.join("addons", "favoriteLinks", "globalPlugins", "favoriteLinks", "favorite_links.json")
	absoluteJsonPath = os.path.abspath(os.path.join(globalVars.appArgs.configPath, relativeJsonPath))

	if os.path.isfile(absoluteJsonPath):
		configPath = globalVars.appArgs.configPath
		addonRelativePath = os.path.join("addons", "favoriteLinks")
		jsonRelativeSuffix = os.path.join("globalPlugins", "favoriteLinks", "favorite_links.json")
		newJsonPath = os.path.join(configPath, addonRelativePath + addonHandler.ADDON_PENDINGINSTALL_SUFFIX, jsonRelativeSuffix)

		try:
			os.rename(absoluteJsonPath, os.path.abspath(newJsonPath))
		except OSError as e:
			messageBox(_(f"Error when renaming file: {e}"), _("Attention"))

def onUninstall():
	# Go through the configuration profiles and try to remove the 'contactBook' key
	for key, value in list(config.conf._profileCache.items()):
		try:
			del config.conf._profileCache[key][ADDON_name]
		except KeyError:
			pass  # Ignore if key does not exist

	# Save configuration changes
	config.conf.save()
