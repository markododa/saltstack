panels = {
    "monitoring.overview": {
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
                    "key": "status",
                    "label": "Status",
                    "width": "20%"
            }, {
                "key": "output",
                "label": "Value"
            }, {
                "key": "action",
                "label": "Actions"
            }
            ],
            "actions": [{
                "action": "restart_functionality",
                "name": "Restart services",
                "class": "danger"
            }
            ],
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
                        "width": "20%"
                    }, {
                        "key": "dns",
                        "label": "DNS servers"
                    }
                    ],
            "id": ["ip"],
            "source": "va_utils.panel_networking"
        }]
    },
    "monitoring.icinga": {
        "title": "Proxy",
        "content": [{
                    "type": "Frame",
                    "name": "frame",
                    "src": "/proxy/"
                    }
                    ]
    },
    "monitoring.chart": {
        "title": "",
        "content": [{
                    "type": "Chart",
                    "name": "chart",
                    "reducers": ["panel"]
                    }
                    ]
    },
    "monitoring.status": {
        "title": "Status",
        "tbl_source": {},
        "content": [

            {
                "type": "Form",
                "name": "form1",
                # "class": "pull-right margina form-inline",
                "elements": [
                        {
                            "type": "Button",
                            "name": "Add Windows host",
                            "glyph": "plus",
                            "action": "modal",
                            "reducers": ["modal", "alert"],
                            "modal": {
                                "title": "Add Windows Host",
                                "buttons": [{
                                    "type": "Button",
                                    "name": "Cancel",
                                    "action": "cancel"
                                }, {
                                    "type": "Button",
                                    "name": "Add record",
                                    "class": "primary",
                                    "action": "add_win_host_to_icinga"
                                }
                                ],
                                "content": [{
                                    "type": "Form",
                                    "name": "form",
                                    "class": "left",
                                    "elements": [{
                                        "type": "text",
                                        "name": "host_name",
                                        "value": "",
                                        "label": "Hostname or IP address",
                                        "required": True
                                    }, {
                                        "type": "text",
                                        "name": "displayname",
                                        "value": "",
                                        "label": "Display Name",
                                        "required": False
                                    },  {
                                        "type": "dropdown",
                                        "name": "always_on",
                                        "values": ["Yes", "No (Desktop)"],
                                        "label": "Always On",
                                        "required": True
                                    }, {
                                        "type": "dropdown",
                                        "name": "joined",
                                        "values": ["Domain Member", "Domain Controller", "Standalone"],
                                        "label": "Domain status",
                                        "required": True
                                    },  {
                                        "type": "dropdown",
                                        "name": "printer",
                                        "values": ["No", "Yes"],
                                        "label": "Printer server role",
                                        "required": True
                                    }, {
                                        "type": "dropdown",
                                        "name": "mssql",
                                        "values": ["No", "Yes", "Express version"],
                                        "label": "MS SQL server role",
                                        "required": True
                                    }, {
                                        "type": "dropdown",
                                        "name": "iis",
                                        "values": ["No", "Yes"],
                                        "label": "IIS server role",
                                        "required": True

                                    }
                                    ]
                                }, {
                                    "type": "Div",
                                    "name": "div",
                                    "class": "right",
                                    "elements": [{
                                        "type": "Heading",
                                        "name": "Fill the form to add Windows host to monitoring"
                                    }, {
                                        "type": "Paragraph",
                                        "name": "Please select all options that are relevant. WMI port should be accessible on this machine"
                                    }
                                    ]
                                }
                                ]
                            }
                        },

                    {
                            "type": "Button",
                            "name": "Windows credentials",
                            "glyph": "edit",
                            "action": "modal",
                            "reducers": ["modal", "alert"],
                            "modal": {
                                "title": "Edit Windows credentials",
                                "buttons": [{
                                    "type": "Button",
                                    "name": "Cancel",
                                    "action": "cancel"
                                }, {
                                    "type": "Button",
                                    "name": "Update",
                                    "class": "primary",
                                    "action": "edit_win_host_credentials"
                                }
                                ],
                                "content": [{
                                    "type": "Form",
                                    "name": "form",
                                    "class": "left",
                                    "elements": [{
                                        "type": "label",

                                        "value": "Standalone hosts:",

                                    }, {
                                        "type": "text",
                                        "name": "standalone_username",
                                        "value": "",
                                        "label": "Username",
                                        "required": False
                                    }, {
                                        "type": "password",
                                        "name": "standalone_password",
                                        "value": "",
                                        "label": "Password",
                                        "required": False
                                    }, {
                                        "type": "label",

                                        "value": "Domain members:",

                                    }, {
                                        "type": "text",
                                        "name": "domain_username",
                                        "value": "",
                                        "label": "Username",
                                        "required": False
                                    }, {
                                        "type": "password",
                                        "name": "domain_password",
                                        "value": "",
                                        "label": "Password",
                                        "required": False
                                    },
                                    ]
                                }, {
                                    "type": "Div",
                                    "name": "div",
                                    "class": "right",
                                    "elements": [{
                                        "type": "Heading",
                                        "name": "Credentails for Windows WMI service"
                                    }, {
                                        "type": "Paragraph",
                                        "name": "There are two sets of credentails. Only non empty fields are updated."
                                        #  "name": "There are two sets of credentails. Joined PCs are queried with domain credentails. For Standalone PCs the other set of credentails is used."
                                    }
                                    ]
                                }
                                ]
                            }
                            }



                ]
            },


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
                        "type": "Heading",
                        "dc": "monitoring :num: services"
                }, {
                    "type": "Table",
                    "pagination": False,
                    "reducers": ["table", "panel", "alert", "filter"],
                    "columns": [{
                            "key": "name",
                            "label": "Service"
                    }, {
                        "key": "output",
                        "label": "Output",
                        "width": "70%"
                    }, {
                        "key": "state",
                        "label": "State",
                        "width": "8%"
                    }, {
                        "key": "action",
                        "label": "Actions",
                        "width": "5%"
                    }
                    ],
                    "panels": {
                        "view_graph": "monitoring.graph"
                    },
                    "rowStyleCol": "state",
                    "actions": [{
                        "name": "View graphs",
                        "action": "chart"
                    }
                    ],
                    "id": "name"
                }
                ]
            }
        ]
    }
}
