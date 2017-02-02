existing-to-backup:
  local.state.apply:
    - tgt: '*'
    - name: base.backup
existing-to-monitoring:
  local.state.apply:
    - tgt: '*'
    - name: base.nrpe
