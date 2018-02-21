panels = {
    "directory.users": {
        "title": "Add and view users",
        "tbl_source": {
            "table": {
                "source": "panel_list_users"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [{
                "type": "Button",
                "name": "Add User",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Create an User",
                    "table_name": "table",
                    "refresh_action": "panel_list_users",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add user",
                        "class": "primary",
                        "action": "add_user"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "username",
                            "value": "",
                            "label": "Username",
                            "required": True
                        }, {
                            "type": "password",
                            "name": "password",
                            "value": "",
                            "label": "Password",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "name",
                            "value": "",
                            "label": "First name"
                        }, {
                            "type": "text",
                            "name": "surname",
                            "value": "",
                            "label": "Last name"
                        }, {
                            "type": "text",
                            "name": "email",
                            "value": "",
                            "label": "E-mail"
                        }, {
                            "type": "text",
                            "name": "organizational_unit",
                            "value": "",
                            "label": "Organizational unit"
                        }, {
                            "type": "checkbox",
                            "name": "change_at_next_login",
                            "value": False,
                            "label": "Change password at next login",
                            "required": False
                        }
                        ]
                    }, {
                        "type": "Div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add a new user"
                        }, {
                            "type": "Paragraph",
                            "name": "The new user will be automatically available on all services."
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
            "reducers": ["table", "filter", "panel", "modal", "alert"],
            "source": "panel_list_users",
            "columns": [{
                "key": "username",
                "label": "Username"
            }, {
                "key": "name",
                "label": "Name"
            }, {
                "key": "description",
                "label": "Description"
            }, {
                "key": "flags",
                "label": "Status"
            }, {
                "key": "action",
                "label": "Actions"
            }
            ],
            "id": "username",
            "modals": {
                "edit_user": {
                    "title": "Edit user",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Change",
                        "class": "primary",
                        "action": "get_user_data"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "form_source": {
                            "action": "get_user_data",
                            "positional_args": 1
                        },
                        "elements": [{
                            "type": "text",
                            "name": "first_name",
                            "value": "",
                            "label": "First name",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "last_name",
                            "value": "",
                            "label": "Last name",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "display_name",
                            "value": "",
                            "label": "Display name",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "description",
                            "value": "",
                            "label": "Description",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "physical_delivery_office_name",
                            "value": "",
                            "label": "Office name",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "email",
                            "value": "",
                            "label": "Email address",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "phone",
                            "value": "",
                            "label": "Phone number",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "company",
                            "value": "",
                            "label": "Company",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "profile_path",
                            "value": "",
                            "label": "Roaming profile path",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "script_path",
                            "value": "",
                            "label": "Script path",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "mobile",
                            "value": "",
                            "label": "Mobile phone",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "home_phone",
                            "value": "",
                            "label": "Home phone",
                            "required": False
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to change data for user"
                        }, {
                            "type": "Paragraph",
                            "name": "The changed data for user will be automatically synchronized."
                        }
                        ]
                    }
                    ]
                },
                "change_ou": {
                    "title": "Change organizational unit",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Change",
                        "class": "primary",
                        "action": "change_ou"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "unit",
                            "name": "unit",
                            "value": "",
                            "label": "Organizational unit",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to change data for user"
                        }, {
                            "type": "Paragraph",
                            "name": "The changed data for user will be automatically synchronized."
                        }
                        ]
                    }
                    ]
                },
                "change_password": {
                    "title": "Change user password",
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
                            "type": "password",
                            "name": "Password",
                            "value": "",
                            "label": "Password",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to change data for user"
                        }, {
                            "type": "Paragraph",
                            "name": "The changed data for user will be automatically synchronized."
                        }
                        ]
                    }
                    ]
                },
                "manage_groupsxx": {
                    "title": "Manage groups",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Submit",
                        "class": "primary",
                        "action": "manage_groups"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "label",
                            "name": "Add user to these groups"
                        }, {
                            "type": "multi_checkbox",
                            "name": "info",
                            "value": False,
                            "label": "Info",
                            "required": False
                        }, {
                            "type": "multi_checkbox",
                            "name": "domain_admins",
                            "value": False,
                            "label": "Domain Admins",
                            "required": False
                        }, {
                            "type": "multi_checkbox",
                            "name": "support",
                            "value": False,
                            "label": "Support",
                            "required": False
                        }, {
                            "type": "multi_checkbox",
                            "name": "sales",
                            "value": False,
                            "label": "Sales",
                            "required": False
                        }, {
                            "type": "multi_checkbox",
                            "name": "dev",
                            "value": False,
                            "label": "Dev",
                            "required": False
                        }, {
                            "type": "multi_checkbox",
                            "name": "remote",
                            "value": False,
                            "label": "Remote Desktop Users",
                            "required": False
                        }, {
                            "type": "label",
                            "name": "Remove user from these groups"
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Manage groups for user : "
                        }
                        ]
                    }
                    ]
                }
            },
            "panels": {
                "list_logins": "directory.list_logins",
                "manage_user_membership": "directory.manage_user_membership"
            },
            "actions": [{
                        "name": "Edit user",
                        "action": "edit_user"
                        }, {
                        "name": "Change password",
                        "action": "change_password"
                        }, {
                        "name": "Delete user",
                        "class": "danger",
                        "action": "delete_user"
                        }, {
                        "name": "Disable user",
                        "class": "danger",
                        "action": "disable_user"
                        }, {
                        "name": "Enable user",
                        "action": "enable_user"
                        }, {
                        "name": "Unlock user",
                        "action": "unlock_user"
                        }, {
                        #		"name": "List logins",
                        #		"action": "list_logins"
                        #	}, {
                        "name": "Manage groups",
                        "action": "manage_user_membership"
                        }, {
                        "name": "Change org. unit",
                        "action": "change_ou"
                        }
                        ]
        }
        ]
    },
    "directory.groups": {
        "title": "All groups",
        "tbl_source": {
            "table": {
                "source": "panel_get_groups"
            },
            "table2": {
                "source": "panel_get_groups"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [{
                "type": "Button",
                "name": "Add group",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "refresh_action": "panel_get_groups",
                    "title": "Add a new group",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add group",
                        "class": "primary",
                        "action": "add_group"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "Groupname",
                            "value": "",
                            "label": "Group name",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add a new group"
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
            "reducers": ["table", "filter", "panel", "alert"],
            "columns": [{
                "key": "groupname",
                "label": "Group name"
            }, {
                "key": "description",
                "label": "Description"
            }, {
                "key": "email",
                "label": "E-mail",
                "width": "15%"
            }, {
                "key": "action",
                "label": "Actions"
            }
            ],
            "panels": {
                "list_group_members": "directory.list_group_members"
            },
            "actions": [{
                        "name": "Edit members",
                        "action": "list_group_members"
                        }, {
                        "name": "Edit e-mail",
                        "action": "edit_group_mail"
                        }, {
                        "name": "Edit description",
                        "action": "edit_group_description"
                        }, {
                        "name": "Delete group",
                        "class": "danger",
                        "action": "delete_group"
                        }
                        ],
            "id": "groupname",
            "source": "panel_get_groups"
        }, {
            "type": "Button",
            "name": "View more",
            "action": "show",
            "target": "div2",
            "reducers": ["div"]
        }, {
            "type": "Div",
            "name": "div2",
            "class": "hidden",
            "reducers": ["div"],
            "elements": [{
                "type": "Form",
                "name": "form2",
                "class": "tbl-ctrl",
                "elements": [{
                    "type": "Button",
                    "name": "Add group",
                    "glyph": "plus",
                    "action": "modal",
                    "reducers": ["modal"],
                    "modal": {
                        "title": "Add a new group",
                        "buttons": [{
                            "type": "Button",
                            "name": "Cancel",
                            "action": "cancel"
                        }, {
                            "type": "Button",
                            "name": "Add group",
                            "class": "primary",
                            "action": "add_group"
                        }
                        ],
                        "content": [{
                            "type": "Form",
                            "name": "form",
                            "class": "left",
                            "elements": [{
                                "type": "text",
                                "name": "Groupname",
                                "value": "",
                                "label": "Group name",
                                "required": True
                            }
                            ]
                        }, {
                            "type": "Div",
                            "name": "div",
                            "class": "right",
                            "elements": [{
                                "type": "Heading",
                                "name": "Fill the form to add a new group"
                            }, {
                                "type": "Paragraph",
                                "name": "Add some users later in the new group."
                            }
                            ]
                        }
                        ]
                    }
                }
                ]
            }, {
                "type": "Table",
                "name": "table2",
                "reducers": ["table", "filter", "panel", "alert"],
                "columns": [{
                    "key": "groupname",
                    "label": "Name"
                }, {
                    "key": "description",
                    "label": "Description"
                }, {
                    "key": "email",
                    "label": "E-mail",
                    "width": "10%"
                }, {
                    "key": "action",
                    "label": "Actions"
                }
                ],
                "actions": [{
                    "name": "List Members",
                    "action": "list_group_members"
                }, {
                    "name": "Delete group",
                    "class": "danger",
                    "action": "delete_group"
                }
                ],
                "id": "groupname",
                "source": "panel_get_groups"
            }
            ]
        }
        ]
    },
    "directory.dns": {
        "title": "DNS records",
        "tbl_source": {
            "table": {
                "source": "list_dns"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [{
                "type": "Button",
                "name": "Add A or AAAA",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal", "alert"],
                "modal": {
                    "title": "Add Host (A or AAAA)",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add record",
                        "class": "primary",
                        "action": "action_add_dns"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "entry_name",
                            "value": "",
                            "label": "Record name",
                            "required": False
                        }, {
                            "type": "dropdown",
                            "name": "entry_type",
                            "values": ["A", "AAAA"],
                            "label": "Type",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "entry_data",
                            "value": "",
                            "label": "IP Address",
                            "required": False
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add record"
                        }, {
                            "type": "Paragraph",
                            "name": "For type A use IPv4, for AAAA use IPv6."
                        }
                        ]
                    }
                    ]
                }
            }, {
                "type": "Button",
                "name": "Add CNAME",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal", "alert"],
                "modal": {
                    "title": "Add Alias (CNAME)",
                    "kwargs": {"entry_type": "CNAME"},
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add record",
                        "class": "primary",
                        "action": "action_add_dns"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "entry_name",
                            "value": "",
                            "label": "Alias",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "entry_data",
                            "value": "",
                            "label": "Hostname",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add record"
                        }, {
                            "type": "Paragraph",
                            "name": "Enter hostname for the Alias record."
                        }
                        ]
                    }
                    ]
                }
            }, {
                "type": "Button",
                "name": "Add MX",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal", "alert"],
                "modal": {
                    "title": "Add MX record",
                    "kwargs": {"entry_type": "MX"},
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add record",
                        "class": "primary",
                        "action": "action_add_dns"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "entry_name",
                            "value": "",
                            "label": "Record name",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "entry_data",
                            "value": "",
                            "label": "Hostname and Priority",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add record"
                        }, {
                            "type": "Paragraph",
                            "name": "Enter the host name of the mail server and priority (separated with space)."
                        }
                        ]
                    }
                    ]
                }
            }, {
                "type": "Button",
                "name": "Add NS",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal", "alert"],
                "modal": {
                    "title": "Add Name Server (NS record)",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add record",
                        "class": "primary",
                        "action": "action_add_dns"
                    }
                    ],
                    "kwargs": {"entry_name": "","entry_type": "NS"},
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "entry_data",
                            "value": "",
                            "label": "Record name",
                            "required": False
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add record"
                        }, {
                            "type": "Paragraph",
                            "name": "Enter the host name of the new DNS server."
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
            "reducers": ["table", "filter", "panel", "modal", "alert", "form"],
            "columns": [{
                "key": "group_name",
                "label": "Record"
            }, {
                "key": "type",
                "label": "Type"
            }, {
                "key": "value",
                "label": "Value"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "10%"
            }
            ],
            "modals": {
                "edit_entry": {
                    "title": "Edit DNS record",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Update record",
                        "class": "primary",
                        "action": "dns_update"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "reducers": ["form"],
                        "elements": [{
                            "type": "readonly_text",
                            "name": "Entryname",
                            "value": "",
                            "label": "Entry name",
                            "required": False
                        }, {
                            "type": "readonly_text",
                            "name": "Type",
                            "value": "",
                            "label": "Type",
                            "required": False
                        }, {
                            "type": "text",
                            "name": "Address",
                            "value": "",
                            "label": "Address",
                            "required": False
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Edit the form to update DNS record"
                        }, {
                            "type": "Paragraph",
                            "name": "If you leave a blank value, it will not change - the old value will be used."
                        }
                        ]
                    }
                    ]
                }
            },
            "readonly": {
                "group_name": "Entryname",
                "type": "Type"
            },
            "actions": [{
                        "name": "Edit record",
                        "action": "update_dns_entry"
                        }, {
                        "name": "Delete record",
                        "class": "danger",
                        "action": "action_rm_dns"
                        }
                        ],
            "id": ["group_name", "type", "value"],
            "source": "list_dns"
        }
        ]
    },
    "directory.org_units": {
        "title": "Organizational units",
        "tbl_source": {
            "table": {
                "source": "panel_list_organizational_units"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [{
                "type": "Button",
                "name": "Add organizational unit",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add an organizational unit",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add",
                        "class": "primary",
                        "action": "create_organizational_unit"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "unit",
                            "value": "",
                            "label": "Name",
                            "required": True
                        }, {
                            "type": "text",
                            "name": "description",
                            "value": "",
                            "label": "Description",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Fill the form to add new organizational unit"
                        }, {
                            "type": "Paragraph",
                            "name": "Organizational units helps you orginize items in Active Directory."
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
                    "get_ou_members": "directory.ou_members"
            },
            "columns": [{
                        "key": "name",
                        "label": "Name"
                        }, {
                        "key": "description",
                        "label": "Description",
                        "width": "60%"
                        }, {
                        "key": "action",
                        "label": "Actions"
                        }
                        ],
            "actions": [{
                        "action": "get_ou_members",
                        "name": "List members"
                        }
                        ],
            "id": ["name"]
        }
        ]
    },
    "directory.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality"
            },
            "table_pass": {
                "source": "panel_get_pass_settings"
            },
            "table_info": {
                "source": "panel_get_dc_info"
            },
            "table_fsmo": {
                "source": "panel_fsmo_show"
            },
            "table_gpos": {
                "source": "panel_gpo_polices"
            },
            "table_jpcs": {
                "source": "panel_get_pcs"
            },
            "table_domc": {
                "source": "panel_get_dcs"
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
            }
            ],
            "id": ["status"],
            "source": "va_utils.check_functionality"
        }, {
            "type": "Table",
            "name": "table_info",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "key",
                "label": "Domain info",
                "width": "30%"
            }, {
                "key": "value",
                "label": "Value"
            }
            ],
            "id": ["domain"],
            "source": "panel_get_dc_info"
        }, {
            "type": "Table",
            "name": "table_pass",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "key",
                "label": "Password Setting",
                "width": "30%"
            }, {
                "key": "value",
                "label": "Value"
            }
            ],
            "id": ["domain"],
            "source": "panel_get_pass_settings"
        }, {
            "type": "Table",
            "name": "table_fsmo",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "key",
                "label": "FSMO Role",
                "width": "30%"
            }, {
                "key": "value",
                "label": "Owner"
            }
            ],
            "id": ["domain"],
            "source": "panel_fsmo_show"
        }, {
            "type": "Table",
            "name": "table_levl",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "key",
                "label": "DC Levels",
                "width": "30%"
            }, {
                "key": "value",
                "label": "Value"
            }
            ],
            "id": ["domain"],
            "source": "panel_level_show"
        }, {
            "type": "Table",
            "name": "table_gpos",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "display name",
                "label": "Group Policy",
                "width": "30%"
            }, {
                "key": "gpo",
                "label": "GPO ID"
            }
            ],
            "id": ["domain"],
            "source": "panel_gpo_polices"
        }, {
            "type": "Table",
            "name": "table_domc",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "hostname",
                "label": "Domain Controllers",
                "width": "30%"
            }
            ],
            "id": ["domain"],
            "source": "panel_get_dcs"
        }, {
            "type": "Table",
            "name": "table_jpcs",
            "pagination": False,
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "hostname",
                "label": "Joined Computers"
            }
            ],
            "id": ["domain"],
            "source": "panel_get_pcs"
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
    "directory.list_logins": {
        "title": "Login list",
        "tbl_source": {
            "table": {
                "source": "users_log"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "date",
                "label": "Date"
            }, {
                "key": "computer",
                "label": "Computer"
            }, {
                "key": "address",
                "label": "IP address"
            }
            ],
            "source": "users_log"
        }
        ]
    },
    "directory.list_group_members": {
        "title": "Group members",
        "tbl_source": {
            "table": {
                "source": "panel_list_group_members"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "reducers": ["panel"],
            "elements": [{
                "type": "Button",
                "name": "Add member",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal"],
                "modal": {
                    "title": "Add member",
                    "refresh_action": "panel_list_group_members",
                    "table_name": "table",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "Add",
                        "class": "primary",
                        "action": "add_user_to_group"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "username",
                            "value": "",
                            "label": "Username",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Enter username to be added to this group"
                        }, {
                            "type": "Paragraph",
                            "name": "The changed data for this group will be automatically synchronized."
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
            "columns": [{
                "key": "username",
                "label": "Member"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "20%"
            }
            ],
            "source": "panel_list_group_members",
            "actions": [{
                "action": "remove_from_group",
                "name": "Remove from group",
                "class": "danger"
            }
            ],
            "id": ["username"]
        }
        ]
    },
    "directory.manage_user_membership": {
        "title": "Group membership",
        "tbl_source": {
            "table": {
                "source": "panel_manage_groups"
            }
        },
        "content": [{
            "type": "Form",
            "name": "form",
            "class": "tbl-ctrl",
            "elements": [{
                "type": "Button",
                "name": "Add Group",
                "glyph": "plus",
                "action": "modal",
                "reducers": ["modal", "alert"],
                "modal": {
                    "title": "Add this user to Group",
                    "buttons": [{
                        "type": "Button",
                        "name": "Cancel",
                        "action": "cancel"
                    }, {
                        "type": "Button",
                        "name": "username",
                        "class": "primary",
                        "action": "add_user_to_group"
                    }
                    ],
                    "content": [{
                        "type": "Form",
                        "name": "form",
                        "class": "left",
                        "elements": [{
                            "type": "text",
                            "name": "group",
                            "value": "",
                            "label": "Group name",
                            "required": True
                        }
                        ]
                    }, {
                        "type": "Div",
                        "name": "div",
                        "class": "right",
                        "elements": [{
                            "type": "Heading",
                            "name": "Enter a group to add user to"
                        }, {
                            "type": "Paragraph",
                            "name": "Users can be members in multiple groups."
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
            "columns": [{
                "key": "groupname",
                "label": "Group"
            }, {
                "key": "action",
                "label": "Actions",
                "width": "20%"
            }
            ],
            "actions": [{
                        "action": "xxxxx_rm_user_from_group",
                        "name": "Remove from group"
                        }
                        ],
            "source": "panel_manage_groups",
            "id": "username"
        }
        ]
    },
    "directory.ou_members": {
        "title": "OU Members",
        "tbl_source": {
            "table": {
                "source": "panel_ou_members"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "member",
                "label": "Member"
            }, {
                "key": "type",
                "label": "Type"
            }
            ],
            "source": "panel_ou_members"
        }
        ]
    }
}
