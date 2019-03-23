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
        t_api = tweepy.API(auth)

        self.ensure_one()
        #        sliced = self.twitter_uuid[:4]
        sliced = str(random.random())[:4]
        #        for status in tweepy.Cursor(t_api.user_timeline).items(10):i
        status_update = (self.twt_update_status + " " + sliced)
        try:
            tweepy.Cursor(t_api.update_status(status=status_update))
        except TweepError as e:
            self.state = "publish"
            raise ValidationError(_('Status updated successfully! Just ignore this {} error \n'.format(e)))
        self.twt_update_status = tweepy.Cursor(t_api.update_status(status=status_update))

        return
