panels = {
    "tux.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality"
            },
            "table_net": {
                "source": "panel_networking",
                "module": "va_utils"
            }
        },
        "content": [
            {
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
                }],
            "rowStyleCol": "state",
            "source": "va_utils.check_functionality"
            },
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