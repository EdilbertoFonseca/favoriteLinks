# -*- coding: UTF-8 -*-

# Description: Module for add-on settings panel
# Author: Edilberto Fonseca
# Email: edilberto.fonseca@outlook.com
# Date of creation: 24/05/2024

import logging
import os

import addonHandler
import config
import gui
import wx
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel

from .varsConfig import initConfiguration, ourAddon

# Logger configuration
logger = logging.getLogger(__name__)

# Start addon translation
addonHandler.initTranslation()

# Initialize settings
initConfiguration()

# Get the addon summary
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Initializing path and index variables
dirJsonFile = os.path.join(os.path.dirname(__file__), "favorite_links.json")
firstJsonFile = ""
altJsonsFile = ""
indexJson = 0
try:
	if config.conf[ourAddon.name]["xx"]:
		# index of Favorite Links.db file to use
		indexJson = int(config.conf[ourAddon.name]["xx"])
		if indexJson == 0:
			dirJsonFile = config.conf[ourAddon.name]["path"]
		else:
			dirJsonFile = config.conf[ourAddon.name]["altPath"]
		firstJsonFile = config.conf[ourAddon.name]["path"]
		altJsonsFile = config.conf[ourAddon.name]["altPath"]
except:
	# Not registered, so use the default path
	pass


class FavoriteLinksSettingsPanel(SettingsPanel):
	title = ADDON_SUMMARY

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		pathBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=_("Path of json files:"))
		pathGroup = guiHelper.BoxSizerHelper(self, sizer=pathBoxSizer)
		settingsSizerHelper.addItem(pathGroup)

		# Translators: Name of combobox with the Favorite Links files path
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

		# Translators: This is the label for the button used to add or change a Favorite Links.db location
		changePathBtn = wx.Button(pathBox, label=_("&Select or add a directory"))
		changePathBtn.Bind(wx.EVT_BUTTON, self.OnDirectory)

	def OnDirectory(self, event):
		self.Freeze()
		global dirJsonFile, firstJsonFile, altJsonsFile, indexJson
		lastDir = os.path.dirname(__file__)
		dDir = lastDir
		dFile = "favorite_links.json"
		frame = wx.Frame(None, -1, 'teste')
		frame.SetSize(0, 0, 200, 50)
		dlg = wx.FileDialog(
			frame,
			_("Choose where to save the json file"),
			dDir,
			dFile,
			wildcard=_("Json files (*.json)"),
			style=wx.FD_SAVE
		)
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
		dlg.Close()
		self.onPanelActivated()
		self._sendLayoutUpdatedEvent()
		self.Thaw()
		event.Skip()

	def onSave(self):
		"""
		Saves the options to the NVDA configuration file.
		"""

		global dirJsonFile, firstJsonFile, altJsonsFile, indexJson

		# Checking paths before saving
		if not firstJsonFile or not os.path.exists(os.path.dirname(firstJsonFile)):
			logger.error(f"Invalid path: {firstJsonFile}")
			raise ValueError("Invalid path for the first JSON file.")

		if altJsonsFile and not os.path.exists(os.path.dirname(altJsonsFile)):
			logger.error(f"Invalid path: {altJsonsFile}")
			raise ValueError("Invalid path for the alternative JSON file.")

		config.conf[ourAddon.name]["path"] = firstJsonFile
		config.conf[ourAddon.name]["altPath"] = altJsonsFile
		config.conf[ourAddon.name]["xx"] = str(self.pathNameCB.GetSelection())
		indexJson = self.pathNameCB.GetSelection()
		dirJsonFile = self.pathList[indexJson]
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()
		self.Hide()

	def onPanelActivated(self):
		"""
		Deactivate all profile triggers and active profiles
		"""

		config.conf.disableProfileTriggers()
		self.Show()

	def onPanelDeactivated(self):
		"""
		Reactivate profiles triggers
		"""

		config.conf.enableProfileTriggers()
		self.Hide()

	def terminate(self):
		super(FavoriteLinksSettingsPanel, self).terminate()
		self.onPanelDeactivated()
