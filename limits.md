# Limits

What mkcert cannot do, and what it must
not be asked to do — the chapter the rest
of the guide has been promising.

## Development only, and that is structural

No machine you do not administer trusts
your root. That is not a licensing limit
or a missing feature; it is the whole
design. A certificate from your CA is
therefore **meaningless on the public
internet** — not weaker, not second-class,
simply unrecognised — and "make my site
trusted by visitors" is not a job mkcert
can be pointed at. Chapter 13's public
system exists for that. Everything in
this guide works because the set of
machines that must trust the certificate
and the set of machines you own are the
same set. The day those sets drift apart,
you have outgrown the tool.

## The root key is a master key

Chapter 1's rule, in its operational
form. While your root is installed on a
machine, **any certificate signed by your
root key is trusted there, for any name**
— a development site, or a perfect copy
of a bank's. The key sits in a folder on
disk, protected by file permissions
alone: no passphrase, no hardware token,
no audit log of what it has signed. That
is proportionate for one developer's
machine and would be negligent anywhere
the key's compromise hurts anyone else.
Three consequences, stated plainly:

- **Never share a CAROOT.** Not with a
  colleague, not in a repo, not in a
  backup that leaves your control. Each
  person makes their own; it takes a
  minute (chapter 12's recipe is about
  *your own* machines).
- **A suspected leak has no remedy but
  replacement.** There is no revocation
  list for a local CA that clients check;
  chapter 11 — uninstall everywhere,
  delete the key, start again — is the
  entire incident response.
- **Uninstalling is hygiene.** A root you
  no longer use, still installed, still
  signs for whoever holds the key. Remove
  what you are not using.

## Trust is per store, per client, forever

The guide's recurring friction is a
limit, not a bug: there is no single
"the machine trusts it". System, NSS,
Java, per-browser and per-program stores
each hold their own list; some clients
(Node, some language runtimes, anything
statically shipped with its own bundle)
read a store `-install` does not write
to, and for those the answer is
chapter 8's explicit routes — a flag, an
environment they honour, a context in
code. mkcert shortens the list of stores
you must visit; it cannot abolish the
plural.

## The names have edges too

The reserved and the routine: mkcert
issues happily for names that will never
resolve usefully (a typo is a valid SAN),
for public names you do not own — the
certificate is real and useless, since
the name resolves to someone else's
server, which will not hold your key —
and for IP addresses, which it treats as
names of another kind (chapter 9).
Certificates for **bare public IPs** and
other exotic subjects belong to the
public system. And the terms are fixed:
leaves live two years and three months,
roots ten years, and neither duration is
configurable — if that arithmetic does
not fit a use, the use belongs to
chapter 13's grown-up CAs, whose
short-lived certificates are a feature
mkcert deliberately does not copy.

## What is not verified here

The lab ran one machine, no graphical
browser, no second device. The Windows
and macOS system stores, the click path
through Firefox's own settings, carrying
a CA to a phone, and Java's keystore
route are all described from the
project's and vendors' documentation —
real procedures, honestly labelled, but
not transcripts in this guide. Where a
reader's machine differs from the lab's,
the invariants that transfer are the
ones chapter 6 teaches: read the
certificate, list the store, and believe
those two documents over any tool's
summary of them — including mkcert's.
