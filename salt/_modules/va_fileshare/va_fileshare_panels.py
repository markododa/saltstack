panels = {
    "fileshare.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality",
                "module": "va_utils"
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
                "width": "20%"
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
            "name": "table_statistics",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "key",
                "label": "Storage",
                "width": "40%"
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
            }, {
                "key": "clock",
                "label": "Clock"
            }
            ],
            "id": ["ip"],
            "source": "va_utils.panel_networking"
        }
        ]
    }, "fileshare.shares": {
        "title": "Shares and Disk usage",
        "tbl_source": {
            "table_shares": {
                "source": "panel_all_fileshares"
            }
        },
        "content": [{
            "type": "Table",
            "pagination": False,
            "name": "table_shares",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                    "key": "share",
                    "label": "Share",
                    "width": "20%"
            }, {
                "key": "subfolder",
                "label": "1st level Subfolders",
                "width": "20%"
            }, {
                "key": "size",
                "label": "Total Size (MB)",
                "width": "15%"
            }, {
                "key": "path",
                "label": "Filesystem path",
                "width": "40%"
            }
            ],
            "id": ["path"],
            "source": "panel_all_fileshares"
        # },
        #     {
        #     "type": "CustomChart",
        #         "chartType": "pie",
        #         "name": "subfolder",
        #         "xCol": "subfolder",
        #     "options" :{"height": "200","legend": {"position": "left"}},
        #     "height": "200",


        #     "legend": [{"position": "left"}],

        #         "reducers": ["table"],
        #         "datasets": [{
        #             "column": "size",
        #            "height": "200",
        #             "name": "subfolder",
                 
        #             "backgroundColor": "#fff",
        #             "borderColor": "#2e6da4",
        #             "hoverBackgroundColor": "#337ab7",
        #             "title": "startTime",
        #             "data": []
        #         }
        #     ],
        #     "target": "table_shares"
        }
        ]
    }
}
