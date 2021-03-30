# -*- coding: utf-8 -*-

from wox import Wox
import os
import json
import re
import subprocess
from github import Github
from datetime import datetime
from win10toast import ToastNotifier

with open(os.path.abspath("config.json"), encoding = "utf-8") as f:
    data = json.load(f)
    v2rayNDirPath = data["v2rayN-Path"]
    GithubAccessToken = data["Github-Token"]
    GithubRepoName = data["Github-Repo-Name"]
    GithubRepoBranchName = data["Github-Repo-Branch-Name"]
    GithubRepoFileName = data["Github-Repo-File-Name"]

pluginHomeDirPath = os.path.dirname(os.path.realpath(__file__))
configFilePath = os.path.join(v2rayNDirPath, 'guiNConfig.json') if len(v2rayNDirPath) > 0 else ''

class V2rayNPACEditor(Wox):

    # query is default function to receive realtime keystrokes from wox launcher
    def query(self, query):
        results = []
        if not v2rayNDirPath or len(v2rayNDirPath) == 0:
            results.append({
                "Title": "Configuration Error",
                "SubTitle": "Add v2rayN home dir to config.json in {}".format(pluginHomeDirPath),
                "IcoPath": "Images/app.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'open_plugin_directory',
                    'dontHideAfterAction': False
                }
            })
            return results

        if not os.path.exists(configFilePath):
            results.append({
                "Title": "Configuration Error",
                "SubTitle": "v2rayN config file NOT FOUND - {}".format(configFilePath),
                "IcoPath": "Images/app.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'open_v2rayN_dir_directory',
                    'dontHideAfterAction': False
                }
            })
            return results

        if len(query) > 0 and query == "sync":
            results.append({
                "Title": "Sync up user rules",
                "SubTitle": "Sync up with github storage",
                "IcoPath": "Images/github.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'sync_up_user_rules',
                    'dontHideAfterAction': False
                }
            })
            return results

        # Opening v2rayN config JSON file
        f = open(configFilePath,)
        # returns JSON object as a dictionary
        data = json.load(f)
        # Closing file
        f.close()

        existingRules = data['userPacRule']
        if len(query) > 0:
            existingRules = filter(lambda rule: rule.startswith(query), existingRules)
            if bool(re.match("(([\da-zA-Z])([_\w-]{,62})\.){,127}(([\da-zA-Z])[_\w-]{,61})?([\da-zA-Z]\.((xn\-\-[a-zA-Z\d]+)|([a-zA-Z\d]{2,})))", query)):
                results.append({
                    "Title": "Add new rule",
                    "SubTitle": "Add this rule - {}".format(query),
                    "IcoPath": "Images/app.png",
                    "ContextData": "ctxData",
                    "JsonRPCAction": {
                        'method': 'take_action_4_new_rule',
                        'parameters': [query],
                        'dontHideAfterAction': False
                    }
                })

        for existingRule in existingRules:
            results.append({
                "Title": existingRule,
                "SubTitle": "Remove this rule",
                "IcoPath": "Images/app.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'take_action_4_existing_rule',
                    'parameters': [existingRule],
                    'dontHideAfterAction': False
                }
            })

        return results

    # context_menu is default function called for ContextData where `data = ctxData`
    def context_menu(self, data):
        results = []
        results.append({
            "Title": "Context menu entry",
            "SubTitle": "Data: {}".format(data),
            "IcoPath": "Images/app.png"
        })
        return results

    def take_action_4_new_rule(self, newRule):
        # Opening v2rayN config JSON file
        f = open(configFilePath,)
        # returns JSON object as a dictionary
        data = json.load(f)
        # Closing file
        f.close()

        # data['userPacRule'].append(newRule)
        ruleSet = set()
        ruleSet.update(data["userPacRule"])
        newRule = newRule.lower().replace("https://", "").replace("http://", "").rstrip("/") # clean up sth unnecessary
        ruleSet.add(newRule)
        ruleList = list(ruleSet)
        ruleList.sort()
        data["userPacRule"] = ruleList

        with open(configFilePath, 'w+', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)

            os.system('taskkill /IM "v2rayN.exe" /F')
            # print(f"killed v2rayN")
            subprocess.Popen([os.path.join(v2rayNDirPath, "v2rayN.exe")])

            toaster.show_toast("Wox.Plugin.v2rayNPAC", "New rule has been added and v2rayN is just restarted !", icon_path = "Images/success_notification.ico", duration = 10, threaded = True)

        return None

    def take_action_4_existing_rule(self, existingRule):
        # Opening v2rayN config JSON file
        f = open(configFilePath,)
        # returns JSON object as a dictionary
        data = json.load(f)
        # Closing file
        f.close()

        ruleList = data["userPacRule"]
        if not (existingRule in ruleList):
            return None

        ruleList.remove(existingRule)
        ruleList.sort()
        data["userPacRule"] = ruleList

        with open(configFilePath, 'w+', encoding = 'utf-8') as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)

            os.system('taskkill /IM "v2rayN.exe" /F')
            # print(f"killed v2rayN")
            subprocess.Popen([os.path.join(v2rayNDirPath, "v2rayN.exe")])

            toaster.show_toast("Wox.Plugin.v2rayNPAC", "Existing rule has been removed and v2rayN is just restarted !", icon_path = "Images/success_notification.ico", duration = 10, threaded = True)

        return None

    def open_plugin_directory(self):
        subprocess.Popen('explorer "{}"'.format(pluginHomeDirPath))

    def open_v2rayN_dir_directory(self):
        if not os.path.isdir(v2rayNDirPath):
            toaster.show_toast("Wox.Plugin.v2rayNPAC", "Configuration Error for v2rayN directory path !", icon_path = "Images/fail_notification.ico", duration = 10, threaded = True)
            return
        subprocess.Popen('explorer "{}"'.format(v2rayNDirPath))

    def sync_up_user_rules(self):
        toaster = ToastNotifier()
        if not GithubAccessToken or len(GithubAccessToken) == 0:
            toaster.show_toast("Wox.Plugin.v2rayNPAC", "Configuration Error for Github Access Token !", icon_path = "Images/fail_notification.ico", duration = 10, threaded = True)
            return
        if not GithubRepoName or len(GithubRepoName) == 0:
            toaster.show_toast("Wox.Plugin.v2rayNPAC", "Configuration Error for Github Repository Name, it should be full name started with the account name !", icon_path = "Images/fail_notification.ico", duration = 10, threaded = True)
            return
        if not GithubRepoBranchName or len(GithubRepoBranchName) == 0:
            toaster.show_toast("Wox.Plugin.v2rayNPAC", "Configuration Error for Github Repository Branch Name, it should be existing !", icon_path = "Images/fail_notification.ico", duration = 10, threaded = True)
            return
        if not GithubRepoFileName or len(GithubRepoFileName) == 0:
            toaster.show_toast("Wox.Plugin.v2rayNPAC", "Configuration Error for Github Repository File Name, it should be in the root directory !", icon_path = "Images/fail_notification.ico", duration = 10, threaded = True)
            return

        # using an access token
        g = Github(GithubAccessToken)
        repo = g.get_repo(GithubRepoName)
        repoFiles = repo.get_contents("", ref = GithubRepoBranchName)
        existingRuleFile = None
        while repoFiles:
            repoFile = repoFiles.pop(0)
            if len(repoFile.name) > 0 and repoFile.name.endswith(GithubRepoFileName):
                existingRuleFile = repoFile
        if not existingRuleFile:
            emptyRules = {}
            emptyRules['rules'] = list()
            repo.create_file(GithubRepoFileName, "Created default rules.json file", json.dumps(emptyRules, indent = 4), branch = GithubRepoBranchName)

        ruleFile = repo.get_contents(GithubRepoFileName, ref = GithubRepoBranchName)
        ruleFileContent = ruleFile.decoded_content.decode('utf8').replace("'", '"')
        ruleFileData = json.loads(ruleFileContent)

        # Opening v2rayN config JSON file
        f = open(configFilePath,)
        # returns JSON object as a dictionary
        configFileData = json.load(f)
        # Closing file
        f.close()

        ruleSet = set()
        ruleSet.update(ruleFileData['rules'])
        ruleSet.update(configFileData["userPacRule"])
        ruleList = list(ruleSet)
        ruleList.sort()
        ruleFileData['rules'] = ruleList
        configFileData["userPacRule"] = ruleList

        now = datetime.now() # current date and time
        currentDateTime = now.strftime("%m/%d/%Y %H:%M:%S")
        repo.update_file(ruleFile.path, "Rules file synced at {}".format(currentDateTime), json.dumps(ruleFileData, indent = 4), ruleFile.sha, branch = GithubRepoBranchName)

        with open(configFilePath, 'w+', encoding = 'utf-8') as f:
            json.dump(configFileData, f, ensure_ascii = False, indent = 4)

            os.system('taskkill /IM "v2rayN.exe" /F')
            # print(f"killed v2rayN")
            subprocess.Popen([os.path.join(v2rayNDirPath, "v2rayN.exe")])

            toaster.show_toast("Wox.Plugin.v2rayNPAC", "Rules has been synced up with github storage and v2rayN is just restarted !", icon_path = "Images/success_notification.ico", duration = 10, threaded = True)


if __name__ == "__main__":
    V2rayNPACEditor()
