# -*- coding: UTF-8 -*-

# Description: Dialog for link additions
# Author: Edilberto Fonseca
# Email: edilberto.fonseca@outlook.com
# Date of creation: 28/05/2024

# import the necessary modules.
import logging

import addonHandler
import wx
from gui import guiHelper, messageBox

from .linkManager import LinkManager

# Configure the logger instance for the current module, allowing logging of log messages.
logger = logging.getLogger(__name__)

# For translation process
addonHandler.initTranslation()


class AddLinks(wx.Dialog):
	"""
	Dialog for link registration.

	Args:
		wx.Dialog: Displays a dialog for selecting the category and adding the URL.
	"""

	def __init__(self, parent, title, selectedCategory=""):
		try:
			wx.Dialog.__init__(self, parent, title=title)
			self.selectedCategory = selectedCategory  # Categoria persistente

			# Initialize LinkManager
			self.link_manager = LinkManager()

			# Load the data from LinkManager
			self.link_manager.load_json()

			# Verify if categories are loaded
			if not self.link_manager.data:
				logger.error("No categories available in LinkManager.")
				# Translators: Message displayed when no category is registered in the system
				self.show_message(_("No categories available. Please add some categories first."), _("Error"))
				self.Destroy()
				return

			panel = wx.Panel(self)
			boxSizer = wx.BoxSizer(wx.VERTICAL)
			sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
			buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

			# Create and set up the category field
			self.category = self._create_category_field(sizerHelper)

			# Create and set up the URL field
			self.textURL = self._create_url_field(sizerHelper)

			# Create buttons (OK and Cancel)
			self._create_buttons(panel, buttonSizer)

			# Add components to sizers
			boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL)
			boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
			panel.SetSizerAndFit(boxSizer)

			# Bind escape key to cancel event
			self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
		except Exception as e:
			logger.error(f"Error initializing AddLinks dialog: {e}")
			# Translators: Message displayed when it is not possible to load the interface
			self.show_message(_("An error occurred while initializing the dialog."), _("Error"), wx.ICON_ERROR)
			self.onCancel()

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
		buttons = [(_("&Ok"), self.onOk), (_("&Cancel"), self.onCancel)]
		for label, handler in buttons:
			button = wx.Button(panel, label=label)
			buttonSizer.addItem(button)
			self.Bind(wx.EVT_BUTTON, handler, button)

	def save_selected_category(self):
		"""
		Saves the selected category for persistence.
		"""
		self.selectedCategory = self.category.GetStringSelection()

	def onOk(self, event):
		"""
		Saves user-entered data to the LinkManager.

		Args:
			event (wx.Event): Event triggered by the OK button.
		"""
		try:
			category = self.category.GetStringSelection()
			url = self.textURL.GetValue()

			# Validate inputs
			if not category:
				# Translators: Message displayed when there are no categories registered
				self.show_message(_("No category selected. Please select or add one!"), _("Attention"))
				self.Destroy()
				return

			if not url:
				# Translators: Message displayed informing the user that the URL field cannot be empty
				self.show_message(_("URL is required!"), _("Attention"))
				self.textURL.SetFocus()
				return

			# Add the link to the category
			try:
				title = self.link_manager.get_title_from_url(url)
				self.link_manager.add_link_to_category(category, title, url)
				self.link_manager.save_links()
				self.link_manager.load_json()
				# Translators: Message displayed informing that the link was added successfully
				self.show_message(_("Link added successfully!"))
			except ValueError as e:
				self.show_message(str(e),)

			# Save selected category before closing
			self.save_selected_category()
			self.EndModal(wx.ID_OK)
			self.Destroy()
		except Exception as e:
			logger.error(f"Error adding link: {e}")
			# Translators: Message displayed to the user informing that there was an error adding the link
			self.show_message(_("An error occurred while adding the link."))

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Displays a message to the user.

		Args:
			message (str): Message to be displayed.
			caption (str, optional): Window title.
			style (int, optional): Style of the message box.
		"""
		messageBox(message, caption, style)

	def onKeyPress(self, event):
		"""
		Handles key press events, including the escape key to close the dialog.

		Args:
			event (wx.Event): The key press event.
		"""
		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_ESCAPE:
			self.onCancel(event)
		event.Skip()

	def onCancel(self, event):
		"""
		Handles the cancel event by closing the dialog.

		Args:
			event (wx.Event): The cancel event.
		"""
		# Save selected category before closing
		self.save_selected_category()
		self.Destroy()
