# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 11/04/2024.
"""

import addonHandler
import api
import globalPluginHandler
import globalVars
import gui
import scriptHandler
import ui
import wx
from gui import mainFrame
from logHandler import log
from scriptHandler import script

from .addLinks import AddLinks
from .configPanel import FavoriteLinksSettingsPanel
from .main import FavoriteLinks 
from .varsConfig import ADDON_SUMMARY, initConfiguration

# Initialize translation support
addonHandler.initTranslation()

# Initialize configuration settings
initConfiguration()

# Function copied from: robEnhancements (NVDA add-on)
# Original source: start.py
# License: GNU GPL v2.0 – https://www.gnu.org/licenses/gpl-2.0.html
# Repository: https://github.com/rainerbrell/robenhancements/
def isBrowser():
	"""
	 Verifies that NVDA is in a browser.
	"""
	obj = api.getFocusObject()
	if obj.treeInterceptor:
		return True
	else:
		return False

# Function copied from: robEnhancements (NVDA add-on)
# Original source: start.py
# License: GNU GPL v2.0 – https://www.gnu.org/licenses/gpl-2.0.html
# Repository: https://github.com/rainerbrell/robenhancements/
def getCurrentDocumentURL():
	""" 
			Get current masked document URL 
	"""
	URL = None
	obj = api.getFocusObject()
	try:
		URL = obj.treeInterceptor.documentConstantIdentifier
	except:
		return None
	return URL


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
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
			FavoriteLinksSettingsPanel)

		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Add-on title in the tools menu.
		self.favoriteLinks = self.toolsMenu.Append(
			wx.ID_ANY, _("&Favorite links..."))
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_activateFavoriteLinks, self.favoriteLinks)

	def onFavoriteLinks(self, event):
		"""
		Handler for displaying the Favorite Links dialog.

		Args:
				evt (wx.Event): The event triggered by the favoriteLinks button.
		"""

		try:
			# Translators: Dialog title Favorite Links
			self.dlg = FavoriteLinks(mainFrame, _("Favorite links."))
			gui.mainFrame.prePopup()
			self.dlg.Show()
			self.dlg.CentreOnScreen()
			gui.mainFrame.postPopup()
		except Exception as e:
			log.error("Error displaying Favorite Links dialog: %s", e)

	def onAddLinks(self):
		"""
		Calls the dialog for adding a new link.

		Args:
			event (wx.Event): The event triggered by the add link button.
		"""

		add_links = FavoriteLinks

		try:
			gui.mainFrame.prePopup()
			add_links.onAddLink
			gui.mainFrame.postPopup()
		except Exception as e:
			log.error("Error displaying Favorite Links dialog: %s", e)

	# defining a script with decorator:
	@script(
		gesture="kb:Windows+alt+K",
		# Translators: Text displayed in NVDA help
		description=_(
				"This addon allows you to save links to a specific page."),
		category=ADDON_SUMMARY
	)
	def script_activateFavoriteLinks(self, gesture):
		"""
		Script to activate the Favorite Links dialog.

		Args:
				gesture (kb): Triggered by the shortcut "windows+alt+K".
		"""
		wx.CallAfter(self.onFavoriteLinks, None)

	# defining a script with decorator:
	@script(
		gesture="kb:Windows+Control+P",
		# Translators: Shows the current URL of the document, press twice = copies to the clipboard.
		description=_("Show document URL, press twice copies to clipboard."),
		category=ADDON_SUMMARY
	)
	def script_ShowDocumentURL(self, gesture):
		if isBrowser():
			URL = getCurrentDocumentURL()
			if URL:
				if scriptHandler.getLastScriptRepeatCount() == 0:
					ui.message(URL)
				elif scriptHandler.getLastScriptRepeatCount() == 1:
					api.copyToClip(URL)
					# Translators: URL copied to clipboard
					ui.message(_("Copied to clipboard {URL}.").format(URL=URL))
			else:
				# Translators: No URL found in browser document
				ui.message(_("Document URL not found."))
		else:
			# Translators: The user is not in a browser.
			ui.message(_("No browser window found."))

	def terminate(self):
		"""
		Clean up when the plugin is terminated.
		"""
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
			FavoriteLinksSettingsPanel)
		if hasattr(self, 'favoriteLinks'):
			try:
				self.toolsMenu.Remove(self.favoriteLinks)
			except Exception as e:
				log.warning("Error removing Favorite Links menu item: %s", e)
