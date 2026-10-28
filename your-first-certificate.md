# Your First Certificate

Outcome of this chapter: a certificate
and key for a name of your choosing, and —
created along the way, whether you asked
for it or not — the local CA itself.

## One command

Ask for a certificate by the name you
want to use. The lab asked for a test
hostname, `devbox.test`, in an empty
folder on a machine where mkcert had
never run:

```text
$ mkcert devbox.test
Created a new local CA 💥
Note: the local CA is not installed in the Firefox and/or Chrome/Chromium trust store.
Run "mkcert -install" for certificates to be trusted automatically ⚠️

Created a new certificate valid for the following names 📜
 - "devbox.test"

The certificate is at "./devbox.test.pem" and the key at "./devbox.test-key.pem" ✅

It will expire on 28 January 2029 🗓
```

(from `mkcert-lab/transcripts/
t01-first-cert-creates-the-ca.txt`).

Three things happened in that one run,
and separating them is most of learning
this tool:

1. **The CA was born.** CAROOT held no
   root, so mkcert made one — "Created a
   new local CA" — before it could sign
   anything. This happens exactly once in
   the life of a CAROOT; every later run
   finds the root waiting.
2. **The leaf was issued.** Two files in
   the *current* folder — certificates are
   written where you stand, not into
   CAROOT: `devbox.test.pem` and
   `devbox.test-key.pem`, the key readable
   only by its owner.
3. **A warning was served.** The root is
   not installed in any trust store yet,
   so no client will accept the new
   certificate without being told to.
   mkcert says so immediately, and keeps
   saying so on later runs until it finds
   a browser store it recognises — a
   detail that becomes a troubleshooting
   entry in chapter 15, because in the
   lab the warning outlived the install.

## The files, afterwards

```text
$ ls -la $CAROOT .
.:
-rw------- 1 root root 1708 devbox.test-key.pem
-rw-r--r-- 1 root root 1468 devbox.test.pem

/home/hatch/workspace/build-check/mkcert-scratch/caroot:
-r-------- 1 root root 2484 rootCA-key.pem
-rw-r--r-- 1 root root 1639 rootCA.pem
```

Read the permissions as part of the
design: private keys (`*-key.pem`, and
`rootCA-key.pem` above all) are locked to
the owner; certificates are ordinary
files, because certificates are public
documents — the secrecy lives entirely in
the keys.

The expiry line deserves a second look,
too. The certificate was made on 28
October 2026 and expires 28 January 2029:
a life of **two years and three months**.
That is mkcert's fixed term for leaves —
long enough to forget about, short enough
to matter eventually. There is no renewal
command because renewal is just issuing
again: run the same command when the date
approaches and hand the server the fresh
files. Chapter 6 confirms the term from
inside the certificate, and the root's
own, longer one.

Check: your folder holds a `.pem` and a
`-key.pem` named after your name, and
CAROOT now holds `rootCA.pem` and
`rootCA-key.pem`. Next, the step that
makes any of it useful: carrying the root
into the trust stores.
