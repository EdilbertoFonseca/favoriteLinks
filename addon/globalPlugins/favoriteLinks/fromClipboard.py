# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html
"""

import webbrowser

import addonHandler
import api
import ui
import wx
from gui import guiHelper
from logHandler import log

addonHandler.initTranslation()


class FromClipboard(wx.Dialog):
	"""
	Dialog for selecting and opening a URL from the clipboard.
	Displayed when multiple URLs are found in the clipboard content.
	Allows the user to pick one URL to open in the browser or copy to clipboard.

	Args:
		parent (wx.Window): The parent window for this dialog.
		urls (list): List of URL strings extracted from the clipboard.
	"""

	def __init__(self, parent, urls):
		# Translators: Title of the dialog shown when multiple URLs are found in the clipboard.
		wx.Dialog.__init__(self, parent, title=_("Choose a link to open"))
		self.urls = urls

		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Translators: Label showing how many links were extracted from the clipboard.
		count_label = _("{count} links found in the clipboard.").format(count=len(urls))
		sizerHelper.addItem(wx.StaticText(panel, label=count_label))

		# Translators: Label for the list of URLs extracted from the clipboard.
		select_link_label = _("Select a link:")
		self.listUrls = sizerHelper.addLabeledControl(
			select_link_label, wx.ListBox, choices=urls
		)
		self.listUrls.SetSelection(0)
		self.listUrls.Bind(wx.EVT_LISTBOX_DCLICK, self.onOpen)
		self.listUrls.Bind(wx.EVT_KEY_DOWN, self.onListKeyPress)

		# Buttons
		# Translators: Label for the button that opens the selected URL.
		open_button = wx.Button(panel, label=_("&Open"))
		open_button.SetDefault()
		# Translators: Label for the button that copies the selected URL to the clipboard.
		copy_button = wx.Button(panel, label=_("&Copy to clipboard"))
		# Translators: Label for the cancel button in the clipboard URL picker dialog.
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
		index = self.listUrls.GetSelection()
		if index == wx.NOT_FOUND:
			return None
		return self.urls[index]

	def onOpen(self, event):
		url = self._get_selected_url()
		if not url:
			return
		try:
			opened = webbrowser.open(url)
			if not opened:
				raise OSError("Browser failed to open URL")
			# Translators: Spoken when a link is opened from the picker dialog.
			ui.message(_("Opening {url}.").format(url=url))
			self.EndModal(wx.ID_OK)
		except Exception as e:
			log.error("Error opening URL from clipboard dialog: %s", e)
			# Translators: Spoken when a link cannot be opened from the picker dialog.
			ui.message(_("Unable to open the link. Please check your browser settings."))
			self.listUrls.SetFocus()

	def onCopyToClipboard(self, event):
		url = self._get_selected_url()
		if not url:
			return
		try:
			api.copyToClip(url)
			# Translators: Spoken when a URL is copied to the clipboard from the picker dialog.
			ui.message(_("Copied to clipboard: {url}").format(url=url))
		except Exception as e:
			log.error("Error copying URL to clipboard: %s", e)
			# Translators: Spoken when copying a URL to the clipboard fails.
			ui.message(_("Failed to copy URL to clipboard."))

	def onCancel(self, event):
		self.EndModal(wx.ID_CANCEL)

	def onKeyPress(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.EndModal(wx.ID_CANCEL)
		else:
			event.Skip()

	def onListKeyPress(self, event):
		if event.GetKeyCode() == wx.WXK_RETURN:
			self.onOpen(event)
		else:
			event.Skip()
