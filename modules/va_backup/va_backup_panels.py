panels = {
    "backup.overview": {
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
            "table_global_config": {
                "source": "panel_default_config"
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
            }, {
                "key": "clock",
                "label": "Clock"
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
            "table": {
                "source": "panel_list_folders",
            },
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
                            "name": "folder",
                            "value": "",
                            "label": "Backup Path/Share",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "backup_filter",
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
                            "name": "Enter the full absolute path or for Windows you can use system shares like D$. With filter backup fill be limited: *.pdf or db_backup"
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
                        "label": "Actions",
                        "width": "5%"
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
                            "name": "backup_filter",
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
                            "name": "backup_filter",
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
            "table": {
                "source": "panel_list_hosts"
            }
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
                            "name": "username",
                            "value": "",
                            "label": "Username",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "password",
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
                            "name": "Enter IP address or hostname. User should have read/write permissions."
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
                        "label": "Backups",
                        }, {
                        "key": "address",
                        "label": "Address",
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
                        "label": "Actions",
                        "width": "5%"
                        }
                        ],
            "actions": [{
                        "action": "start_backup",
                        "name": "Backup now",
                        }, {
                        "action": "create_archive",
                        "name": "Create archive",
                        "class": "danger"
                        }, {
                        "action": "change_address",
                        "name": "Edit address"
                        }, {
                        "action": "change_password",
                        "name": "Update password"
                        }, {
                        "action": "rm_host",
                        "name": "Remove source",
                        "class": "danger"
                        }
                        ],
            "id": ["host"],
            "modals": {
                "change_address": {
                    "title": "Edit address for the host",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Change",
                        "class": "primary",
                        "action": "change_address"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                                "type": "text",
                                "name": "new_data",
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
                            "name": "Enter IP address or hostname. Make sure the DNS used can resolve the hostname"
                        }
                        ]
                    }
                    ]
                },
                "change_password": {
                    "title": "Update Windows password",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Change",
                        "class": "primary",
                        "action": "change_password"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                                "type": "text",
                                "name": "new_data",
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
                            "name": "Enter the new password if it is cahnged on the Windows source"
                        }
                        ]
                    }
                    ]
                }
            }
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
                "width": "30%",
                "action": "folder:dir_structure1",
                "colClass": "type"
            }, {
                "key": "size",
                "label": "Size",
                "width": "10%",
            }, {
                "key": "time",
                "label": "Time"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
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
            "table": {
                "source": "backup_info"
            },
            "table_graph": {
                "source": "backup_info_graph"
            }
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
                "key": "sizeNew",
                "label": "New data"
            }, {
                "key": "size",
                "label": "Size"
            }, {
                "key": "type",
                "label": "Type"
            }
            ],
            "id": ["link"]
        },
            {
            "type": "CustomChart",
                "chartType": "line",
                "name": "graph1",
                "xCol": "startTime",
            "height": "50",
            # "xCol": "startTimeStamp",
            # "xColType": "date",
                "reducers": ["table"],
                "datasets": [{
                    "column": "sizeGraph",
                    "label": "Size (MB)",
                    "backgroundColor": "#337ab7",
                    #"backgroundColor": "#fff",
                    "borderColor": "#2e6da4",

                    "data": []
                }
                ],
            "target": "table_graph"
        }
        ]
    },
    "backup.schedule": {
        "title": "Backup Schedule",
        "tbl_source": {
            "table": {
                "source": "panel_list_schedule"
            },
            "table2": {
                "source": "panel_list_sequences"
            }
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
                "label": "Days between full backups",
            }, {
                "key": "fullmax",
                "label": "Full backups count",
            }, {
                "key": "incrperiod",
                "label": "Days between incr. backups",
            }, {
                "key": "incrmax",
                "label": "Incr. backups count",
            }, {
                "key": "action",
                "label": "Actions",
                "width": "5%"
            }
            ],
            "actions": [{
                "action": "change_fullperiod",
                "name": "Change full interval",
            }, {
                "action": "change_fullmax",
                "name": "Change full count"
            }, {
                "action": "change_incrperiod",
                "name": "Change incr. interval"
            }, {
                "action": "change_incrmax",
                "name": "Change incr. count"
            }, {
                "action": "reset_schedule",
                "name": "Use recommended values",
                "class": "danger"
            }
            ],
            "id": ["host"],
            "modals": {
                "change_fullperiod": {
                    "title": "Time between Full backups",
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
                            "name": "new_data",
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
                    "title": "Maximum number of full backups",
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
                            "name": "new_data",
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
                    "title": "Interval between incremental backups",
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
                            "name": "new_data",
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
                    "title": "Maximum number of incremental backups",
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
                            "name": "new_data",
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
                "label": "Expected Full backups history (days)",
            }, {
                "key": "incrseq",
                "label": "Incr. backups history (days)",
                "width": "25%"
            }
            ],
            "id": ["host"]
        }
        ]
    }
}
