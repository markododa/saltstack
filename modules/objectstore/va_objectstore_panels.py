panels = {
  
    "objectstore.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality"
            }
            "table_stats": {
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
                "width": "12%"
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
                "width": "25%"
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
    }
}