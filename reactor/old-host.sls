existing-to-backup:
  local.state.apply:
    - tgt: '*'
    - name: base.backup
