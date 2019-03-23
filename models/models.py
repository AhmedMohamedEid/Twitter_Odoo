# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.exceptions import UserError, ValidationError

import tweepy
from tweepy import OAuthHandler,TweepError
import random

class TweetConfig(models.Model):
    _name = 'twt.config'
    _description = 'Twitter Config'

    name = fields.Char(string="Account Name")
    api_key = fields.Char(string="Consumer API key", required=True)
    api_secret_key = fields.Char(string="Consumer API Secret", required=True)
    access_token = fields.Char(string="Access token", required=True)
    access_token_secret = fields.Char(string="Access secret token", required=True)


class TweetStatus(models.Model):
    _name = 'twt.status'
    _rec_name = 'name'
    _description = ''

    name = fields.Char(string="Tweet Name", required=True)
    twitter_account = fields.Many2one('twt.config', string="Twitter Account", required=True)
    user_name = fields.Char(string="User Name", required=True)
    twt_update_status = fields.Text(string="Update Status", required=True)

    state = fields.Selection(string="state", selection=[('draft', 'Draft'), ('publish', 'Published'), ], default='draft')

    @api.one
    @api.model
    def updatetweet(self):
        auth = OAuthHandler(self.twitter_account.api_key, self.twitter_account.api_secret_key)
        auth.set_access_token(self.twitter_account.access_token, self.twitter_account.access_token_secret)
        tw_api = tweepy.API(auth)

        # public_tweets = tw_api.home_timeline()
        # for tweet in public_tweets:
        #     print tweet.text
        #
        # user = tw_api.get_user('eng_ahmed_m_eid')
        # print user.screen_name
        # print user.followers_count
        # for friend in user.friends():
        #     print friend.screen_name

        self.ensure_one()
        rand = str(random.random())[:4]
        status_update = (self.twt_update_status+"Eng.A.E\n"+rand)

        try:
            tweepy.Cursor(tw_api.update_status(status=status_update))
            self.state = "publish"
            # raise ValidationError(_('Successfully Status Update'))
        except tweepy.TweepError as e:
            raise ValidationError(_('Just ignore this {} error \n'.format(e)))
        # self.twt_update_status = tweepy.Cursor(tw_api.update_status(status=status_update))
        return
