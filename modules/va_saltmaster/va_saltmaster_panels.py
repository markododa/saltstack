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
                    "view_graph": "saltmaster.graph",
                    "month_history": "saltmaster.service_history_monthly",
                    "week_history": "saltmaster.service_history_weekly",
                },
                "rowStyleCol": "state",
                "actions": [{
                    "name": "Test",
                    "action": "none"
                }],
                "id": ["minion"]
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
