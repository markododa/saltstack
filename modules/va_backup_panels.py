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
			"table_global_config": {
				"action": "panel_default_config",
				"cols": ["key", "value"]
			},
			"table_statistics": {
				"action": "panel_statistics",
				"cols": ["key", "value"]
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
						"label": "Statistics",
						"width": "30%"
					}, {
						"key": "value",
						"label": "Value"
					}
				],
				"id": ["key"],
				"source": "panel_statistics"
			}, {
				"type": "Table",
				"name": "table_global_config",
				"pagination": False,
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "key",
						"label": "Global Config",
						"width": "30%"
					}, {
						"key": "value",
						"label": "Value"
					}
				],
				"id": ["key"],
				"source": "panel_default_config"
			}, {
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
					}
				],
				"id": ["ip"],
				"source": "va_utils.panel_networking"
			}
		]
	},
	"backup.manage": {
		"title": "Backup paths and filters",
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
											"label": "Source",
											"required": True
										}, {
											"type": "text",
											"name": "backup_path",
											"value": "",
											"label": "Backup Path/Share",
											"required": True
										}, {
											"type": "text",
											"name": "include_filter",
											"value": "",
											"label": "Include Filter",
											"required": False
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
											"name": "Enter the full absolute path to the backup. For Windows, you can use system shares like D$. With include filter backup fill be limited: *.pdf or db_backup/"
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
				"reducers": ["table", "panel", "modal", "alert"],
				"panels": {
					"link": "backup.browse"
				},
				"columns": [{
						"key": "app",
						"width": "20%",
						"label": "Source"
					}, {
						"key": "path",
						"label": "Path/Share to backup",
						"width": "30%"
					}, {
						"key": "include",
						"label": "Backup filter (include only)",
						"width": "30%"
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"actions": [{
						"action": "rm_folder",
						"name": "Remove folder",
						"class": "danger"

					}, {
						"action": "rm_filter_from_path",
						"name": "Remove filter",
						"class": "danger"

					}, {
						"action": "add_filter_to_path",
						"name": "Add filter"
					}

				],
				"id": ["app", "path"],
				"modals": {
					"rm_filter_from_path": {
						"title": "Remove include filter",
						"buttons": [{
								"type": "Button",
								"name": "Cancel",
								"action": "cancel"
							}, {
								"type": "Button",
								"name": "Remove",
								"class": "primary",
								"action": "rm_filter_from_path"
							}
						],
						"content": [{
								"type": "Form",
								"name": "form",
								"class": "left",
								"elements": [{
										"type": "text",
										"name": "value",
										"value": "",
										"label": "Filter string"
									}
								]
							}, {
								"type": "Div",
								"name": "div",
								"class": "right",
								"elements": [{
										"type": "Heading",
										"name": "Fill the form to remove the filter"
									}, {
										"type": "Paragraph",
										"name": "Typed filter will be removed from the list of filters for this folder"
									}
								]
							}
						]
					},
					"add_filter_to_path": {
						"title": "Add include filter",
						"buttons": [{
								"type": "Button",
								"name": "Cancel",
								"action": "cancel"
							}, {
								"type": "Button",
								"name": "Add",
								"class": "primary",
								"action": "add_filter_to_path"
							}
						],
						"content": [{
								"type": "Form",
								"name": "form",
								"class": "left",
								"elements": [{
										"type": "text",
										"name": "value",
										"value": "",
										"label": "Filter string"
									}
								]
							}, {
								"type": "Div",
								"name": "div",
								"class": "right",
								"elements": [{
										"type": "Heading",
										"name": "Fill the form to add a filter"
									}, {
										"type": "Paragraph",
										"name": "If there is at least one filter, backup will be limited to listed filters"
									}
								]
							}
						]
					},

				}
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
						"name": "Add known Source",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add a known backup Source",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add backup",
									"class": "primary",
									"action": "add_rsync_host"
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
											"label": "Minion name",
											"required": True
										}

									]
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to define access to the source"
										}, {
											"type": "Paragraph",
											"name": "Only minion name is required. The source will be backed up with rsync protocol. Should already have the public SSH key from va-backup"
										}

									]
								}
							]
						}
					}, {
						"type": "Button",
						"name": "Add new Linux source",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add a new Linux backup Source",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add backup",
									"class": "primary",
									"action": "add_rsync_host"
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
											"label": "Hostname",
											"required": True
										}, {
											"type": "text",
											"name": "address",
											"value": "",
											"label": "IP address (leave blank if listed in DNS)",
											"required": False
										}, {
											"type": "text",
											"name": "password",
											"value": "",
											"label": "Root password",
											"required": False
										}

									]
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to define access to the source"
										}, {
											"type": "Paragraph",
											"name": "Enter IP adress if the Source is not listed in the DNS. Root password is needed to upload the public SSH key. Backup will be done with rsync."
										}
									]
								}
							]
						}
					}, {
						"type": "Button",
						"name": "Add new Windows source",
						"glyph": "plus",
						"action": "modal",
						"reducers": ["modal"],
						"modal": {
							"title": "Add a new Windows backup Source",
							"buttons": [{
									"type": "Button",
									"name": "Cancel",
									"action": "cancel"
								}, {
									"type": "Button",
									"name": "Add backup",
									"class": "primary",
									"action": "add_smb_host"
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
											"label": "Hostname",
											"required": True
										}, {
											"type": "text",
											"name": "address",
											"value": "",
											"label": "IP address",
											"required": False
										}, {
											"type": "text",
											"name": "SmbShareUserName",
											"value": "",
											"label": "Username",
											"required": False
										}, {
											"type": "text",
											"name": "SmbSharePasswd",
											"value": "",
											"label": "Password",
											"required": False
										}

									]
								}, {
									"type": "Div",
									"name": "div",
									"class": "right",
									"elements": [{
											"type": "Heading",
											"name": "Fill the form to define access to the source"

										}, {
											"type": "Paragraph",
											"name": "Enter IP adress if the Source is not listed in the DNS. User should have read permissions to do backup and write permissions if you want to do restore. It is recommnded to make full backups only (keep Incremental period higher)"
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
						"key": "protocol",
						"label": "Protocol"
					}, {
						"key": "status",
						"label": "Status"
					}, {
						"key": "error",
						"label": "Error"
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"actions": [{
						"action": "start_backup",
						"name": "Backup Now",
					}, {
						"action": "create_archive",
						"name": "Create Archive",
						"class": "danger"

					}, {
						"action": "rm_host",
						"name": "Remove Source",
						"class": "danger"
					}
				],
				"id": ["host"]
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
			}, {
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
						"label": "Age"
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
	},

	"backup.schedule": {
		"title": "Backup Schedule",
		"tbl_source": {
			"table": {}
		},
		"content": [{
				"type": "Table",
				"name": "table",
				"reducers": ["table", "panel", "modal", "alert"],
				"columns": [{
						"key": "host",
						"label": "Source",
					}, {
						"key": "fullperiod",
						"label": "Days between Full backups",
					}, {
						"key": "fullmax",
						"label": "Full backups count",
					}, {
						"key": "incrperiod",
						"label": "Days between Incr backups",
					}, {
						"key": "incrmax",
						"label": "Incr Backups count",
					}, {
						"key": "action",
						"label": "Actions"
					}
				],
				"actions": [{
						"action": "change_fullperiod",
						"name": "Change Full Period",
					}, {
						"action": "change_fullmax",
						"name": "Change Full Count"
					}, {
						"action": "change_incrperiod",
						"name": "Change Incr Period"
					}, {
						"action": "change_incrmax",
						"name": "Change Incr Count"
					}, {
						"action": "reset_schedule",
						"name": "Use recommended values",
						"class": "danger"

					}

				],
				"id": ["host"],
				"modals": {
					"change_fullperiod": {
						"title": "Period between Full backups",
						"buttons": [{
								"type": "Button",
								"name": "Cancel",
								"action": "cancel"
							}, {
								"type": "Button",
								"name": "Change",
								"class": "primary",
								"action": "change_fullperiod"
							}
						],
						"content": [{
								"type": "Form",
								"name": "form",
								"class": "left",
								"elements": [{
										"type": "text",
										"name": "value",
										"value": "",
										"label": "New value"
									}
								]
							}, {
								"type": "Div",
								"name": "div",
								"class": "right",
								"elements": [{
										"type": "Heading",
										"name": "Fill the form to change the value"
									}, {
										"type": "Paragraph",
										"name": "The value is number od days between backups. Use sligthly lower number (0.97 for once daily). Enter 0.04 for each hour. Leave empty field to reset to global config."
									}
								]
							}
						]
					},

					"change_fullmax": {
						"title": "Maximum number of Full backups",
						"buttons": [{
								"type": "Button",
								"name": "Cancel",
								"action": "cancel"
							}, {
								"type": "Button",
								"name": "Change",
								"class": "primary",
								"action": "change_fullmax"
							}
						],
						"content": [{
								"type": "Form",
								"name": "form",
								"class": "left",
								"elements": [{
										"type": "text",
										"name": "value",
										"value": "",
										"label": "New value"
									}
								]
							}, {
								"type": "Div",
								"name": "div",
								"class": "right",
								"elements": [{
										"type": "Heading",
										"name": "Fill the form to change the value"
									}, {
										"type": "Paragraph",
										"name": "Enter full number ot enter list of numbers to take advantage of exponential backup expiry. Leave empty field to reset to global config"
									}
								]
							}
						]
					},

					"change_incrperiod": {
						"title": "Period between Incremental backups",
						"buttons": [{
								"type": "Button",
								"name": "Cancel",
								"action": "cancel"
							}, {
								"type": "Button",
								"name": "Change",
								"class": "primary",
								"action": "change_incrperiod"
							}
						],
						"content": [{
								"type": "Form",
								"name": "form",
								"class": "left",
								"elements": [{
										"type": "text",
										"name": "value",
										"value": "",
										"label": "New value"
									}
								]
							}, {
								"type": "Div",
								"name": "div",
								"class": "right",
								"elements": [{
										"type": "Heading",
										"name": "Fill the form to change the value"
									}, {
										"type": "Paragraph",
										"name": "The value is number od days between backups. Use sligthly lower number (0.97 for once daily). Enter 0.04 for each hour. Leave empty field to reset to global config."
									}
								]
							}
						]
					},

					"change_incrmax": {
						"title": "Maximum number of Incremental backups",
						"buttons": [{
								"type": "Button",
								"name": "Cancel",
								"action": "cancel"
							}, {
								"type": "Button",
								"name": "Change",
								"class": "primary",
								"action": "change_incrmax"
							}
						],
						"content": [{
								"type": "Form",
								"name": "form",
								"class": "left",
								"elements": [{
										"type": "text",
										"name": "value",
										"value": "",
										"label": "New value"
									}
								]
							}, {
								"type": "Div",
								"name": "div",
								"class": "right",
								"elements": [{
										"type": "Heading",
										"name": "Fill the form to change the value"
									}, {
										"type": "Paragraph",
										"name": "Enter full number. Leave empty field to reset to global config"
									}
								]
							}
						]
					},

				}
			}, {
				"type": "Table",
				"name": "table2",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "host",
						"label": "Source",
                                                "width": "20%"

					}, {
						"key": "fullseq",
						"label": "Full Backups Sequence (days)",

					}, {
						"key": "incrseq",
						"label": "Incr Backup Sequence (days)",
                                                "width": "25%"

					}
				],
				"id": ["host"]

			}
		]
	}

}

