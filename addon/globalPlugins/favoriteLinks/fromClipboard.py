# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Feature inspired by the Link Manager add-on by Abdallah Hader:
https://github.com/abdallah-hader/linkManager

Created on: 08/03/2025
"""

import webbrowser

import addonHandler
import api
import ui
import wx
from gui import guiHelper, messageBox
from logHandler import log

# Initialize translation support
addonHandler.initTranslation()


class FromClipboard(wx.Dialog):
	"""
	Dialog that extracts URLs from the clipboard and lets the user open or
	copy one of them.

	If only one URL is found it is opened immediately without showing the
	dialog. If multiple URLs are found the dialog lists them all so the user
	can choose. If the clipboard contains no recognisable URL a spoken
	message is given and the dialog is not shown.

	Args:
		parent (wx.Window): The parent window for this dialog.
		link_manager (LinkManager): The shared LinkManager instance used
			for URL extraction.
	"""

	def __init__(self, parent, link_manager):
		self.link_manager = link_manager

		# Translators: Title of the dialog shown when multiple URLs are found in the clipboard.
		wx.Dialog.__init__(self, parent, title=_("Choose a link to open"))

		try:
			clipboard_text = api.getClipData()
		except OSError as e:
			log.error("Error reading clipboard: %s", e)
			# Translators: Spoken when the clipboard cannot be read.
			ui.message(_("Unable to read the clipboard."))
			self.Destroy()
			return

		urls = self.link_manager.extract_urls_from_text(clipboard_text)
		# Normalize bare "www." URLs to https.
		urls = [("https://" + u if u.lower().startswith("www.") else u) for u in urls]

		if not urls:
			# Translators: Spoken when the clipboard holds no recognisable URL.
			ui.message(_("The clipboard does not contain any links."))
			self.Destroy()
			return

		if len(urls) == 1:
			# Open the single URL straight away without a dialog.
			try:
				webbrowser.open(urls[0])
				# Translators: Spoken when a single clipboard URL is opened.
				ui.message(_("Opening {url}.").format(url=urls[0]))
			except Exception as e:
				log.error("Error opening clipboard URL: %s", e)
			self.Destroy()
			return

		self.urls = urls

		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Translators: Label showing how many links were extracted from the clipboard.
		count_label = _("{count} links found in the clipboard.").format(count=len(urls))
		sizerHelper.addItem(wx.StaticText(panel, label=count_label))

		# Translators: Label for the list of URLs extracted from the clipboard.
		self.listUrls = sizerHelper.addLabeledControl(
			_("Select a link:"), wx.ListBox, choices=urls
		)
		self.listUrls.SetSelection(0)
		self.listUrls.Bind(wx.EVT_LISTBOX_DCLICK, self.onOpen)
		self.listUrls.Bind(wx.EVT_KEY_DOWN, self.onListKeyPress)

		# Buttons
		open_button = wx.Button(panel, label=_("&Open"))
		open_button.SetDefault()
		copy_button = wx.Button(panel, label=_("&Copy to clipboard"))
		cancel_button = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"))

		buttonSizer.addItem(open_button)
		buttonSizer.addItem(copy_button)
		buttonSizer.addItem(cancel_button)

		self.Bind(wx.EVT_BUTTON, self.onOpen, open_button)
		self.Bind(wx.EVT_BUTTON, self.onCopyToClipboard, copy_button)
		self.Bind(wx.EVT_BUTTON, self.onCancel, cancel_button)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL | wx.EXPAND)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)
		self.Fit()

	def _get_selected_url(self):
		"""
		Returns the URL currently selected in the list, or an empty string if
		nothing is selected.
		"""
		index = self.listUrls.GetSelection()
		if index == wx.NOT_FOUND:
			return ""
		return self.urls[index]

	def onOpen(self, event):
		"""
		Opens the selected URL in the default browser.

		Args:
			event (wx.Event): The event triggered by the Open button or a
				double-click on the list.
		"""
		url = self._get_selected_url()
		if not url:
			# Translators: Spoken when no link is selected in the picker dialog.
			self.show_message(_("No link selected to open!"))
			self.listUrls.SetFocus()
			return
		try:
			if url.lower().startswith("www."):
				url = "https://" + url
			webbrowser.open(url)
			# Translators: Spoken when a link is opened from the picker dialog.
			ui.message(_("Opening {url}.").format(url=url))
		except Exception as e:
			log.error("Error opening URL from clipboard dialog: %s", e)
		self.EndModal(wx.ID_OK)

	def onCopyToClipboard(self, event):
		"""
		Copies the selected URL to the system clipboard.

		Args:
			event (wx.Event): The event triggered by the Copy to clipboard button.
		"""
		url = self._get_selected_url()
		if not url:
			# Translators: Spoken when no link is selected in the picker dialog.
			self.show_message(_("No link selected to copy!"))
			self.listUrls.SetFocus()
			return
		if api.copyToClip(url):
			# Translators: Spoken when the URL has been copied to the clipboard.
			ui.message(_("URL copied to clipboard."))

	def onCancel(self, event):
		"""
		Closes the dialog without taking any action.

		Args:
			event (wx.Event): The cancel event.
		"""
		self.EndModal(wx.ID_CANCEL)

	def onListKeyPress(self, event):
		"""
		Allows pressing Enter on a list item to open the selected URL.

		Args:
			event (wx.Event): The key-down event on the URL list.
		"""
		if event.GetKeyCode() == wx.WXK_RETURN:
			self.onOpen(event)
			return
		event.Skip()

	def onKeyPress(self, event):
		"""
		Handles dialog-level key presses: Escape closes the dialog.

		Args:
			event (wx.Event): The key-hook event.
		"""
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.onCancel(event)
			return
		event.Skip()

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Displays a message to the user.
		"""
		messageBox(message, caption, style)
