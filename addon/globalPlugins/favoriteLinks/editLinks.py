# -*- coding: UTF-8 -*-

# Description: Dialog box for link edits

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2022-2025 Edilberto Fonseca

# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation: 28/05/2024

# import the necessary modules.
import addonHandler
import wx
from gui import guiHelper, messageBox
from logHandler import log

from .linkManager import LinkManager

# Initializes the translation
addonHandler.initTranslation()


class EditLinks(wx.Dialog):
	"""
	Dialog for links editions.

	Args:
		wx.Dialog: Displays a dialog box for editing the category, link, and URL.
	"""

	def __init__(self, parent, title, old_category, old_title="", old_url="", selected_category=""):
		try:
			wx.Dialog.__init__(self, parent, title=title)
			self.old_category = old_category
			self.old_title = old_title
			self.old_url = old_url
			self.selected_category = selected_category if selected_category else old_category  # Categoria persistente

			# Initialize LinkManager
			self.link_manager = LinkManager()

			panel = wx.Panel(self)
			boxSizer = wx.BoxSizer(wx.VERTICAL)
			sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
			buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

			# Field to select category
			self.category = sizerHelper.addLabeledControl(
				_("Select a Category"), wx.Choice, choices=list(self.link_manager.data.keys())
			)
			self.link_manager.load_json(self)

			# Set the selected category to the passed old_category
			if self.old_category in self.link_manager.data.keys():
				self.category.SetStringSelection(self.old_category)

			# Field to edit title
			self.textTitle = sizerHelper.addLabeledControl(
				_("Enter a title for the URL:"), wx.TextCtrl
			)
			self.textTitle.SetValue(self.old_title)

			# Field to edit URL
			self.textURL = sizerHelper.addLabeledControl(
				_("Enter link URL:"), wx.TextCtrl
			)
			self.textURL.SetValue(self.old_url)

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

			# Initialize result attribute if needed
			# self.result = None

			# Bind escape key to cancel event
			self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
		except Exception as e:
			log.error(f"Error initializing EditLinks dialog: {e}")
			# Translators: Message displayed when, for some reason, it is not possible to load the interface
			self.show_message(_("An error occurred while initializing the dialog."), _("Error"), wx.ICON_ERROR)
			self.onCancel()

	def save_selected_category(self):
		"""
		Save the selected category for persistence.
		"""
		self.selected_category = self.category.GetStringSelection()

	def onOk(self, event):
		"""
		Handles the OK button click event and captures the edited link details.

		Args:
			event (wx.Event): Event triggered by the OK button.
		"""
		new_category = self.category.GetStringSelection()
		new_title = self.textTitle.GetValue()
		new_url = self.textURL.GetValue()

		if not new_category or not new_title or not new_url:
			# Translators: Message displayed informing the user that all fields are required
			self.show_message(_("All fields are required"), _("Error"), wx.OK | wx.ICON_ERROR)
			return

		if not self.link_manager.is_valid_url(new_url):
			# Translators: Message displayed informing the user that the URL is not valid
			self.show_message(_("Invalid URL"), _("Error"), wx.OK | wx.ICON_ERROR)
			return

		try:
			self.selected_category = new_category  # Update the selected category

			if new_title and new_url:
				if new_category != self.old_category:
					# Remove the link from the old category
					self.link_manager.remove_link_from_category(self.old_category, self.old_title)
					# Add the link to the new category
					self.link_manager.add_link_to_category(new_category, new_title, new_url)
				else:
					# Edit the link within the same category
					self.link_manager.edit_link_in_category(self.old_category, self.old_title, new_title, new_url)

				self.link_manager.save_links()
				self.link_manager.load_json()
				# Translators: Message displayed informing that the edit was successful.
			self.show_message(_("Link edited successfully!"))

			# Persist the selected category before closing
			self.save_selected_category()
			self.EndModal(wx.ID_OK)
			self.Destroy()
		except Exception as e:
			# Translators: Message displayed informing that there was an error updating the link
			self.show_message(f'Error updating link: {e}', 'Error', wx.OK | wx.ICON_ERROR)

	def onKeyPress(self, event):
		"""
		Closes the dialog by pressing the Esc key and destroys the window.

		Args:
			event (wx.Event): The event triggered by pressing the Esc key.
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
		# Persist the selected category before closing
		self.save_selected_category()
		self.Destroy()

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Formats and displays messages to the user.

		Args:
			message (str): Message to be displayed.
			caption (str, optional): Window title. The default is _("Attention").
			style (int, optional): Message box style, combining flags like wx.OK, wx.CANCEL, wx.ICON_INFORMATION, etc.
			The default is wx.OK | wx.ICON_INFORMATION.
		"""
		messageBox(message, caption, style)
