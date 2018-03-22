panels = {
    "proxy.rules": {
        "title": "Additional Rules",
        "tbl_source": {
            "table": {
                "source": "panel_banned_list"
            }
            ,
            "table2": {
                "source": "panel_exceptions_list"
            }
        },
        "content": [{
                "type": "Form",
                "name": "form",
                "class": "tbl-ctrl",
                "elements": [{
                        "type": "Button",
                        "name": "Add banned item",
                        "glyph": "plus",
                        "action": "modal",
                        "reducers": ["modal"],
                        "modal": {
                            "refresh_action": "panel_banned_list",
                            "title": "Add new item in banned list",
                            "buttons": [{
                                "type": "Button",
                                "name": "Cancel",
                                "action": "cancel"
                            }, {
                                "type": "Button",
                                "name": "Add item",
                                "class": "primary",
                                "action": "add_banned_site"
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
                                    "name": "**s is for all https web sites."
                                }]
                            }]
                        }
                    },
                    {
                        "type": "Button",
                        "name": "Add exception item",
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
                                    "name": "**s is for all https web sites."
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
                    "key": "group",
                    "label": "Group name",
                    "width": "25%"
                }, {
                    "key": "item",
                    "label": "Banned item"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "actions": [{
                    "name": "Remove item",
                    "action": "remove_banned_site"
                }],
                "id": ["group", "item"],
                "source": "panel_banned_list"
            },

            {
                "type": "Table",
                "name": "table2",
                "reducers": ["table", "panel", "alert"],
                "columns": [{
                    "key": "group",
                    "label": "Group name",
                    "width": "25%"
                }, {
                    "key": "item",
                    "label": "Exception item"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "actions": [{
                    "name": "Remove item",
                    "action": "remove_exception_site"
                }],
                "id": ["group", "item"],
                "source": "panel_exceptions_list"
            }
        ]
    },
    "proxy.advanced": {
        "title": "Advanced settings",
        "tbl_source": {

            "table_custom": {
                "source": "panel_custom_list"
            },
            "table_ext": {
                "source": "panel_exceptions_extensions"
            }
        },
        "content": [{
                "type": "Form",
                "name": "form",
                "class": "tbl-ctrl",
                "elements": [

                    {
                        "type": "Button",
                        "name": "Add item to custom category",
                        "glyph": "plus",
                        "action": "modal",
                        "reducers": ["modal"],
                        "modal": {
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
                    # ,
                    # {
                    #     "type": "Button",
                    #     "name": "Add file extension filter",
                    #     "glyph": "plus",
                    #     "action": "modal",
                    #     "reducers": ["modal"],
                    #     "modal": {
                    #         "title": "Add new file extension to blocked list",
                    #         "buttons": [{
                    #             "type": "Button",
                    #             "name": "Cancel",
                    #             "action": "cancel"
                    #         }, {
                    #             "type": "Button",
                    #             "name": "Add extension",
                    #             "class": "primary",
                    #             "action": "add_extension"
                    #         }],
                    #         "content": [{
                    #             "type": "Form",
                    #             "name": "form",
                    #             "class": "left",
                    #             "elements": [{
                    #                 "type": "text",
                    #                 "name": "extension",
                    #                 "value": "",
                    #                 "label": "Extension",
                    #                 "required": True
                    #             }]
                    #         }, {
                    #             "type": "Div",
                    #             "name": "div",
                    #             "class": "right",
                    #             "elements": [{
                    #                 "type": "Heading",
                    #                 "name": "Fill the form to add a new item"
                    #             }, {
                    #                 "type": "Paragraph",
                    #                 "name": "File extension examples: .exe, .rar, .torrent "
                    #             }]
                    #         }]
                    #     }
                    # }
                ]
            }, {
                "type": "Table",
                "name": "table_custom",
                "reducers": ["table", "filter","panel", "modal", "alert"],
                "columns": [{
                    "key": "item",
                    "label": "Items in Custom list",
                    "width": "95%"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "actions": [{
                    "name": "Remove item",
                    "action": "remove_customlist"
                }],
                "id": ["item"],
                "source": "panel_custom_list"
            }
            # ,
            # {
            #     "type": "Table",
            #     "name": "table_ext",
            #     "reducers": ["table", "filter", "panel", "modal","alert"],
            #     "columns": [{
            #         "key": "extension",
            #         "label": "Allowed file extensions",
            #         "width": "95%"
            #     }, {
            #         "key": "action",
            #         "label": "Actions",
            #         "width": "5%"
            #     }],
            #     "actions": [{
            #         "name": "Remove item",
            #         "action": "remove_extension"
            #     }],
            #     "id": ["extension"],
            #     "source": "panel_exceptions_extensions"
            # }
        ]
    },
    "proxy.categories": {
        "title": "Denied web site categories",
        "tbl_source": {
            "table": {
                "source": "panel_categories"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "category",
                "label": "Category"
            }, {
                "key": "size",
                "label": "Items",
                "width": "20%"
            }, {
                "key": "VIP",
                "label": "VIP group",
                "width": "15%"
            }, {
                "key": "Standard",
                "label": "Standard group",
                "width": "15%"
            }, {
                "key": "Safe",
                "label": "Safe group",
                "width": "15%"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }],
            "actions": [{
                "action": "toggle_vip",
                "name": "Toggle for VIP"
            }, {
                "action": "toggle_standard",
                "name": "Toggle for Standard"
            }, {
                "action": "toggle_safe",
                "name": "Toggle for Safe"
            }],
            "id": ["category"],
            "source": "panel_categories",
        }]
    },
    "proxy.groups": {
        "title": "Groups by IP range",
        "tbl_source": {
            "table": {
                "source": "panel_ip_groups"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [{
                "type": "Button",
                "name": "Add range",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Addd IP range to Group",
                    "table_name": "table",
                    "refresh_action": "panel_ip_groups",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add range",
                        "class": "primary",
                        "action": "action_add_ip_group"
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
                            "name": "range",
                            "value": "",
                            "label": "Range",
                            "required": True
                        }]
                    }, {
                        "type": "Div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add a new range"
                        }, {
                            "type": "Paragraph",
                            "name": "There are 3 possible build-in groups. All IPs outside defined ranges are classified as Standard group too."
                        }]
                    }]
                }
            }]
        }, {
            "type": "Table",
            "name": "table",
            "reducers": ["table", "panel", "modal", "alert"],
            "columns": [{
                "key": "group",
                "label": "Group",
                "width": "20%"
            }, {
                "key": "range",
                "label": "IP range"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }],
            "actions": [{
                "action": "action_remove_ip_group",
                "name": "Remove",
                "class": "danger"
            }],
            "id": ["group","range"],
            "source": "panel_ip_groups"
            
        }]
    },
    "proxy.overview": {
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
                "key": "status",
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
                "width": "15%"
            },{
                "key": "ip",
                "label": "IP",
                "width": "15%"
            },{
                "key": "group",
                "label": "Group",
                "width": "10%"
            },{
                "key": "domain",
                "label": "Last blocked Domains",
                "width": "30%"
            },{
                "key": "reason",
                "label": "Reason",
                "width": "30%"
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
            }],
            "id": ["ip"],
            "source": "va_utils.panel_networking"
        }]
    },
    "proxy.edit_user_details": {
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