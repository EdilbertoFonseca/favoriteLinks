# -*- coding: UTF-8 -*-

# Description: This add-on aims to: Save, edit and remove links from a list.

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2022-2025 Edilberto Fonseca

# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation: 11/04/2024.

# import the necessary modules.
import addonHandler
import globalPluginHandler
import globalVars
import gui
import wx
from logHandler import log
from scriptHandler import script

from .configPanel import FavoriteLinksSettingsPanel
from .main import FavoriteLinks
from .varsConfig import ADDON_SUMMARY, initConfiguration

# Initializes the translation
addonHandler.initTranslation()

# Initialize configuration settings
initConfiguration()


def disableInSecureMode(decoratedCls):
	"""
	Decorator to disable the plugin in secure mode.
	"""
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Global Plugin class for the Favorite Links addon."""

	def __init__(self):
		# Initialize the Global Plugin.
		super(GlobalPlugin, self).__init__()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(FavoriteLinksSettingsPanel)
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Add-on title in the tools menu.
		self.favoriteLinks = self.toolsMenu.Append(wx.ID_ANY, _("&Favorite links..."))
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_activateFavoriteLinks, self.favoriteLinks)

	def onFavoriteLinks(self, evt):
		"""
		Handler for displaying the Favorite Links dialog.

		Args:
			evt (wx.Event): The event triggered by the favoriteLinks button.
		"""

		try:
			# Translators: Dialog title Favorite Links
			self.dlg = FavoriteLinks(gui.mainFrame, _("Favorite links."))
			gui.mainFrame.prePopup()
			self.dlg.Show()
			self.dlg.CentreOnScreen()
			gui.mainFrame.postPopup()
		except Exception as e:
			log.error("Error displaying Favorite Links dialog: %s", e)

	@script(
		gesture="kb:Windows+alt+K",
		# Translators: Text displayed in NVDA help
		description=_("This addon allows you to save links to a specific page."),
		category=ADDON_SUMMARY
	)
	def script_activateFavoriteLinks(self, gesture):
		"""
		Script to activate the Favorite Links dialog.

		Args:
			gesture (kb): Triggered by the shortcut "windows+alt+K".
		"""
		wx.CallAfter(self.onFavoriteLinks, None)

	def terminate(self):
		"""
		Clean up when the plugin is terminated.
		"""
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(FavoriteLinksSettingsPanel)
		if hasattr(self, 'favoriteLinks'):
			try:
				self.toolsMenu.Remove(self.favoriteLinks)
			except Exception as e:
				log.warning("Error removing Favorite Links menu item: %s", e)
