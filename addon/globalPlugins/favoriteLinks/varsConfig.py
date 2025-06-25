# -*- coding: UTF-8 -*-

# Description:# Variables for the Favorite links add-on

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2022-2025 Edilberto Fonseca

# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation: 24/05/2024

# Import the necessary modules
import addonHandler
import config
from logHandler import log

# Get the title of the addon defined in the summary
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Initializes the translation
addonHandler.initTranslation()

def getOurAddon():
	"""
	Retrieves the current add-on.
	Returns:
		addonHandler.Addon: The current add-on instance.
	"""
	try:
		return addonHandler.getCodeAddon()
	except Exception as e:
		log.error(f"Error getting the add-on: {e}")
		raise RuntimeError(f"Error getting the add-on: {e}")


# Retrieve the current add-on instance
ourAddon = getOurAddon()


def initConfiguration():
	"""
	Initializes the configuration specification for the add-on.
	"""
	try:
		confspec = {
			"path": "string(default='')",
			"altPath": "string(default='')",
			"xx": "string(default='')",
		}
		config.conf.spec[ourAddon.name] = confspec
	except Exception as e:
		log.error(f"Error initializing configuration: {e}")
		raise RuntimeError(f"Error initializing configuration: {e}")


# Initialize the configuration
initConfiguration()
