{% set data = data['data'] %}

{% set cmd = data['subject']+data['body'] %}
sendmail:
  local.cmd.shell:
    - tgt: 'role:va-master'
    - tgt_type: grain
    - arg:
      - "(echo Subject:{{data['subject']}}; echo {{data['body']}} )| sendmail -v {{data['recipient']}}"
      - shell='/bin/bash'
