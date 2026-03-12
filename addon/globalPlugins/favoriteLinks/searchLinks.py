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


class SearchLinks(wx.Dialog):
	"""
	Dialog that allows users to search for saved links by title or URL.

	The user selects a category, types a search term, chooses whether to
	search by link name or by URL, and sees the matching results in a list.
	From the results list the user can open the selected link or copy its
	URL to the clipboard.

	Args:
		parent (wx.Window): The parent window for this dialog.
		link_manager (LinkManager): A `LinkManager` instance
			containing all saved categories and links.
	"""

	def __init__(self, parent, link_manager):
		self.link_manager = link_manager
		self.results = []

		# Translators: Title of the search links dialog.
		wx.Dialog.__init__(self, parent, title=_("Search links"))

		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Category selector — first item is a catch-all for global search
		# Translators: First option in the category dropdown; searches across all categories.
		all_categories_label = _("(All categories)")
		original_categories = list(self.link_manager.data.keys())

		display_all_label = all_categories_label
		suffix = 1
		while display_all_label in original_categories:
			display_all_label = "{} ({})".format(all_categories_label, suffix)
			suffix += 1

		categories = [display_all_label] + original_categories

		self.categoryChoice = sizerHelper.addLabeledControl(
			# Translators: Label for the category dropdown in the search dialog.
			_("Select a category:"), wx.Choice, choices=categories
		)
		self.categoryChoice.SetSelection(0)

		# Search field
		self.txtSearch = sizerHelper.addLabeledControl(
			# Translators: Label for the search text input field.
			_("Search word:"), wx.TextCtrl, style=wx.TE_PROCESS_ENTER
		)
		self.txtSearch.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

		# Search type radio
		choice_name = _("Name")
		choice_url = _("URL")

		self.searchBy = wx.RadioBox(
			panel,
			label=_("Search by"),
			choices=[choice_name, choice_url]
		)

		sizerHelper.addItem(self.searchBy)

		# Results
		self.resultsLabel = wx.StaticText(panel, label="")
		sizerHelper.addItem(self.resultsLabel)

		self.listResults = wx.ListBox(panel, choices=[])
		self.listResults.Bind(wx.EVT_LISTBOX_DCLICK, self.onOpenResult)
		self.listResults.Bind(wx.EVT_KEY_DOWN, self.onResultsKeyPress)

		sizerHelper.addItem(self.listResults)

		self.resultsLabel.Hide()
		self.listResults.Hide()

		# Buttons
		search_button = wx.Button(panel, label=_("&Search"))
		search_button.SetDefault()

		self._openButton = wx.Button(panel, label=_("&Open"))
		self._copyButton = wx.Button(panel, label=_("&Copy URL"))

		cancel_button = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"))

		self._openButton.Disable()
		self._copyButton.Disable()

		buttonSizer.addItem(search_button)
		buttonSizer.addItem(self._openButton)
		buttonSizer.addItem(self._copyButton)
		buttonSizer.addItem(cancel_button)

		self.Bind(wx.EVT_BUTTON, self.onSearch, search_button)
		self.Bind(wx.EVT_BUTTON, self.onOpenResult, self._openButton)
		self.Bind(wx.EVT_BUTTON, self.onCopyUrl, self._copyButton)
		self.Bind(wx.EVT_BUTTON, self.onCancel, cancel_button)

		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL | wx.EXPAND)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)

		panel.SetSizerAndFit(boxSizer)
		self.Fit()

	def _get_selected_result(self):
		index = self.listResults.GetSelection()
		if index == wx.NOT_FOUND:
			return None
		return self.results[index]

	def _update_action_buttons(self):
		has_results = self.listResults.IsShown() and self.listResults.GetCount() > 0
		self._openButton.Enable(has_results)
		self._copyButton.Enable(has_results)

	def onSearch(self, event):

		search_word = self.txtSearch.GetValue().strip()

		if not search_word:
			self.show_message(_("Please enter a search word."))
			self.txtSearch.SetFocus()
			return

		category_idx = self.categoryChoice.GetSelection()

		if category_idx == 0:
			# All categories
			links = []
			for cat_links in self.link_manager.data.values():
				links.extend(cat_links)
		else:
			category = self.categoryChoice.GetStringSelection()
			links = self.link_manager.data.get(category, [])

		search_by_url = self.searchBy.GetSelection() == 1

		self.results = []

		for title, url in links:

			title_str = str(title) if title else ""
			url_str = str(url) if url else ""

			haystack = url_str if search_by_url else title_str

			if search_word.lower() in haystack.lower():
				self.results.append((title_str, url_str))

		self.listResults.Clear()

		if not self.results:

			self.resultsLabel.Hide()
			self.listResults.Hide()

			self.Layout()
			self.Fit()

			self.show_message(_("No results found."), _("Search"))

			self._update_action_buttons()

			return

		for title, url in self.results:
			self.listResults.Append(f"{title}  —  {url}")

		count = len(self.results)

		self.resultsLabel.SetLabel(_("Results: {count} found.").format(count=count))

		self.resultsLabel.Show()
		self.listResults.Show()

		self.Layout()
		self.Fit()

		self.listResults.SetSelection(0)
		self.listResults.SetFocus()

		self._update_action_buttons()

		ui.message(_("{count} results found.").format(count=count))

	def onOpenResult(self, event):

		result = self._get_selected_result()

		if result is None:
			self.show_message(_("No result selected to open!"))
			return

		title, url = result

		if not self.link_manager.is_internet_connected():

			self.show_message(
				_("No active internet connection!"),
				_("Error"),
				wx.OK | wx.ICON_ERROR
			)

			return

		try:

			if not webbrowser.open(url):
				raise RuntimeError

			ui.message(_("Opening {title}.").format(title=title))

			self.EndModal(wx.ID_OK)

		except Exception as e:

			log.error("Error opening search result URL: %s", e)

			self.show_message(
				_("Unable to open the selected link. Please check your browser."),
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)

	def onCopyUrl(self, event):

		result = self._get_selected_result()

		if result is None:
			self.show_message(_("No result selected to copy!"))
			return

		_, url = result

		try:
			api.copyToClip(url)
			ui.message(_("URL copied to clipboard."))
		except Exception as e:
			log.error("Error copying URL: %s", e)
			ui.message(_("Failed to copy URL to clipboard."))

	def onCancel(self, event):
		self.EndModal(wx.ID_CANCEL)

	def onResultsKeyPress(self, event):

		if event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.onOpenResult(event)
			return

		event.Skip()

	def onKeyPress(self, event):

		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.onCancel(event)
			return

		event.Skip()

	def show_message(self, message, caption=None, style=wx.OK | wx.ICON_INFORMATION):

		if caption is None:
			caption = _("Search Links")

		messageBox(message, caption, style)
