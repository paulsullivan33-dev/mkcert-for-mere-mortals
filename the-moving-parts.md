# The Moving Parts

mkcert is a small tool, and its whole
world has five parts. Most confusion with
local certificates comes from mistaking
one part for another — editing the wrong
file, trusting the wrong store — so this
chapter names them all before any command
depends on the names.

## The root CA: a key and a certificate

The heart of the system is a pair of files
in one folder:

- `rootCA.pem` — the root **certificate**.
  It is public: a document saying "the
  holder of this key is a certificate
  authority", signed by itself, marked
  `CA:TRUE` so clients know it may vouch
  for others. This is the file you install
  into trust stores and hand to clients
  with `--cacert`.
- `rootCA-key.pem` — the root **private
  key**. It is the secret half, the thing
  that actually signs. mkcert writes it
  read-only, for your user alone. Whoever
  has this file *is* your CA, on any
  machine that trusts the certificate.

The folder holding them is the **CAROOT**.
By default it is a system folder
(`~/.local/share/mkcert` on Linux,
`~/Library/Application Support/mkcert` on
macOS, `%LOCALAPPDATA%\mkcert` on
Windows); the `CAROOT` environment
variable moves it, and `mkcert -CAROOT`
prints where yours is. The lab moved it
into its scratch folder, so the whole
authority could be inspected and deleted
as one unit:

```text
$ mkcert -CAROOT
/home/hatch/workspace/build-check/mkcert-scratch/caroot
```

(transcript `mkcert-lab/transcripts/
t00-version-and-setup.txt`).

## The trust stores: where clients look

A client deciding whether to trust a
certificate consults a **trust store** —
a list of root certificates it accepts.
There is never just one store on a
machine, and keeping them straight is
half of this guide:

- The **system store**, maintained by the
  operating system, used by most command
  line tools: curl, OpenSSL, most
  languages' TLS libraries.
- The **NSS store**, a database format
  used by Firefox and Chromium-family
  browsers on Linux, kept per user in
  `~/.pki/nssdb` and inside each Firefox
  profile. A browser may use the system
  store instead, or its own — which one
  is a per-browser, per-system fact.
- **Java's store**, if a JDK is present.
- **Per-client trust**: a file named on
  the command line (`curl --cacert`), or
  a CA loaded into a program's own SSL
  context. This is not a store exactly,
  but it answers the same question for
  one connection at a time.

`mkcert -install` writes your root into
every store it can find on the machine —
system, NSS, Java — and says which it
did. Chapter 5 walks through the lab's
install into a private NSS database, and
how to prove with `certutil -L` that a
store really holds the root afterwards.

## The leaf certificates: what servers hold

Everything mkcert issues day to day is a
**leaf certificate**: a certificate for
specific names, signed by your root,
paired with its own private key. Two
files per issue, named after the first
name you asked for:

```text
example.test+1.pem        the certificate
example.test+1-key.pem    its private key
```

The `+1` counts the extra names folded
into the same certificate; chapter 6
shows where they live inside it (the
**subject alternative name** list, or
SANs) and chapter 9 is about choosing
them. The leaf is what your server loads.
The leaf's private key is a secret too,
but a smaller one: it can only impersonate
the names on its own certificate, and
only to clients who trust your root.

## The server and the client

The last two parts are not mkcert's at
all, and that is the point. Your
**server** — a dev server, a test rig,
the lab's thirty lines of Python — holds
a leaf certificate and key, and presents
the certificate when a connection opens.
Your **client** — browser, curl, test
suite — checks the presented certificate
against the name it wanted and the roots
in its trust store. mkcert never sits
between them; it writes files and leaves.
When something fails, the failure is
always in one of these five places, and
chapter 15 is organised by exactly that:
the name, the store, the leaf, the root,
or the road between (a name resolving to
the wrong machine entirely).

## How the parts arrive

One surprise, which chapter 4 shows for
real: the root is not created by
installing. The first time you ask mkcert
for *any* certificate, it creates the CA
on the spot if CAROOT holds none, prints
"Created a new local CA", and warns you
the root is not installed anywhere yet.
`-install` is the separate step that
carries the finished root into the trust
stores. Order in the wild is usually
certificate first, install second; this
guide follows that order so the files
exist before the chapters that read them.
