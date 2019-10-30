from sym_api_client_python.processors.message_formatter import MessageFormatter

class Messages:
    def __init__(self, bot_id):
        self.finance_approval_message = dict(message = """<messageML>
                                            <span><p>Your expense was approved, waiting on finance approval.</p></span>
                                       </messageML>""".format(bot_id))

        self.help_message = dict(message = """<messageML>
                                    <h3>Use ExpenseBot to create, update, and submit an expense form using Symphony Elements</h3>
                                        <li><mention uid="{0}"/> help</li>
                                        <li><mention uid="{0}"/> create</li>
                                        <li><mention uid="{0}"/> end</li>
                                </messageML>
                    """.format(bot_id))

        self.clear_message = dict(message = """<messageML>
                                        <br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
                                      </messageML>""")

        self.create_message = dict(message = """<messageML>
                                          <form id="form_id">
                                            <span><p>Create and fill up the report and I'll send it over!</p></span>
                                            <br />
                                            <div style='padding-top:1px;padding-left:5px;'>
                                                <button name="create-report" type="action">CREATE REPORT</button>
                                            </div>
                                          </form>
                                       </messageML>""".format(bot_id))

        self.manager_submit_message = MessageFormatter().format_message('Now I need to know who is the finance responsible for the report and reimbursement.')
        self.start_report_message = MessageFormatter().format_message('Create and fill up the report then I will send it over!')
        self.choose_boss_message = MessageFormatter().format_message('Please select your manager and I will send them your expense report')
        self.review_message = MessageFormatter().format_message('Here is the expense report, please review and send your response.')
        self.room_message = MessageFormatter().format_message('You can only interact with a bot inside an IM, please open an IM chat with me!')
        self.reject_message = MessageFormatter().format_message('Expenses Rejected, contact your manager')
        self.end_message = dict(message = """<messageML><p>You already have an active report, type <mention uid="{0}"/> end</p></messageML>""".format(bot_id))
        self.instruction_message = dict(message = """<messageML><p>Type <mention uid="{0}"/> create</p></messageML>""".format(bot_id))
