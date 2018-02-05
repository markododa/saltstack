panel = {
	"monitoring.overview": {
		"title": "Overview",
		"tbl_source": {
			"table_chkf": {
				"action": "panel_check_functionality",
				"module": "va_utils",
				"cols": ["status", "output"]
			},
			"table_statistics": {
				"action": "panel_overview",
				"cols": ["key", "value"]
			},
                        "table_net": {
                                "action": "panel_networking",
                                "module": "va_utils",
                                "cols": ["ip", "dns"]
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
		},{
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
		"title": "Icinga proxy",
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
		"content": [{
				"type": "Form",
				"name": "form",
				"class": "pull-right margina form-inline",
				"elements": [{
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
								"label": "Name"
							}, {
								"key": "output",
								"label": "Output",
								"width": "80%"
							}, {
								"key": "state",
								"label": "State"
							}, {
								"key": "action",
								"label": "Actions"
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
