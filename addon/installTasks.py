# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 03/03/2023.
"""

import os

import addonHandler
import globalVars
from gui import messageBox

# Initialize translation support
addonHandler.initTranslation()

# Get the name of the addon defined in the manifest.
ADDON_name = addonHandler.getCodeAddon().manifest["name"]


def onInstall():
	"""
	Moves the add-on's json file to a new location during installation.
	"""

	configPath = globalVars.appArgs.configPath
	if not configPath:
		return

	relativeJsonPath = os.path.join(
		"addons",
		"favoriteLinks",
		"globalPlugins",
		"favoriteLinks",
		"favorite_links.json",
	)
	absoluteJsonPath = os.path.abspath(os.path.join(configPath, relativeJsonPath))

	if os.path.isfile(absoluteJsonPath):
		addonRelativePath = os.path.join("addons", "favoriteLinks")
		jsonRelativeSuffix = os.path.join("globalPlugins", "favoriteLinks", "favorite_links.json")
		newJsonPath = os.path.join(
			configPath,
			addonRelativePath + addonHandler.ADDON_PENDINGINSTALL_SUFFIX,
			jsonRelativeSuffix,
		)

		try:
			os.rename(absoluteJsonPath, os.path.abspath(newJsonPath))
		except OSError as e:
			messageBox(_("Error when renaming file: {}").format(e), _("Attention"))
