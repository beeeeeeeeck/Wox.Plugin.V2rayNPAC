# Wox - Plugin for v2rayN PAC editing and syncing

### Quick start
Pull down this repository at your Wox plugin directory which is usually in **[USER_DIR\AppData\Local\Wox\app-x.x.xxx\Plugins]()**.
 - `pac xxxx.com` to add new user rule
 - `pac xxx` and then select existing rule to remove it
 - `pac sync` to sync up with github storage (Note that the [github access configuration](#config) should be set before this)

---

### <a name="config"></a>Configuration - define `config.json` in the plugin directory

 ```
{
    "v2rayN-Path":"D:/v2ray/v2rayN",
    "Github-Token":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "Github-Repo-Name":"xxxxxx/pac-user-rules",
    "Github-Repo-Branch-Name":"main",
    "Github-Repo-File-Name":"rules.json"
}
 ```


### Prerequisites

 > `Wox`: Install Wox from [here](https://github.com/Wox-launcher/Wox/releases)
 >
 > `Python`: this is required by Wox - [check this out to install](https://www.python.org/downloads/windows/)
 >
 > `Python libs`: since this plugin is implemented by Python, we need the following python libs installed
 > - `pip install PyGithub`
 > - `pip install win10toast`
 >
 > `Github Repository`:
 > 1. Create a new private repository with the default **README.md** file
 > 2. Create github access token for this plugin
 > 3. Update plugin [configuration](#config) accordingly

---

Start to play the plugin and enjoy the convenient !