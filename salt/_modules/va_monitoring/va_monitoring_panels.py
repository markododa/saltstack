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
    "monitoring.service_history_weekly": {
        "title": "Last week events",
        "tbl_source": {
            "table_events": {
                "source": "panel_history_events_weekly"
            },
            "table_summ": {
                "source": "panel_history_summary_weekly"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_summ",
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
            "source": "panel_history_summary_weekly"
        },

            {
                "type": "Table",
                "name": "table_events",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                    "key": "key",
                    "label": "Time",
                    "width": "13%"
                }, {
                    "key": "duration",
                    "label": "Duration",
                    "width": "13%"
                }, {
                    "key": "state",
                    "label": "State",
                    "width": "7%"
                }, {
                    "key": "type",
                    "label": "Type",
                    "width": "7%"
                }, {
                    "key": "service",
                    "label": "Service",
                    "width": "10%"
                }, {
                    "key": "output",
                    "label": "Output",
                    "width": "60%"
                }],
                "rowStyleCol": "state",
                "id": ["key"],
                "source": "panel_history_events_weekly"
        }


        ]
    },
    "monitoring.service_history_monthly": {
        "title": "Last month events",
        "tbl_source": {
            "table_events": {
                "source": "panel_history_events_monthly"
            },
            "table_summ": {
                "source": "panel_history_summary_monthly"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_summ",
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
            "source": "panel_history_summary_monthly"
        }, {
            "type": "Table",
            "name": "table_events",
            "pagination": False,
            "reducers": ["table", "panel", "alert", "filter"],
            "columns": [{
                "key": "key",
                "label": "Time",
                "width": "13%"
            }, {
                "key": "duration",
                "label": "Duration",
                "width": "13%"
            }, {
                "key": "state",
                "label": "State",
                "width": "7%"
            }, {
                "key": "type",
                "label": "Type",
                "width": "7%"
            }, {
                "key": "service",
                "label": "Service",
                "width": "10%"
            }, {
                "key": "output",
                "label": "Output",
                "width": "60%"
            }],
            "rowStyleCol": "state",
            "id": ["key"],
            "source": "panel_history_events_monthly"
        }]
    },
    "monitoring.icinga": {
        "title": "Proxy",
        "content": [{
            "type": "Frame",
            "name": "frame",
            "src": "/proxy/"
        }]
    },
    "monitoring.chart": {
        "title": "",
        "content": [{
            "type": "Chart",
            "name": "chart",
            "reducers": ["panel"]
        }]
    },
    "monitoring.details": {
        "title": "Monitoring details",
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
                    }],
                    "panels": {
                        "view_graph": "monitoring.graph",
                        "view_multi_graph_1h": "monitoring.multi_charts_1h",
                        "view_multi_graph_1d": "monitoring.multi_charts_1d",
                        "view_multi_graph_1w": "monitoring.multi_charts_1w",
                        "month_history": "monitoring.service_history_monthly",
                        "week_history": "monitoring.service_history_weekly",
                    },
                    "rowStyleCol": "state",
                    "actions": [{
                        "name": "Graphs (last hour)",
                        "action": "view_multi_graph_1h"
                    }, {
                        "name": "Graphs (last day)",
                        "action": "view_multi_graph_1d"
                    }, {
                        "name": "Graphs (last week)",
                        "action": "view_multi_graph_1w"
                    },  {
                        "name": "Last month history",
                        "action": "month_history"
                    },
                        {
                        "name": "Force check now",
                        "action": "force_check"
                    }],
                    "id": ["name", "host_name"]
                }]
            }
        ]
    },
    "monitoring.problems": {
        "title": "Current problems",
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
                    }],
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
                    "actions": [{
                        "name": "View graphs",
                        "action": "chart"
                    }, {
                        "name": "Graphs (last hour)",
                        "action": "view_multi_graph_1h"
                    }, {
                        "name": "Graphs (last day)",
                        "action": "view_multi_graph_1d"
                    }, {
                        "name": "Graphs (last week)",
                        "action": "view_multi_graph_1w"
                    }, {
                        "name": "Last month history",
                        "action": "month_history"
                    },
                        {
                        "name": "Force check now",
                        "action": "force_check"
                    }],
                    "id": ["name", "host_name"]
                }]
            }
        ]
    },
    "monitoring.multi_charts_1h": {
        "title": "Charts (last hour)",
        "tbl_source": {},
        "content": [{
            "type": "MultiTable",
            "name": "div",
            "reducers": ["table"],
            "elements": [{
                    "type": "Heading"
            },
                {
                "type": "CustomChart",
                "chartType": "line",
                "xCol": "timestamp",
                "colorAuto": True,
                "height": 50,
                "colorAuto": True,
                "target": "auto",
                "reducers": ["table"],
                "options":{
                        "legend": {"display": False,
                                   "hidden": True
                                   }
                },
                "datasets": [{
                    "column": "y",
                    "data": []
                }
                ],

            }]
        }
        ]
    },
    "monitoring.multi_charts_1d": {
        "title": "Charts (last 24 hours)",
        "tbl_source": {},
        "content": [
                {
                "type": "MultiTable",
                "name": "div",
                "reducers": ["table"],
                "elements": [{
                    "type": "Heading"
                },         {
                    "type": "CustomChart",
                    "chartType": "line",
                    "xCol": "timestamp",
                "colorAuto": True,
                "target": "auto",
                                "options": {
                        "legend": {"display": False,
                                   "hidden": True
                                   }
                },
                "reducers": ["table"],
                    "height": 50,
                    "datasets": [{
                        "column": "y",
                        "data": []
                    }
                    ],
                    "columns": [{
                        "key": "timestamp",
                        "label": "time"
                    }, {
                        "key": "y",
                        "label": "y",
                        "width": "50%"
                    }]
                }]
            }
        ]
    },
    "monitoring.multi_charts_1w": {
        "title": "Charts (last 7 days)",
        "tbl_source": {},
        "content": [{
            "type": "MultiTable",
            "name": "div",
            "reducers": ["table"],
            "elements": [{
                    "type": "Heading"
            },   
                      {
                "type": "CustomChart",
                "chartType": "line",
                "xCol": "timestamp",
                "height": 50,
                "colorAuto": True,
                "target": "auto",
                "reducers": ["table"],
                "options": {
                        "legend": {"display": False,
                                   "hidden": True
                                   }
                },
                "datasets": [{
                    "column": "y",
                    "data": []
                }
                ]
            }]
        }
        ]
    },
    "monitoring.summary": {
        "title": "Summary",
        "tbl_source": {
            "table_summary": {
                "source": "icinga2_summary"
            }},
        "content": [
            {
                "type": "Form",
                "name": "form1",
                "elements": [{
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
                            }],
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
                                }, {
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
                                }, {
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

                                }]
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
                                }]
                            }]
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
                            }],
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
                                }, ]
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
                                }]
                            }]
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

                "type": "Table",
                "name": "table_summary",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [
                    {
                        "key": "host_name",
                        "label": "Hostname",
                        "width": "25%"
                    }, {
                        "key": "OK",
                        "label": "OK",
                        "width": "14%"
                    }, {
                        "key": "Warning",
                        "label": "Warning",
                        "width": "14%"
                    }, {
                        "key": "Critical",
                        "label": "Critical",
                        "width": "14%"
                    }, {
                        "key": "Unknown",
                        "label": "Unknown",
                        "width": "14%"
                    }, {
                        "key": "Pending",
                        "label": "Pending",
                        "width": "14%"
                    }, {
                        "key": "action",
                        "label": "Actions",
                        "width": "5%"
                    }],
                "panels": {
                    "details": "monitoring.details"
                },
                "rowStyleCol": "state",
                "actions": [{
                    "name": "Details",
                    "action": "details"
                }],
                "id": ["host_name"]

            }
        ]
    },
    "monitoring.history": {
        "title": "Event history (one month)",
        "tbl_source": {},
        "content": [

            {
                "type": "Form",
                "name": "form1",
                #"class": "pull-right margina form-inline",
                "elements": [

                ]
            },

            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    {
                        "type": "Filter",
                        "name": "Filter1",
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
                        "key": "key",
                        "label": "Time",
                        "width": "13%"
                        # }, {
                        #     "key": "duration",
                        #     "label": "Duration",
                        #     "width": "13%"
                    }, {
                        "key": "state",
                        "label": "State",
                        "width": "7%"
                    }, {
                        "key": "type",
                        "label": "Type",
                        "width": "7%"
                    }, {
                        "key": "service",
                        "label": "Service",
                        "width": "10%"
                    }, {
                        "key": "output",
                        "label": "Output",
                        "width": "60%"
                    }],
                    "panels": {
                        "view_graph": "monitoring.graph",
                        "month_history": "monitoring.service_history_monthly",
                        "week_history": "monitoring.service_history_weekly",
                    },
                    "rowStyleCol": "state",
                    "actions": [{
                        "name": "View graphs",
                        "action": "chart"
                    }, {
                        "name": "Last month history",
                        "action": "month_history"
                    }, {
                        "name": "Last week history",
                        "action": "week_history"
                    }]
                }]
            }
        ]
    }
}
