gnutls-bin:
  pkg.installed: []

python-libvirt:
  pkg.installed: []


/etc/pki/CA:
  file.directory:
   - makedirs: True

/etc/pki/libvirt:
  file.directory:
    - makedirs: True

libvirt_keys:
  virt.keys:
    - expiration_days: 3650
