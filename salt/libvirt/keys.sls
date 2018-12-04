gnutls-bin:
  pkg.installed: []

python-libvirt:
  pkg.installed: []


/etc/pki/CA:
  file.directory

/etc/pki/libvirt:
  file.directory

libvirt_keys:
  virt.keys:
    - expiration_days: 3650
