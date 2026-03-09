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
from gui import guiHelper, mainFrame, messageBox
from logHandler import log

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
		link_manager (LinkManager): The shared LinkManager instance
			containing all saved categories and links.
	"""

	def __init__(self, parent, link_manager):
		self._link_manager = link_manager

		# Translators: Title of the search links dialog.
		super(SearchLinks, self).__init__(
			parent,
			title=_("Search links")
		)

		if not self._link_manager.data:
			# Translators: Spoken / shown when there are no saved categories to search.
			ui.message(_("No categories found. Please add some links first."))
			self.Destroy()
			return

		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Category selector
		categories = list(self._link_manager.data.keys())
		self._categoryChoice = sizerHelper.addLabeledControl(
			_("Select a category:"), wx.Choice, choices=categories
		)
		self._categoryChoice.SetSelection(0)

		# Search term field
		self._txtSearch = sizerHelper.addLabeledControl(
			_("Search word:"), wx.TextCtrl, style=wx.TE_PROCESS_ENTER
		)
		self._txtSearch.Bind(wx.EVT_TEXT_ENTER, self.onSearch)

		# Search-by radio box
		# Translators: Label for the radio group that selects what field to search.
		self._searchBy = wx.RadioBox(
			panel,
			label=_("Search by"),
			# Translators: Radio option to search links by their display name.
			# Translators: Radio option to search links by their URL.
			choices=[_("Name"), _("URL")]
		)
		sizerHelper.addItem(self._searchBy)

		# Results list (hidden until a search is performed)
		# Translators: Label for the list that shows search results.
		self._resultsLabel = wx.StaticText(panel, label="")
		sizerHelper.addItem(self._resultsLabel)
		self._listResults = wx.ListBox(panel, choices=[])
		self._listResults.Bind(wx.EVT_LISTBOX_DCLICK, self.onOpenResult)
		self._listResults.Bind(wx.EVT_KEY_DOWN, self.onResultsKeyPress)
		sizerHelper.addItem(self._listResults)

		# Hide results section until a search has been run
		self._resultsLabel.Hide()
		self._listResults.Hide()

		# Buttons
		search_button = wx.Button(panel, label=_("&Search"))
		search_button.SetDefault()
		open_button = wx.Button(panel, label=_("&Open"))
		copy_button = wx.Button(panel, label=_("&Copy URL"))
		cancel_button = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"))

		buttonSizer.addItem(search_button)
		buttonSizer.addItem(open_button)
		buttonSizer.addItem(copy_button)
		buttonSizer.addItem(cancel_button)

		self.Bind(wx.EVT_BUTTON, self.onSearch, search_button)
		self.Bind(wx.EVT_BUTTON, self.onOpenResult, open_button)
		self.Bind(wx.EVT_BUTTON, self.onCopyUrl, copy_button)
		self.Bind(wx.EVT_BUTTON, self.onCancel, cancel_button)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL | wx.EXPAND)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)
		self.Fit()

	# ------------------------------------------------------------------
	# Private helpers
	# ------------------------------------------------------------------

	def _get_selected_result(self):
		"""
		Returns the ``(title, url)`` pair for the currently selected result,
		or ``None`` if nothing is selected.

		Returns:
			tuple or None: ``(title, url)`` of the selected result, or None.
		"""
		index = self._listResults.GetSelection()
		if index == wx.NOT_FOUND:
			return None
		return self._results[index]

	# ------------------------------------------------------------------
	# Event handlers
	# ------------------------------------------------------------------

	def onSearch(self, event):
		"""
		Executes the search and populates the results list.

		Args:
			event (wx.Event): The event triggered by the Search button or
				pressing Enter in the search field.
		"""
		search_word = self._txtSearch.GetValue().strip()
		if not search_word:
			# Translators: Spoken when the user activates Search with an empty field.
			self.show_message(_("Please enter a search word."))
			self._txtSearch.SetFocus()
			return

		category = self._categoryChoice.GetStringSelection()
		links = self._link_manager.data.get(category, [])
		search_by_url = self._searchBy.GetSelection() == 1

		self._results = []
		for title, url in links:
			haystack = url if search_by_url else title
			if search_word.lower() in haystack.lower():
				self._results.append((title, url))

		self._listResults.Clear()

		if not self._results:
			self._resultsLabel.Hide()
			self._listResults.Hide()
			self.Layout()
			self.Fit()
			# Translators: Shown when the search produces no matches.
			self.show_message(_("No results found."), _("Search"))
			return

		for title, url in self._results:
			self._listResults.Append("{title}  —  {url}".format(title=title, url=url))

		count = len(self._results)
		# Translators: Label shown above the results list; {count} is the number of matches.
		self._resultsLabel.SetLabel(
			_("Results: {count} found.").format(count=count)
		)
		self._resultsLabel.Show()
		self._listResults.Show()
		self.Layout()
		self.Fit()
		self._listResults.SetSelection(0)
		self._listResults.SetFocus()
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
			self._listResults.SetFocus()
			return
		title, url = result
		try:
			webbrowser.open(url)
			# Translators: Announced when a found link is being opened.
			ui.message(_("Opening {title}.").format(title=title))
			self.EndModal(wx.ID_OK)
		except Exception as e:
			log.error("Error opening search result URL: %s", e)
			# Translators: Shown when a link cannot be opened in the browser.
			self.show_message(
				_("Unable to open the selected link. Please check your browser or the URL and try again."),
				caption=_("Error"),
				style=wx.OK | wx.ICON_ERROR,
			)

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
			self._listResults.SetFocus()
			return
		_title, url = result
		if api.copyToClip(url):
			# Translators: Announced when a URL from the search results is copied to the clipboard.
			ui.message(_("URL copied to clipboard."))
		else:
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

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Displays a message to the user in a dialog box.

		Args:
			message (str): The message to be displayed.
			caption (str, optional): The dialog title. Defaults to "Attention".
			style (int, optional): The dialog style flags. Defaults to
				wx.OK | wx.ICON_INFORMATION.
		"""
		messageBox(message, caption, style)
