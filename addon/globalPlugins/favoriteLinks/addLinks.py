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

	def __init__(self, parent, title):
		try:
			wx.Dialog.__init__(self, parent, title=title)
			panel = wx.Panel(self)
			boxSizer = wx.BoxSizer(wx.VERTICAL)
			sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
			buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

			# Bind the escape key event to the onCancel method
			self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

			# Initialize LinkManager
			self.link_manager = LinkManager()

			self.category = sizerHelper.addLabeledControl(
				_("Select a Category"), wx.Choice, choices=[]
			)
			self.link_manager.load_json(self)

			self.textURL = sizerHelper.addLabeledControl(
				_("Enter link URL:"), wx.TextCtrl
			)
			self.textURL.SetValue(self.link_manager.get_url_from_clipboard())

			buttons = [
				(_("&Ok"), self.onOk),
				(_("&Cancel"), self.onCancel),
			]

			for label, handler in buttons:
				button = wx.Button(panel, label=label)
				buttonSizer.addItem(button)
				self.Bind(wx.EVT_BUTTON, handler, button)

			boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL)
			boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
			panel.SetSizerAndFit(boxSizer)
		except Exception as e:
			logger.error(f"Error initializing AddLinks dialog: {e}")

	def onOk(self, event):
		"""
		Saves user-entered data to a JSON file.

		Args:
			event (wx.Event): Event triggered by the OK button.
		"""

		try:
			category = self.category.GetStringSelection()
			url_from_clipboard = self.textURL.GetValue()
			from_clipboard = url_from_clipboard if url_from_clipboard else ""
			url = from_clipboard
			if not category:
				self.show_message(_("No category selected. Please select or add one!"), _("Attention"))
				self.Destroy()
				return
			if not url:
				self.show_message(_("URL is required!"), _("Attention"))
				self.textURL.SetFocus()
				return
			if url:
				if category:
					try:
						title = self.link_manager.get_title_from_url(url)
						self.link_manager.add_link_to_category(category, title, url)
						self.link_manager.save_links()
						self.link_manager.load_json(self)
						self.show_message(_("Link added successfully!"))
					except ValueError as e:
						self.show_message(str(e))
			self.Destroy()
		except Exception as e:
			logger.error(f"Error adding link: {e}")
			self.show_message(_("An error occurred while adding the link."))

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Formats and displays messages to the user.

		Args:
			message (str): Message to be displayed.
			caption (str, optional): Window title. The default is _("Message").
			style (int, optional): Message box style, combining flags like wx.OK, wx.CANCEL, wx.ICON_INFORMATION, etc.
			The default is wx.OK | wx.ICON_INFORMATION.
		"""
		messageBox(message, caption, style)

	def onKeyPress(self, event):
		"""
		Closes the dialog window by pressing the Esc key.
		Args:
			event (wx.Event): The key press event that allows the window to be closed using the Esc key.
		"""
		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_ESCAPE:
			self.onCancel(event)
		event.Skip()

	def onCancel(self, event):
		"""
		Handles the cancel event and destroys the current window.

		Args:
			event (wx.Event): The cancel event that triggered this action.
		"""
		self.Destroy()
