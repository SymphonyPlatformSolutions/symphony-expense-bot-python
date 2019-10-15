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
                            <p>Type @ExpenseBot <b>'create new expense'</b> to create an expense approval form</p>
                            <p>In order to assign your expense approval form to your manager, you must first add an expense</p>
                                      </messageML>
                    """)

clear_message = dict(message = """<messageML>
                                        <br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
                                      </messageML>""")

reply_message = dict(message = """<messageML>
                                          <form id="form_id">
                                            <span><p>Hey <mention uid="{0}"/> create and fill up the report and I'll send it over!</p></span>
                                            <br />
                                            <span style="margin-left:400px;margin-right:200px"><button name="create-report" type="action">CREATE REPORT</button></span>
                                          </form>
                                       </messageML>""".format(bot_id))

manager_submit_message = MessageFormatter().format_message('Now I need to know who is the finance responsible for the report and reimbursement.')
start_report_message = MessageFormatter().format_message('Create and fill up the report then I will send it over!')
choose_boss_message = MessageFormatter().format_message('Please select your manager and I will send them your expense report')
review_message = MessageFormatter().format_message('Here is the expense report, please review and send your response.')
room_message = MessageFormatter().format_message('You can only interact with a bot inside an IM, please open an IM chat with me!')
