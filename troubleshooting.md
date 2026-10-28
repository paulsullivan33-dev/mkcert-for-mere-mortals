# Troubleshooting

Organised the way chapter 2 promised: by
the part that is wrong — the name, the
trust, the road between, the store, the
tool talking about all of them. Every
entry below was met for real in the lab.

## "Unable to get local issuer certificate" — trust

curl exit 60 with that sentence, OpenSSL's
`Verify return code: 21`, Python's
`CERTIFICATE_VERIFY_FAILED … unable to get
local issuer certificate`. The certificate
is probably fine; the client does not
know your root. Three checks, in order:
is the root in the store *this client*
reads (chapter 5's listing); if the client
takes a file, is it being handed
`rootCA.pem` from the CAROOT you think it
is (`mkcert -CAROOT` — more than one CA
can exist across folders and users); and
is the leaf actually signed by that root —
chapter 6, compare the leaf's **issuer**
with the root's **subject**. Do not reach
for `-k`: it silences this and every real
alarm with it.

## "No alternative certificate subject name matches" — the name

Also exit 60, entirely different disease
(chapter 9 has both transcripts side by
side). The client *trusts* the root and
*rejects the name*: the name requested is
not in the certificate's SAN list, or a
wildcard was asked to stretch a second
level (`deep.api.example.test` against
`*.example.test`). Read the SANs (chapter
6), compare letter by letter with the
requested name — remember addresses and
names are different kinds of SAN, so
asking by `127.0.0.1` for a certificate
naming only `localhost` fails here too —
and reissue with the full set of names in
one command.

## The warning that will not go away

Every `mkcert` run keeps printing *the
local CA is not installed in the Firefox
and/or Chrome/Chromium trust store* — yet
you installed, and clients are being
served. In the lab this persisted after a
proved install: mkcert decides that
warning by looking for *browser trust
stores it recognises* — Firefox profiles
above all — and the lab's fenced `HOME`
had none to find, even though the root
sat in the NSS database it had just
written (the full exchange is transcript
`t02`). The warning reports what mkcert
could *see*, not what is true. Believe
the store's own listing (`certutil -L`)
and a client's actual verification over
the warning; on a machine with a real
Firefox profile present, the warning
clears when the root reaches that
profile's store.

## `-install` ends in an error, but the root got in

The lab's install exited 1 on a
*read-only database* error from
`/etc/pki/nssdb` — a system NSS store
mkcert attempts when running as root —
*after* succeeding in the user's own
store. A multi-store tool can fail in one
store and succeed in another, and the
exit code testifies only about the
failure. After any `-install` error,
list the stores you actually use before
retrying or concluding anything; and if
you run as root on Linux, know that
`/etc/pki/nssdb` exists and may be the
one complaining. The companion case on a
normal machine: a store mkcert cannot
write without privileges asks for sudo —
decline it, and you have installed into
the remaining stores only.

## An environment variable a client ignores

OpenSSL programs are widely documented to
honour `SSL_CERT_FILE` — point it at a CA
file and verification uses it. In the
lab, curl 8.5 did not:

```text
$ SSL_CERT_FILE=$CAROOT/rootCA.pem curl -sS --resolve example.test:18443:127.0.0.1 https://example.test:18443/
curl: (60) SSL certificate problem: unable to get local issuer certificate
```

The identical file succeeded one command
earlier via `--cacert` (transcript `t06`
keeps both). Whether a build of a client
consults that variable — its compiled-in
CA path can take precedence — is a fact
about the build, not about your
certificate. When an env-var route fails,
test the same file through the client's
explicit option before doubting the root.

## The client went to the wrong machine entirely

The lab's Python client, handed the root
and the right port, failed with
`Connection reset by peer` — no TLS error
at all. The trail (transcript `t06`):

```text
$ getent hosts example.test
198.18.130.179  example.test
```

The lab machine's DNS *answered* for the
`.test` name, with an address belonging
to the sandbox's network interception —
a machine that is not the lab server and
owes the client nothing. curl never fell
for it because every lab request carried
`--resolve`; the Python run trusted DNS
and drove off the map. On your own
machine the equivalent is a missing or
stale `/etc/hosts` line: the name
resolves somewhere that is not your
server, and the resulting error speaks
of connections, not certificates. When
the failure is not a certificate error,
check the resolution (`getent`, `ping`)
before the certificates — chapter 7's
plumbing point, learned the hard way so
the chapter could be written calmly.

## It worked yesterday; the certificate expired

The leaf's term is two years and three
months (chapter 6), and servers present
an expired certificate as faithfully as a
fresh one; clients refuse with an expiry
error that names the cause. The fix is
chapter 12's renewal recipe — reissue
with the same command, restart the
server, delete the old pair. If the
*root* has expired — ten years is a long
development project — the remedy is
chapter 11 whole: new CA, install,
reissue every leaf.
