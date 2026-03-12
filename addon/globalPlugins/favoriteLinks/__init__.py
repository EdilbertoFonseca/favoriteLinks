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
from gettext import ngettext

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


def isBrowser():
	"""Verifies if NVDA is currently in a browser."""
	obj = api.getFocusObject()
	return bool(obj.treeInterceptor)


def getCurrentDocumentURL():
	"""Gets the current masked document URL if in a browser."""
	obj = api.getFocusObject()
	try:
		return obj.treeInterceptor.documentConstantIdentifier
	except AttributeError:
		return None


def disableInSecureMode(decoratedCls):
	"""Decorator to disable the plugin in secure mode."""
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	"""Global Plugin class for the Favorite Links NVDA addon."""

	def __init__(self):
		super(GlobalPlugin, self).__init__()

		# Add settings panel to NVDA configuration dialog
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
			FavoriteLinksSettingsPanel
		)

		# Tools menu setup
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.favoriteLinks = self.toolsMenu.Append(
			wx.ID_ANY, _("&Favorite links...")
		)
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_activateFavoriteLinks, self.favoriteLinks
		)

		# Navigation state
		self._nav_category_index = 0
		self._nav_link_index = 0
		self._nav_link_manager = LinkManager.empty()
		try:
			self._nav_link_manager.load_json()
		except Exception as e:
			log.error("Error loading navigation data at startup: %s", e)

	# -------------------------------
	# Navigation helpers
	# -------------------------------
	def _reload_nav_data(self):
		"""Reloads link data from JSON into the navigation link manager."""
		try:
			self._nav_link_manager.load_json()
			categories = list(self._nav_link_manager.data.keys())
			if categories:
				self._nav_category_index = min(self._nav_category_index, len(categories) - 1)
				links = self._nav_link_manager.data.get(categories[self._nav_category_index], [])
				self._nav_link_index = min(self._nav_link_index, max(0, len(links) - 1))
			else:
				self._nav_category_index = 0
				self._nav_link_index = 0
		except Exception as e:
			log.error("Error reloading navigation data: %s", e)

	def _get_nav_categories(self):
		"""Returns a sorted list of category names from navigation data."""
		return list(self._nav_link_manager.data.keys())

	def _announce_current_link(self):
		"""Announces the currently selected link via NVDA speech."""
		categories = self._get_nav_categories()
		if not categories:
			ui.message(_("No links saved."))
			return
		category = categories[self._nav_category_index]
		links = self._nav_link_manager.data.get(category, [])
		if not links:
			ui.message(_("No links in this category."))
			return
		title, url = links[self._nav_link_index]
		msg = title
		if config.conf[ourAddon.name]["readUrlAfterName"]:
			msg += "  " + url
		ui.message(msg)

	# -------------------------------
	# Dialog management
	# -------------------------------
	def onFavoriteLinks(self, event):
		"""Opens the Favorite Links dialog."""
		try:
			self.dlg = FavoriteLinks(mainFrame, _("Favorite links."))
			gui.mainFrame.prePopup()
			self.dlg.CentreOnScreen()
			self.dlg.Show()
			gui.mainFrame.postPopup()
			self.dlg.Bind(wx.EVT_WINDOW_DESTROY, self._onDialogClosed)
		except Exception as e:
			log.error("Error displaying Favorite Links dialog: %s", e)

	def _onDialogClosed(self, event):
		"""Reloads navigation data when the dialog is destroyed."""
		event.Skip()
		self._reload_nav_data()

	def onAddLinks(self):
		"""Calls the dialog for adding a new link."""
		try:
			gui.mainFrame.prePopup()
			FavoriteLinks.onAddLink
			gui.mainFrame.postPopup()
		except Exception as e:
			log.error("Error displaying Favorite Links dialog: %s", e)

	# -------------------------------
	# NVDA scripts
	# -------------------------------
	@script(gesture="kb:Windows+alt+K",
			description=_("This addon allows you to save links to a specific page."),
			category=ADDON_SUMMARY)
	def script_activateFavoriteLinks(self, gesture):
		wx.CallAfter(self.onFavoriteLinks, None)

	@script(gesture="kb:Windows+Control+P",
			description=_("Show document URL, press twice copies to clipboard."),
			category=ADDON_SUMMARY)
	def script_ShowDocumentURL(self, gesture):
		if isBrowser():
			URL = getCurrentDocumentURL()
			if URL:
				if scriptHandler.getLastScriptRepeatCount() == 0:
					ui.message(URL)
				elif scriptHandler.getLastScriptRepeatCount() == 1:
					api.copyToClip(URL)
					ui.message(_("Copied to clipboard {URL}.").format(URL=URL))
			else:
				ui.message(_("Document URL not found."))
		else:
			ui.message(_("No browser window found."))

	@script(gesture="kb:NVDA+Shift+G",
			description=_("Search saved links by name or URL."),
			category=ADDON_SUMMARY)
	def script_searchLinks(self, gesture):
		"""Opens the Search Links dialog."""
		def open_dialog():
			try:
				lm = LinkManager()
			except Exception as e:
				log.error("Error loading link manager for search: %s", e)
				ui.message(_("Failed to load links. Please check the file."))
				return
			if not lm.data:
				ui.message(_("No saved links found. If you had links before, the links file may have been corrupt and was reset. Please add links to begin."))
				return
			try:
				dlg = SearchLinks(mainFrame, lm)
			except Exception as e:
				log.error("Error creating search dialog: %s", e)
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

	@script(description=_("Open a URL from the clipboard."),
			category=ADDON_SUMMARY)
	def script_openFromClipboard(self, gesture):
		"""Opens URLs from the clipboard or shows picker dialog if multiple found."""
		def _open():
			try:
				clipboard_text = api.getClipData() or ""
			except OSError as e:
				log.error("Error reading clipboard: %s", e)
				ui.message(_("Unable to read the clipboard."))
				return
			urls = LinkManager.extract_urls_from_text(clipboard_text)
			urls = [("https://" + u if u.lower().startswith("www.") else u) for u in urls]
			if not urls:
				ui.message(_("The clipboard does not contain any links."))
				return
			if len(urls) == 1:
				try:
					opened = webbrowser.open(urls[0])
					if not opened:
						raise OSError("Browser failed to open URL")
					ui.message(_("Opening {url}.").format(url=urls[0]))
				except Exception as e:
					log.error("Error opening clipboard URL: %s", e)
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

	# -------------------------------
	# Keyboard navigation scripts
	# -------------------------------
	@script(gesture="kb:control+shift+f12",
			description=_("Move to the next saved link in the current category."),
			category=ADDON_SUMMARY)
	def script_nextLink(self, gesture):
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(categories[self._nav_category_index], [])
		if not links:
			beep(200, 100)
			return
		if self._nav_link_index < len(links) - 1:
			self._nav_link_index += 1
		else:
			beep(250, 50)
		self._announce_current_link()

	@script(gesture="kb:control+shift+f11",
			description=_("Move to the previous saved link in the current category."),
			category=ADDON_SUMMARY)
	def script_previousLink(self, gesture):
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(categories[self._nav_category_index], [])
		if not links:
			beep(200, 100)
			return
		if self._nav_link_index > 0:
			self._nav_link_index -= 1
		else:
			beep(200, 50)
		self._announce_current_link()

	@script(gesture="kb:control+shift+f10",
			description=_("Move to the next category of saved links."),
			category=ADDON_SUMMARY)
	def script_nextCategory(self, gesture):
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		if self._nav_category_index < len(categories) - 1:
			self._nav_category_index += 1
		else:
			beep(250, 50)
		self._nav_link_index = 0
		category = categories[self._nav_category_index]
		links = self._nav_link_manager.data.get(category, [])
		count = len(links)
		ui.message(ngettext(
			"{category}: Contains {count} link",
			"{category}: Contains {count} links",
			count,
		).format(category=category, count=count))

	@script(gesture="kb:control+shift+f9",
			description=_("Move to the previous category of saved links."),
			category=ADDON_SUMMARY)
	def script_previousCategory(self, gesture):
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		if self._nav_category_index > 0:
			self._nav_category_index -= 1
		else:
			beep(200, 50)
		self._nav_link_index = 0
		category = categories[self._nav_category_index]
		links = self._nav_link_manager.data.get(category, [])
		count = len(links)
		ui.message(ngettext(
			"{category}: Contains {count} link",
			"{category}: Contains {count} links",
			count,
		).format(category=category, count=count))

	@script(gesture="kb:nvda+shift+control+f11",
			description=_("Move to the first saved link in the current category."),
			category=ADDON_SUMMARY)
	def script_firstLink(self, gesture):
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(categories[self._nav_category_index], [])
		if not links:
			beep(200, 100)
			return
		self._nav_link_index = 0
		self._announce_current_link()

	@script(gesture="kb:nvda+shift+control+f12",
			description=_("Move to the last saved link in the current category."),
			category=ADDON_SUMMARY)
	def script_lastLink(self, gesture):
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(categories[self._nav_category_index], [])
		if not links:
			beep(200, 100)
			return
		self._nav_link_index = len(links) - 1
		self._announce_current_link()

	@script(gesture="kb:control+shift+enter",
			description=_("Open the currently selected link in the default browser."),
			category=ADDON_SUMMARY)
	def script_openCurrentLink(self, gesture):
		categories = self._get_nav_categories()
		if not categories:
			beep(200, 100)
			return
		links = self._nav_link_manager.data.get(categories[self._nav_category_index], [])
		if not links:
			beep(200, 100)
			return
		title, url = links[self._nav_link_index]
		try:
			webbrowser.open(url)
			msg = _("Opening {title}.").format(title=title)
			if config.conf[ourAddon.name]["readUrlAfterName"]:
				msg += "  " + url
			ui.message(msg)
		except Exception as e:
			log.error("Error opening URL via keyboard navigation: %s", e)
			ui.message(_("Unable to open {title}.").format(title=title))

	@script(gesture="kb:control+shift+l",
			description=_("Toggle reading the URL after the link name during keyboard navigation."),
			category=ADDON_SUMMARY)
	def script_toggleReadUrl(self, gesture):
		current = config.conf[ourAddon.name]["readUrlAfterName"]
		config.conf[ourAddon.name]["readUrlAfterName"] = not current
		if config.conf[ourAddon.name]["readUrlAfterName"]:
			ui.message(_("Read URL after name turned on."))
		else:
			ui.message(_("Read URL after name turned off."))

	# -------------------------------
	# Plugin termination
	# -------------------------------
	def terminate(self):
		"""Clean up when the plugin is terminated."""
		super(GlobalPlugin, self).terminate()
		if FavoriteLinksSettingsPanel in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(FavoriteLinksSettingsPanel)
		if hasattr(self, 'favoriteLinks'):
			try:
				self.toolsMenu.Remove(self.favoriteLinks)
			except Exception as e:
				log.warning("Error removing Favorite Links menu item: %s", e)
