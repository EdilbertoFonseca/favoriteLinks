# -*- coding: UTF-8 -*-

# Description: This script is part of a simple contact book add-on for NVDA (NonVisual Desktop Access).
#              It handles the installation process by moving the existing database file to a new location.
#              The script checks if the database file exists in the current configuration path and renames
#              it to ensure compatibility with pending installations.
# Author: Edilberto Fonseca.
# Email: edilberto.fonseca@outlook.com.
# Date of creation: 03/03/2023.

import os

import addonHandler
import globalVars
from gui import messageBox

# For translation process
addonHandler.initTranslation()


def onInstall():
	"""
	Move o arquivo json do add-on para um novo local durante a instalação.
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
