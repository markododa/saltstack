panels = {
    "saltmaster.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality",
                "module": "va_utils"
            },
            "table_statistics": {
                "source": "panel_overview"
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
                "width": "20%"
            }, {
                "key": "output",
                "label": "Value"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }],
            "actions": [{
                "action": "restart_functionality",
                "name": "Restart services",
                "class": "danger"
            }],
            "rowStyleCol": "state",
            "id": ["status"],
            "source": "va_utils.check_functionality"
        }, {
            "type": "Table",
            "name": "table_statistics",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "key",
                "label": "Item",
                "width": "20%"
            }, {
                "key": "value",
                "label": "Value"
            }],
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
                "width": "20%"
            }, {
                "key": "dns",
                "label": "DNS servers"
            }, {
                "key": "clock",
                "label": "Clock"
            }],
            "id": ["ip"],
            "source": "va_utils.panel_networking"
        }]
    },
    "saltmaster.keys": {
        "title": "Salt Keys",
        "tbl_source": {},
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    {
                        "type": "Filter",
                        "name": "Filter",
                        "reducers": ["filter"]
                    }
                ]
            },  {
                "type": "Table",
                "source":"salt_keys",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "minion",
                        "label": "Minion name",
                    "width": "30%"
                }, {
                    "key": "status",
                    "label": "Key",
                    "width": "30%"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "view_graph": "saltmaster.graph",
                    "month_history": "saltmaster.service_history_monthly",
                    "week_history": "saltmaster.service_history_weekly",
                },
                "rowStyleCol": "state",
                "actions": [{
                    "name": "Accept key",
                    "action": "minion_key_accept"
                }, {
                    "name": "Reject key",
                    "action": "minion_key_reject"
                }, {
                    "name": "Delete key",
                    "action": "minion_key_delete",
                    "class": "danger"
                }],
                "id": ["minion"]
            }

        ]
    },
    "saltmaster.ssh": {
        "title": "SSH Keys",
        "tbl_source": {
            "table": {
                "source": "list_minions_ssh_keys"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    {
                        "type": "Filter",
                        "name": "Filter",
                        "reducers": ["filter"]
                    }
                ]
            },  {
                "type": "Table",
                "source":"list_minions_ssh_keys",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [
                #     {
                #         "key": "minion",
                #         "label": "Minion name",
                #     "width": "30%"
                # },
                {
                        "key": "comment",
                        "label": "User",
                    "width": "25%"
                }, {
                        "key": "enc",
                        "label": "Encryption",
                    "width": "10%"
                }, {
                    "key": "key_short",
                    "label": "SSH key (partial)",
                    "width": "40%"
                },{
                    "key": "fingerprint",
                    "label": "Fingerprint",
                    "width": "40%"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "view_graph": "saltmaster.graph"
                },
                "actions": [{
                    "name": "Add to minion",
                    "action": "minion_key_ept"
                }, {
                    "name": "Delete key",
                    "action": "ssh_keey_delete",
                    "class": "danger"
                }],
                "id": ["minion"]
            }

        ]
    },
    "saltmaster.integrations": {
        "title": "Integrations",
        "tbl_source": {
            "table": {
                "source": "list_minions_integrations"
            }
            # ,
            # "down": {
            #     "source": "list_minions_down"
            # }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    {
                        "type": "Filter",
                        "name": "Filter",
                        "reducers": ["filter"]
                    }
                ]
            },  {
                "type": "Table",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "modal", "alert", "filter"],
                "columns": [{
                        "key": "minion",
                        "label": "Minion",
                    "width": "10%"
                }, {
                    "key": "role",
                    "label": "Role",
                    "width": "10%"
                }, {
                    "key": "integrations",
                    "label": "Integration description",
                    "width": "75%"
                },{
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "ssh_keys": "saltmaster.list_ssh_keys"

                },
                "rowStyleCol": "state",
                "actions": [{
                    "name": "Apply to...",
                    "action": "apply_integration"
                }],
                "id": ["minion"],
                "modals": {
                "apply_integration": {
                    "title": "Apply integration",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Apply",
                        "class": "primary",
                        "action": "apply_integration"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "new_data",
                            "value": "",
                            "label": "Target minion"
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form with the integration reciever"
                        }, {
                            "type": "Paragraph",
                            "name": "Operation can not be undone. Existing data will be overwritten if integration was applied before!"
                        }
                        ]
                    }
                    ]
                }
            }
            }

        ]
    },
    "saltmaster.minions": {
        "title": "Minions",
        "tbl_source": {
            "table": {
                "source": "list_minions_details"
            }
            # ,
            # "down": {
            #     "source": "list_minions_down"
            # }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    {
                        "type": "Filter",
                        "name": "Filter",
                        "reducers": ["filter"]
                    }
                ]
            },  {
                "type": "Table",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "minion",
                        "label": "Minion name",
                    "width": "20%"
                }, {
                    "key": "role",
                    "label": "Role",
                    "width": "20%"
                }, {
                    "key": "saltversion",
                    "label": "Salt version",
                    "width": "20%"
                },{
                    "key": "os",
                    "label": "OS",
                    "width": "20%"
                },{
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "ssh_keys": "saltmaster.list_ssh_keys",
                    "hardware": "saltmaster.hardware"

                },
                "rowStyleCol": "state",
                "actions": [{
                    "name": "Hardware details",
                    "action": "hardware"
                },{
                    "name": "List SSH keys",
                    "action": "ssh_keys"
                },{
                    "name": "Add known SSH key",
                    "action": "add_ssh_keys_by_fingerprint"
                }],
                "id": ["minion"]
            }

        ]
    },
    "saltmaster.hardware": {
        "title": "Hardware details",
        "tbl_source": {
            "table": {
                "source": "panel_minion_grains"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    {
                        "type": "Filter",
                        "name": "Filter",
                        "reducers": ["filter"]
                    }
                ]
            },  {
                "type": "Table",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "item",
                        "label": "Item",
                    "width": "30%"
                }, {
                    "key": "value",
                    "label": "Value",
                    "width": "70%"
                }],
                "id": ["key"]
            }

        ]
    },
    "saltmaster.list_ssh_keys": {
        "title": "Authorized SSH keys as root",
        "tbl_source": {
            "table": {
                "source": "list_minion_ssh_keys"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [{
                "type": "Button",
                "name": "Add a known SSH key",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add a known SSH key",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add backup",
                        "class": "primary",
                        "action": "add_known_key"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "key_code",
                            "value": "",
                            "label": "Fingerprint",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form with the fingerprint of the SSH key"
                        }, {
                            "type": "Paragraph",
                            "name": "Find the SSH key fingerprint in the SSH Keys panel"
                        }
                        ]
                    }
                    ]
                }
            }, {
                "type": "Button",
                "name": "Add new SSH key",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add a new SSH key",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add key",
                        "class": "primary",
                        "action": "add_ssh_key"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "user",
                            "value": "",
                            "label": "User",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "enc",
                            "value": "",
                            "label": "Encryption",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "key",
                            "value": "",
                            "label": "Key",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to define a new SSH key"
                        }, {
                            "type": "Paragraph",
                            "name": "Enter all 3 parts of the key."
                        }
                        ]
                    }
                    ]
                }
            }
            ]
        },  {
                "type": "Table",
                "name": "table",
                "pagination": True,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "comment",
                        "label": "User",
                    "width": "25%"
                }, {
                        "key": "enc",
                        "label": "Encryption",
                    "width": "10%"
                }, {
                    "key": "key_short",
                    "label": "SSH key (partial)",
                    "width": "60%"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "view_graph": "saltmaster.graph",
                    "month_history": "saltmaster.service_history_monthly",
                    "week_history": "saltmaster.service_history_weekly",
                },
                "actions": [{
                    "name": "Remove",
                    "action": "remove_ssh_key"
                }],
                "id": ["key"]
            }

        ]
    },
    "saltmaster.pillars": {
        "title": "Pillars (Global variables)",
        "tbl_source": {
            "table": {
                "source": "list_pillars"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    {
                        "type": "Filter",
                        "name": "Filter",
                        "reducers": ["filter"]
                    }
                ]
            },  {
                "type": "Table",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "pillar",
                        "label": "Pillar",
                    "width": "25%"
                }, {
                        "key": "human_name",
                        "label": "Description",
                    "width": "35%"
                }, {
                    "key": "value",
                    "label": "Value",
                    "width": "35%"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "view_graph": "saltmaster.graph",
                    "month_history": "saltmaster.service_history_monthly",
                    "week_history": "saltmaster.service_history_weekly",
                },
                "rowStyleCol": "state",
                "actions": [{
                    "name": "Test",
                    "action": "none"
                }],
                "id": ["pillar"]
            }

        ]
    },
    "saltmaster.functionality": {
        "title": "Functionality tests",
        "tbl_source": {},
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    {
                        "type": "Filter",
                        "name": "Filter",
                        "reducers": ["filter"]
                    }
                ]
            }, {
                "type": "MultiTable",
                "name": "div",
                "reducers": ["table"],
                "elements": [{
                    "type": "Heading"
                }, {
                    "type": "Table",
                    "pagination": False,
                    "reducers": ["table", "panel", "alert", "filter"],
                    "columns": [{
                        "key": "state",
                        "label": "State",
                        "width": "8%"
                    },{
                        "key": "output",
                        "label": "Output",
                        "width": "70%"
                    }
                    # , {
                    #     "key": "action",
                    #     "label": "Actions",
                    #     "width": "5%"
                    # }
                    ],
                    "panels": {
                        "view_graph": "monitoring.graph",
                        "view_multi_graph": "monitoring.multi_charts",
                        "view_multi_graph_1h": "monitoring.multi_charts_1h",
                        "view_multi_graph_1d": "monitoring.multi_charts_1d",
                        "view_multi_graph_1w": "monitoring.multi_charts_1w",
                        "month_history": "monitoring.service_history_monthly",
                        "week_history": "monitoring.service_history_weekly",
                    },
                    "rowStyleCol": "state",
                    "actions": [
                        {
                            "name": "Force check now",
                            "action": "force_check"
                        }],
                    "id": ["name", "host_name"]
                }]
            }
        ]
    },
}
