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
import webbrowser
import wx
from gui import mainFrame
from logHandler import log
from scriptHandler import script

from .configPanel import FavoriteLinksSettingsPanel
from .fromClipboard import FromClipboard
from .main import FavoriteLinks
from .searchLinks import SearchLinks
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
	except AttributeError:
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
			self.dlg.CentreOnScreen()
			self.dlg.Show()
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

	@script(
		gesture="kb:NVDA+shift+g",
		# Translators: Description shown in NVDA input gestures for opening the search links dialog.
		description=_("Search saved links by name or URL."),
		category=ADDON_SUMMARY
	)
	def script_searchLinks(self, gesture):
		"""
		Opens the Search Links dialog, which lets the user search for saved
		links by their display name or URL within a selected category.

		Inspired by the Link Manager add-on by Abdallah Hader:
		https://github.com/abdallah-hader/linkManager

		Args:
			gesture (kb): Triggered by NVDA+Shift+G.
		"""
		def open_dialog():
			from .linkManager import LinkManager as _LM
			lm = _LM()
			if not lm.data:
				# Translators: Spoken when there are no saved links to search.
				ui.message(_("No categories found. Please add some links first."))
				return
			dlg = SearchLinks(mainFrame, lm)
			gui.mainFrame.prePopup()
			try:
				dlg.CentreOnScreen()
				dlg.ShowModal()
			finally:
				gui.mainFrame.postPopup()
				dlg.Destroy()
		wx.CallAfter(open_dialog)

	@script(
		gesture="kb:nvda+z",
		# Translators: Description shown in NVDA input gestures for opening a URL from the clipboard.
		description=_("Open a URL from the clipboard."),
		category=ADDON_SUMMARY
	)
	def script_openFromClipboard(self, gesture):
		"""
		Reads URLs from the clipboard and either opens the single URL directly
		or shows a picker dialog when multiple URLs are found.

		Args:
			gesture (kb): Triggered by NVDA+Z.
		"""
		def _open():
			from .linkManager import LinkManager
			try:
				clipboard_text = api.getClipData()
			except OSError as e:
				log.error("Error reading clipboard: %s", e)
				# Translators: Spoken when the clipboard cannot be read.
				ui.message(_("Unable to read the clipboard."))
				return
			urls = LinkManager.extract_urls_from_text(clipboard_text)
			urls = [("https://" + u if u.lower().startswith("www.") else u) for u in urls]
			if not urls:
				# Translators: Spoken when the clipboard holds no recognisable URL.
				ui.message(_("The clipboard does not contain any links."))
				return
			if len(urls) == 1:
				try:
					webbrowser.open(urls[0])
					# Translators: Spoken when a single clipboard URL is opened.
					ui.message(_("Opening {url}.").format(url=urls[0]))
				except Exception as e:
					log.error("Error opening clipboard URL: %s", e)
					# Translators: Spoken when a clipboard URL cannot be opened.
					ui.message(_("Unable to open the link. Please check your browser settings."))
				return
			dlg = FromClipboard(mainFrame, urls)
			gui.mainFrame.prePopup()
			try:
				dlg.CentreOnScreen()
				dlg.ShowModal()
			finally:
				gui.mainFrame.postPopup()
				dlg.Destroy()
		wx.CallAfter(_open)

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
