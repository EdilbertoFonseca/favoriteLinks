# -*- coding: UTF-8 -*-

# Description: This add-on aims to: Save, edit and remove links from a list.
# Author: Edilberto Fonseca.
# Date of creation: 11/04/2024.

# import the necessary modules.
import logging

import webbrowser
import addonHandler
import gui
import queueHandler
import ui
import wx
from gui import guiHelper, mainFrame, messageBox

from .addLinks import AddLinks
from .editLinks import EditLinks
from .configPanel import dirJsonFile
from .linkManager import LinkManager

# Configure the logger instance for the current module, allowing logging of log messages.
logger = logging.getLogger(__name__)

# To start the translation process
addonHandler.initTranslation()

# Get the title of the addon defined in the summary.
ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


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
		self.link_manager = LinkManager(json_file_path=dirJsonFile)

		WIDTH = 1500
		HEIGHT = 500

		super(FavoriteLinks, self).__init__(parent, title=title, size=(WIDTH, HEIGHT),
		style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
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
		self.labelSortLinks = _("&Sort links")
		self.labelCancel = _("&Exit")

		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

		self.category = sizerHelper.addLabeledControl(
			_("Select a Category"), wx.Choice, choices=[]
		)
		self.category.Bind(wx.EVT_CHOICE, self.onCategorySelected)
		self.category.Bind(wx.EVT_CONTEXT_MENU, self.onCategoryContextMenu)

		self.listLinks = sizerHelper.addLabeledControl(
			_("List of links..."), wx.ListCtrl, style=wx.LC_REPORT | wx.SUNKEN_BORDER
		)
		self.listLinks.Bind(wx.EVT_CONTEXT_MENU, self.onListContextMenu)
		self.listLinks.Bind(wx.EVT_KEY_DOWN, self.onListKeyPress)
		self.set_columns()
		self.link_manager.load_json(self)

		buttons = [
			(self.labelOpenLinks, self.onOpenLink),
			(self.labelAddLinks, self.onAddLink),
			(self.labelEditLink, self.onEditLink),
			(self.labelDeleteLink, self.onDeleteLink),
			(self.labelAddCategory, self.onAddCategory),
			(self.labelCancel, self.onCancel)
		]

		for label, handler in buttons:
			button = wx.Button(panel, label=label)
			buttonSizer.addItem(button)
			self.Bind(wx.EVT_BUTTON, handler, button)

		boxSizer.Add(sizerHelper.sizer, border=10, flag=wx.ALL | wx.EXPAND)
		boxSizer.Add(buttonSizer.sizer, border=5, flag=wx.CENTER)
		panel.SetSizerAndFit(boxSizer)
		self.Fit()

	def onCategoryContextMenu(self, event):
		"""
		Displays a context menu for manipulating categories.

		Args:
			event (wx.Event): The event triggered by the context menu.
		"""
		gui.mainFrame.prePopup()
		self.category.PopupMenu(self.category_context_menu(), self.category.GetPosition())
		gui.mainFrame.postPopup()

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

		gui.mainFrame.prePopup()
		self.listLinks.PopupMenu(self.link_list_context_menu(), self.listLinks.GetPosition())
		gui.mainFrame.postPopup()

	def link_list_context_menu(self):
		"""
Itens do menu wx.ListCtrl.

		Returns:
			wx.Menu: A menu containing items for adding, editing, deleting, exporting, importing, and ordering links.
		"""

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
		sortLinks = menu.Append(wx.ID_ANY, self.labelSortLinks, _("Sort the links alphabetically."))
		self.Bind(wx.EVT_MENU, self.onOrdernar, sortLinks)
		return menu

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
		Closes the dialog by pressing the Esc key and destroys the window.

		Args:
			event (wx.Event): The event triggered by pressing the Esc key.
		"""

		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_ESCAPE:
			self.onCancel(event)
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
				self.show_message(_("Links exported successfully!"))
				self.listLinks.SetFocus()
			except Exception as e:
				logger.error(f"Error exporting links: {e}")
				self.show_message(_(f"Error exporting links: {e}"), _("Error"), wx.OK | wx.ICON_ERROR)

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
				self.link_manager.load_json(self)
				self.show_message(_("Links imported successfully!"))
				self.listLinks.SetFocus()
			except Exception as e:
				logger.error("Error importing links: %s", e)
				self.show_message(_(f"Error importing links: {e}"), _("Error"), wx.OK | wx.ICON_ERROR)

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
			webbrowser.open(url)
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
		self.handle_user_input(_("Enter new category name:"), _("Add Category"), handler=self.add_category)

	def add_category(self, category):
		"""
		Adds a new category to the list.

		Args:
			event (wx.Event): The event triggered by the add category button.
	"""

		try:
			self.link_manager.add_category(category)
			self.link_manager.save_links()
			self.link_manager.load_json(self)
			self.show_message(_("Category added successfully!"))
		except ValueError as e:
			self.show_message(str(e))

	def onAddLink(self, event):
		"""
		Calls the dialog for adding a new link.

		Args:
			event (wx.Event): The event triggered by the add link button.
		"""

		# Armazena a seleção da categoria
		self.selectedCategory = self.category.GetStringSelection()

		# Abre o diálogo para adicionar um novo link
		dlg = AddLinks(mainFrame, _("Add New Link"), self.selectedCategory)
		gui.mainFrame.prePopup()
		dlg.ShowModal()
		dlg.CenterOnScreen()
		dlg.Destroy()
		gui.mainFrame.postPopup()

		# Atualiza a lista de links
		wx.CallAfter(self.link_manager.load_json, self)

		# Restaura a seleção da categoria
		wx.CallAfter(self.category.SetStringSelection(self.selectedCategory))

		# Garante que o foco será restaurado na categoria após a atualização
		wx.CallAfter(self.category.SetFocus)

	def onEditLink(self, event):
		"""
		Edit a selected link using the EditLinks dialog.

		Args:
			event (wx.Event): The event triggered by the edit link button.

		Returns:
			bool: True if the link was edited successfully, False otherwise.
		"""

		selected_item = self.listLinks.GetFirstSelected()
		if selected_item != -1:
			old_category = self.category.GetStringSelection()
			old_title = self.listLinks.GetItem(selected_item, 0).GetText()
			old_url = self.listLinks.GetItem(selected_item, 1).GetText()

			# Create the EditLinks dialog
			dlg = EditLinks(
				mainFrame,
				title=_("Edit Link"),
				old_category=old_category,
				old_title=old_title,
				old_url=old_url
			)
			gui.mainFrame.prePopup()
			dlg.ShowModal()
			dlg.CenterOnScreen()
			wx.CallAfter(self.link_manager.load_json, self)
			dlg.Destroy()
			gui.mainFrame.postPopup()
			self.category.SetStringSelection(old_category)
			self.listLinks.SetFocus()
		else:
			self.show_message(_("No link selected to edit!"))

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
			self.link_manager.load_json(self)
			self.show_message(_("Link deleted successfully!"))
			self.category.SetStringSelection(self.selectedCategory)
			self.listLinks.SetFocus()
		else:
			self.show_message(_("No link selected to delete!"))
			self.listLinks.SetFocus()

	def onEditCategory(self, event):
		"""
		Edit a selected category.

		Args:
			event (wx.Event): The event triggered by the edit category button.
		"""

		old_category = self.category.GetStringSelection()
		if old_category:
			new_category = self.get_user_input(
				_("Edit category name:"),
				_("Edit Category"),
				old_category
			)
			if new_category:
				self.link_manager.edit_category_name(old_category, new_category)
				self.link_manager.save_links()
				self.link_manager.load_json(self)
				self.show_message(_("Category name edited successfully!"))
				self.category.SetFocus()
		else:
			self.show_message(_("No category selected to edit!"))
			self.category.SetFocus()

	def onDeleteCategory(self, event):
		"""
		Removes a category from the list.

		Args:
			event (wx.Event): The event triggered by the remove category button.
		"""

		selected_category = self.category.GetStringSelection()
		if selected_category:
			if messageBox(
				_("Are you sure you want to delete the category '{}' and all its links?").format(selected_category),
				_("Confirm Delete"), style=wx.ICON_QUESTION | wx.YES_NO) == wx.YES:
				self.link_manager.delete_category(selected_category)
				self.link_manager.save_links()
				self.link_manager.load_json(self)
				self.show_message(_("Category deleted successfully!"))
				self.category.SetFocus()
		else:
			self.show_message(_("No category selected to delete!"))
			self.category.SetFocus()

	def get_user_input(self, message, caption, default_value=""):
		"""
		Displays a dialog box for the user to enter text.

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

		gui.messageBox(message, caption, style)

	def onCancel(self, event):
		"""
		Cancels the dialogue and destroys the window.

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

	def onOrdernar(self, event):
		"""
		Sort the links alphabetically.

		Args:
			event (wx.Event): The event triggered by the sort button.
		"""

		try:
			self.link_manager.sort_json()
			self.show_message(_("Successfully ordered!"))
			self.link_manager.load_json(self)
			self.listLinks.SetFocus()
		except OSError:
			self.show_message(_("Error when ordering!"))
