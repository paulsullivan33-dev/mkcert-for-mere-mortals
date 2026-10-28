# mkcert for Mere Mortals

Modern development keeps bumping into a
small, stubborn problem: your code runs on
your own machine, behind **HTTPS** — the
encrypted web protocol — and your browser
or HTTP client refuses to trust it. The
certificate is self-signed, so you get a
warning page, an error 60 from curl, or a
test suite that only works with
verification switched off. **mkcert** is
the honest fix. It creates a small
**certificate authority** (CA) — a root
key and certificate that can sign other
certificates — installs that root into the
trust stores your tools already consult,
and then issues certificates for
`localhost` and your test names that those
tools accept without a murmur and without
`-k`.

This guide explains how that works, how
to issue your first certificate, how to
read what is actually inside one, how to
serve a real local HTTPS site with it and
prove that three different clients trust
it for three different reasons, what
wildcards and IP addresses do to a
certificate, and how to remove the whole
authority when you are done — including
the part `-uninstall` deliberately leaves
behind.

The rule that governs everything here is
the mirror image of the one in the
mitmproxy guide: **a trusted local CA is
a key to every encrypted conversation on
that machine, so it belongs on machines
you own, for names that stay local, and
nowhere else.** mkcert certificates are
for development. They are worthless —
deliberately — anywhere else: no other
machine trusts your root, which is
exactly what makes the arrangement safe
to use and pointless to abuse. Chapter 14
returns to this with the edge cases.

The lab behind this guide ran the real
thing: **mkcert 1.4.4**, the official
binary, exercised end to end in a sandbox
with one deliberate precaution — the
lab's `HOME`, its `CAROOT` (the folder
mkcert keeps the CA in) and its browser
trust store all pointed into a scratch
folder, and installs were restricted to
that store, so nothing outside the lab's
fence was modified. Inside the fence
everything was real: the CA was created,
installed into an NSS trust database and
proved present with `certutil`; certifi-
cates were issued for `localhost`, both
loopback addresses, a test domain and a
wildcard; a small Python HTTPS server
served them; and curl, OpenSSL's
`s_client` and a Python client each
refused the certificates first and
accepted them once they trusted the root.
The failures were kept too: a hostname
mismatch, a wildcard asked to stretch one
level too far, an environment variable
one client quietly ignored, and a name
the lab machine's own DNS answered for
in a way that sent a client somewhere
else entirely.

What the lab could not do, it did not
fake. It had no graphical browser and no
second machine, so clicking through a
browser's certificate settings, the
Windows and macOS trust stores, and
sharing one CA across a workbench of
devices are taught from the documentation
and labelled as such wherever they
appear. `criteria.md` keeps the full
ledger of what was run and what was only
read.

## What this guide covers

- [**What mkcert is**](what-mkcert-is.md) —
  the mental model: why local HTTPS breaks,
  what a certificate authority is, and the
  rule that keeps a powerful tool safe
- [**The moving parts**](the-moving-parts.md) —
  the root CA, the CAROOT folder, the trust
  stores, the leaf certificates, and which
  part a client actually checks
- [**Installing mkcert**](installing-mkcert.md) —
  the single binary, where it comes from,
  and how to confirm it runs
- [**Your first certificate**](your-first-certificate.md) —
  one command, two files, and the moment
  the CA is born — issuing a certificate
  creates the authority first, if it has to
- [**Installing the CA**](installing-the-ca.md) —
  `mkcert -install`: what "trust" means,
  which stores exist, what `CAROOT` and
  `TRUST_STORES` control, and how to prove
  a store really holds your root
- [**Reading a certificate**](reading-a-certificate.md) —
  a guided tour with `openssl x509`:
  subject, issuer, subject alternative
  names, dates, and the difference between
  the root and a leaf
- [**Serving HTTPS locally**](serving-https-locally.md) —
  the lab's small Python server under a
  mkcert certificate, and the name problem:
  `/etc/hosts`, or `--resolve`, but the
  name must reach the machine
- [**Teaching clients to trust**](teaching-clients-to-trust.md) —
  three clients, three mechanisms:
  `--cacert`, a trust store, and an SSL
  context — each first refusing, then
  accepting, the same certificate
- [**Names, wildcards and addresses**](names-and-wildcards.md) —
  what a certificate is *for*: several
  names on one certificate, the one-level
  wildcard rule proven both ways, and IP
  addresses as names
- [**More kinds of certificate**](more-kinds-of-certificate.md) —
  ECDSA keys, PKCS #12 bundles for tools
  that want one file, client certificates,
  and naming the output files yourself
- [**Removing the CA**](removing-the-ca.md) —
  `mkcert -uninstall`, and the honest
  catch: the root key stays in CAROOT
  until you delete it, and anything
  pointed at the root file goes on
  trusting it
- [**Recipes**](recipes.md) — HTTPS for a
  local dev site by name, one CA for the
  whole workbench, certificates for a
  test suite, and a clean slate
- [**The neighbours**](the-neighbours.md) —
  Let's Encrypt and the servers that fetch
  from it automatically, hand-rolled
  OpenSSL self-signed certificates,
  step-ca, and doing nothing at all
- [**Limits**](limits.md) — development
  only, one machine's trust, the root key
  as a liability, no revocation, and the
  names mkcert cannot help with
- [**Troubleshooting**](troubleshooting.md) —
  the warning that will not go away, an
  `-install` error that is not the whole
  story, two exit-60s that look alike and
  are not, and a DNS answer that sent the
  lab's client to the wrong machine
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Certificates for the public internet —
your root is trusted by nobody else's
machine, and chapter 13 explains the real
system (Let's Encrypt and friends) that
exists for that. Running a CA for a team
or an organisation, with enrolment and
audit trails, is pointed at (step-ca) and
not taught. Anything about TLS below the
certificate layer — ciphers, protocol
versions, hardening a public server — is
another guide's country; this one stays
with one person, one machine, and names
that never leave it.

## How to use this guide

Read chapter 1 for the model and the
rule, and chapter 2 before installing
anything — knowing which file is the root
and which store a client consults turns
later confusion into a named problem.
Chapters 4 and 5 both create the CA, in
the order real life usually meets them:
you will probably issue a certificate
first and install the root second.
Chapter 6 is the one to linger on: a
reader who can read a certificate can
diagnose every error in chapter 15
without help. The lab's server and client
scripts live in `mkcert-lab/server/`; its
transcripts live in `mkcert-lab/
transcripts/`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Caddy for Mere Mortals](https://paulsullivan33-dev.github.io/caddy-for-mere-mortals/)
- [OpenSSL for Mere Mortals](https://paulsullivan33-dev.github.io/openssl-for-mere-mortals/)
- [mitmproxy for Mere Mortals](https://paulsullivan33-dev.github.io/mitmproxy-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/mkcert-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/mkcert-for-mere-mortals/blob/main/LICENSE-CODE).
