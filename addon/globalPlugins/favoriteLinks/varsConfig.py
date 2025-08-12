# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 24/05/2024
"""

import os

import addonHandler
import config
from logHandler import log

# Initialize translation support
addonHandler.initTranslation()

# Get the path to the root of the current add-on
addonPath = os.path.dirname(__file__)

# Get the title of the addon defined in the summary
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]
ADDON_DESCRIPTION = addonHandler.getCodeAddon().manifest["description"]

def getOurAddon():
	"""
	Retrieves the current add-on.
	Returns:
		addonHandler.Addon: The current add-on instance.
	"""
	try:
		return addonHandler.getCodeAddon()
	except Exception as e:
		log.error("Error getting the add-on: {}".format(e))
		raise RuntimeError("Error getting the add-on: {}".format(e))


# Retrieve the current add-on instance
ourAddon = getOurAddon()


def initConfiguration():
	"""
	Initializes the configuration specification for the add-on.
	"""
	try:
		confspec = {
			"browserPath": "string(default='')",
			"path": "string(default='')",
			"altPath": "string(default='')",
			"xx": "string(default='')",
		}
		config.conf.spec[ourAddon.name] = confspec
	except Exception as e:
		log.error("Error initializing configuration: {}".format(e))
		raise RuntimeError("Error initializing configuration: {}".format(e))


# Initialize the configuration
initConfiguration()
