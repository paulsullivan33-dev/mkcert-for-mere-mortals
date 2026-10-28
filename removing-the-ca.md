# Removing the CA

Outcome of this chapter: a CA fully
retired — trust removed from the stores,
*and* the root key destroyed — and a
clear view of why those are two steps,
not one.

## What `-uninstall` does

`-uninstall` reverses chapter 5: it
visits the same trust stores `-install`
wrote to and removes your root from each.
The lab's run, against its fenced NSS
store (transcript `mkcert-lab/
transcripts/
t08-uninstall-and-what-remains.txt`):

```text
$ mkcert -uninstall
The local CA is now uninstalled from the Firefox and/or Chrome/Chromium trust store(s)! 👋

$ certutil -L -d sql:$HOME/.pki/nssdb

Certificate Nickname                                         Trust Attributes
                                                             SSL,S/MIME,JAR/XPI
```

The store is empty again, proved the same
way the install was proved — with the
store's own listing, not the tool's
farewell. Anything reading that store is
back to refusing your leaves, which is
the state a borrowed or retired machine
should be left in.

## What it deliberately leaves

Now the catch, and it is the most
important operational fact in this guide.
Look at CAROOT afterwards:

```text
$ ls -la $CAROOT
-r-------- 1 root root 2484 rootCA-key.pem
-rw-r--r-- 1 root root 1639 rootCA.pem
```

**The CA itself is untouched.**
`-uninstall`'s own help text says it —
"Uninstall the local CA (but do not
delete it)" — and the reason is sound:
you might want the same root again
tomorrow, on this machine or carried to
another of yours (chapter 12), and
re-installing is one command while
re-creating means re-teaching every
client and re-issuing every leaf. But the
consequence must be understood, and the
lab demonstrated it in the same breath.
Immediately after uninstalling, this
still worked:

```text
$ curl -sS --cacert $CAROOT/rootCA.pem --resolve example.test:18443:127.0.0.1 https://example.test:18443/
Hello from the mkcert lab server.
```

Of course it did: `--cacert` does not
consult a store, it reads the file, and
the file — and its key, and therefore the
authority — still exist. Uninstall
removes *ambient* trust (stores, and the
clients that read them). It does not
retire the CA.

## Retiring it for real

Full removal is therefore two steps:

1. `mkcert -uninstall` — out of the
   stores.
2. **Delete the CAROOT folder** — the
   only copy of `rootCA-key.pem`. This
   is the moment the authority actually
   dies: certificates it signed become
   unverifiable history, and no one,
   including you, can mint new ones that
   existing stores would have trusted.

Do them in that order (delete first and
`-uninstall` can no longer find the root
it is meant to remove — a hungover store
entry for a key that no longer exists is
harmless but untidy, and must then be
removed with the store's own tools, like
`certutil -D`). After both steps, a
hunted-down check — `certutil -L`, the
system store's listing, a `curl` that
used to work — confirms the machine has
forgotten your CA entirely.

When is full retirement right? When a
machine leaves your hands; when a
project ends and its lab is archived;
when the root key may have been copied
somewhere it should not be — there is no
revocation story for a local CA
(chapter 14), so a suspected leak has
exactly one remedy, and it is this
chapter: uninstall everywhere it was
installed, delete the key, make a fresh
CA, re-issue the leaves. Ten minutes,
and the old root is a dead letter
everywhere you control — which, for this
tool, is everywhere that ever trusted it.

Check: after both steps, yesterday's
successful curl fails with chapter 8's
issuer error again, and `mkcert -CAROOT`
points at a folder that is gone. The
test suite that needs the CA will be the
first to tell you it worked.
