# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 11/04/2024.
"""

import webbrowser

import addonHandler
import api
import config
import globalPluginHandler
import globalVars
import gui
import scriptHandler
import ui
import wx
from gui import mainFrame
from logHandler import log
from scriptHandler import script
from tones import beep

from .configPanel import FavoriteLinksSettingsPanel
from .fromClipboard import FromClipboard
from .linkManager import LinkManager
from .main import FavoriteLinks
from .searchLinks import SearchLinks
from .varsConfig import ADDON_SUMMARY, initConfiguration, ourAddon

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

		# Navigation state for keyboard browsing without opening the dialog.
		self._nav_category_index = 0
		self._nav_link_index = 0
		self._nav_link_manager = LinkManager()

	def _reload_nav_data(self):
		"""
		Reloads link data from the JSON file into the navigation link manager.
		Called after the main dialog closes so navigation reflects any changes.
		"""
		try:
			self._nav_link_manager.load_json()
			categories = list(self._nav_link_manager.data.keys())
			# Clamp indices to valid range after reload.
			if categories:
				self._nav_category_index = min(
					self._nav_category_index, len(categories) - 1
				)
				links = self._nav_link_manager.data.get(
					categories[self._nav_category_index], []
				)
				self._nav_link_index = min(
					self._nav_link_index, max(0, len(links) - 1)
				)
			else:
				self._nav_category_index = 0
				self._nav_link_index = 0
		except Exception as e:
			log.error("Error reloading navigation data: %s", e)

	def _get_nav_categories(self):
		"""
		Returns the list of category names from navigation link manager data.

		Returns:
			list: Sorted list of category name strings.
		"""
		return list(self._nav_link_manager.data.keys())

	def _announce_current_link(self):
		"""
		Announces the name of the currently selected link via NVDA speech.
		If the 'readUrlAfterName' option is enabled, the URL is also spoken.
		"""
		categories = self._get_nav_categories()
		if not categories:
			# Translators: Spoken when no categories or links have been saved yet.
			ui.message(_("No links saved."))
			return
		category = categories[self._nav_category_index]
		links = self._nav_link_manager.data.get(category, [])
		if not links:
			# Translators: Spoken when the current category contains no links.
			ui.message(_("No links in this category."))
			return
		title, url = links[self._nav_link_index]
		msg = title
		if config.conf[ourAddon.name]["readUrlAfterName"]:
			msg = msg + "  " + url
		ui.message(msg)

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
			# Reload navigation data so keyboard shortcuts reflect any changes
			# made in the dialog.
			self.dlg.Bind(wx.EVT_WINDOW_DESTROY, self._onDialogClosed)
		except Exception as e:
			log.error("Error displaying Favorite Links dialog: %s", e)

	def _onDialogClosed(self, event):
		"""
		Called when the Favorite Links dialog is destroyed.
		Reloads the navigation data so keyboard navigation stays in sync.

		Args:
			event (wx.Event): The window destroy event.
		"""
		event.Skip()
		self._reload_nav_data()

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
		gesture="kb:NVDA+Shift+G",
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
			try:
				lm = LinkManager()
			except Exception as e:
				log.error("Error loading link manager for search: %s", e)
				# Translators: Spoken when the link data file cannot be loaded.
				ui.message(_("Failed to load links. Please check the file."))
				return
			if not lm.data:
				# Translators: Spoken when there are no saved links to search, or when
				# the links file was corrupt and was automatically reset.
				ui.message(_("No saved links found. If you had links before, the links file may have been corrupt and was reset. Please add links to begin."))
				return
			try:
				dlg = SearchLinks(mainFrame, lm)
			except Exception as e:
				log.error("Error creating search dialog: %s", e)
				# Translators: Spoken when the search dialog cannot be opened.
				ui.message(_("Unable to open the search dialog."))
				return
			gui.mainFrame.prePopup()
			try:
				dlg.CentreOnScreen()
				dlg.ShowModal()
			finally:
				dlg.Destroy()
				gui.mainFrame.postPopup()
		wx.CallAfter(open_dialog)

	@script(
		# Translators: Description shown in NVDA input gestures for opening a URL from the clipboard.
		description=_("Open a URL from the clipboard."),
		category=ADDON_SUMMARY
	)
	def script_openFromClipboard(self, gesture):
		"""
		Reads URLs from the clipboard and either opens the single URL directly
		or shows a picker dialog when multiple URLs are found.
		No default gesture is assigned; use NVDA Input Gestures to bind a key.
		"""
		def _open():
			try:
				clipboard_text = api.getClipData()
			except OSError as e:
				log.error("Error reading clipboard: %s", e)
				# Translators: Spoken when the clipboard cannot be read.
				ui.message(_("Unable to read the clipboard."))
				return
			clipboard_text = clipboard_text or ""
			urls = LinkManager.extract_urls_from_text(clipboard_text)
			urls = [("https://" + u if u.lower().startswith("www.") else u) for u in urls]
			if not urls:
				# Translators: Spoken when the clipboard holds no recognisable URL.
				ui.message(_("The clipboard does not contain any links."))
				return
			if len(urls) == 1:
				try:
					opened = webbrowser.open(urls[0])
					if not opened:
						raise OSError("Browser failed to open URL")
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
				dlg.Destroy()
				gui.mainFrame.postPopup()
		wx.CallAfter(_open)

	# -----------------------------------------------------------------------
	# Keyboard navigation scripts (no dialog required)
	# Inspired by the Link Manager add-on by Abdallah Hader:
	# https://github.com/abdallah-hader/linkManager
	# -----------------------------------------------------------------------

	@script(
		gesture="kb:control+shift+f12",
		# Translators: Description shown in NVDA input gestures for moving to the next link.
		description=_("Move to the next saved link in the current category."),
		category=ADDON_SUMMARY
	)
	def script_nextLink(self, gesture):
		"""
		Moves the navigation cursor to the next link in the current category
		and announces its name. Plays a boundary tone at the last link.

		Args:
			gesture (kb): Triggered by Control+Shift+F12.
		"""
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(
			categories[self._nav_category_index], []
		)
		if not links:
			beep(200, 100)
			return
		if self._nav_link_index < len(links) - 1:
			self._nav_link_index += 1
		else:
			beep(250, 50)
		self._announce_current_link()

	@script(
		gesture="kb:control+shift+f11",
		# Translators: Description shown in NVDA input gestures for moving to the previous link.
		description=_("Move to the previous saved link in the current category."),
		category=ADDON_SUMMARY
	)
	def script_previousLink(self, gesture):
		"""
		Moves the navigation cursor to the previous link in the current category
		and announces its name. Plays a boundary tone at the first link.

		Args:
			gesture (kb): Triggered by Control+Shift+F11.
		"""
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(
			categories[self._nav_category_index], []
		)
		if not links:
			beep(200, 100)
			return
		if self._nav_link_index > 0:
			self._nav_link_index -= 1
		else:
			beep(200, 50)
		self._announce_current_link()

	@script(
		gesture="kb:control+shift+f10",
		# Translators: Description shown in NVDA input gestures for moving to the next category.
		description=_("Move to the next category of saved links."),
		category=ADDON_SUMMARY
	)
	def script_nextCategory(self, gesture):
		"""
		Moves the navigation cursor to the next category and announces its name
		along with the number of links it contains. Plays a boundary tone at
		the last category.

		Args:
			gesture (kb): Triggered by Control+Shift+F10.
		"""
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		if self._nav_category_index < len(categories) - 1:
			self._nav_category_index += 1
		else:
			beep(250, 50)
		# Reset link index to the first link of the new category.
		self._nav_link_index = 0
		category = categories[self._nav_category_index]
		links = self._nav_link_manager.data.get(category, [])
		count = len(links)
		# Translators: Announced when switching to a category; shows its name and link count.
		lnk_word = _("link") if count == 1 else _("links")
		ui.message(
			_("{category}: Contains {count} {lnk_word}").format(
				category=category, count=count, lnk_word=lnk_word
			)
		)

	@script(
		gesture="kb:control+shift+f9",
		# Translators: Description shown in NVDA input gestures for moving to the previous category.
		description=_("Move to the previous category of saved links."),
		category=ADDON_SUMMARY
	)
	def script_previousCategory(self, gesture):
		"""
		Moves the navigation cursor to the previous category and announces its
		name along with the number of links it contains. Plays a boundary tone
		at the first category.

		Args:
			gesture (kb): Triggered by Control+Shift+F9.
		"""
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		if self._nav_category_index > 0:
			self._nav_category_index -= 1
		else:
			beep(200, 50)
		# Reset link index to the first link of the new category.
		self._nav_link_index = 0
		category = categories[self._nav_category_index]
		links = self._nav_link_manager.data.get(category, [])
		count = len(links)
		# Translators: Announced when switching to a category; shows its name and link count.
		lnk_word = _("link") if count == 1 else _("links")
		ui.message(
			_("{category}: Contains {count} {lnk_word}").format(
				category=category, count=count, lnk_word=lnk_word
			)
		)

	@script(
		gesture="kb:nvda+shift+control+f11",
		# Translators: Description shown in NVDA input gestures for jumping to the first link.
		description=_("Move to the first saved link in the current category."),
		category=ADDON_SUMMARY
	)
	def script_firstLink(self, gesture):
		"""
		Moves the navigation cursor to the first link in the current category
		and announces its name.

		Args:
			gesture (kb): Triggered by NVDA+Shift+Control+F11.
		"""
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(
			categories[self._nav_category_index], []
		)
		if not links:
			beep(200, 100)
			return
		self._nav_link_index = 0
		self._announce_current_link()

	@script(
		gesture="kb:nvda+shift+control+f12",
		# Translators: Description shown in NVDA input gestures for jumping to the last link.
		description=_("Move to the last saved link in the current category."),
		category=ADDON_SUMMARY
	)
	def script_lastLink(self, gesture):
		"""
		Moves the navigation cursor to the last link in the current category
		and announces its name.

		Args:
			gesture (kb): Triggered by NVDA+Shift+Control+F12.
		"""
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(
			categories[self._nav_category_index], []
		)
		if not links:
			beep(200, 100)
			return
		self._nav_link_index = len(links) - 1
		self._announce_current_link()

	@script(
		gesture="kb:control+shift+enter",
		# Translators: Description shown in NVDA input gestures for opening the current link.
		description=_("Open the currently selected link in the default browser."),
		category=ADDON_SUMMARY
	)
	def script_openCurrentLink(self, gesture):
		"""
		Opens the currently selected link in the user's default web browser
		and announces which URL is being opened.

		Args:
			gesture (kb): Triggered by Control+Shift+Enter.
		"""
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(
			categories[self._nav_category_index], []
		)
		if not links:
			beep(200, 100)
			return
		title, url = links[self._nav_link_index]
		try:
			webbrowser.open(url)
			# Translators: Announced when a link is opened via keyboard navigation.
			ui.message(_("Opening {title}.").format(title=title))
		except Exception as e:
			log.error("Error opening URL via keyboard navigation: %s", e)

	@script(
		gesture="kb:control+shift+l",
		# Translators: Description shown in NVDA input gestures for toggling URL announcement.
		description=_("Toggle reading the URL after the link name during keyboard navigation."),
		category=ADDON_SUMMARY
	)
	def script_toggleReadUrl(self, gesture):
		"""
		Toggles whether the URL is announced alongside the link name during
		keyboard navigation. The new state is confirmed by a spoken message.

		Args:
			gesture (kb): Triggered by Control+Shift+L.
		"""
		current = config.conf[ourAddon.name]["readUrlAfterName"]
		config.conf[ourAddon.name]["readUrlAfterName"] = not current
		if config.conf[ourAddon.name]["readUrlAfterName"]:
			# Translators: Announced when the user enables reading the URL after the link name.
			ui.message(_("Read URL after name turned on."))
		else:
			# Translators: Announced when the user disables reading the URL after the link name.
			ui.message(_("Read URL after name turned off."))

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
