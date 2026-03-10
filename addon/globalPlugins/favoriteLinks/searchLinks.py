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

		# Category selector
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
			# Translators: Label for the dropdown used to choose the category to search.
			_("Select a category:"), wx.Choice, choices=categories
		)
		self.categoryChoice.SetSelection(0)

		# Search term field
		self.txtSearch = sizerHelper.addLabeledControl(
			# Translators: Label for the input where users type the search text.
			_("Search word:"), wx.TextCtrl, style=wx.TE_PROCESS_ENTER
		)
		self.txtSearch.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

		# Search-by radio box
		# Translators: Radio option to search links by their display name.
		choice_name = _("Name")
		# Translators: Radio option to search links by their URL.
		choice_url = _("URL")
		# Translators: Label for the radio group that selects what field to search.
		search_by_label = _("Search by")
		self.searchBy = wx.RadioBox(
			panel,
			label=search_by_label,
			choices=[choice_name, choice_url]
		)
		sizerHelper.addItem(self.searchBy)

		# Results list (hidden until a search is performed)
		# Translators: Label for the list that shows search results.
		self.resultsLabel = wx.StaticText(panel, label="")
		sizerHelper.addItem(self.resultsLabel)
		self.listResults = wx.ListBox(panel, choices=[])
		self.listResults.Bind(wx.EVT_LISTBOX_DCLICK, self.onOpenResult)
		self.listResults.Bind(wx.EVT_KEY_DOWN, self.onResultsKeyPress)
		sizerHelper.addItem(self.listResults)

		# Hide results section until a search has been run
		self.resultsLabel.Hide()
		self.listResults.Hide()

		# Buttons
		# Translators: Label for the button that starts searching links.
		search_button = wx.Button(panel, label=_("&Search"))
		search_button.SetDefault()
		# Translators: Label for the button that opens the selected result.
		self._openButton = wx.Button(panel, label=_("&Open"))
		# Translators: Label for the button that copies the selected result URL.
		self._copyButton = wx.Button(panel, label=_("&Copy URL"))
		# Translators: Label for the button that closes the search dialog.
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
		"""
		Returns the (title, url) pair for the currently selected result,
		or None if nothing is selected.
		"""
		index = self.listResults.GetSelection()
		if index == wx.NOT_FOUND:
			return None
		return self.results[index]

	def _update_action_buttons(self):
		"""Enable or disable Open/Copy based on whether results are visible."""
		has_results = self.listResults.IsShown() and self.listResults.GetCount() > 0
		self._openButton.Enable(has_results)
		self._copyButton.Enable(has_results)

	def onSearch(self, event):
		"""
		Executes the search and populates the results list.

		Args:
			event (wx.Event): The event triggered by the Search button or
				pressing Enter in the search field.
		"""
		search_word = self.txtSearch.GetValue().strip()
		if not search_word:
			# Translators: Spoken when the user activates Search with an empty field.
			self.show_message(_("Please enter a search word."))
			self.txtSearch.SetFocus()
			return

		category_idx = self.categoryChoice.GetSelection()
		if category_idx == 0:
			links = []
			for cat_links in self.link_manager.data.values():
				links.extend(cat_links)
		else:
			category = self.categoryChoice.GetStringSelection()
			links = self.link_manager.data.get(category, [])
		search_by_url = self.searchBy.GetSelection() == 1

		self.results = []
		for title, url in links:
			# Coerce to str to guard against non-string values in hand-edited JSON.
			title_str = str(title) if title is not None else ""
			url_str = str(url) if url is not None else ""
			haystack = url_str if search_by_url else title_str
			if search_word.lower() in haystack.lower():
				self.results.append((title_str, url_str))

		self.listResults.Clear()

		if not self.results:
			self.resultsLabel.Hide()
			self.listResults.Hide()
			self.Layout()
			self.Fit()
			# Translators: Shown when the search produces no matches.
			no_results_message = _("No results found.")
			# Translators: Caption for informational messages in the search dialog.
			search_caption = _("Search")
			self.show_message(no_results_message, search_caption)
			self._update_action_buttons()
			return

		for title, url in self.results:
			self.listResults.Append("{title}  —  {url}".format(title=title, url=url))

		count = len(self.results)
		# Translators: Label shown above the results list; {count} is the number of matches.
		results_count_label = _("Results: {count} found.").format(count=count)
		self.resultsLabel.SetLabel(
			results_count_label
		)
		self.resultsLabel.Show()
		self.listResults.Show()
		self.Layout()
		self.Fit()
		self.listResults.SetSelection(0)
		self.listResults.SetFocus()
		self._update_action_buttons()
		# Translators: Announced when results appear; {count} is the number of matches.
		ui.message(_("{count} results found.").format(count=count))

	def onOpenResult(self, event):
		"""
		Opens the selected search result in the default browser.

		Args:
			event (wx.Event): The event triggered by the Open button or a
				double-click / Enter on the results list.
		"""
		result = self._get_selected_result()
		if result is None:
			# Translators: Spoken when the user tries to open a result without selecting one.
			self.show_message(_("No result selected to open!"))
			if self.listResults.IsShown():
				self.listResults.SetFocus()
			else:
				self.txtSearch.SetFocus()
			return
		title, url = result
		try:
			if not webbrowser.open(url):
				raise RuntimeError("webbrowser.open returned False")
			# Translators: Announced when a found link is being opened.
			ui.message(_("Opening {title}.").format(title=title))
			self.EndModal(wx.ID_OK)
		except Exception as e:
			log.error("Error opening search result URL: %s", e)
			# Translators: Shown when a link cannot be opened in the browser.
			open_error_message = _("Unable to open the selected link. Please check your browser or the URL and try again.")
			# Translators: Caption for error messages in the search dialog.
			error_caption = _("Error")
			self.show_message(
				open_error_message,
				caption=error_caption,
				style=wx.OK | wx.ICON_ERROR,
			)
			self.listResults.SetFocus()

	def onCopyUrl(self, event):
		"""
		Copies the URL of the selected search result to the system clipboard.

		Args:
			event (wx.Event): The event triggered by the Copy URL button.
		"""
		result = self._get_selected_result()
		if result is None:
			# Translators: Spoken when the user tries to copy a URL without selecting a result.
			self.show_message(_("No result selected to copy!"))
			if self.listResults.IsShown():
				self.listResults.SetFocus()
			else:
				self.txtSearch.SetFocus()
			return
		_title, url = result
		try:
			api.copyToClip(url)
			# Translators: Announced when a URL from the search results is copied to the clipboard.
			ui.message(_("URL copied to clipboard."))
		except Exception as e:
			log.error("Error copying URL to clipboard: %s", e)
			# Translators: Announced/shown when copying a URL to the clipboard fails.
			ui.message(_("Failed to copy URL to clipboard."))

	def onCancel(self, event):
		"""
		Closes the dialog without taking any action.

		Args:
			event (wx.Event): The cancel event.
		"""
		self.EndModal(wx.ID_CANCEL)

	def onResultsKeyPress(self, event):
		"""
		Handles key presses inside the results list:
		Enter opens the selected result.

		Args:
			event (wx.Event): The key-down event on the results list.
		"""
		if event.GetKeyCode() == wx.WXK_RETURN:
			self.onOpenResult(event)
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

	def show_message(self, message, caption=None, style=wx.OK | wx.ICON_INFORMATION):
		"""
		Displays a message to the user.
		"""
		if caption is None:
			# Translators: Default caption for attention messages in the search dialog.
			caption = _("Attention")
		messageBox(message, caption, style)
