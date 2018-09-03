# -*- coding: utf-8 -*-
# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import common


class TestPollQuestionCommon(common.TransactionCase):

    def setUp(self):
        super(TestPollQuestionCommon, self).setUp()

        # Usefull models
        self.PollQuestion = self.env['poll.question']
        self.QuestionOption = self.env['question.option']
        self.QuestionAnswer = self.env['question.answer']
        self.PollGroup = self.env['poll.group']
        self.IrModelData = self.env['ir.model.data']
        self.IrConfigParam = self.env['ir.config_parameter']
        self.PollMailScheduler = self.env['poll.mail.scheduler']
        self.ResPartner = self.env['res.partner']
        self.MailTemplate = self.env['mail.template']
        self.IrUiView = self.env['ir.ui.view']

        self.partner_id = self.env.ref('base.res_partner_1').id

        # Test Group Creation
        group_vals = {'name': 'Poll Group Test',
                      'res_partner_ids': [(0, 0, {
                          'name': 'Test Partner',
                          'email': 'test_partner@yourcompany.example.com'
                      })]}
        self.poll_group = self.PollGroup.create(group_vals)

        # Test Poll Questions creation
        self.simple_text_question = self.PollQuestion.create({
            'title': 'Simple Text Question',
            'type': 'simple_text',
            'end_date': fields.Datetime.now(),
            'yes_no_maybe': True,
            'option_ids': [(0, 0, {'name': 'Test Option 01'})],
            'group_ids': [(6, 0, [self.poll_group.id])]
        })
        self.choose_date_question = self.PollQuestion.create({
            'title': 'Choose Date Question',
            'type': 'date',
            'end_date': fields.Datetime.now(),
            'yes_no_maybe': False,
            'option_ids': [
                (0, 0, {'name_date': fields.Date.today()}),
                (0, 0, {'name_date': fields.Date.from_string('2018-08-30')}),
            ],
        })
        self.choose_date_time_question = self.PollQuestion.create({
            'title': 'Choose DateTime Question',
            'type': 'date_time',
            'end_date': fields.Datetime.now(),
            'yes_no_maybe': True,
            'option_ids': [(0, 0, {
                'name_datetime': fields.Datetime.now(),
            })],
        })

        # Test Poll Mail Scheduler creation
        self.poll_mail_scheduler = self.PollMailScheduler.create({
            'interval_nbr': 2,
            'interval_unit': 'days',
            'template_id': self.ref(
                'simple_poll.email_reminder_template_edi_poll'),
            'poll_id': self.choose_date_time_question.id,
        })
