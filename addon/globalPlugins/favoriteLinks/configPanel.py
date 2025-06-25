# -*- coding: UTF-8 -*-

# Description: Module for add-on settings panel

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2024-2025 Edilberto Fonseca

# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation: 24/05/2024

# Import the necessary modules
import os

import addonHandler
import config
import gui
import wx
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel
from logHandler import log

from .varsConfig import ADDON_SUMMARY, ourAddon, initConfiguration

# Initializes the translation
addonHandler.initTranslation()

# Initialize settings
initConfiguration()

# Initializing path and index variables
dirJsonFile = os.path.join(os.path.dirname(__file__), "favorite_links.json")
firstJsonFile = ""
altJsonsFile = ""
indexJson = 0
pathList = []


class FavoriteLinksSettingsPanel(SettingsPanel):
	title = ADDON_SUMMARY

	def makeSettings(self, settingsSizer):
		# Initializing variables with default values
		self.dirJsonFile = dirJsonFile

		# Initializing JSON file paths
		self.firstJsonFile = firstJsonFile
		self.altJsonsFile = altJsonsFile
		self.indexJson = indexJson
		self.pathList = pathList

		# Load settings from files or use default values
		try:
			if config.conf[ourAddon.name]["xx"]:
				self.indexJson = int(config.conf[ourAddon.name]["xx"])
				if self.indexJson == 0:
					self.firstJsonFile = config.conf[ourAddon.name]["path"]
				else:
					self.firstJsonFile = config.conf[ourAddon.name]["altPath"]
				self.altJsonsFile = config.conf[ourAddon.name]["altPath"]
		except KeyError:
			# In case of error, use default values
			self.firstJsonFile = os.path.join(os.path.dirname(__file__), "favorite_links.json")
			self.altJsonsFile = ""

		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		pathBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=_("Path of json files:"))
		pathGroup = guiHelper.BoxSizerHelper(self, sizer=pathBoxSizer)
		settingsSizerHelper.addItem(pathGroup)
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		pathBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=_("Path of json files:"))
		pathGroup = guiHelper.BoxSizerHelper(self, sizer=pathBoxSizer)
		settingsSizerHelper.addItem(pathGroup)

		# Now initializing pathList correctly
		self.pathList = [self.firstJsonFile, self.altJsonsFile]

		# If pathList is still empty or contains invalid values, initialize with default paths
		if not self.pathList or not os.path.exists(self.firstJsonFile):
			self.pathList = [self.firstJsonFile, self.altJsonsFile]

		# Translators: Name of combobox with the Favorite Links files path
		pathBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label=_("Path of json files:"))
		pathBox = pathBoxSizer.GetStaticBox()
		pathGroup = guiHelper.BoxSizerHelper(self, sizer=pathBoxSizer)
		settingsSizerHelper.addItem(pathGroup)
		self.pathNameCB = pathGroup.addLabeledControl("", wx.Choice, choices=self.pathList)
		self.pathNameCB.SetSelection(self.indexJson)

		# Translators: This is the label for the button used to add or change a Favorite Links.db location
		changePathBtn = wx.Button(pathBox, label=_("&Select or add a directory"))
		changePathBtn.Bind(wx.EVT_BUTTON, self.OnDirectory)

	def OnDirectory(self, event):
		self.Freeze()
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
					self.firstJsonFile = fname
				else:
					os.rename(self.firstJsonFile, fname)
					self.firstJsonFile = fname
			else:
				if os.path.exists(fname):
					self.altJsonsFile = fname
				else:
					if self.altJsonsFile == "":
						self.altJsonsFile = fname
					else:
						os.rename(self.altJsonsFile, fname)
						self.altJsonsFile = fname
			self.dirJsonFile = fname

			# Update the combobox choices and selection
			self.pathList = [self.firstJsonFile, self.altJsonsFile]
			self.pathNameCB.Set(self.pathList)
			self.pathNameCB.SetSelection(index)

		dlg.Close()
		self.onPanelActivated()
		self._sendLayoutUpdatedEvent()
		self.Thaw()
		event.Skip()

	def onSave(self):
		"""
Saves the options to the NVDA configuration file.

		Raises:
			ValueError: If the path to the first JSON file is invalid or does not exist.
			ValueError: If the path to the alternate JSON file is invalid or does not exist.
		"""

		global dirJsonFile, firstJsonFile, altJsonsFile, indexJson

		# Check paths before saving
		#if not firstJsonFile or not os.path.exists(os.path.dirname(firstJsonFile)):
			#logger.error(f"Invalid path: {firstJsonFile}")
			#raise ValueError("Invalid path for the first JSON file.")

		if altJsonsFile and not os.path.exists(os.path.dirname(altJsonsFile)):
			log.error(f"Invalid path: {altJsonsFile}")
			raise ValueError("Invalid path for the alternative JSON file.")

		config.conf[ourAddon.name]["path"] = self.firstJsonFile
		config.conf[ourAddon.name]["altPath"] = self.altJsonsFile
		config.conf[ourAddon.name]["xx"] = str(self.pathNameCB.GetSelection())
		indexJson = self.pathNameCB.GetSelection()
		dirJsonFile = self.pathList[	indexJson]
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()

	def onPanelActivated(self):
		config.conf.disableProfileTriggers()
		self.Show()

	def onPanelDeactivated(self):
		config.conf.enableProfileTriggers()
		self.Hide()

	def terminate(self):
		super(FavoriteLinksSettingsPanel, self).terminate()
		self.onPanelDeactivated()
