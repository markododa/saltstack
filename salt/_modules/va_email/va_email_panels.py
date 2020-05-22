panels = {
    "email.user": {
        "title": "Email accounts",
        "tbl_source": {
            "table_users": {
                "source": "list_users"
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
            },
            {
                "key": "name",
                "label": "Name"
            },

            {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }

            ],
            "source": "list_users",
            "actions": [{
                "action": "get_allowed_recipients",
                "name": "Manage recipients",
                "class": "danger"
            }
            ],

            	"panels": {
            		"get_allowed_recipients": "get_allowed_recipients"
            	},
            #	"actions": [{
            #			"action": "list_rules",
            #			"name": "List rules"
            #		}
            #	],
            "id": ["user"]
        }
        ]
    },
    "email.queue": {
        "title": "Mail queue",
        "tbl_source": {
            "table": {
                "source": "mail_queue"
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
                            "name": "This will force resending of all unsent items. Are you sure?"
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
                "label": "Actions",
                "width": "5%"
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
                        }, {
                        "action": "error_mail_queue_id",
                        "name": "Show error"
                        }
                        ],
            "id": ["queue_id"]
        }
        ]
    },
    "email.filterlists": {
        "title": "Global mail restrictions",
        "tbl_source": {
            "tablew": {
                "source": "get_whitelist"
            },
            "tableb": {
                "source": "get_blacklist"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "reducers": ["panel"],
            "elements": [{
                "type": "Button",
                "name": "Add to inbound whitelist",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add item to inbound whitelist",
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
                            "name": "filter",
                            "value": "",
                            "label": "Allow sender",
                            "required": True
                        }, {
                            "type": "label",
                            "name": "lbl",
                            "value": "example: user: username@domain.com\ndomain: @domain.com\ndomain with sub-domains: @.domain.com\nEveryone: @. (With the ending dot)"
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add item to the inbound whitelist"
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
                "name": "Add to inbound blacklist",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add item to inbound blacklist",
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
                            "name": "filter",
                            "value": "",
                            "label": "Block sender",
                            "required": True
                        }, {
                            "type": "label",
                            "name": "lbl",
                            "value": "example: user: username@domain.com\ndomain: @domain.com\ndomain with sub-domains: @.domain.com\nEveryone: @. (With the ending dot)"

                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add item to the inbound blacklist"
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
                "key": "address",
                "label": "Inbound whitelist items"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }
            ],
            "source": "get_whitelist",
            "actions": [{
                "action": "delete_filter_whitelist",
                "name": "Delete",
                "class": "danger"
            }
            ],
            "id": ["address"]
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
                "key": "address",
                "label": "Inbound blacklist items"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }
            ],
            "source": "get_blacklist",
            "actions": [{
                "action": "delete_filter_blacklist",
                "name": "Delete",
                "class": "danger"
            }
            ],
            "id": ["address"]
        }
        ]
    },
    "email.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality"
            },
            "table_dns": {
                "source": "panel_get_dns_config"
            },
            "table_config": {
                "source": "panel_server_config"
            },
            "table_statistics": {
                "source": "panel_statistics"
            },
            "table_net": {
                "source": "panel_networking",
                "module": "va_utils"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_chkf",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "state",
                "label": "Status",
                "width": "30%"
            }, {
                "key": "output",
                "label": "Value"
            }
            ],
            "rowStyleCol": "state",
            "id": ["status"],
            "source": "va_utils.check_functionality"
        }, {
            "type": "Table",
            "name": "table_dns",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "dns",
                "label": "Needed DNS records",
                "width": "30%"
            }, {
                "key": "type",
                "label": "Type"
            }, {
                "key": "value",
                "label": "Value"
            }
            ],
            "id": ["dns"],
            "source": "panel_get_dns_config"
        }, {
            "type": "Table",
            "name": "table_config",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "key",
                "label": "Item",
                "width": "30%"
            }, {
                "key": "value",
                "label": "Value"
            }
            ],
            "id": ["key"],
            "source": "panel_server_config"
        }, {
            "type": "Table",
            "name": "table_statistics",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "key",
                "label": "Storage",
                "width": "30%"
            }, {
                "key": "value",
                "label": "Value"
            }
            ],
            "id": ["key"],
            "source": "panel_statistics"
            },
            
            
        #     {
        #     "type": "CustomChart",
        #     "chartType": "line",
        #     "name": "graph1",
        #     "xCol": "key",
        #     "reducers": ["table"],
        #     "datasets": [{
        #         "column": "value",
        #         "label": "Value",
        #         "color": "#11eeee",
        #         "backgroundColor": "#ee11ee",
        #         "borderColor": "#eeee11",
        #         "data":[]
        #     }
        #     ],
        #      "target": "table_statistics"
        # },
            
             {
            "type": "Table",
            "name": "table_net",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "ip",
                "label": "IP addresses",
                "width": "30%"
            }, {
                "key": "dns",
                "label": "DNS servers"
            }, {
                "key": "clock",
                "label": "Clock"
            }
            ],
            "id": ["ip"],
            "source": "va_utils.panel_networking"
        }
        ]
    },
    "get_allowed_recipients": {
        "title": "Allowed recipients",
        "tbl_source": {
            "table": {
                "source": "get_allowed_recipents"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "reducers": ["panel"],
            "elements": [{
                "type": "Button",
                "name": "Add Recipient",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add Recipient",
                    "refresh_action": "get_allowed_recipients",
                    "table_name": "table",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add",
                        "class": "primary",
                        "action": "add_allowed_recipient"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "recipient",
                            "value": "",
                            "label": "Allow recipient",
                            "required": True
                        },
                        {
                            "type": "text",
                            "name": "name",
                            "value": "",
                            "label": "Name",
                            "required": False
                        },

                        {
                            "type": "label",
                            "name": "lbl",
                            "value": "example:\n user@domain.com (for user)\n\n @domain.com (for domain)"
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
                "name": "Add multiple recipients",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Select recipients from domain",
                    "refresh_action": "get_allowed_recipients",
                    "table_name": "table",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add",
                        "class": "primary",
                        "action": ["add_allowed_recipients"]
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
                "key": "address",
                "label": "Allowed to"
            },
            {
                "key": "Name",
                "label": "Name"
            },
            {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }
            ],
            "source": "get_allowed_recipient",
            "actions": [{
                "action": "remove_allowed_recipient",
                "name": "Remove"
            }
            ],
            "id": ["address"]
        }
        ]
    }
}
