from sym_api_client_python.processors.message_formatter import MessageFormatter

bot_id = "349026222344902"
reply_message = dict(message = """<messageML>
                                            <span><p>Hey <mention uid="{0}"/> start your expense report by clicking the button below or mention me and upload the receipt image.</p></span>
                                       </messageML>""".format(bot_id))

finance_approval_message = dict(message = """<messageML>
                                            <span><p><mention uid="{0}"/> Your expense was approved, waiting on finance approval.</p></span>
                                       </messageML>""".format(bot_id))

help_message = dict(message = """<messageML>
                                    <h3>Use ExpenseBot to create, update, and submit an expense form using Symphony Elements</h3>
                                    <ul>
                                        <li>'@ExpenseBot create new expense'</li>
                                    </ul>
                                </messageML>
                    """)

clear_message = dict(message = """<messageML>
                                        <br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
                                      </messageML>""")

create_message = dict(message = """<messageML>
                                          <form id="form_id">
                                            <span><p>Hey <mention uid="{0}"/> create and fill up the report and I'll send it over!</p></span>
                                            <br />
                                            <div style='padding-top:1px;padding-left:5px;'>
                                                <button name="create-report" type="action">CREATE REPORT</button>
                                            </div>
                                          </form>
                                       </messageML>""".format(bot_id))

manager_submit_message = MessageFormatter().format_message('Now I need to know who is the finance responsible for the report and reimbursement.')
start_report_message = MessageFormatter().format_message('Create and fill up the report then I will send it over!')
choose_boss_message = MessageFormatter().format_message('Please select your manager and I will send them your expense report')
review_message = MessageFormatter().format_message('Here is the expense report, please review and send your response.')
room_message = MessageFormatter().format_message('You can only interact with a bot inside an IM, please open an IM chat with me!')
reject_message = MessageFormatter().format_message('Expenses Rejected, contact your manager')
