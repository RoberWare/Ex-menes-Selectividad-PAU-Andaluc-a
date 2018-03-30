# -*- coding: utf-8 -*-

from github3 import login

user="bot"
pw="pleasedon'ttakethis"

gh = login(user, pw)
issue = gh.issue(user, repo, num)
if issue.is_closed():
    issue.reopen()

issue.edit('New issue title', issue.body + '\n------\n**Update:** Text to append')
