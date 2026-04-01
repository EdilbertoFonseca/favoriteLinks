# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 - 2026 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

-------------------------------------------------------------------------
AI DISCLOSURE / NOTA DE IA:
This project utilizes AI for code refactoring and logic suggestions.
All AI-generated code was manually reviewed and tested by the author.
-------------------------------------------------------------------------

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

	def __init__(self, parent, linkManager):
		self.linkManager = linkManager
		self.results = []

		# Translators: Title of the search links dialog.
		wx.Dialog.__init__(self, parent, title=_("Search links"))

		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Translators: First option in the category dropdown; searches across all categories.
		allCategoriesLabel = _("(All categories)")
		originalCategories = list(self.linkManager.data.keys())

		displayAllLabel = allCategoriesLabel
		suffix = 1
		while displayAllLabel in originalCategories:
			displayAllLabel = "{} ({})".format(allCategoriesLabel, suffix)
			suffix += 1

		categories = [displayAllLabel] + originalCategories

		self.categoryChoice = sizerHelper.addLabeledControl(
			# Translators: Label for the category dropdown in the search dialog.
			_("Select a category:"), wx.Choice, choices=categories
		)
		self.categoryChoice.SetSelection(0)

		# Search field
		self.textSearch = sizerHelper.addLabeledControl(
			# Translators: Label for the search text input field.
			_("Search word:"), wx.TextCtrl, style=wx.TE_PROCESS_ENTER
		)
		self.textSearch.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

		# Search type radio
		choiceName = _("Name")
		choiceURL = _("URL")

		self.searchBy = wx.RadioBox(
			panel,
			label=_("Search by"),
			choices=[choiceName, choiceURL]
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
		searchButton = wx.Button(panel, label=_("&Search"))
		searchButton.SetDefault()

		self._openButton = wx.Button(panel, label=_("&Open"))
		self._copyButton = wx.Button(panel, label=_("&Copy URL"))

		cancelButton = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"))

		self._openButton.Disable()
		self._copyButton.Disable()

		buttonSizer.addItem(searchButton)
		buttonSizer.addItem(self._openButton)
		buttonSizer.addItem(self._copyButton)
		buttonSizer.addItem(cancelButton)

		self.Bind(wx.EVT_BUTTON, self.onSearch, searchButton)
		self.Bind(wx.EVT_BUTTON, self.onOpenResult, self._openButton)
		self.Bind(wx.EVT_BUTTON, self.onCopyURL, self._copyButton)
		self.Bind(wx.EVT_BUTTON, self.onCancel, cancelButton)

		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL | wx.EXPAND)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)

		panel.SetSizerAndFit(boxSizer)
		self.Fit()

	def _getSelectedResult(self):
		index = self.listResults.GetSelection()
		if index == wx.NOT_FOUND:
			return None
		return self.results[index]

	def _updateActionButtons(self):
		has_results = self.listResults.IsShown() and self.listResults.GetCount() > 0
		self._openButton.Enable(has_results)
		self._copyButton.Enable(has_results)

	def onSearch(self, event):

		searchWord = self.textSearch.GetValue().strip()

		if not searchWord:
			self.showMessage(_("Please enter a search word."))
			self.textSearch.SetFocus()
			return

		category_idx = self.categoryChoice.GetSelection()

		if category_idx == 0:
			# All categories
			links = []
			for cat_links in self.linkManager.data.values():
				links.extend(cat_links)
		else:
			category = self.categoryChoice.GetStringSelection()
			links = self.linkManager.data.get(category, [])

		search_by_url = self.searchBy.GetSelection() == 1

		self.results = []

		for title, url in links:

			title_str = str(title) if title else ""
			url_str = str(url) if url else ""

			haystack = url_str if search_by_url else title_str

			if searchWord.lower() in haystack.lower():
				self.results.append((title_str, url_str))

		self.listResults.Clear()

		if not self.results:

			self.resultsLabel.Hide()
			self.listResults.Hide()

			self.Layout()
			self.Fit()

			self.showMessage(_("No results found."), _("Search"))

			self._updateActionButtons()

			return

		for title, url in self.results:
			self.listResults.Append(f"{title}  -  {url}")

		count = len(self.results)

		self.resultsLabel.SetLabel(_("Results: {count} found.").format(count=count))

		self.resultsLabel.Show()
		self.listResults.Show()

		self.Layout()
		self.Fit()

		self.listResults.SetSelection(0)
		self.listResults.SetFocus()

		self._updateActionButtons()

		ui.message(_("{count} results found.").format(count=count))

	def onOpenResult(self, event):

		result = self._getSelectedResult()

		if result is None:
			self.showMessage(_("No result selected to open!"))
			return

		title, url = result

		if not self.linkManager.is_internet_connected():

			self.showMessage(
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

			self.showMessage(
				_("Unable to open the selected link. Please check your browser."),
				_("Error"),
				wx.OK | wx.ICON_ERROR,
			)

	def onCopyURL(self, event):

		result = self._getSelectedResult()

		if result is None:
			self.showMessage(_("No result selected to copy!"))
			return

		url = result[1]

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

	def showMessage(self, message, caption=None, style=wx.OK | wx.ICON_INFORMATION):
		"""Shows a message box to the user.

		Args:
			message: The message to display in the message box.
			caption: The caption for the message box. If None, defaults to "Search Links".
			style: The style flags for the message box (e.g., wx.OK, wx.ICONINFORMATION).
			   	Defaults to wx.OK | wx.ICONINFORMATION.
		"""

		if caption is None:
			# translators: Default caption for message boxes in the search links dialog.
			caption = _("Attention")

		messageBox(message, caption, style)
