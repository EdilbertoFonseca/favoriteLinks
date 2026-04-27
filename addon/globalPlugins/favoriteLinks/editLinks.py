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

# Initialize translation support
addonHandler.initTranslation()


class EditLinks(wx.Dialog):
	"""
	Dialog for link editions.
	This class is responsible for collecting user input to edit a link.
	It does not perform any business logic.

	Args:
		wx.Dialog: Displays a dialog box for editing the category, link, and URL.
	"""

	def __init__(self, parent, link_manager_instance, title, oldCategory, oldTitle="", oldURL=""):
		wx.Dialog.__init__(self, parent, title=title)

		# Receives the instance of the Linkmanager from the main dialogue
		self.linkManager = link_manager_instance
		self.oldCategory = oldCategory
		self.oldTitle = oldTitle
		self.oldURL = oldURL

		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Field to select the category
		categories = list(self.linkManager.data.keys())
		self.categoryChoice = sizerHelper.addLabeledControl(
			_("Select a Category"), wx.Choice, choices=categories
		)
		if self.oldCategory in categories:
			self.categoryChoice.SetStringSelection(self.oldCategory)

		# Field to edit the title
		self.textTitle = sizerHelper.addLabeledControl(
			_("Enter a title for the URL:"), wx.TextCtrl
		)
		self.textTitle.SetValue(self.oldTitle)

		# Field to edit the URL
		self.textURL = sizerHelper.addLabeledControl(
			_("Enter link URL:"), wx.TextCtrl
		)
		self.textURL.SetValue(self.oldURL)

		#Buttons
		okButton = wx.Button(panel, wx.ID_OK, _("&Ok"))
		cancelButton = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"))

		buttonSizer.addItem(okButton)
		buttonSizer.addItem(cancelButton)

		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)
		self.Fit()
		
		self.Bind(wx.EVT_BUTTON, self.onOk, okButton)
		self.Bind(wx.EVT_BUTTON, self.onCancel, cancelButton)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

	def onOk(self, event):
		"""
		Handles the OK button click event, validates the data, and closes the dialog.
		"""
		newCategory = self.categoryChoice.GetStringSelection()
		newTitle = self.textTitle.GetValue()
		newURL = self.textURL.GetValue()

		if not newCategory or not newTitle or not newURL:
			# translators: Error message displayed when the user leaves a field empty.
			self.showMessage(_("All fields are required"), _("Error"), wx.OK | wx.ICON_ERROR)
			return

		if not self.linkManager.isValidURL(newURL):
			# translators: Error message displayed when the user enters an invalid URL.
			self.showMessage(_("Invalid URL"), _("Error"), wx.OK | wx.ICON_ERROR)
			return
		
		# Returns the values ​​for the main dialog
		self.EndModal(wx.ID_OK)

	def onCancel(self, event):
		"""
		Handles the cancel event and closes the current window.
		"""
		self.EndModal(wx.ID_CANCEL)

	def onKeyPress(self, event):
		"""
		Closes the dialog by pressing the Esc key.
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
