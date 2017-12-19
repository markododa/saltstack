panel = {
	"owncloud.overview": {
		"title": "Overview",
		"tbl_source": {
			"table_chkf": {
				"action": "panel_check_functionality",
				"cols": ["status", "output"]
			},
			"table_plugins": {
				"action": "panel_plugins",
				"cols": ["plugin", "status"]
			}
		},
		"content": [{
				"type": "Table",
				"name": "table_chkf",
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
						"label": "Plugin name",
						"width": "30%"
					}, {
						"key": "status",
						"label": "Status"
					}
				],
				"id": ["status"],
				"source": "panel_plugins"
			}
		]
	},
	"owncloud.users": {
		"title": "Users",
		"tbl_source": {
			"table_users": {
				"action": "panel_list_users",
				"cols": ["name", "username", "lastlogin"]
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
				"action": "panel_quota",
				"cols": ["displayname", "enabled", "used", "total"]
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
						"label": "Used bytes"
					}, {
						"key": "total",
						"label": "Total bytes"
					}
				],
				"id": ["displayname"],
				"source": "panel_quota"
			}
		]
	},
	"owncloud.shares": {
		"title": "Shares",
		"tbl_source": {
			"table_shares": {
				"action": "panel_shares",
				"cols": ["displayname_owner", "expiration", "file_target", "item_type", "share_with"]
			}
		},
		"content": [{
				"type": "Table",
				"name": "table_shares",
				"reducers": ["table", "panel", "alert"],
				"columns": [{
						"key": "displayname_owner",
						"label": "Share Owner",
					}, {
						"key": "expiration",
						"label": "Expire"
					}, {
						"key": "file_target",
						"label": "Target"
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

