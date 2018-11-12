panels = {
    "cloudshare.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality"
            },
            "table_plugins": {
                "source": "panel_plugins"
            },
            "table_net": {
                "source": "panel_networking",
                "module": "va_utils"
            },
            "table_statistics": {
                "source": "panel_statistics"
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
            "name": "table_plugins",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "plugin",
                "label": "App / Version",
                "width": "30%"
            }, {
                "key": "status",
                "label": "Status"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }
            ],
            "id": ["plugin", "status"],
            "actions": [{
                "action": "action_toggle_app",
                "name": "Toggle"
            }
            ],
            
            "source": "panel_plugins"
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
        }, {
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
    "cloudshare.users": {
        "title": "Users",
        "tbl_source": {
            "table_users": {
                "source": "panel_list_users"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_users",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "username",
                "label": "Username",
                "width": "20%"
            }, {
                "key": "name",
                "label": "Display Name",
                "width": "50%"

            }, {
                "key": "lastlogin",
                "label": "Last Login (UTC)"
           }
            ],
            "id": ["username"],
            "source": "panel_list_users"
        }
        ]
    },
    "cloudshare.quotas": {
        "title": "Quotas",
        "tbl_source": {
            "table_quota": {
                "source": "panel_quota"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_quota",
            "reducers": ["table", "panel", "modal", "alert"],
            "columns": [{
                "key": "username",
                "label": "Username",
                "width": "20%"

            }, {
                "key": "displayname",
                "label": "Display Name",
                "width": "20%"

            }, {
                "key": "enabled",
                "label": "Enabled",
                "width": "10%"

            }, {
                "key": "used",
                "label": "Used space"
            }, {
                "key": "total",
                "label": "Limit"

            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }
            ],
            "actions": [{
                "action": "setquota",
                "name": "Set Quota"
            }
            ],
            "id": ["username"],
            "source": "panel_quota",
            "modals": {
                "setquota": {
                    "title": "Set Quota",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Set",
                        "class": "primary",
                        "action": "action_setquota"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "storage_quota",
                            "value": "",
                            "label": "Size"
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to set quota"
                        }, {
                            "type": "Paragraph",
                            "name": "Enter value in format: 100MB, 5GB etc."
                        }
                        ]
                    }
                    ]
                },

            }
        }
        ]
    },
    "cloudshare.shares": {
        "title": "Shares by Admin",
        "tbl_source": {
            "table_shares": {
                "source": "panel_shares"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_shares",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "path",
                "label": "Path"
            }, {
                "key": "expiration",
                "label": "Expire"
            }, {
                "key": "item_type",
                "label": "Type"
            }, {
                "key": "share_with",
                "label": "Shared with"
            }
            ],
            "id": ["displayname"],
            "source": "panel_shares"
        }
        ]
    }
}
