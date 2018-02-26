panels = {
    "owncloud.overview": {
        "title": "Overview",
        "tbl_source": {
            "table_chkf": {
                "source": "panel_check_functionality"
            },
            "table_plugins": {
                "source": "panel_plugins"
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
            "name": "table_plugins",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "plugin",
                "label": "App / Version",
                "width": "30%"
            }, {
                "key": "status",
                "label": "Status"
            }
            ],
            "id": ["status"],
            "source": "panel_plugins"
        }, {
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
    "owncloud.users": {
        "title": "Users",
        "tbl_source": {
            "table_users": {
                "source": "panel_list_users"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_users",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "username",
                "label": "Username"
            }, {
                "key": "name",
                "label": "Name",
            }, {
                "key": "lastlogin",
                "label": "Last Login"
            }
            ],
            "id": ["username"],
            "source": "panel_list_users"
        }
        ]
    },
    "owncloud.quotas": {
        "title": "Quotas",
        "tbl_source": {
            "table_quota": {
                "source": "panel_quota"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_quota",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "displayname",
                "label": "Name",
            }, {
                "key": "enabled",
                "label": "Enabled"
            }, {
                "key": "used",
                "label": "Used space"
            }, {
                "key": "total",
                "label": "Quota"
            }
            ],
            "id": ["displayname"],
            "source": "panel_quota"
        }
        ]
    },
    "owncloud.shares": {
        "title": "Shares by Admin",
        "tbl_source": {
            "table_shares": {
                "source": "panel_shares"
            }
        },
        "content": [{
            "type": "Table",
            "name": "table_shares",
            "reducers": ["table", "panel", "alert"],
            "columns": [{
                "key": "path",
                "label": "Path"
            }, {
                "key": "expiration",
                "label": "Expire"
            }, {
                "key": "item_type",
                "label": "Type"
            }, {
                "key": "share_with",
                "label": "Shared with"
            }
            ],
            "id": ["displayname"],
            "source": "panel_shares"
        }
        ]
    }
}
