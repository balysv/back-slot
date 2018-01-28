'''
MIT License Copyright(c) 2018 Balys Valentukevicius
'''

from slackclient import SlackClient
from config import Config
from slack_bot import *

class SlackPost:
    def __init__(self):
        config = Config()
        slackClient = SlackClient(config.slack_api_token)
        userData = UserData(slackClient)
        self.messagePoster = MessagePoster(slackClient,userData)

    def post(self):
        args = ArgParser(sys.argv[1:])
        self.messagePoster.post(args.channel, args.message, args.username, args.name, args.imageUrl, args.emoji)

'''
Usage: python slack_post.py (-u <username> | -n <name> (-e <emoji> | -i <image_url>)) -c <channel> -m <message>
'''
if __name__ == '__main__':
    SlackPost().post()
