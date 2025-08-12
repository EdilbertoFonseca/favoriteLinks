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

	def __init__(self, parent, link_manager_instance, title, old_category, old_title="", old_url=""):
		wx.Dialog.__init__(self, parent, title=title)

		# Receives the instance of the Linkmanager from the main dialogue
		self.link_manager = link_manager_instance
		self.old_category = old_category
		self.old_title = old_title
		self.old_url = old_url

		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		# Campo para selecionar a categoria (com o nome corrigido para 'categoryChoice')
		categories = list(self.link_manager.data.keys())
		self.categoryChoice = sizerHelper.addLabeledControl(
			_("Select a Category"), wx.Choice, choices=categories
		)
		if self.old_category in categories:
			self.categoryChoice.SetStringSelection(self.old_category)

		# Campo para editar o título (com o nome corrigido para 'txtTitle')
		self.txtTitle = sizerHelper.addLabeledControl(
			_("Enter a title for the URL:"), wx.TextCtrl
		)
		self.txtTitle.SetValue(self.old_title)

		# Campo para editar a URL (com o nome corrigido para 'txtUrl')
		self.txtUrl = sizerHelper.addLabeledControl(
			_("Enter link URL:"), wx.TextCtrl
		)
		self.txtUrl.SetValue(self.old_url)
		
		# Botões
		ok_button = wx.Button(panel, wx.ID_OK, _("&Ok"))
		cancel_button = wx.Button(panel, wx.ID_CANCEL, _("&Cancel"))
		
		buttonSizer.addItem(ok_button)
		buttonSizer.addItem(cancel_button)

		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)
		self.Fit()
		
		self.Bind(wx.EVT_BUTTON, self.onOk, ok_button)
		self.Bind(wx.EVT_BUTTON, self.onCancel, cancel_button)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

	def onOk(self, event):
		"""
		Handles the OK button click event, validates the data, and closes the dialog.
		"""
		new_category = self.categoryChoice.GetStringSelection()
		new_title = self.txtTitle.GetValue()
		new_url = self.txtUrl.GetValue()

		if not new_category or not new_title or not new_url:
			self.show_message(_("All fields are required"), _("Error"), wx.OK | wx.ICON_ERROR)
			return

		if not self.link_manager.is_valid_url(new_url):
			self.show_message(_("Invalid URL"), _("Error"), wx.OK | wx.ICON_ERROR)
			return
		
		# Retorna os valores para o diálogo principal
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

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Formats and displays messages to the user.
		"""
		messageBox(message, caption, style)
