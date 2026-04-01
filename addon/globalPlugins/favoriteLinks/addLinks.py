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

Created on: 28/05/2024
"""

import addonHandler
import wx
from gui import guiHelper, messageBox
from logHandler import log

# Initialize translation support
addonHandler.initTranslation()


class AddLinks(wx.Dialog):
	"""
	Dialog for link registration.
	This class is responsible for collecting user input to add a new link.
	It does not perform any business logic.

	Args:
		wx.Dialog: Displays a dialog for selecting the category and adding the URL.
	"""

	def __init__(self, parent, linkManagerInstance, title, selectedCategory=""):
		# Dialog window title.
		self.title=title

		wx.Dialog.__init__(self, parent, title=title)

		# Receive the linkmanager instance
		self.linkManager = linkManagerInstance
		self.selectedCategory = selectedCategory
		self.result = {}

		# Load the data from LinkManager
		if not self.linkManager.data:
			log.error("No categories available in LinkManager.")
			self.showMessage(_("No categories available. Please add some categories first."), _("Error"))
			self.Destroy()
			return

		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Create and set up the category field
		self.categoryChoice = self._createCategoryField(sizerHelper)

		# Create and set up the URL field
		self.textUrl = self._createURLField(sizerHelper)

		# Create buttons (OK and Cancel)
		self._createButtons(panel, buttonSizer)

		# Add components to sizers
		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)

		self.Fit()

		# Bind escape key to cancel event
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

	def _createCategoryField(self, sizerHelper):
		"""
		Creates and initializes the category field.
		"""
		categories = list(self.linkManager.data.keys())
		category_field = sizerHelper.addLabeledControl(
			_("Select a Category"), wx.Choice, choices=categories
		)
		if self.selectedCategory in categories:
			category_field.SetStringSelection(self.selectedCategory)
		return category_field

	def _createURLField(self, sizerHelper):
		"""
		Creates and initializes the URL text field.

		The field is pre-populated using the following strategy, inspired by
		the Link Manager add-on by Abdallah Hader
		(https://github.com/abdallah-hader/linkManager):

		1. If the clipboard holds a plain, valid URL it is used as-is.
		2. Otherwise the clipboard text is scanned with a regular expression
		   so that URLs embedded inside sentences (e.g. copied article text)
		   are still detected and the first match is used.
		3. If nothing is found the field is left empty.
		"""
		url_field = sizerHelper.addLabeledControl(
			_("Enter link URL:"), wx.TextCtrl
		)
		# First try a clean, validated URL from the clipboard.
		url = self.linkManager.getURLFromClipboard()
		if not url:
			# Fall back to regex extraction so URLs embedded in text are found.
			try:
				from api import getClipData
				clipboard_text = getClipData()
				extracted = self.linkManager.extract_urls_from_text(clipboard_text)
				if extracted:
					candidate = extracted[0]
					# Normalize bare "www." URLs to https so they become valid.
					if candidate.lower().startswith("www."):
						candidate = "https://" + candidate
					url = candidate
			except Exception as e:
				log.error("Error extracting URL from clipboard text: %s", e)
		url_field.SetValue(url)
		return url_field

	def _createButtons(self, panel, buttonSizer):
		"""
		Creates the OK and Cancel buttons and binds events to them.
		"""
		ok_button = wx.Button(panel, wx.ID_OK, _("&Ok"))
		cancel_button = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"))

		buttonSizer.addItem(ok_button)
		buttonSizer.addItem(cancel_button)

		self.Bind(wx.EVT_BUTTON, self.onOk, ok_button)
		self.Bind(wx.EVT_BUTTON, self.onCancel, cancel_button)

	def onOk(self, event):
		"""
		Handles the OK button click event, validates the data, and returns it.
		"""
		category = self.categoryChoice.GetStringSelection()
		url = self.textUrl.GetValue()

		if not category:
			# translators: Error message shown when no category is selected.
			self.showMessage(_("No category selected. Please select or add one!"), _("Attention"))
			return

		if not url:
			# translators: Error message shown when the URL field is empty.
			self.showMessage(_("URL is required!"), _("Attention"))
			self.textUrl.SetFocus()
			return

		# Attributes the results to a dictionary for easy access
		self.result = {'category': category, 'url': url}
		self.EndModal(wx.ID_OK)

	def onCancel(self, event):
		"""
		Handles the cancel event by closing the dialog.
		"""
		self.EndModal(wx.ID_CANCEL)

	def onKeyPress(self, event):
		"""
		Handles key press events, including the escape key to close the dialog.
		"""
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.onCancel(event)
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
