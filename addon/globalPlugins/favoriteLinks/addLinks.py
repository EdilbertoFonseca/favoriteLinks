# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

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

	def __init__(self, parent, link_manager_instance, title, selectedCategory=""):
		# Dialog window title.
		self.title=title

		wx.Dialog.__init__(self, parent, title=title)
		
		# Receive the linkmanager instance
		self.link_manager = link_manager_instance
		self.selectedCategory = selectedCategory
		self.result = {}

		# Load the data from LinkManager
		if not self.link_manager.data:
			log.error("No categories available in LinkManager.")
			self.show_message(_("No categories available. Please add some categories first."), _("Error"))
			self.Destroy()
			return
			
		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Create and set up the category field
		self.categoryChoice = self._create_category_field(sizerHelper)

		# Create and set up the URL field
		self.txtUrl = self._create_url_field(sizerHelper)

		# Create buttons (OK and Cancel)
		self._create_buttons(panel, buttonSizer)

		# Add components to sizers
		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)

		self.Fit()

		# Bind escape key to cancel event
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

	def _create_category_field(self, sizerHelper):
		"""
		Creates and initializes the category field.
		"""
		categories = list(self.link_manager.data.keys())
		category_field = sizerHelper.addLabeledControl(
			_("Select a Category"), wx.Choice, choices=categories
		)
		if self.selectedCategory in categories:
			category_field.SetStringSelection(self.selectedCategory)
		return category_field

	def _create_url_field(self, sizerHelper):
		"""
		Creates and initializes the URL text field.
		"""
		url_field = sizerHelper.addLabeledControl(
			_("Enter link URL:"), wx.TextCtrl
		)
		url_field.SetValue(self.link_manager.get_url_from_clipboard())
		return url_field

	def _create_buttons(self, panel, buttonSizer):
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
		url = self.txtUrl.GetValue()

		if not category:
			self.show_message(_("No category selected. Please select or add one!"), _("Attention"))
			return

		if not url:
			self.show_message(_("URL is required!"), _("Attention"))
			self.txtUrl.SetFocus()
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

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Displays a message to the user.
		"""
		messageBox(message, caption, style)
