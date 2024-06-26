# -*- coding: UTF-8 -*-

# Description: Module for add-on settings panel
# Author: Edilberto Fonseca
# Email: edilberto.fonseca@outlook.com
# Date of creation: 24/05/2024

# Import the necessary modules
import logging
import os

import addonHandler
import config
import gui
import wx
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel

from .varsConfig import initConfiguration, ourAddon

# Configure the logger instance for the current module, allowing logging of log messages.
logger = logging.getLogger(__name__)

# To start the translation process
addonHandler.initTranslation()

# Initialize configuration settings
initConfiguration()

# Get the title of the addon defined in the summary
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Read configuration from INI file
dirJsonFile = os.path.join(os.path.dirname(__file__), "favorite_links.json")
firstJsonFile = ""
altJsonsFile = ""
indexJson = 0
try:
	if config.conf[ourAddon.name]["xx"]:
		# Index of the favorite_links.json file to use
		indexJson = int(config.conf[ourAddon.name]["xx"])
		if indexJson == 0:
			dirJsonFile = config.conf[ourAddon.name]["path"]
		else:
			dirJsonFile = config.conf[ourAddon.name]["altPath"]
		firstJsonFile = config.conf[ourAddon.name]["path"]
		altJsonsFile = config.conf[ourAddon.name]["altPath"]
except FileNotFoundError:
	# Not registered, so use the default path
	pass


class FavoriteLinksSettingsPanel(SettingsPanel):
	# Translators: Title of the Favorite Links settings dialog in the NVDA settings.
	title = ADDON_SUMMARY

	def makeSettings(self, settingsSizer):
		"""
		Creates the settings panel UI.
		"""
		try:
			settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
			# Translators: Name of combobox with the json files path
			pathBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=_("Path of json files:"))
			pathBox = pathBoxSizer.GetStaticBox()
			pathGroup = guiHelper.BoxSizerHelper(self, sizer=pathBoxSizer)
			settingsSizerHelper.addItem(pathGroup)
			global firstJsonFile
			if firstJsonFile == "":
				firstJsonFile = dirJsonFile
			self.pathList = [firstJsonFile, altJsonsFile]
			self.pathNameCB = pathGroup.addLabeledControl("", wx.Choice, choices=self.pathList)
			self.pathNameCB.SetSelection(indexJson)
			# Translators: This is the label for the button used to add or change a favorite_links.json location
			changePathBtn = wx.Button(pathBox, label=_("&Select or add a directory"))
			changePathBtn.Bind(wx.EVT_BUTTON, self.OnDirectory)
		except Exception as e:
			logger.error(f"Error creating settings UI: {e}")

	def OnDirectory(self, event):
		"""
		Handles the directory selection for saving the favorite_links.json file.
		"""
		self.Freeze()
		global dirJsonFile, firstJsonFile, altJsonsFile, indexJson
		lastDir = os.path.dirname(__file__)
		dDir = lastDir
		dFile = "favorite_links.json"
		frame = wx.Frame(None, -1, 'teste')
		frame.SetSize(0, 0, 200, 50)
		try:
			with wx.FileDialog(
				frame,
				_("Choose where to save the json file"),
				dDir,
				dFile,
				wildcard=_("Json files (*.json)"),
				style=wx.FD_SAVE
			) as dlg:
				if dlg.ShowModal() == wx.ID_OK:
					fname = dlg.GetPath()
					index = self.pathNameCB.GetSelection()
					if index == 0:
						if os.path.exists(fname):
							firstJsonFile = fname
						else:
							os.rename(firstJsonFile, fname)
							firstJsonFile = fname
					else:
						if os.path.exists(fname):
							altJsonsFile = fname
						else:
							if altJsonsFile == "":
								altJsonsFile = fname
							else:
								os.rename(altJsonsFile, fname)
								altJsonsFile = fname
					dirJsonFile = fname
					self.pathList = [firstJsonFile, altJsonsFile]
		except Exception as e:
			logger.error(f"Error handling directory selection: {e}")
		self.onPanelActivated()
		self._sendLayoutUpdatedEvent()
		self.Thaw()
		event.Skip()

	def onSave(self):
		"""
		Saves the settings to the INI file.
		"""

		config.conf[ourAddon.name]["path"] = firstJsonFile
		config.conf[ourAddon.name]["altPath"] = altJsonsFile
		config.conf[ourAddon.name]["xx"] = str(self.pathList.index(self.pathNameCB.GetStringSelection()))
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()

	def onPanelActivated(self):
		"""
		Handles the activation of the settings panel.
		"""
		# Deactivate all profile triggers and active profiles
		config.conf.disableProfileTriggers()
		self.Show()

	def onPanelDeactivated(self):
		"""
		Handles the deactivation of the settings panel.
		"""
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()
		self.Hide()

	def terminate(self):
		"""
		Clean up when the panel is terminated.
		"""
		super(FavoriteLinksSettingsPanel, self).terminate()
		self.onPanelDeactivated()
