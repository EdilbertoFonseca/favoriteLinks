# -*- coding: UTF-8 -*-

"""
Author: Abel Passos <abel.passos.listas@gmail.com>
Copyright: (C) 2025 Abel Passos 

This file is covered by the GNU General Public License.
See the file COPYING for more details or visit:
https://www.gnu.org/licenses/gpl-2.0.html

Created on: 20/12/2025
"""

import html as html_lib
import json
import os
import re
import threading
from urllib.request import Request, urlopen

import addonHandler
import ui
import wx
from gui import guiHelper, messageBox

from ..jsonConfig import json_config

# Initialize translation support
addonHandler.initTranslation()


def extract_urls_from_html(html_text: str):
	pattern = re.compile(
		r'<a\s+[^>]*href\s*=\s*["\']([^"\']+)["\']',
		re.IGNORECASE
	)
	return [
		html_lib.unescape(m.group(1).strip())
		for m in pattern.finditer(html_text)
		if m.group(1).strip()
	]


def fetch_page_title(url: str, timeout=8) -> str:
	try:
		req = Request(url, headers={"User-Agent": "NVDA-FavoriteLinks"})
		with urlopen(req, timeout=timeout) as r:
			if "text/html" not in r.headers.get("Content-Type", ""):
				return url
			data = r.read(256_000).decode("utf-8", errors="replace")
			m = re.search(r"<title[^>]*>(.*?)</title>", data, re.I | re.S)
			if m:
				return re.sub(r"\s+", " ", html_lib.unescape(m.group(1))).strip()
	except Exception:
		pass
	return url[:80]


class ProgressDialog(wx.Dialog):
	"""Progress dialog (SAFE)"""

	def __init__(self, parent):
		super().__init__(parent, title=_("Importing"), size=(420, 160))
		self.cancelled = False

		self.lblStatus = wx.StaticText(self, label=_("Starting…"))
		self.gauge = wx.Gauge(self, range=100)
		self.btnCancel = wx.Button(self, label=_("Cancel"))

		self.btnCancel.Bind(wx.EVT_BUTTON, self.on_cancel)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.lblStatus, 0, wx.ALL | wx.EXPAND, 10)
		sizer.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 10)
		sizer.Add(self.btnCancel, 0, wx.ALL | wx.ALIGN_CENTER, 10)

		self.SetSizer(sizer)
		self.CentreOnParent()

	def on_cancel(self, evt):
		self.cancelled = True



class ImportWorker(threading.Thread):
	"""
	Worker thread for importing bookmarks.
	"""

	def __init__(self, parent, html_path):
		super().__init__(daemon=True)
		self.parent = parent
		self.html_path = html_path
		self.cancelled = False

	def stop(self):
		self.cancelled = True

	def run(self):
		try:
			with open(self.html_path, "r", encoding="utf-8", errors="replace") as f:
				html = f.read()

			urls = list(dict.fromkeys(extract_urls_from_html(html)))
			if not urls:
				wx.CallAfter(self.parent.on_error, _("No links found."))
				return

			wx.CallAfter(self.parent.on_start, len(urls))

			items = []
			total = len(urls)

			for i, url in enumerate(urls, 1):
				if self.cancelled:
					wx.CallAfter(self.parent.on_cancelled)
					return

				title = fetch_page_title(url)
				items.append((title, url))

				wx.CallAfter(self.parent.on_progress, i, total, title)

			wx.CallAfter(self.parent.on_done, items)

		except Exception as e:
			wx.CallAfter(self.parent.on_error, str(e))



class ImportBookmarksDialog(wx.Dialog):
	"""Main dialog (NVDA-style)"""

	def __init__(self, parent, title, onFinish=None):
		# Dialog window title.
		self.title=title

		super().__init__(parent, title=title)
		self.onFinish = onFinish
		self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

		panel = wx.Panel(self)
		self.worker = None
		self.progressDlg = None
		self.html_path = ""

		boxSizer = wx.BoxSizer(wx.VERTICAL)
		sizerHelper = guiHelper.BoxSizerHelper(panel, wx.VERTICAL)

		self.txtHtml = sizerHelper.addLabeledControl(
			_("HTML file:"), wx.TextCtrl
		)

		self.btnBrowse = sizerHelper.addItem(
			wx.Button(panel, label=_("&Select HTML..."))
		)
		self.btnBrowse.Bind(wx.EVT_BUTTON, self.on_browse)

		self.btnImport = sizerHelper.addItem(
			wx.Button(panel, label=_("&Import"))
		)
		self.btnImport.Bind(wx.EVT_BUTTON, self.on_import)

		boxSizer.Add(sizerHelper.sizer, 1, wx.ALL | wx.EXPAND, 10)
		panel.SetSizerAndFit(boxSizer)
		self.Fit()


	def on_browse(self, evt):
		with wx.FileDialog(
			self,
			_("Select HTML file"),
			wildcard="HTML (*.html)|*.html",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as dlg:
			if dlg.ShowModal() == wx.ID_OK:
				self.html_path = dlg.GetPath()
				self.txtHtml.SetValue(self.html_path)

	def on_import(self, evt):
		if not os.path.isfile(self.html_path):
			ui.message(_("Select a valid HTML file."))
			return

		self.btnImport.Disable()

		self.progressDlg = ProgressDialog(self)
		self.progressDlg.Show()

		self.worker = ImportWorker(self, self.html_path)
		self.worker.start()

	# Worker callbacks
	def on_start(self, total):
		self.total = total
		self.progressDlg.lblStatus.SetLabel(_("Importing links…"))

	def on_progress(self, current, total, title):
		if self.progressDlg.cancelled:
			self.worker.stop()
			return

		percent = int((current / total) * 100)
		self.progressDlg.gauge.SetValue(percent)
		self.progressDlg.lblStatus.SetLabel(f"{current}/{total} – {title}")

	def on_done(self, items):
		self._close_progress()

		json_path = json_config.get_current_json_path()
		data = {}

		if os.path.isfile(json_path):
			try:
				with open(json_path, "r", encoding="utf-8") as f:
					data = json.load(f)
			except Exception:
				data = {}

		category = _("Imported Bookmarks")
		data.setdefault(category, [])

		existing = {u for _, u in data[category]}
		for title, url in items:
			if url not in existing:
				data[category].append([title, url])

		with open(json_path, "w", encoding="utf-8") as f:
			json.dump(data, f, indent=2, ensure_ascii=False)

		messageBox(_("Import completed successfully."))

		if callable(self.onFinish):
			wx.CallAfter(self.onFinish)

		self.btnImport.Enable()
		self.Destroy()

	def on_cancelled(self):
		self._close_progress()
		ui.message(_("Import cancelled."))
		self.btnImport.Enable()

	def on_error(self, msg):
		self._close_progress()
		ui.message(msg)
		self.btnImport.Enable()

	def _close_progress(self):
		if self.progressDlg:
			self.progressDlg.Destroy()
			self.progressDlg = None

	def on_key_press(self, evt):
		if evt.GetKeyCode() == wx.WXK_ESCAPE:
			if self.worker and self.worker.is_alive():
				self.worker.stop()
			self.Destroy()
			return
		evt.Skip()
