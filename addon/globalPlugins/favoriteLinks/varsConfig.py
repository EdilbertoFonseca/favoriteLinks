# -*- coding: UTF-8 -*-

# Description: Variables for the Favorite links add-on
# Author: Edilberto Fonseca
# Email: edilberto.fonseca@outlook.com
# Date of creation: 24/05/2024

# Import the necessary modules
import logging

import addonHandler
import config

# Configure the logger instance for the current module, allowing logging of log messages.
logger = logging.getLogger(__name__)

# To start the translation process
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
		logger.error(f"Error getting the add-on: {e}")
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
		logger.error(f"Error initializing configuration: {e}")
		raise RuntimeError(f"Error initializing configuration: {e}")


# Initialize the configuration
initConfiguration()
