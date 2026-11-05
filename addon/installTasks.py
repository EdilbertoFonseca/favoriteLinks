# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 - 2026 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 03/03/2023.
"""

import os
import shutil

import addonHandler
import globalVars
from logHandler import log

# Initialize translation support
addonHandler.initTranslation()

ADDON_NAME = addonHandler.getCodeAddon().manifest["name"]
JSON_FILENAME = "favorite_links.json"


def onInstall() -> None:
	"""
	Executes installation tasks for the addon.
	Migrates legacy JSON configuration file from the previous addon directory
	to the dedicated user configuration folder if present.
	"""
	configPath = globalVars.appArgs.configPath
	if not configPath:
		return

	# Path to the old JSON file in the currently installed addon directory
	oldJsonPath = os.path.join(
		configPath,
		"addons",
		ADDON_NAME,
		"globalPlugins",
		ADDON_NAME,
		JSON_FILENAME,
	)

	# Target directory and path inside user configuration (NVDA/favoriteLinks)
	targetDir = os.path.join(configPath, ADDON_NAME)
	targetJsonPath = os.path.join(targetDir, JSON_FILENAME)

	# If old file exists and target doesn't exist yet, perform the migration
	if os.path.isfile(oldJsonPath):
		try:
			# Ensure target directory exists before moving
			if not os.path.exists(targetDir):
				os.makedirs(targetDir, exist_ok=True)

			if not os.path.exists(targetJsonPath):
				shutil.move(oldJsonPath, targetJsonPath)
				log.info(
					f"[{ADDON_NAME}] Successfully migrated '{JSON_FILENAME}' "
					f"from '{oldJsonPath}' to '{targetJsonPath}'",
				)
			else:
				log.info(
					f"[{ADDON_NAME}] Configuration file already exists at '{targetJsonPath}'. "
					"Skipping migration.",
				)
		except Exception as e:
			log.error(f"[{ADDON_NAME}] Failed to migrate configuration file: {e}")
