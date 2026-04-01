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

Created on: 11/04/2024
"""

import os
import webbrowser
from urllib.error import URLError
from webbrowser import BackgroundBrowser

import addonHandler
import api
import config
import queueHandler
import ui
import wx
from gui import guiHelper, mainFrame, messageBox
from logHandler import log

from .importBookmarks.gui import ImportBookmarksDialog
from .addLinks import AddLinks
from .editLinks import EditLinks
from .linkManager import LinkManager
from .varsConfig import ADDON_SUMMARY, ourAddon

# Initialize translation support
addonHandler.initTranslation()


class FavoriteLinks(wx.Dialog):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(FavoriteLinks, cls).__new__(cls, *args, **kwargs)
		else:
			msg = _("An instance of {} is already open.").format(ADDON_SUMMARY)
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, msg)
		return cls._instance

	def __init__(self, parent, title):
		if hasattr(self, "initialized"):
			return
		self.initialized = True

		self.title = title

		# LinkManager no longer needs json_file_path explicitly, it gets it from json_config
		self.linkManager = LinkManager()

		# Initializes the selected category as an empty string
		self.selectedCategory = ""

		WIDTH = 1500
		HEIGHT = 500

		super(FavoriteLinks, self).__init__(
			parent, title=title, size=(WIDTH, HEIGHT), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
		panel = wx.Panel(self)
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)
		buttonSizer = guiHelper.BoxSizerHelper(panel, wx.HORIZONTAL)

		self.labelOpenLinks = _("&Open link")
		self.labelAddLinks = _("&Add link")
		self.labelEditLink = _("&Edit link")
		self.labelDeleteLink = _("De&lete link")
		self.labelAddCategory = _("Add Cate&gory")
		self.labelEditCategory = _("Edi&t category")
		self.labelDeleteCategory = _("&Delete category")
		self.labelExportLinks = _("E&xport links")
		self.labelImportLinks = _("&Import links")
		self.labelImportWorker = _("Import &favorites from your browsers")
		self.labelSortLinks = _("&Sort links")
		self.labelCopyUrl = _("C&opy URL")
		self.labelExit = _("E&xit")

		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

		self.category = sizerHelper.addLabeledControl(
			_("Select a category"), wx.Choice, choices=[]
		)
		self.category.Bind(wx.EVT_CHOICE, self.onCategorySelected)
		self.category.Bind(wx.EVT_CONTEXT_MENU, self.onCategoryContextMenu)

		self.listLinks = sizerHelper.addLabeledControl(
			_("List of links..."), wx.ListCtrl, style=wx.LC_REPORT | wx.SUNKEN_BORDER
		)
		self.listLinks.Bind(wx.EVT_CONTEXT_MENU, self.onListContextMenu)
		self.listLinks.Bind(wx.EVT_KEY_DOWN, self.onListKeyPress)
		self.setColumns()

		buttons = [
			(self.labelOpenLinks, self.onOpenLink),
			(self.labelAddLinks, self.onAddLink),
			(self.labelEditLink, self.onEditLink),
			(self.labelDeleteLink, self.onDeleteLink),
			(self.labelAddCategory, self.onAddCategory),
			(self.labelExit, self.onExit)
		]

		for label, handler in buttons:
			button = wx.Button(panel, label=label)
			buttonSizer.addItem(button)
			self.Bind(wx.EVT_BUTTON, handler, button)

		boxSizer.Add(sizerHelper.sizer, 1, wx.ALL | wx.EXPAND, 10)  #, border=10, flag=wx.ALL | wx.EXPAND)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)
		self.Fit()

		# Update the UI elements
		self.updateAllUI()

	def onCategoryContextMenu(self, event):
		"""
		Displays a context menu for manipulating categories.

		Args:
			event (wx.Event): The event triggered by the context menu.
		"""
		mainFrame.prePopup()
		self.category.PopupMenu(self.categoryContextMenu(), self.category.GetPosition())
		mainFrame.postPopup()

	def categoryContextMenu(self):
		"""
		Creates a context menu for manipulating categories.

		Returns:
			wx.Menu: A menu containing options to add, edit, and delete categories,
			in addition to exporting and importing links.
		"""

		menu = wx.Menu()
		addCategory = menu.Append(wx.ID_ANY, self.labelAddCategory, _("Add a new category to the list."))
		self.Bind(wx.EVT_MENU, self.onAddCategory, addCategory)
		editCategory = menu.Append(wx.ID_ANY, self.labelEditCategory, _("Edit a category in the list."))
		self.Bind(wx.EVT_MENU, self.onEditCategory, editCategory)
		deleteCategory = menu.Append(wx.ID_ANY, self.labelDeleteCategory, _("Delete a category from the list."))
		self.Bind(wx.EVT_MENU, self.onDeleteCategory, deleteCategory)
		exportLinks = menu.Append(wx.ID_ANY, self.labelExportLinks, _("Export links"))
		self.Bind(wx.EVT_MENU, self.onExportLinks, exportLinks)
		importLinks = menu.Append(wx.ID_ANY, self.labelImportLinks, _("Import links"))
		self.Bind(wx.EVT_MENU, self.onImportLinks, importLinks)
		return menu

	def onListContextMenu(self, event):
		"""
		Displays a menu with several options for working with links.

		Args:
			event (wx.Event): The event triggered by the context menu.
		"""

		mainFrame.prePopup()
		menu = wx.Menu()

		addLink = menu.Append(wx.ID_ANY, self.labelAddLinks, _("Add a new link to the list."))
		self.Bind(wx.EVT_MENU, self.onAddLink, addLink)

		editLink = menu.Append(wx.ID_ANY, self.labelEditLink, _("Edit link."))
		self.Bind(wx.EVT_MENU, self.onEditLink, editLink)

		deleteLink = menu.Append(wx.ID_ANY, self.labelDeleteLink, _("Delete link"))
		self.Bind(wx.EVT_MENU, self.onDeleteLink, deleteLink)

		copyUrl = menu.Append(wx.ID_ANY, self.labelCopyUrl, _("Copy URL to clipboard."))
		self.Bind(wx.EVT_MENU, self.onCopyUrl, copyUrl)

		exportLinks = menu.Append(wx.ID_ANY, self.labelExportLinks, _("Export links"))
		self.Bind(wx.EVT_MENU, self.onExportLinks, exportLinks)

		importLinks = menu.Append(wx.ID_ANY, self.labelImportLinks, _("Import links"))
		self.Bind(wx.EVT_MENU, self.onImportLinks, importLinks)

		importWorker = menu.Append(wx.ID_ANY, self.labelImportWorker, _("Import Worker"))
		self.Bind(wx.EVT_MENU, self.onImportWorker, importWorker)

		sortLinks = menu.Append(wx.ID_ANY, self.labelSortLinks, _("Sort the links alphabetically."))
		self.Bind(wx.EVT_MENU, self.onSortTheLinksAlphabetically, sortLinks)

		openLink = menu.Append(wx.ID_ANY, self.labelOpenLinks, _("Open links in secondary browser."))
		self.Bind(wx.EVT_MENU, self.onOpenLinksSecondaryBrowser, openLink)

		self.listLinks.PopupMenu(menu, self.listLinks.GetPosition())
		mainFrame.postPopup()

	def onListKeyPress(self, event):
		"""
		Triggers the opening of the selected link in the default browser.

		Args:
			event (wx.Event): The event triggered when pressing enter on a link in the list.
		"""

		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_RETURN:
			self.onOpenLink(event)
		event.Skip()

	def setColumns(self):
		"""
		Adds the columns with titles to wx.ListCtrl.
		"""

		self.listLinks.InsertColumn(0, _("Title"), width=350)
		self.listLinks.InsertColumn(1, _("URL"), width=450)

	def onKeyPress(self, event):
		"""
			Handles key presses: closes dialog with Esc, deletes with Delete, edits with F2.

		Args:
			event (wx.Event): The event triggered when pressing a key. If Esc is pressed, the dialog is closed;
			if Delete is pressed, the selected link is deleted; if F2 is pressed, the link is edited.
		"""

		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_ESCAPE:
			self.onExit(event)
			return
		elif keyCode == wx.WXK_DELETE:
			self.onDeleteLink(event)
			return
		elif keyCode == wx.WXK_F2:
			self.onEditLink(event)
			return
		elif keyCode == ord('C') and event.ControlDown():
			self.onCopyUrl(event)
			return
		event.Skip()

	def onExportLinks(self, event):
		"""
		Exports system links to a json file.

		Args:
			event (wx.Event): The event triggered by the export links button.
		"""

		with wx.FileDialog(
			self, message=_("Save export file"), wildcard="JSON files (*.json)|*.json",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			exportPath = fileDialog.GetPath()
			try:
				self.linkManager.exportLinks(exportPath)

				# Translators: Message displayed when completing a link export
				self.showMessage(_("Links exported successfully!"), _("Success"))
			except Exception as e:
				log.error("Error exporting links: {}".format(e))

				# Translators: Message displayed when the export fails
				self.showMessage(_("Error exporting links: {}").format(e), _("Error"), wx.OK | wx.ICON_ERROR)

	def onImportLinks(self, event):
		"""
		Imports saved links back into the system.

		Args:
			event (wx.Event): The event triggered by the import links button.
		"""

		with wx.FileDialog(
			self, message=_("Open import file"), wildcard="JSON files (*.json)|*.json",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			importPath = fileDialog.GetPath()
			try:
				self.linkManager.importLinks(importPath)
				self.linkManager.loadJson()

				# Translators: Message displayed when completing a link import
				self.showMessage(_("Links imported successfully!"), _("Attention"))
				# Updates the interface
				self.updateAllUI()
			except Exception as e:
				log.error("Error importing links: %s", e)

				# Translators: Message displayed when the import fails
				self.showMessage(_("Error importing links: {}").format(e), _("Error"), wx.OK | wx.ICON_ERROR)

	def onOpenLink(self, event):
		"""
		Opens a saved link in your default browser.

		Args:
			event (wx.Event): The event triggered by the open link button.
		"""

		if not self.linkManager.is_internet_connected():
			# Translators: Message displayed when there is no internet connection
			self.showMessage(_("No active internet connection!"), _("Attention"))
			return
		self.listLinks.SetFocus()
		selectedItem = self.listLinks.GetFirstSelected()
		if selectedItem != -1:
			idx = selectedItem
			url = self.listLinks.GetItem(idx, 1).GetText()
			self.Close()
			try:
				webbrowser.open(url)
			except Exception as e:
				log.error(f"Error opening URL: {e}")
				# Translators: Message displayed when failing to open a link
				self.showMessage(_("Failed to open link: {}").format(e), _("Error"), wx.OK | wx.ICON_ERROR)
		else:
			# Translators: Message displayed when no link is selected
			self.showMessage(_("No link selected to open!"), _("Attention"))
			self.listLinks.SetFocus()

	def handleUserInput(self, message, caption, defaultValue="", handler=None):
		"""
		Displays a text input dialog to the user and optionally processes the input with a handler.

		Args:
			message (str): The message to be displayed in the dialog.
			caption (str): The title of the dialogue.
			default_value (str, optional): The default value to display in the input field. Defaults to "".
			handler (function, optional): A handling function that will be called with the entered value
		"""
		result = self.getUserInput(message, caption, defaultValue)
		if result and handler:
			handler(result)

	def onAddCategory(self, event):
		"""
		Calls the dialog for adding a new category.

		Args:
			event (wx.Event): The event triggered by the add category button.
		"""

		# Get the name of the new category of the user
		newCategory = self.getUserInput(_("Enter new category name:"), _("Add Category"))

		# Checks if the user has not canceled or left the field empty
		if newCategory:
			try:
				# Try to add the category
				self.linkManager.addCategory(newCategory)
				self.linkManager.saveLinks()

				# Updates the interface, passing the name of the new category
				# so that it is selected.
				self.selectedCategory = newCategory
				self.updateAllUI()

				# translators: Message displayed when a category is added
				self.showMessage(_("Category added successfully!"), _("Attention"))

			except ValueError as e:
				# translators: Message displayed when a category cannot be added
				self.showMessage(str(e))

	def addCategory(self, category):
		"""
		Adds a new category to the list.

		Args:
			event (wx.Event): The event triggered by the add category button.
	"""

		try:
			self.linkManager.addCategory(category)
			self.linkManager.saveLinks()
			self.linkManager.loadJson()

			# Translators: Message displayed when a category is added
			self.showMessage(_("Category added successfully!"), _("Attention"))
		except ValueError as e:
			# Translators: Message displayed when a category cannot be added
			self.showMessage(str(e), _("Error"), wx.OK | wx.ICON_ERROR)

	def onAddLink(self, event):
		selected_category = self.category.GetStringSelection()

		dlg = AddLinks(
			mainFrame,
			self.linkManager,
			title=_("Add New Link"),
			selectedCategory=selected_category
		)
		mainFrame.prePopup()

		if dlg.ShowModal() == wx.ID_OK:
			result = dlg.result
			category = result['category']
			url = result['url']

		# Ensure the variable exists
		title = ""

		try:
			# Try to get the title automatically
			title = self.linkManager.getTitleFromURL(url)
		except URLError as e:
			# It only logs the error, but does not interrupt the flow
			log.warning(f"Could not get title from URL: {e}")

		# Preserves captured (or empty) value
		title_temp = title

		# Always asks the user, using the title as the default value
		title = self.getUserInput(
			_("Enter the name of the link:"),
			_("Link name"),
			default_value=title_temp
		)

		if title:
			try:
				self.linkManager.addLinkToCategory(category, title, url)
				# translators: Message displayed when a link is added
				self.showMessage(_("Link added successfully!"), _("Attention"))
				self.selectedCategory = category

				# Always updates the UI
				self.updateAllUI()

			except ValueError as e:
				# translators: Message displayed when a link cannot be added
				self.showMessage(str(e), _("Error"), wx.OK | wx.ICON_ERROR)
		else:
			# translators: Message displayed when a link addition is cancelled
			self.showMessage(_("Link addition cancelled."), _("Attention"))

		# Always updates the UI
		self.updateAllUI()

		dlg.Destroy()
		mainFrame.postPopup()

	def onEditLink(self, event):
		"""
			Edit a selected link using the EditLinks dialog.
		"""
		# Get selection at the beginning of the method
		selected_item = self.listLinks.GetFirstSelected()
    
		# Make sure there is a valid selection
		if selected_item == -1:
			# translators: Message displayed when no link is selected to edit
			self.showMessage(_("No link selected to edit!"), _("Attention"))
			self.listLinks.SetFocus()
			return

		# Get the current data from the link
		oldCategory = self.category.GetStringSelection()
		oldTitle = self.listLinks.GetItem(selected_item, 0).GetText()
		oldURL = self.listLinks.GetItem(selected_item, 1).GetText()

		# Creates the dialogue passing the instance of Link Manager and the old data
		dlg = EditLinks(
			mainFrame,
			self.linkManager,
			title=_("Edit Link"),
			oldCategory=oldCategory,
			oldTitle=oldTitle,
			oldURL=oldURL
		)
		mainFrame.prePopup()

		if dlg.ShowModal() == wx.ID_OK:
			new_category = dlg.categoryChoice.GetStringSelection()
			new_title = dlg.textTitle.GetValue()
			new_url = dlg.textURL.GetValue()

			try:
				if new_category != oldCategory:
					self.linkManager.removeLinkFromCategory(oldCategory, oldTitle)
					self.linkManager.addLinkToCategory(new_category, new_title, new_url)
				else:
					self.linkManager.editLinkInCategory(oldCategory, oldTitle, new_title, new_url)
				# translators: Message displayed when a link is edited successfully
				self.showMessage(_("Link edited successfully!"), _("Attention"))
				self.selectedCategory = new_category  # Sets the category to be restored

			except (ValueError, KeyError) as e:
				# translators: Message displayed when a link cannot be edited
				self.showMessage(str(e), _("Error"), wx.OK | wx.ICON_ERROR)

			# Updates the interface
			self.updateAllUI()

		dlg.Destroy()
		mainFrame.postPopup()

	def onDeleteLink(self, event):
		"""
		Removes a link from the list.

		Args:
			event (wx.Event): The event triggered by the remove link button.
		"""

		self.selectedCategory = self.category.GetStringSelection()

		selected_item = self.listLinks.GetFirstSelected()
		if selected_item != -1:
			title = self.listLinks.GetItem(selected_item, 0).GetText()
			category = self.category.GetStringSelection()
			self.linkManager.removeLinkFromCategory(category, title)
			self.linkManager.saveLinks()
			self.linkManager.loadJson()

			# Translators: Message displayed when removing a link from the list
			self.showMessage(_("Link deleted successfully!"))
			self.category.SetStringSelection(category)

			# Call the function that updates the list of links
			self.onCategorySelected(None)
			self.listLinks.SetFocus()
		else:
			# Translators: Message displayed when no item has been selected from the list
			self.showMessage(_("No link selected to delete!"))
			self.listLinks.SetFocus()

	def onCopyUrl(self, event):
		"""
		Copies the URL of the selected link to the clipboard.

		Args:
			event (wx.Event): The event triggered by the copy URL option.
		"""

		selected_item = self.listLinks.GetFirstSelected()
		if selected_item != -1:
			url = self.listLinks.GetItem(selected_item, 1).GetText()
			api.copyToClip(url)

			# Translators: Message displayed when the URL is copied to the clipboard
			ui.message(_("URL copied to clipboard."))
		else:
			# Translators: Message displayed when no link is selected to copy
			self.showMessage(_("No link selected to copy!"))
			self.listLinks.SetFocus()

	def onEditCategory(self, event):
		"""
		Edits a selected category.

		Args:
			event (wx.Event): The event triggered by the edit category button.
		"""
		oldCategory = self.category.GetStringSelection()
		if not oldCategory:
			# translators: Message displayed when no category is selected to edit
			self.showMessage(_("No category selected to edit!"), _("Attention"))
			self.category.SetFocus()
			return

		# Get the new name of the User category
		newCategory = self.getUserInput(
			_("Edit category name:"),
			_("Edit Category"),
			oldCategory
		)

		if newCategory and newCategory != oldCategory:
			try:
				# Performs the editing operation
				self.linkManager.editCategoryName(oldCategory, newCategory)
				self.linkManager.saveLinks()

				# Defines the new selected category
				self.selectedCategory = newCategory

				# Calls the auxiliary function to update the interface
				self.updateAllUI()

				# translators: Message displayed when a category name is edited successfully
				self.showMessage(_("Category name edited successfully!"))

			except ValueError as e:
				# translators: Message displayed when a category name cannot be edited
				self.showMessage(str(e), _("Error"), wx.OK | wx.ICON_ERROR)

		self.category.SetFocus()

	def onDeleteCategory(self, event):
		"""
		Removes a category from the list.

		Args:
			event (wx.Event): The event triggered by the remove category button.
		"""
		selected_category = self.category.GetStringSelection()
		if not selected_category:
			# translators: Message displayed when no category is selected to delete
			self.showMessage(_("No category selected to delete!"))
			self.category.SetFocus()
			return

		# Confirm with the user if they really want to delete
		confirmMessage = _("Are you sure you want to delete the category '{}' and all its links?").format(selected_category)
		if messageBox(confirmMessage, _("Confirm Delete"), style=wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
			try:
				# Call the Linkmanager method to delete the category
				self.linkManager.deleteCategory(selected_category)

				# Defines the selected category as NONE so that the UI adjusts
				self.selectedCategory = None

				# Calls the auxiliary function to update the interface
				self.updateAllUI()

				# translators: Message displayed when a category is deleted successfully
				self.showMessage(_("Category deleted successfully!"))

			except Exception as e:
				# Treats possible errors that linkmanager may have
				log.error(f"Error deleting category: {e}")
				# translators: Message displayed when a category cannot be deleted
				self.showMessage(_("Error deleting category: {}").format(e), _("Error"), wx.OK | wx.ICON_ERROR)

	def getUserInput(self, message, caption, default_value=""):
		"""
		Displays an input dialog to get text from the user.

		Args:
			message (str): The message to display in the dialog box.
			caption (str): The title of the dialog box.
			default_value (str, optional): The default value of the input field. The default is "".

		Returns:
			str: The value entered by the user, or None if the dialog is cancelled.
		"""

		dlg = wx.TextEntryDialog(self, message, caption, value=default_value)
		if dlg.ShowModal() == wx.ID_OK:
			return dlg.GetValue()
		return None

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

	def onExit(self, event):
		"""
		Closes the dialog and destroys the window.

		Args:
			event (wx.Event): The event triggered by the cancel button.
		"""

		self.Destroy()
		FavoriteLinks._instance = None

	def onCategorySelected(self, event):
		"""
		Handles the selection of a category in the combobox and updates the list of displayed links.

		Args:
			event (wx.Event): The category selection event in the combobox.
		"""

		category = self.category.GetStringSelection()
		if category:
			self.listLinks.DeleteAllItems()
			links = self.linkManager.data.get(category, [])
			for idx, (title, url) in enumerate(links):
				self.listLinks.InsertItem(idx, title)
				self.listLinks.SetItem(idx, 1, url)

	def onSortTheLinksAlphabetically(self, event):
		"""
		Sort the links alphabetically.
		"""

		try:
			# Call the new method to order the links
			self.linkManager.sortAllLinksAndSave()
			# translators: Message displayed when links are sorted successfully
			self.showMessage(_("Successfully ordered!"))

			# Updates the interface
			self.updateAllUI()

		except Exception as e:
			log.error(f"Error when sorting links: {e}")
			# translators: Message displayed when there is an error ordering the links
			self.showMessage(_(f"Error when ordering! Details: {e}"), _("Error"), wx.OK | wx.ICON_ERROR)

	def updateAllUI(self):
		"""
		Auxiliary function to update the user interface after any data operation.
		"""
		# Recharge the data from the JSON file to the memory.
		self.linkManager.loadJson()

		# Updates the list of categories in the selection box.
		self.category.Clear()
		categories = list(self.linkManager.data.keys())
		self.category.AppendItems(categories)

		# Restores the selected category.
		if self.selectedCategory and self.selectedCategory in categories:
			self.category.SetStringSelection(self.selectedCategory)
		elif categories:
			# If the selected category no longer exists, select the first.
			self.category.SetSelection(0)
			self.selectedCategory = self.category.GetStringSelection()
		else:
			# If there are no categories, define selected category as an empty string.
			self.selectedCategory = ""

		# Update the list of links.
		self.onCategorySelected(None)

		# Defines the focus back to the link list.
		self.listLinks.SetFocus()

	def openLinkInSpecificBrowser(self, link):
		browser_path = config.conf[ourAddon.name].get("browserPath")

		if not browser_path:
			# translators: Message displayed when no browser path is configured
			self.showMessage(_("No browser path configured."))
			return

		# Checks if the browser executable exists
		if not os.path.exists(browser_path):
			# translators: Message displayed when the browser executable is not found
			self.showMessage(_("Browser not found at path: {}".format(browser_path)))
			return

		# Register the custom browser
		browserName = "customPortable"
		webbrowser.register(browserName, None, BackgroundBrowser(browser_path))

		# Open the link using the specified browser
		try:
			webbrowser.get(browserName).open(link)
		except webbrowser.Error:
			# translators: Message displayed when there is an error opening the link with the specified browser
			self.showMessage(_("Error opening the link with the browser: {}".format(browser_path)))

	def onOpenLinksSecondaryBrowser(self, event):
		if not self.linkManager.is_internet_connected():
			self.showMessage(_("No active internet connection!"))
			return
		self.listLinks.SetFocus()
		selected_item = self.listLinks.GetFirstSelected()
		if selected_item != -1:
			idx = selected_item
			url = self.listLinks.GetItem(idx, 1).GetText()
			self.Close()
			self.openLinkInSpecificBrowser(url)
		else:
			# translators: Message displayed when no link is selected to open
			self.showMessage(_("No link selected to open!"))
			self.listLinks.SetFocus()

	def onImportWorker(self, event):
		dlg = ImportBookmarksDialog(
			mainFrame,
			title=_("Import bookmarks from HTML"),
			onFinish=self.updateAllUI
		)
		mainFrame.prePopup()
		dlg.Show()
		mainFrame.postPopup()
