# -*- coding: utf-8 -*-
import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

import ctypes

def get_desktop_path():
	# 获取桌面路径，兼容多语言Windows
	try:
		import winshell
		return winshell.desktop()
	except ImportError:
		return os.path.join(os.path.expanduser("~"), 'Desktop')

def create_shortcut(target, shortcut_path, icon=None, description=None):
	# 创建Windows快捷方式
	import pythoncom
	from win32com.shell import shell, shellcon
	from win32com.client import Dispatch
	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut(shortcut_path)
	shortcut.Targetpath = target
	if icon:
		shortcut.IconLocation = icon
	if description:
		shortcut.Description = description
	shortcut.WorkingDirectory = os.path.dirname(target)
	shortcut.save()

def main():
	root = tk.Tk()
	root.withdraw()
	messagebox.showinfo("安装向导", "请选择安装路径，点击确定后开始安装。")

	install_dir = filedialog.askdirectory(title="选择安装路径")
	if not install_dir:
		messagebox.showwarning("安装取消", "未选择安装路径，安装已取消。")
		sys.exit(0)

	# 新建 collector 文件夹
	collector_dir = os.path.join(install_dir, "collector")
	os.makedirs(collector_dir, exist_ok=True)

	# 需要复制的文件
	files_to_copy = [
		("collect.exe", "collect.exe"),
		("logo_matrix.npy", "logo_matrix.npy"),
		("major.json", "major.json")
	]

	# 支持PyInstaller打包后内含数据文件
	if hasattr(sys, '_MEIPASS'):
		base_path = sys._MEIPASS
	else:
		base_path = os.path.dirname(sys.argv[0])
	for src, dst in files_to_copy:
		src_path = os.path.join(base_path, src)
		dst_path = os.path.join(collector_dir, dst)
		if not os.path.exists(src_path):
			messagebox.showerror("文件缺失", f"找不到 {src_path}，请确保所有安装文件与安装器在同一目录下！")
			sys.exit(1)
		shutil.copy2(src_path, dst_path)

	# 创建桌面快捷方式

	desktop = get_desktop_path()
	shortcut_name = "意向生收集系统.lnk"
	shortcut_path = os.path.join(desktop, shortcut_name)
	exe_path = os.path.join(collector_dir, "collect.exe")
	try:
		create_shortcut(exe_path, shortcut_path, icon=exe_path, description="意向生收集系统")
	except Exception as e:
		messagebox.showwarning("快捷方式创建失败", f"快捷方式创建失败：{e}\n请手动创建。")

	messagebox.showinfo("安装完成", f"安装完成！\n程序已安装到：{collector_dir}\n桌面已创建快捷方式。")

if __name__ == "__main__":
	main()
