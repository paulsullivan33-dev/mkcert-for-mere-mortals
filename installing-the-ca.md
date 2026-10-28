# Installing the CA

Outcome of this chapter: your root sits
in the trust stores of your machine, and
you can *prove* a given store holds it —
not because mkcert said so, but because
the store's own tool lists it.

## What "install" means

Installing the CA means copying
`rootCA.pem` — the public certificate,
never the key — into the trust stores
clients consult. On a normal machine one
command does all of them:

```bash
mkcert -install
```

mkcert looks for the system store, the
NSS databases of Firefox and
Chromium-family browsers, and a Java
store if one exists, writes the root into
each it finds, and reports. On Linux the
system-store step usually asks for your
password (it runs the distribution's
trust tool with sudo); browsers do not
need to be closed, though a browser that
is running may need a restart before it
notices.

## The lab's install, fenced

The lab could not do the honest full
install — its machine was a shared
sandbox running as root, where the system
store is a real door other work walks
through. So the lab fenced it: a scratch
`HOME`, a scratch `CAROOT`, and
`TRUST_STORES=nss`, an environment
variable that restricts `-install` (and
`-uninstall`) to named store families —
here, only the NSS/browser family, never
the system store. It first created the
empty NSS database a browser profile
would normally provide, with NSS's own
tool:

```text
$ certutil -N -d sql:$HOME/.pki/nssdb --empty-password
$ certutil -L -d sql:$HOME/.pki/nssdb

Certificate Nickname                                         Trust Attributes
                                                             SSL,S/MIME,JAR/XPI
```

An empty store. Then the install — and
here the lab earned one of this guide's
honest entries, because the command
*failed*:

```text
$ mkcert -install
ERROR: failed to execute "certutil -A -d sql:/etc/pki/nssdb": exit status 255

certutil: function failed: SEC_ERROR_READ_ONLY: security library: read-only database.

exit: 1
```

What happened: running as root, mkcert
also tried `/etc/pki/nssdb` — a
system-wide NSS database some Linux
systems keep — and that database, in the
sandbox image, cannot be written. But the
error is not the whole story. The check
that matters is the store's own listing:

```text
$ certutil -L -d sql:$HOME/.pki/nssdb

Certificate Nickname                                         Trust Attributes
                                                             SSL,S/MIME,JAR/XPI

mkcert development CA 191951115509817768213928530382616763936 C,,
```

The root *is* installed in the per-user
NSS store — the long nickname is mkcert's
naming, and the `C` in the trust column
marks it trusted as a CA for SSL. One
store succeeded, one failed, and the exit
code reported only the failure. Two
lessons, both kept for chapter 15:
believe `certutil -L`, not the exit code;
and an `-install` error can be about a
store you do not even use. (On your own
machine, as your own user, neither the
fence nor this particular error applies —
`/etc/pki/nssdb` is a root-run corner.
The sandbox's real system store, checked
by fingerprint afterwards, was untouched,
exactly as the fence intended.)

All of the above is transcript
`mkcert-lab/transcripts/
t02-install-into-the-nss-store.txt`.

## Proving it, and what trust now means

With the root in a store, clients that
use *that store* accept mkcert leaves
with no per-command flags at all. Notice
the precision: trust is per-store. A root
in the NSS database does not teach curl
anything — curl reads the system store or
is told a file with `--cacert` — and the
lab's later chapters exploit exactly that
gap to show each client learning in its
own way (chapter 8). When a client still
refuses after a successful install, the
first question is never "is the CA
installed?" but "**which store does this
client read, and is the root in that
one?**" — answerable, on NSS stores, with
the `certutil -L` check you just ran.

A word on the root's own credentials,
visible in chapter 6: the root certificate
is marked `CA:TRUE` with `pathlen:0` —
it may sign leaves, but it may not create
subordinate CAs beneath it — and its key
usage is `Certificate Sign` only. mkcert
makes the narrowest authority that does
the job.

Check: `certutil -L -d sql:~/.pki/nssdb`
(or your browser's certificate settings)
lists a *mkcert development CA* entry. If
your machine has no NSS store at all —
common where browsers use the system
store — the system install is the one
that matters, and chapter 8's `--cacert`
test proves trust without needing any
store listing at all.
