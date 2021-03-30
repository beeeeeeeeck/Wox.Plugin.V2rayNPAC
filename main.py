# -*- coding: utf-8 -*-

from wox import Wox
import os
import json
import re
import subprocess

with open(os.path.abspath("config.json"), encoding = "utf-8") as f:
    data = json.load(f)
    v2rayNDirPath = data["v2rayN-Path"]

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
                "IcoPath":"Images/app.png",
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
                "IcoPath":"Images/app.png",
                "ContextData": "ctxData",
                "JsonRPCAction": {
                    'method': 'open_v2rayN_dir_directory',
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
                    "IcoPath":"Images/app.png",
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
                "IcoPath":"Images/app.png",
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
            "IcoPath":"Images/app.png"
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

        return None

    def open_plugin_directory(self):
        subprocess.Popen('explorer "{}"'.format(pluginHomeDirPath))

    def open_v2rayN_dir_directory(self):
        if not os.path.isdir(v2rayNDirPath):
            return
        subprocess.Popen('explorer "{}"'.format(v2rayNDirPath))

if __name__ == "__main__":
    V2rayNPACEditor()
