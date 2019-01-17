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

                    # {
                    #     "type": "Filter",
                    #     "name": "Filter",
                    #     "reducers": ["filter"]
                    # }
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
    "saltmaster.ssh": {
        "title": "SSH Keys",
        "tbl_source": {
            "table": {
                "source": "list_store_ssh_keys"
            },
            "root_keys": {
                "source": "list_minions_ssh_keys"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "tbl-ctrl",
                "elements": [{
                "type": "Button",
                "name": "Add new SSH key",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add a new SSH key",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add key",
                        "class": "primary",
                        "action": "add_ssh_key_store"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "comment",
                            "value": "",
                            "label": "User",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "enc",
                            "value": "",
                            "label": "Encryption",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "key",
                            "value": "",
                            "label": "Key",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to define a new SSH key"
                        }, {
                            "type": "Paragraph",
                            "name": "Enter all 3 parts of the key."
                        }
                        ]
                    }
                    ]
                }
            }
            # ,
            #         {
            #             "type": "Filter",
            #             "name": "Filter",
            #             "reducers": ["filter"]
            #         }
                ]
            },  {
                "type": "Table",
                "source":"list_store_ssh_keys",
                "name": "table",
                "pagination": True,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [
                #     {
                #         "key": "minion",
                #         "label": "Minion name",
                #     "width": "30%"
                # },
                {
                        "key": "comment",
                        "label": "Known key in SSH store",
                    "width": "25%"
                }, {
                        "key": "enc",
                        "label": "Encryption",
                    "width": "10%"
                }, {
                    "key": "key_short",
                    "label": "SSH key (partial)",
                    "width": "25%"
                },{
                    "key": "fingerprint",
                    "label": "Fingerprint",
                    "width": "30%"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "view_graph": "saltmaster.graph"
                },
                "actions": [{
                    "name": "Upload to a minion",
                    "action": "key_to_minion"
                }, {
                    "name": "Delete key from store",
                    "action": "ssh_key_delete_store",
                    "class": "danger"
                }],
                "id": ["comment","enc","key"],
                "modals": {
                "key_to_minion": {
                    "title": "Upload the public key to a minion",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Apply",
                        "class": "primary",
                        "action": "upload_ssh_key_minion"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "minion",
                            "value": "",
                            "label": "Target minion"
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form with the target minion name"
                        }, {
                            "type": "Paragraph",
                            "name": "You can remove the key later from the Minion panel."
                        }
                        ]
                    }
                    ]
                }
            }},
            {
                "type": "Table",
                "source":"list_minions_ssh_keys",
                "name": "root_keys",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [
                #     {
                #         "key": "minion",
                #         "label": "Minion name",
                #     "width": "30%"
                # },
                {
                        "key": "comment",
                        "label": "Root access to va-master",
                    "width": "25%"
                }, {
                        "key": "enc",
                        "label": "Encryption",
                    "width": "10%"
                }, {
                    "key": "key_short",
                    "label": "SSH key (partial)",
                    "width": "25%"
                },{
                    "key": "fingerprint",
                    "label": "Fingerprint",
                    "width": "30%"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "view_graph": "saltmaster.graph"
                },
                "actions": [{
                    "name": "Copy to SSH store",
                    "action": "key_to_store"
                },{
                    "name": "Download public key*",
                    "action": "download_pubkey"
                }],
                "id": ["comment","enc","key"],
            }

        ]
    },
    "saltmaster.integrations": {
        "title": "Integrations",
        "tbl_source": {
            "table": {
                "source": "list_minions_integrations"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [
                ]
            },  {
                "type": "Table",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "modal", "alert", "filter"],
                "columns": [{
                        "key": "minion",
                        "label": "Minion",
                    "width": "10%"
                }, {
                    "key": "role",
                    "label": "Role",
                    "width": "10%"
                }, {
                    "key": "integrations",
                    "label": "Integration description",
                    "width": "75%"
                },{
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "panels": {
                    "apply_integration": "saltmaster.apply_integrations"

                },
                "actions": [{
                    "name": "Apply to...",
                    "action": "apply_integration"
                }],
                "id": ["minion","role"],

            }

        ]
    },
    "saltmaster.apply_integrations": {
        "title": "Integrations available",
        "tbl_source": {
            "table": {
                "source": "apply_minions_integrations"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [
                ]
            },  {
                "type": "Table",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "modal", "alert", "filter"],
                "columns": [{
                        "key": "from",
                        "label": "Integrator (role)",
                    "width": "15%"
                }, {
                    "key": "to",
                    "label": "Target (role)",
                    "width": "15%"
                },{
                    "key": "integrations",
                    "label": "Integration description",
                    "width": "65%"
                },{
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "actions": [{
                    "name": "Integrate*",
                    "action": "apply_integration_state"
                }],
                "id": ["minion","role","lookfor","target","target_role"],

            }

        ]
    },
    "saltmaster.minions": {
        "title": "Minions",
        "tbl_source": {
            "table": {
                "source": "list_minions_details"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                # "class": "pull-right margina form-inline",
                "elements": [{
                "type": "Button",
                "name": "Bulk Updates",
                "glyph": "refresh",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Perform upgrade action",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Run action",
                        "class": "primary",
                        "action": "bulk_update_minions"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "dropdown",
                            "name": "bulk_update_command",
                            "values": ["Check for updates", "Upgrade all"],
                            "label": "Type",
                            "required": True
                        }, {
                            "type": "checkbox",
                            "name": "distro",
                            "value": False,
                            "label": "Latest distro",
                            "required": False
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Pick a command to be run on all online minions"
                        }, {
                            "type": "Paragraph",
                            "name": "It takes time for the command to complete. Please wait after pressing the action."
                        }
                        ]
                    }
                    ]
                }
            },{
                "type": "Button",
                "name": "Sync Salt",
                "glyph": "transfer",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Sync minions",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Sync all",
                        "class": "primary",
                        "action": "salt_sync_all"
                    }
                    ],
                    "content": [{
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Sync down all of the dynamic modules"
                        }, {
                            "type": "Paragraph",
                            "name": "This function synchronizes custom modules, states, beacons, grains, returners, output modules, renderers and utils."
                        }
                        ]
                    }
                    ]
                }
            }
                ]
            },  {
                "type": "Table",
                "name": "table",
                "source": "list_minions_details",
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
                    "ssh_keys": "saltmaster.list_ssh_keys",
                    "hardware": "saltmaster.hardware",
                    "minion_upgrades": "saltmaster.minion_upgrades"
                },
                "rowStyleCol": "state",
                "actions": [{
                    "name": "Hardware details",
                    "action": "hardware"
                },{
                    "name": "Manage SSH access",
                    "action": "ssh_keys"
                },{
                    "name": "List updates",
                    "action": "minion_upgrades"
                },{
                    "name": "Update'n'upgrade all packages",
                    "action": "upgrade_all_packages",
                        "class": "danger",
                }],
                "id": ["minion"],
            "modals": {
                "upgrade_all_packages": {
                    "title": "Upgrade all packages",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Upgrade all",
                        "class": "primary",
                        "action": "minion_upgrade_all"
                    }
                    ],
                    "content": [
                    #     {
                    #     "type": "Form",
                    #     "name": "form",
                    #     "class": "left",
                    #     "elements": [
                    #         #Confirmation?
                    #     ]
                    # },
                    {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Install all avaiable upgrades"
                        }, {
                            "type": "Paragraph",
                            "name": "Upgrade can take some time. This dialog will be closed at the end of the process. Please wait."
                        }
                        ]
                    }
                    ]
                }
            }

                }

        ]
    },
    "saltmaster.hardware": {
        "title": "Hardware details",
        "tbl_source": {
            "table": {
                "source": "panel_minion_grains"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    # {
                    #     "type": "Filter",
                    #     "name": "Filter",
                    #     "reducers": ["filter"]
                    # }
                ]
            },  {
                "type": "Table",
                "name": "table",
                "pagination": False,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "item",
                        "label": "Item",
                    "width": "30%"
                }, {
                    "key": "value",
                    "label": "Value",
                    "width": "70%"
                }],
                "id": ["key"]
            }

        ]
    },
    "saltmaster.list_ssh_keys": {
        "title": "Authorized SSH keys as root",
        "tbl_source": {
            "table": {
                "source": "list_minion_ssh_keys"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [{
                "type": "Button",
                "name": "Add a known SSH key",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add a known SSH key",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add backup",
                        "class": "primary",
                        "action": "add_known_key"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "key_code",
                            "value": "",
                            "label": "Fingerprint",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form with the SSH key fingerprint without colon signs"
                        }, {
                            "type": "Paragraph",
                            "name": "Fingerprint can be copied form the SSH Keys panel. Only keys from the SSH store can be used. This will allow root access to the minion instance."
                        }
                        ]
                    }
                    ]
                }
            }
            ]
        },  {
                "type": "Table",
                "name": "table",
                "pagination": True,

                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "comment",
                        "label": "User",
                    "width": "25%"
                }, {
                        "key": "enc",
                        "label": "Encryption",
                    "width": "10%"
                }, {
                    "key": "key_short",
                    "label": "SSH key (partial)",
                    "width": "60%"
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
                "actions": [{
                    "name": "Remove",
                    "action": "remove_ssh_key_minion"
                }],
                "id": ["comment","enc","key","minion"],
                "source": "list_minion_ssh_keys",
            }

        ]
    },
    "saltmaster.minion_upgrades": {
        "title": "Available upgrades",
        "tbl_source": {
            "table": {
                "source": "list_minion_upgrades"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [

            ]
        },  {
                "type": "Table",
                "name": "table",
                # "source": "list_minions_details",
                "pagination": True,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "package",
                        "label": "Package",
                    "width": "55%"
                }, {
                        "key": "ver",
                        "label": "Version",
                    "width": "40%"
                }, {
                    "key": "action",
                    "label": "Actions",
                    "width": "5%"
                }],
                "actions": [{
                    "name": "Upgrade",
                    "action": "minion_upgrade"
                }],
                "id": ["package"]
            }

        ]
    },
    "saltmaster.pillars": {
        "title": "Pillars (Global variables)",
        "tbl_source": {
            "table": {
                "source": "list_pillars"
            }
        },
        "content": [
            {
                "type": "Form",
                "name": "form",
                "class": "pull-right margina form-inline",
                "elements": [

                    # {
                    #     "type": "Filter",
                    #     "name": "Filter",
                    #     "reducers": ["filter"]
                    # }
                ]
            },  {
                "type": "Table",
                "name": "table",
                "pagination": True,
                "reducers": ["table", "panel", "alert", "filter"],
                "columns": [{
                        "key": "pillar",
                        "label": "Pillar",
                    "width": "25%"
                }, {
                        "key": "human_name",
                        "label": "Description",
                    "width": "35%"
                }, {
                    "key": "value",
                    "label": "Value",
                    "width": "35%"
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
                    "name": "Test",
                    "action": "none"
                }],
                "id": ["pillar"]
            }

        ]
    },
    "saltmaster.functionality": {
        "title": "Functionality tests",
        "tbl_source": {},
        "content": [
            # {
            #     "type": "Form",
            #     "name": "form",
            #     "class": "pull-right margina form-inline",
            #     "elements": [

            #         {
            #             "type": "Filter",
            #             "name": "Filter",
            #             "reducers": ["filter"]
            #         }
            #     ]
            # },
             {
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
                        "width": "10%"
                    },{
                        "key": "output",
                        "label": "Output",
                        "width": "90%"
                    }
                    #, {
                    #     "key": "action",
                    #     "label": "Actions",
                    #     "width": "5%"
                    # }
                    ],
                    "panels": {
                        "view_graph": "monitoring.graph",
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
