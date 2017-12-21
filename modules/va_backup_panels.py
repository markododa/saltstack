panel = {
	"backup.overview": {
		"title": "Overview",
		"tbl_source": {
			"table_chkf": {
				"action": "panel_check_functionality",
				"module": "va_utils",
				"cols": ["status", "output"]
			},
			"table_net": {
				"action": "panel_networking",
				"module": "va_utils",
				"cols": ["ip", "dns"]
			},
			"table_statistics": {
				"action": "panel_statistics",
				"cols": ["key", "value"]
			}
		},
		"content": [{
				"type": "Table",
				"name": "table_chkf",
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
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "ip",
						"label": "IP addresses",
						"width": "50%"
					}, {
						"key": "dns",
						"label": "DNS servers"
					}
				],
				"id": ["ip"],
				"source": "va_utils.panel_networking"
			}
		]
	},
	"backup.manage": {
		"title": "Backup paths",
		"tbl_source": {
			"table": {}
		},
		"content": [{
				"type": "Form",
				"name": "form",
				"class": "tbl-ctrl",
				"elements": [{
						"type": "Button",
						"name": "Add Backup",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add a backup",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add backup",
									"class": "primary",
									"action": "add_folder"
								}
							],
							"content": [{
									"type": "Form",
									"name": "form",
									"class": "left",
									"elements": [{
											"type": "text",
											"name": "hostname",
											"value": "",
											"label": "App",
											"required": True
										}, {
											"type": "text",
											"name": "backup_path",
											"value": "",
											"label": "Backup path",
											"required": True
										}
									]
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to add a new backup"
										}, {
											"type": "Paragraph",
											"name": "Enter the full absolute path to the backup. The file must exist."
										}
									]
								}
							]
						}
					}
				]
			}, {
				"type": "Table",
				"name": "table",
				"reducers": ["table", "panel", "alert"],
				"panels": {
					"link": "backup.browse"
				},
				"columns": [{
						"key": "app",
						"label": "App"
					}, {
						"key": "path",
						"label": "Path",
						"width": "60%"
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"actions": [{
						"action": "rm_folder",
						"name": "Remove"
					}
				],
				"id": ["app", "path"]
			}
		]
	},
	"backup.hosts": {
		"title": "Manage Backup Sources",
		"tbl_source": {
			"table": {}
		},
		"content": [{
				"type": "Form",
				"name": "form",
				"class": "tbl-ctrl",
				"elements": [{
						"type": "Button",
						"name": "Add Backup Source",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add a Backup Source",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add backup",
									"class": "primary",
									"action": "add_host"
								}
							],
							"content": [{
									"type": "Form",
									"name": "form",
									"class": "left",
									"elements": [{
											"type": "text",
											"name": "hostname",
											"value": "",
											"label": "IP or Hostname",
											"required": True
										}
									]
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to add a new Backup Source"
										}
									]
								}
							]
						}
					}
				]
			}, {
				"type": "Table",
				"name": "table",
				"reducers": ["table", "panel", "alert"],
				"subpanels": {
					"link": "backup.info"
				},
				"columns": [{
						"key": "host",
						"label": "Source",
						"action": "all:link",
						"colClass": "link"
					}, {
						"key": "total_backups",
						"label": "Total backups",
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"actions": [{
						"action": "start_backup",
						"name": "Backup Now",
					}, {
						"action": "rm_host",
						"name": "Remove Source",
						"class": "danger"
					}
				],
				"id": ["app", "path"]
			}
		]
	},
	"backup.browse": {
		"title": "Browse backups",
		"tbl_source": {
			"table": {}
		},
		"content": [{
				"type": "Path",
				"name": "path",
				"action": "dir_structure1",
				"target": "table",
				"reducers": ["table", "panel"]
			},  {
				"type": "Table",
				"name": "table",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "dir",
						"label": "Files/Folders",
						"width": "20%",
						"action": "folder:dir_structure1",
						"colClass": "type"
					}, {
						"key": "size",
						"label": "Size"
					}, {
						"key": "time",
						"label": "Time"
					}, {
						"key": "action",
						"width": "15%",
						"label": "Actions"
					}
				],
				"actions": [{
						"action": "rm_folder",
						"name": "Remove"
					}, {
						"action": "restore",
						"name": "Restore"
					}, {
						"action": "restore_backup",
						"name": "Restore to Host"
					}, {
						"action": {
							"type": "download",
							"name": "download_zip"
						},
						"name": "Download"
					}
				],
				"id": ["dir"]
			}
		]
	},
	"backup.info": {
		"title": "Backup info",
		"tbl_source": {
			"table": {}
		},
		"content": [{
				"type": "Table",
				"name": "table",
				"reducers": ["table", "panel", "alert"],
				"panels": {
					"link": "backup.browse"
				},
				"columns": [{
						"key": "age",
						"label": "Age (hh:mm:ss)"
					}, {
						"key": "backup",
						"label": "Backup number",
						"action": "all:link",
						"width": "15%",
						"colClass": "link"
					}, {
						"key": "duration",
						"label": "Duration"
					}, {
						"key": "startTime",
						"label": "Start time"
					}, {
						"key": "endTime",
						"label": "End time"
					}, {
						"key": "type",
						"label": "Type"
					}
				],
				"id": ["link"]
			}
		]
	}
}

