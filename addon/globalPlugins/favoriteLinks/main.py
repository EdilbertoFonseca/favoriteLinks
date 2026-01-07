# -*- coding: UTF-8 -*-

"""
Author: Edilberto Fonseca <edilberto.fonseca@outlook.com>
Copyright: (C) 2025 Edilberto Fonseca

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 11/04/2024
"""

import os
import webbrowser
from urllib.error import URLError
from webbrowser import BackgroundBrowser

import addonHandler
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
		self.link_manager = LinkManager()

		# Initializes the selected category as an empty string
		self.selected_category = ""

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
		self.set_columns()

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

		self.update_all_ui()

	def onCategoryContextMenu(self, event):
		"""
		Displays a context menu for manipulating categories.

		Args:
			event (wx.Event): The event triggered by the context menu.
		"""
		mainFrame.prePopup()
		self.category.PopupMenu(self.category_context_menu(), self.category.GetPosition())
		mainFrame.postPopup()

	def category_context_menu(self):
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

	def set_columns(self):
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
			export_path = fileDialog.GetPath()
			try:
				self.link_manager.export_links(export_path)

				# Translators: Message displayed when completing a link export
				self.show_message(_("Links exported successfully!"))
			except Exception as e:
				log.error("Error exporting links: {}".format(e))

				# Translators: Message displayed when the export fails
				self.show_message(_("Error exporting links: {}").format(e), _("Error"), wx.OK | wx.ICON_ERROR)

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
			import_path = fileDialog.GetPath()
			try:
				self.link_manager.import_links(import_path)
				self.link_manager.load_json()

				# Translators: Message displayed when completing a link import
				self.show_message(_("Links imported successfully!"))
				# Updates the interface
				self.update_all_ui()
			except Exception as e:
				log.error("Error importing links: %s", e)

				# Translators: Message displayed when the import fails
				self.show_message(_("Error importing links: {}").format(e), _("Error"), wx.OK | wx.ICON_ERROR)

	def onOpenLink(self, event):
		"""
		Opens a saved link in your default browser.

		Args:
			event (wx.Event): The event triggered by the open link button.
		"""

		if not self.link_manager.is_internet_connected():
			self.show_message(_("No active internet connection!"))
			return
		self.listLinks.SetFocus()
		selected_item = self.listLinks.GetFirstSelected()
		if selected_item != -1:
			idx = selected_item
			url = self.listLinks.GetItem(idx, 1).GetText()
			self.Close()
			try:
				webbrowser.open(url)
			except Exception as e:
				log.error(f"Error opening URL: {e}")
				self.show_message(_("Failed to open link: {}").format(e), _("Error"), wx.OK | wx.ICON_ERROR)
		else:
			self.show_message(_("No link selected to open!"))
			self.listLinks.SetFocus()

	def handle_user_input(self, message, caption, default_value="", handler=None):
		"""
		Displays a text input dialog to the user and optionally processes the input with a handler.

		Args:
			message (str): The message to be displayed in the dialog.
			caption (str): The title of the dialogue.
			default_value (str, optional): The default value to display in the input field. Defaults to "".
			handler (function, optional): A handling function that will be called with the entered value
		"""
		result = self.get_user_input(message, caption, default_value)
		if result and handler:
			handler(result)

	def onAddCategory(self, event):
		"""
		Calls the dialog for adding a new category.

		Args:
			event (wx.Event): The event triggered by the add category button.
		"""

		# Get the name of the new category of the user
		new_category = self.get_user_input(_("Enter new category name:"), _("Add Category"))

		# Checks if the user has not canceled or left the field empty
		if new_category:
			try:
				# Try to add the category
				self.link_manager.add_category(new_category)
				self.link_manager.save_links()

				# Updates the interface, passing the name of the new category
				# so that it is selected.
				self.selected_category = new_category
				self.update_all_ui()

				# Displays a success message
				self.show_message(_("Category added successfully!"))

			except ValueError as e:
				# Treat the error if the category already exists or the name is invalid
				self.show_message(str(e))

	def add_category(self, category):
		"""
		Adds a new category to the list.

		Args:
			event (wx.Event): The event triggered by the add category button.
	"""

		try:
			self.link_manager.add_category(category)
			self.link_manager.save_links()
			self.link_manager.load_json()

			# Translators: Message displayed when a category is added
			self.show_message(_("Category added successfully!"))
		except ValueError as e:
			self.show_message(str(e))

	def onAddLink(self, event):
		selected_category = self.category.GetStringSelection()

		dlg = AddLinks(
			mainFrame,
			self.link_manager,
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
			title = self.link_manager.get_title_from_url(url)
		except URLError as e:
			# It only logs the error, but does not interrupt the flow
			log.warning(f"Could not get title from URL: {e}")

		# Preserves captured (or empty) value
		title_temp = title

		# Always asks the user, using the title as the default value
		title = self.get_user_input(
			_("Enter the name of the link:"),
			_("Link name"),
			default_value=title_temp
		)

		if title:
			try:
				self.link_manager.add_link_to_category(category, title, url)
				self.show_message(_("Link added successfully!"))
				self.selected_category = category
			except ValueError as e:
				self.show_message(str(e), _("Error"), wx.OK | wx.ICON_ERROR)
		else:
			self.show_message(_("Link addition cancelled."))

		# Always updates the UI
		self.update_all_ui()

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
			self.show_message(_("No link selected to edit!"))
			self.listLinks.SetFocus()
			return

		# Get the current data from the link
		old_category = self.category.GetStringSelection()
		old_title = self.listLinks.GetItem(selected_item, 0).GetText()
		old_url = self.listLinks.GetItem(selected_item, 1).GetText()

		# Creates the dialogue passing the instance of Link Manager and the old data
		dlg = EditLinks(
			mainFrame,
			self.link_manager,
			title=_("Edit Link"),
			old_category=old_category,
			old_title=old_title,
			old_url=old_url
		)
		mainFrame.prePopup()

		if dlg.ShowModal() == wx.ID_OK:
			new_category = dlg.categoryChoice.GetStringSelection()
			new_title = dlg.txtTitle.GetValue()
			new_url = dlg.txtUrl.GetValue()

			try:
				if new_category != old_category:
					self.link_manager.remove_link_from_category(old_category, old_title)
					self.link_manager.add_link_to_category(new_category, new_title, new_url)
				else:
					self.link_manager.edit_link_in_category(old_category, old_title, new_title, new_url)

				self.show_message(_("Link edited successfully!"))
				self.selected_category = new_category  # Define a categoria para ser restaurada

			except (ValueError, KeyError) as e:
				self.show_message(str(e), _("Error"), wx.OK | wx.ICON_ERROR)

			# Updates the interface
			self.update_all_ui()

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
			self.link_manager.remove_link_from_category(category, title)
			self.link_manager.save_links()
			self.link_manager.load_json()

			# Translators: Message displayed when removing a link from the list
			self.show_message(_("Link deleted successfully!"))
			self.category.SetStringSelection(category)

			# Call the function that updates the list of links
			self.onCategorySelected(None)
			self.listLinks.SetFocus()
		else:
			# Translators: Message displayed when no item has been selected from the list
			self.show_message(_("No link selected to delete!"))
			self.listLinks.SetFocus()

	def onEditCategory(self, event):
		"""
		Edits a selected category.

		Args:
			event (wx.Event): The event triggered by the edit category button.
		"""
		old_category = self.category.GetStringSelection()
		if not old_category:
			self.show_message(_("No category selected to edit!"))
			self.category.SetFocus()
			return

		# Get the new name of the User category
		new_category = self.get_user_input(
			_("Edit category name:"),
			_("Edit Category"),
			old_category
		)

		if new_category and new_category != old_category:
			try:
				# Performs the editing operation
				self.link_manager.edit_category_name(old_category, new_category)
				self.link_manager.save_links()

				# Defines the new selected category
				self.selected_category = new_category

				# Calls the auxiliary function to update the interface
				self.update_all_ui()

				# Displays a success message
				self.show_message(_("Category name edited successfully!"))

			except ValueError as e:
				# Treat errors as an existing category name
				self.show_message(str(e), _("Error"), wx.OK | wx.ICON_ERROR)

		self.category.SetFocus()

	def onDeleteCategory(self, event):
		"""
		Removes a category from the list.

		Args:
			event (wx.Event): The event triggered by the remove category button.
		"""
		selected_category = self.category.GetStringSelection()
		if not selected_category:
			self.show_message(_("No category selected to delete!"))
			self.category.SetFocus()
			return

		# Confirm with the user if they really want to delete
		confirm_message = _("Are you sure you want to delete the category '{}' and all its links?").format(selected_category)
		if messageBox(confirm_message, _("Confirm Delete"), style=wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
			try:
				# Call the Linkmanager method to delete the category
				self.link_manager.delete_category(selected_category)

				# Defines the selected category as NONE so that the UI adjusts
				self.selected_category = None

				# Calls the auxiliary function to update the interface
				self.update_all_ui()

				# Displays a success message
				self.show_message(_("Category deleted successfully!"))

			except Exception as e:
				# Treats possible errors that linkmanager may have
				log.error(f"Error deleting category: {e}")
				self.show_message(_("Error deleting category: {}").format(e), _("Error"), wx.OK | wx.ICON_ERROR)

	def get_user_input(self, message, caption, default_value=""):
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

	def show_message(self, message, caption=_("Attention"), style=wx.OK | wx.ICON_INFORMATION):
		"""
		Displays a message to the user in a dialog box.

		Args:
			message (str): The message to be displayed.
			caption (str, optional): The title of the dialog box. The default is ("Message").
			style (int, optional): The style of the dialog box,
			combining flags like wx.OK,
			wx.CANCEL, wx.ICON INFORMATION, etc. The default is wx.OK | wx.ICON INFORMATION.
		"""

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
			links = self.link_manager.data.get(category, [])
			for idx, (title, url) in enumerate(links):
				self.listLinks.InsertItem(idx, title)
				self.listLinks.SetItem(idx, 1, url)

	def onSortTheLinksAlphabetically(self, event):
		"""
		Sort the links alphabetically.
		"""

		try:
			# Call the new method to order the links
			self.link_manager.sort_all_links_and_save()

			self.show_message(_("Successfully ordered!"))

			# Updates the interface
			self.update_all_ui()

		except Exception as e:
			log.error(f"Error when sorting links: {e}")
			self.show_message(_(f"Error when ordering! Details: {e}"), _("Error"), wx.OK | wx.ICON_ERROR)

	def update_all_ui(self):
		"""
		Auxiliary function to update the user interface after any data operation.
		"""
		# Recharge the data from the JSON file to the memory.
		self.link_manager.load_json()

		# Updates the list of categories in the selection box.
		self.category.Clear()
		categories = list(self.link_manager.data.keys())
		self.category.AppendItems(categories)

		# Restores the selected category.
		if self.selected_category and self.selected_category in categories:
			self.category.SetStringSelection(self.selected_category)
		elif categories:
			# If the selected category no longer exists, select the first.
			self.category.SetSelection(0)
			self.selected_category = self.category.GetStringSelection()
		else:
			# If there are no categories, define selected category as an empty string.
			self.selected_category = ""

		# Update the list of links.
		self.onCategorySelected(None)

		# Defines the focus back to the link list.
		self.listLinks.SetFocus()

	def open_link_in_specific_browser(self, link):
		browser_path = config.conf[ourAddon.name].get("browserPath")

		if not browser_path:
			self.show_message(_("No browser path configured."))
			return

		# Checks if the browser executable exists
		if not os.path.exists(browser_path):
			self.show_message(_("Browser not found at path: {}".format(browser_path)))
			return

		# Register the custom browser
		browser_name = "customPortable"
		webbrowser.register(browser_name, None, BackgroundBrowser(browser_path))

		# Open the link using the specified browser
		try:
			webbrowser.get(browser_name).open(link)
		except webbrowser.Error:
			self.show_message(_("Error opening the link with the browser: {}".format(browser_path)))

	def onOpenLinksSecondaryBrowser(self, event):
		if not self.link_manager.is_internet_connected():
			self.show_message(_("No active internet connection!"))
			return
		self.listLinks.SetFocus()
		selected_item = self.listLinks.GetFirstSelected()
		if selected_item != -1:
			idx = selected_item
			url = self.listLinks.GetItem(idx, 1).GetText()
			self.Close()
			self.open_link_in_specific_browser(url)
		else:
			self.show_message(_("No link selected to open!"))
			self.listLinks.SetFocus()

	def onImportWorker(self, event):
		dlg = ImportBookmarksDialog(
			mainFrame,
			title=_("Import bookmarks from HTML"),
			onFinish=self.update_all_ui
		)
		mainFrame.prePopup()
		dlg.Show()
		mainFrame.postPopup()
