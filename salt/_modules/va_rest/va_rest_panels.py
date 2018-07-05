panels = {
    "rest.providers": {
        "title": "Providers",
        "tbl_source": {
            "table": {
                "source": "panel_providers_list"
            }
        },
        "content": [{
                "type": "Form",
                "name": "form",
                "class": "tbl-ctrl",
                "elements": [
                    {
                        "type": "Button",
                        "name": "Add provider",
                        "glyph": "plus",
                        "action": "modal",
                        "reducers": ["modal"],
                        "modal": {
                            "refresh_action": "panel_exception_list",
                            "title": "Add new item in exception list",
                            "buttons": [{
                                "type": "Button",
                                "name": "Cancel",
                                "action": "cancel"
                            }, {
                                "type": "Button",
                                "name": "Add exception",
                                "class": "primary",
                                "action": "add_exception_site"
                            }],
                            "content": [{
                                "type": "Form",
                                "name": "form",
                                "class": "left",
                                "elements": [{
                                    "type": "dropdown",
                                    "name": "group",
                                    "values": ["Standard", "VIP", "Safe"],
                                    "label": "Group",
                                    "required": True
                                }, {
                                    "type": "text",
                                    "name": "site",
                                    "value": "",
                                    "label": "Item",
                                    "required": True
                                }]
                            }, {
                                "type": "Div",
                                "name": "div",
                                "class": "right",
                                "elements": [{
                                    "type": "Heading",
                                    "name": "Fill the form to add a new item"
                                }, {
                                    "type": "Paragraph",
                                    "name": "Enter domain name only or TLD. **s = all https web sites. *ip = all sites accessed by IP. *ips = all https sites accesed by IP"
                                }]
                            }]
                        }
                    }
                ]
            }, {
                "type": "Table",
                "name": "table",
                "reducers": ["table", "panel", "alert"],
                "columns": [{
                    "key": "provider",
                    "label": "Provider name",
                    "width": "25%"
                }, {
                    "key": "ip",
                    "label": "IP"
                },{
                    "key": "instances",
                    "label": "Instances"
                },{
                    "key": "driver",
                    "label": "Driver"
                },{
                    "key": "status",
                    "label": "Status"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "actions": [{
                    "name": "Delete",
                    "action": "delete_provider"
                },
                {
                    "name": "Edit",
                    "action": "edit_provider"
                }],
                "id": ["provider"],
                "source": "panel_providers_list"
            }
        ]
    },
    "rest.servers": {
        "title": "Servers",
        "tbl_source": {
            "table_servers": {
                "source": "panel_servers_list"
            }
        },
        "content": [{
                "type": "Form",
                "name": "form",
                "class": "tbl-ctrl",
                "elements": [
                    {
                        "type": "Button",
                        "name": "Create server",
                        "glyph": "plus",
                        "action": "modal",
                        "reducers": ["modal"],
                        "modal": {
                            "refreshAction": "panel_custom_list",
                            "tableName": "table_custom",
                            "title": "Add new item to the _custom category",
                            "buttons": [{
                                "type": "Button",
                                "name": "Cancel",
                                "action": "cancel"
                            }, {
                                "type": "Button",
                                "name": "Add item",
                                "class": "primary",
                                "action": "add_customlist"
                            }],
                            "content": [{
                                "type": "Form",
                                "name": "form",
                                "class": "left",
                                "elements": [{
                                    "type": "text",
                                    "name": "item",
                                    "value": "",
                                    "label": "Item",
                                    "required": True
                                }]
                            }, {
                                "type": "Div",
                                "name": "div",
                                "class": "right",
                                "elements": [{
                                    "type": "Heading",
                                    "name": "Fill the form to add a new item"
                                }, {
                                    "type": "Paragraph",
                                    "name": "Item shoud be in format domain.com"
                                }]
                            }]
                        }
                    }

                ]
            }, {
                "type": "Table",
                "name": "table_servers",
                "reducers": ["table", "filter","panel", "modal", "alert"],
                "columns": [{
                    "key": "server",
                    "label": "Hostname",
                    "width": "15%"
                }, {
                    "key": "ip",
                    "label": "IP"
                }, {
                    "key": "size",
                    "label": "Size"
                }, {
                    "key": "status",
                    "label": "Status"
                }, {
                    "key": "provider",
                    "label": "Provider"
                },  {
                    "key": "managedby",
                    "label": "Managed by"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "actions": [{
                    "name": "Start",
                    "action": "star_server"
                },{
                    "name": "Reboot",
                    "action": "reboot_server"
                },{
                    "name": "Shutdown",
                    "action": "shutdown_server"
                }],
                "id": ["server"],
                "source": "panel_servers_list"
            }

        ]
    },
    "rest.services": {
        "title": "Services",
        "tbl_source": {
            "table_services": {
                "source": "panel_services_list"
            }
        },
        "content": [{
                "type": "Form",
                "name": "form",
                "class": "tbl-ctrl",
                "elements": [
                    {
                        "type": "Button",
                        "name": "Add service",
                        "glyph": "plus",
                        "action": "modal",
                        "reducers": ["modal"],
                        "modal": {
                            "refreshAction": "panel_custom_list",
                            "tableName": "table_custom",
                            "title": "Add new item to the _custom category",
                            "buttons": [{
                                "type": "Button",
                                "name": "Cancel",
                                "action": "cancel"
                            }, {
                                "type": "Button",
                                "name": "Add item",
                                "class": "primary",
                                "action": "add_customlist"
                            }],
                            "content": [{
                                "type": "Form",
                                "name": "form",
                                "class": "left",
                                "elements": [{
                                    "type": "text",
                                    "name": "item",
                                    "value": "",
                                    "label": "Item",
                                    "required": True
                                }]
                            }, {
                                "type": "Div",
                                "name": "div",
                                "class": "right",
                                "elements": [{
                                    "type": "Heading",
                                    "name": "Fill the form to add a new item"
                                }, {
                                    "type": "Paragraph",
                                    "name": "Item shoud be in format domain.com"
                                }]
                            }]
                        }
                    }

                ]
            }, {
                "type": "Table",
                "name": "table_services",
                "reducers": ["table", "filter","panel", "modal", "alert"],
                "columns": [{
                    "key": "name",
                    "label": "Name",
                    "width": "15%"
                }, {
                    "key": "address",
                    "label": "Address"
                }, {
                    "key": "port",
                    "label": "Port"
                }, {
                    "key": "tags",
                    "label": "Tags"
                }, {
                    "key": "checks",
                    "label": "Checks"
                },   {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "actions": [{
                    "name": "Act1",
                    "action": "star_server"
                },{
                    "name": "Act2",
                    "action": "reboot_server"
                },{
                    "name": "Act3",
                    "action": "shutdown_server"
                }],
                "id": ["server"],
                "source": "panel_services_list"
            }

        ]
    },
    "rest.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality"
            },
            "table_config": {
                "source": "panel_config"
            },
            "table_stats": {
                "source": "panel_statistics"
            },
            "table_net": {
                "source": "panel_networking",
                "module": "va_utils"
            },
            "table_top": {
                "source": "panel_top_visits"
            },
            "table_blocked": {
                "source": "panel_top_blocked"
            },
            "table_last": {
                "source": "panel_last_blocked"
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
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }],
            "actions": [{
                "action": "restart_functionality",
                "name": "Restart services",
                "class": "danger"
            },{
                "action": "e2guardian_reload",
                "name": "Reload config"
            }],
            "rowStyleCol": "state",
            "source": "va_utils.check_functionality"
        },


        {
            "type": "CustomChart",
            "chartType": "line",
            "name": "graph1",
            "xCol": "time",
            "height": "70",
            "options": {
                "scales": {
                    "yAxes": [{
                        "ticks": {
                            "suggestedMin": 30,
                            "beginAtZero": True
                        }
                    }],
                    "xAxes": [{
                            "ticks": {
                                "autoSkip": True,
                                "autoSkipPadding": 84

                            }
                        }

                        ]

                }
            },
            "reducers": ["table"],
            "datasets": [{
                    "column": "childs",
                    "label": "Children",
                    "backgroundColor": "#2e6da422",
                    #"backgroundColor": "#fff",
                    "borderColor": "#2e6da4",
                    "fill": False,
                    "pointRadius" : 0,

                    "data": []
                }, {
                    "column": "free",
                    "type": "line",
                    "label": "Free Children",
                    "borderColor": "#2E6F00",
                    "backgroundColor": "#2E6F0022",
                    # "fill": False,
                                "pointRadius" : 0,
                    "data": []

                },
                {
                    "column": "conx/s",
                    "type": "line",
                    "label": "Connections/Sec",
                    "borderColor": "#6F0020",
                    "backgroundColor": "#6F002022",
                    "fill": False,
                                "pointRadius" : 0,
                    "data": []
                }
                # ,
                # {
                #     "column": "wait",
                #     "type": "line",
                #     "label": "Waiting",
                #     "borderColor": "#C17504",
                #     "fill": False,
                #                 "pointRadius" : 0,
                #     "data": []
                # }
            ],
            "target": "table_stats"
        },

        {
            "type": "Table",
            "name": "table_top",
            # "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "site",
                "label": "Top requested domains",
                "width": "30%"
            },{
                "key": "count",
                "label": "Count"
            }],
            "source": "panel_top_visits"
        },{
            "type": "Table",
            "name": "table_blocked",
            # "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "site",
                "label": "Top blocked domains",
                "width": "30%"
            },{
                "key": "count",
                "label": "Count"
            }],
            "source": "panel_top_blocked"
        },{
            "type": "Table",
            "name": "table_last",
            # "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "time",
                "label": "Time",
                "width": "16%"
            },{
                "key": "group",
                "label": "Group",
                "width": "7%"
            },{
                "key": "ip",
                "label": "IP",
                "width": "12%"
            },{
                "key": "hostname",
                "label": "Hostname"
                ,
                "width": "14%"
            },{
                "key": "domain",
                "label": "Last blocked Domains",
                "width": "30%"
            },{
                "key": "reason",
                "label": "Reason",
                "width": "21%"
            }],
            "source": "panel_last_blocked"
        },
        {
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
            }],
            "source": "panel_config"
        }
        # ,
        #  {
        #     "type": "Table",
        #     "name": "table_stats",
        #     #"pagination": False,
        #     "reducers": ["table", "panel", "alert"],
        #     "columns": [{
        #         "key": "time",
        #         "label": "Time",
        #         "width": "18%"
        #     }, {
        #         "key": "childs",
        #         "label": "Childs",
        #         "width": "10%"
        #     }, {
        #         "key": "busy",
        #         "label": "Busy",
        #         "width": "10%"
        #     }, {
        #         "key": "free",
        #         "label": "Free",
        #         "width": "10%"
        #     }, {
        #         "key": "wait",
        #         "label": "Wait",
        #         "width": "10%"
        #     }, {
        #         "key": "births",
        #         "label": "Births",
        #         "width": "10%"
        #     }, {
        #         "key": "deaths",
        #         "label": "Deaths",
        #         "width": "10%"
        #     }, {
        #         "key": "conx",
        #         "label": "Connections",
        #         "width": "10%"
        #     }, {
        #         "key": "conx/s",
        #         "label": "Connections/sec",
        #         "width": "10%"
        #     }, ]
        # }
        ,
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
            }],
            "id": ["ip"],
            "source": "va_utils.panel_networking"
        }]
    },
    "rest.edit_user_details": {
        "title": "User details",
        "tbl_source": {
            "table": {
                "source": "panel_user_details"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table",
            "pagination": False,
            "reducers": ["table", "panel", "modal", "alert"],
            "columns": [{
                "key": "item",
                "label": "Item",
                "width": "20%"
            }, {
                "key": "value",
                "label": "Value"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }],
            "actions": [{
                "action": "edit_attribute",
                "name": "Change"
            }],
            "source": "panel_user_details",
            "id": ["item"],
            "modals": {
                "edit_attribute": {
                    "title": "Edit value",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Change",
                        "class": "primary",
                        "action": "change_user_detail"
                    }],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "new_value",
                            "value": "",
                            "label": "New value",
                            "required": True

                        }]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to change data"
                        }, {
                            "type": "Paragraph",
                            "name": "The changed data for user will be automatically synchronized."
                        }]
                    }]
                }

            },
        }],

    }
}
