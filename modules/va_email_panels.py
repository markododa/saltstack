panel = {
	"email.user": {
		"title": "List users",
		"tbl_source": {
			"table_users": {
				"action": "list_users",
				"cols": ["user", "samaccountname"]
			}
		},
		"content": [{
				"type": "Table",
				"name": "table_users",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "user",
						"label": "E-mail address"
					}, {
						"key": "samaccountname",
						"label": "User/Group"
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"source": "list_users",
				"panels": {
					"list_rules": "email.rules"
				},
				"actions": [{
						"action": "list_rules",
						"name": "List rules"
					}
				],
				"id": ["user"]
			}
		]
	},
	"email.queue": {
		"title": "Mail queue",
		"tbl_source": {
			"table": {
				"action": "mail_queue"
			}
		},
		"content": [{
				"type": "Form",
				"name": "form",
				"class": "tbl-ctrl",
				"reducers": ["panel"],
				"elements": [{
						"type": "Button",
						"name": "Resend All",
						"glyph": "send",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Resend All",
							"table_name": "table",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Resend All",
									"class": "primary",
									"action": "force_mail_queue"
								}
							],
							"content": [{
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Confirmation"
										}, {
											"type": "Paragraph",
											"name": "This will force resending all unsent items. Are you sure?"
										}
									]
								}
							]
						}
					}, {
						"type": "Button",
						"name": "Clear Queue",
						"glyph": "trash",
						"class": "danger",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Clear Queue",
							"table_name": "table",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Clear",
									"class": "primary",
									"action": "delete_mail_queue"
								}
							],
							"content": [{
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Confirmation"
										}, {
											"type": "Paragraph",
											"name": "This will remove all unsent messages from the queue. Are you sure?"
										}
									]
								}
							]
						}
					}
				]
			}, {
				"type": "Table",
				"name": "table",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "arrival_time",
						"label": "Time"
					}, {
						"key": "queue_id",
						"label": "Mail ID"
					}, {
						"key": "sender",
						"label": "Sender"
					}, {
						"key": "recipients",
						"label": "Recipients"
					}, {
						"key": "size",
						"label": "Size (b)"
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"source": "mail_queue",
				"panels": {
					"list_rules": "email.rules"
				},
				"actions": [{
						"action": "force_mail_queue_id",
						"name": "Send Now"
					}, {
						"action": "delete_mail_queue_id",
						"name": "Delete",
						"class": "danger"
					}
				],
				"id": ["queue_id"]
			}
		]
	},
	"email.filterlists": {
		"title": "Mail filters",
		"tbl_source": {
			"tablew": {
				"action": "get_whitelist"
			},
			"tableb": {
				"action": "get_blacklist"
			}
		},
		"content": [{
				"type": "Form",
				"name": "form",
				"class": "tbl-ctrl",
				"reducers": ["panel"],
				"elements": [{
						"type": "Button",
						"name": "Add to whitelist",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add item to whitelist",
							"refresh_action": "get_whitelist",
							"table_name": "table",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add",
									"class": "primary",
									"action": "add_filter_whitelist"
								}
							],
							"content": [{
									"type": "Form",
									"name": "form",
									"class": "left",
									"elements": [{
											"type": "text",
											"name": "Filter",
											"value": "",
											"label": "Allow sender",
											"required": True
										}, {
											"type": "label",
											"name": "lbl",
											"value": "example:a single user: username@domain.com\na single domain: @domain.com\nentire domain and all its sub-domains: @.domain.com\nanyone: @. (the ending dot is required)"
										}
									]
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to add item to the whitelist"
										}, {
											"type": "Paragraph",
											"name": "The changed data for user will be automatically synchronized."
										}
									]
								}
							]
						}
					}, {
						"type": "Button",
						"name": "Add to blacklist",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add item to blacklist",
							"refresh_action": "get_blacklist",
							"table_name": "table",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add",
									"class": "primary",
									"action": "add_filter_blacklist"
								}
							],
							"content": [{
									"type": "Form",
									"name": "form",
									"class": "left",
									"elements": [{
											"type": "text",
											"name": "Filter",
											"value": "",
											"label": "Block sender",
											"required": True
										}, {
											"type": "label",
											"name": "lbl",
											"value": "example:a single user: username@domain.com\na single domain: @domain.com\nentire domain and all its sub-domains: @.domain.com\nanyone: @. (the ending dot is required)"
										}
									]
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to add item to the blacklist"
										}, {
											"type": "Paragraph",
											"name": "The changed data for user will be automatically synchronized."
										}
									]
								}
							]
						}
					}
				]
			}, {
				"type": "Table",
				"name": "tablew",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "filter_id",
						"label": "Whitelist items"
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"source": "get_whitelist",
				"actions": [{
						"action": "delete_filter_whitelist",
						"name": "Delete",
						"class": "danger"
					}
				],
				"id": ["filter_id"]
			}, {
				"type": "Form",
				"name": "form2",
				"class": "tbl-ctrl2",
				"reducers": ["panel"],
				"elements": []
			}, {
				"type": "Table",
				"name": "tableb",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "filter_id",
						"label": "Blacklist items"
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"source": "get_blacklist",
				"actions": [{
						"action": "delete_filter_blacklist",
						"name": "Delete",
						"class": "danger"
					}
				],
				"id": ["filter_id"]
			}
		]
	},
	"email.overview": {
		"title": "Overview",
		"tbl_source": {
			"table_chkf": {
				"action": "panel_check_functionality",
				"cols": ["status", "output"]
			},
			"table_dns": {
				"action": "panel_get_dns_config",
				"cols": ["dns", "type", "value"]
			}
		},
		"content": [{
				"type": "Table",
				"name": "table_chkf",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "status",
						"label": "Status",
						"width": "30%"
					}, {
						"key": "output",
						"label": "Value"
					}
				],
				"id": ["status"],
				"source": "va_utils.check_functionality"
			}, {
				"type": "Table",
				"name": "table_dns",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "dns",
						"label": "DNS record"
					}, {
						"key": "type",
						"label": "Type"
					}, {
						"key": "value",
						"label": "Value"
					}
				],
				"id": ["key"],
				"source": "panel_get_dns_config"
			}
		]
	},
	"email.rules": {
		"title": "List rules",
		"tbl_source": {
			"table": {
				"action": "get_user_rules"
			}
		},
		"content": [{
				"type": "Form",
				"name": "form",
				"class": "tbl-ctrl",
				"reducers": ["panel"],
				"elements": [{
						"type": "Button",
						"name": "Add rule",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add rule",
							"refresh_action": "get_user_rules",
							"table_name": "table",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add",
									"class": "primary",
									"action": "add_user_recipient"
								}
							],
							"content": [{
									"type": "Form",
									"name": "form",
									"class": "left",
									"elements": [{
											"type": "text",
											"name": "Rule",
											"value": "",
											"label": "Allow recipient",
											"required": True
										}, {
											"type": "label",
											"name": "lbl",
											"value": "example:\n- user@domain.com (for particular user)\n- @gmail.com (for whole domain *@gmail.com)"
										}
									]
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to change rule for user"
										}, {
											"type": "Paragraph",
											"name": "The changed data for user will be automatically synchronized with Email server."
										}
									]
								}
							]
						}
					}, {
						"type": "Button",
						"name": "Add multiple users",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add rule",
							"refresh_action": "get_user_rules",
							"table_name": "table",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add",
									"class": "primary",
									"action": ["add_multiple_user_recipients", "va-owncloud.kam.com.mk:add_user_contact"]
								}
							],
							"content": [{
									"type": "Form",
									"name": "form",
									"class": "left",
									"elements": []
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to change rule for user"
										}, {
											"type": "Paragraph",
											"name": "The changed data for user will be automatically synchronized with Email server."
										}
									]
								}
							]
						}
					}
				]
			}, {
				"type": "Table",
				"name": "table",
				"reducers": ["table", "panel", "alert", "modal"],
				"columns": [{
						"key": "rule",
						"label": "Rule"
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"source": "get_user_rules",
				"actions": [{
						"action": "rm_user_recipient",
						"name": "Remove"
					}
				],
				"id": ["rule"]
			}
		]
	}
}

