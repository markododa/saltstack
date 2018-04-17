panels = {
    "objectstore.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality"
            },
            "table_config": {
                "source": "panel_config"
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
                }],
                "source": "va_utils.check_functionality"
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
            } ,{
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
        }
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
            }
        ]
    }
}