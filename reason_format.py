from __future__ import print_function

import subprocess
import os, os.path
import re
import sublime, sublime_plugin


class ReasonFormatCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    # Hide the console window on Windows
    shell = False
    path_separator = ':'
    if os.name == "nt":
        shell = True
        path_separator = ';'

    settings = sublime.load_settings('Reason.sublime-settings')
    path = settings.get('reason_paths', '')

    if path:
      old_path = os.environ['PATH']
      os.environ['PATH'] = os.path.expandvars(path + path_separator + '$PATH')

    command = ['refmt.exe', self.view.file_name()]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)

    if path:
      os.environ['PATH'] = old_path

    output, errors = p.communicate()

    sel = sublime.Region(0, self.view.size())
    self.view.replace(edit, sel, output.decode("utf-8"))

    if settings.get('debug', False):
        print('(refmt) ' + str(output.strip()), '\nerrors: ' + str(errors.strip()))
        if str(errors.strip()):
            print('Your PATH is: ', os.environ['PATH'])
