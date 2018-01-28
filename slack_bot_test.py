'''
MIT License Copyright(c) 2018 Balys Valentukevicius
'''

import unittest
from slack_bot import *

class ValidatorTest(unittest.TestCase):

    def setUp(self):
        userMap = {'test': {'id': 'ID', 'real_name': 'Test', 'image': 'image'}}
        self.validator = Validator(userMap)

    def tearDown(self):
        self.validator = None

    def test_channel_required(self):
        result = self.validator.validate(channel=None, message="msg", username="test", name=None, imageUrl=None, emoji=None)
        self.assertFalse(result[0])

    def test_message_required(self):
        result = self.validator.validate(channel="channel", message=None, username="test", name=None, imageUrl=None, emoji=None)
        self.assertFalse(result[0])

    def test_username_required_if_no_image_or_emoji(self):
        result = self.validator.validate(channel="channel", message="msg", username=None, name=None, imageUrl=None, emoji=None)
        self.assertFalse(result[0])

    def test_username_in_userMap(self):
        result = self.validator.validate(channel="channel", message="msg", username="test", name=None, imageUrl=None, emoji=None)
        self.assertTrue(result[0])

    def test_username_not_in_userMap(self):
        result = self.validator.validate(channel="channel", message="msg", username="test_new", name=None, imageUrl=None, emoji=None)
        self.assertFalse(result[0])

    def test_username_and_name_cannot_be_set(self):
        result = self.validator.validate(channel="channel", message="msg", username="test", name="name", imageUrl=None, emoji=None)
        self.assertFalse(result[0])

    def test_username_and_imageUrl_cannot_be_set(self):
        result = self.validator.validate(channel="channel", message="msg", username="test", name=None, imageUrl="image", emoji=None)
        self.assertFalse(result[0])

    def test_username_and_emoji_cannot_be_set(self):
        result = self.validator.validate(channel="channel", message="msg", username="test", name=None, imageUrl=None, emoji="emoji")
        self.assertFalse(result[0])

    def test_imageUrl_and_emoji_cannot_be_set(self):
        result = self.validator.validate(channel="channel", message="msg", username=None, name=None, imageUrl="image", emoji="emoji")
        self.assertFalse(result[0])

    def test_imageUrl_and_name_required(self):
        result = self.validator.validate(channel="channel", message="msg", username=None, name=None, imageUrl="image", emoji=None)
        self.assertFalse(result[0])

    def test_imageUrl_and_name(self):
        result = self.validator.validate(channel="channel", message="msg", username=None, name="name", imageUrl="image", emoji=None)
        self.assertTrue(result[0])

    def test_emoji_and_name_required(self):
        result = self.validator.validate(channel="channel", message="msg", username=None, name=None, imageUrl=None, emoji="emoji")
        self.assertFalse(result[0])

    def test_emoji_and_name(self):
        result = self.validator.validate(channel="channel", message="msg", username=None, name="name", imageUrl=None, emoji="emoji")
        self.assertTrue(result[0])

class ArgParserTest(unittest.TestCase):

    def test_default_args_None(self):
        args = ArgParser([])
        self.assertArgs(args)

    def test_parse_all_args(self):
        args = ArgParser(['-c', '#channel', '-m', 'message', '-u', 'username', '-n', 'name', '-e', ':emoji:', '-i', 'imageUrl'])
        self.assertArgs(args, '#channel', 'message', 'username', 'name', ':emoji:', 'imageUrl')

    def test_channel_arg_hash_prepended(self):
        args = ArgParser(['-c', 'channel'])
        self.assertArgs(args, channel='#channel')

    def test_emoji_arg_with_colons(self):
        args = ArgParser(['-e', ':emoji:'])
        self.assertArgs(args, emoji=':emoji:')

    def test_emoji_arg_without_end_colon(self):
        args = ArgParser(['-e', ':emoji'])
        self.assertArgs(args, emoji=':emoji:')

    def test_emoji_arg_without_start_colon(self):
        args = ArgParser(['-e', 'emoji:'])
        self.assertArgs(args, emoji=':emoji:')

    def test_emoji_args_without_colons(self):
        args = ArgParser(['-e', 'emoji'])
        self.assertArgs(args, emoji=':emoji:')

    def assertArgs(self, args, channel=None, message=None, username=None, name=None, emoji=None, imageUrl=None):
        self.assertEquals(args.channel, channel)
        self.assertEquals(args.message, message)
        self.assertEquals(args.username, username)
        self.assertEquals(args.name, name)
        self.assertEquals(args.emoji, emoji)
        self.assertEquals(args.imageUrl, imageUrl)

if __name__ == '__main__':
    unittest.main()
