# Wox - Plugin for v2rayN PAC editing and syncing

### Flow for plugin
 - Define `plugin.json`
 - Make `main.py`

---
### Define `plugin.json`
 
 ```
 {
    "ID":"4f134ec8-7d55-11e9-bc5b-2a86e4085a59",
    "ActionKeyword":"h",
    "Name":"Hello World Python",
    "Description":"Hello World",
    "Author":"Wox",
    "Version":"1.0",
    "Language":"python",
    "Website":"https://github.com/Wox-launche/Wox",
    "IcoPath":"Images\\app.png",
    "ExecuteFileName":"main.py"
}
 ```
 
 > `ID`: defines uniqueness of plugin and can be generated from `https://www.uuidgenerator.net/`
 >
 > `ActionKeyword`: to enable the plugin in launcher
 > 
 > `Name`: Name of Plugin
 > 
 > `Description`: Short Description of the plugin
 >
 > `Author`: Name of creator of plugin
 >
 > `Version`: Version of Plugin
 >
 > `Language`: "python"
 >
 > `Website`: Website link to plugin
 >
 > `IcoPath`: Path to icon
 >
 > `ExecuteFileName`: The main file from where the execution to plugin can start

