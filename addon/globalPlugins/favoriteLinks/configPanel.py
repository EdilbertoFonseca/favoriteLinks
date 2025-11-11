# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 24/01/2023.
"""

import os

import addonHandler
import config
import gui
import wx
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel

from .jsonConfig import json_config  # Import the new json_config instance
from .varsConfig import ADDON_SUMMARY

# Initialize translation support
addonHandler.initTranslation()


class FavoriteLinksSettingsPanel(SettingsPanel):
	title = ADDON_SUMMARY

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
				# JSON File Path Settings (MODIFIED)
		pathBoxSizer = wx.StaticBoxSizer(
			wx.HORIZONTAL, self, label=_("Path of file json:")
		)
		pathBox = pathBoxSizer.GetStaticBox()
		pathGroup = guiHelper.BoxSizerHelper(self, sizer=pathBoxSizer)
		settingsSizerHelper.addItem(pathGroup)

		# Populate pathList from json_config
		self.pathList = [json_config.first_json_file]
		if json_config.alt_json_file:
			self.pathList.append(json_config.alt_json_file)

		# Ensure pathList is not empty if both paths are empty (shouldn't happen with json_config)
		if not self.pathList:
			self.pathList.append(json_config.default_path)

		self.pathNameCB = pathGroup.addLabeledControl("", wx.Choice, choices=self.pathList)
		# Set selection, ensuring it's within bounds of current pathList
		self.pathNameCB.SetSelection(min(json_config.index_json, len(self.pathList) - 1))

		changePathBtn = wx.Button(pathBox, label=_("&Select or add a directory"))
		pathGroup.sizer.Add(changePathBtn, 0, wx.ALL, 5) # Add button to sizer
		changePathBtn.Bind(wx.EVT_BUTTON, self.onDirectory)

		# Browser Path Settings (NEW)
		browserPathBoxSizer = wx.StaticBoxSizer(
			wx.HORIZONTAL, self, label=_("Secondary browser path:")
		)
		browserPathBox = browserPathBoxSizer.GetStaticBox()
		browserPathGroup = guiHelper.BoxSizerHelper(self, sizer=browserPathBoxSizer)
		settingsSizerHelper.addItem(browserPathGroup)

		# Assume we store the browser path in json_config
		self.browserPath = json_config.browser_path or ''  # Fallback to empty string if not set
		self.browserPathCB = browserPathGroup.addLabeledControl("", wx.TextCtrl, value=self.browserPath)

		# Button to select the browser path
		changeBrowserPathBtn = wx.Button(browserPathBox, label=_("Select &browser path"))
		browserPathGroup.sizer.Add(changeBrowserPathBtn, 0, wx.ALL, 5)  # Add button to sizer
		changeBrowserPathBtn.Bind(wx.EVT_BUTTON, self.onSelectBrowserPath)

	def onDirectory(self, event):
		"""
		Selects a directory to save the Favorite Links JSON file.
		"""
		self.Freeze() # Freeze UI updates for performance

		try:
			# Use gui.mainFrame as the parent for the FileDialog
			frame = gui.mainFrame
			
			# Get initial directory and filename for the dialog
			current_path = json_config.get_current_json_path()
			initial_dir = os.path.dirname(current_path) if current_path else os.path.dirname(__file__)
			initial_file = os.path.basename(current_path) if current_path else "favorite_links.json"

			dlg = wx.FileDialog(
				frame,
				_("Choose where to save the file json"),
				initial_dir,
				initial_file,
				wildcard=_("JSON files (*.json)|*.json"),
				style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT # Add overwrite prompt
			)

			if dlg.ShowModal() == wx.ID_OK:
				fname = dlg.GetPath()
				current_selection_index = self.pathNameCB.GetSelection()

				# Update json_config internal state
				json_config.index_json = current_selection_index
				json_config.update_json_file_path(fname) # Let json_config handle file renaming/path updates

				# Refresh the wx.Choice control with updated paths from json_config
				self.pathList = [json_config.first_json_file]
				if json_config.alt_json_file:
					self.pathList.append(json_config.alt_json_file)
				
				# Ensure pathList is not empty
				if not self.pathList:
					self.pathList.append(json_config.default_path)

				self.pathNameCB.Set(self.pathList)
				self.pathNameCB.SetSelection(current_selection_index) # Keep current selection

				# Re-activate panel and update layout (might not be strictly necessary, but good practice)
				self.onPanelActivated()
				self._sendLayoutUpdatedEvent()

		finally:
			dlg.Destroy() # Destroy the dialog
			self.Thaw() # Unfreeze UI updates
			event.Skip() # Allow default event processing

	def onSelectBrowserPath(self, event):
		"""
Select the browser path.
		"""
		self.Freeze()  # Freeze UI updates for performance

		try:
			# Use gui.mainFrame as the parent for the FileDialog
			frame = gui.mainFrame
			
			# Use wx.FileDialog to let the user select the browser's executable
			dlg = wx.FileDialog(
				frame,
				_("Choose browser path"),
				style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
				wildcard=_("Executable files (*.exe)|*.exe"),
			)

			if dlg.ShowModal() == wx.ID_OK:
				selectedPath = dlg.GetPath()
				self.browserPath = selectedPath  # Update the browser path

				# Update the text field with the selected path
				self.browserPathCB.SetValue(selectedPath)

				# Update the configuration
				json_config.browser_path = selectedPath  # Assume json_config has browser_path

		finally:
			dlg.Destroy()  # Destroy the dialog
			self.Thaw()  # Unfreeze UI updates
			event.Skip()  # Allow default event processing

	def onSave(self):
		"""
		Saves the options to the NVDA configuration file.
		"""
		# Update selected index and save paths using json_config
		json_config.index_json = self.pathNameCB.GetSelection()
		json_config.save_config() # This call saves the path and altPath to config.conf

		# Save browser path
		json_config.browser_path = self.browserPath  # Save browser path
		json_config.save_config()  # Save again to update browser_path

		# Reactivate profiles triggers (important for NVDA config system)
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
