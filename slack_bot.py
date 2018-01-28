'''
MIT License Copyright(c) 2018 Balys Valentukevicius
'''

import time, json, sys, getopt

def printHelpAndExit(message=None):
    if message:
        print(message)
    print("Usage: slack_post (-u <username> | -n <name> (-e <emoji> | -i <image_url>)) -c <channel> -m <message>")
    sys.exit(2)

class UserData:
    def __init__(self, slackclient):
        users = slackclient.api_call("users.list")
        self.userMap = { user['profile']['display_name']: {
            "id": user['id'],
            "real_name": user['profile']['real_name'],
            "image": user['profile']['image_512']
        } for user in users['members']}

class ArgParser:
    def __init__(self, argv):
        self.username = None
        self.name = None
        self.emoji = None
        self.imageUrl = None
        self.channel = None
        self.message = None

        try:
            opts, args = getopt.getopt(argv, "u:c:m:n:e:i:")
        except getopt.GetoptError:
            printHelpAndExit()
        for opt, arg in opts:
            if opt in ("-u"):
                self.username = arg
            elif opt in ("-n"):
                self.name = arg
            elif opt in ("-e"):
                if not arg.startswith(":"):
                    arg = ":" + arg
                if not arg.endswith(":"):
                    arg = arg + ":"
                self.emoji = arg
            elif opt in ("-c"):
                if not arg.startswith("#"):
                    arg = "#" + arg
                self.channel = arg
            elif opt in ("-m"):
                self.message = arg
            elif opt in ("-i"):
                self.imageUrl = arg

class ArgValidator:

    def __init__(self, userMap):
        self.userMap = userMap

    def validate(self, channel, message, username, name, imageUrl, emoji):
        if not channel or not message:
            return (False, "Must provide 'channel' and 'message'")

        if username:
            if name or emoji or imageUrl:
                return (False, "Must not provide 'name', 'emoji' or 'image_url' when username is set!")
            if username not in self.userMap:
                return (False, "User with display name '" + username + "' does not exist! Check the one shown below the real name, i.e john.smith.")
            else:
                return (True, None)

        elif emoji:
            if imageUrl:
                return (False, "Must not provide or 'image_url' when 'emoji' is set!")
            if not name:
                return (False, "Must provide 'name' when 'emoji' is set!")
            else:
                return (True, None)

        elif imageUrl:
            if not name:
                return (False, "Must provide 'name' when 'imageUrl' is set!")
            else:
                return (True, None)
        else:
            return (False, "Must provide 'username', 'emoji' or 'imageUrl'")

class MessagePoster:

    def __init__(self, slackclient, userData):
        self.slackclient = slackclient
        self.userMap = userData.userMap
        self.validator = ArgValidator(userData.userMap)

    def post(self, channel, message, username=None, name=None, imageUrl=None, emoji=None):
        validationResult = self.validator.validate(channel, message, username, name, imageUrl, emoji)
        if not validationResult[0]:
            printHelpAndExit(validationResult[1])

        if username:
            self.postInSlack(channel, message, self.userMap[username]['real_name'], iconUrl=self.userMap[username]['image'])
        elif imageUrl:
            self.postInSlack(channel, message, name, iconUrl=imageUrl)
        elif emoji:
            self.postInSlack(channel, message, name, emoji=emoji)

    def postInSlack(self, channel, text, username, iconUrl=None, emoji=None):
        if iconUrl:
            self.slackclient.api_call("chat.postMessage", channel=channel, text=text, as_user="false", username=username, icon_url=iconUrl)
        else:
            self.slackclient.api_call("chat.postMessage", channel=channel, text=text, as_user="false", username=username, icon_emoji=emoji)
        print("OK!")
