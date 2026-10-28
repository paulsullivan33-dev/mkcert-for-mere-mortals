# Glossary

**CAROOT** — the folder holding the root
CA's two files. Printed by `mkcert
-CAROOT`, moved by the `CAROOT`
environment variable (chapters 2, 4).

**Certificate** — a signed document
binding a public key to names (the SAN
list), an issuer, a usage and a pair of
dates (chapter 6).

**Certificate authority (CA)** — a key
and certificate entitled — by the
`CA:TRUE` marker — to sign other
certificates. mkcert makes a small,
local one (chapter 1).

**Client certificate** — a certificate a
client presents to prove itself, issued
with `mkcert -client` (chapter 10).

**Extended key usage** — the certificate
field saying what the certificate may be
used for: serving, client authentication,
or both (chapters 6, 10).

**Fingerprint** — a short hash naming a
certificate uniquely, used to compare a
root between machines without comparing
the whole file (chapter 6).

**Leaf certificate** — a certificate for
specific names, signed by a root, held
by a server (or client). Everything
mkcert issues day to day (chapter 2).

**NSS store** — the certificate database
format used by Firefox and Chromium on
Linux, kept in `~/.pki/nssdb` and in each
Firefox profile, and listed with
`certutil -L` (chapter 5).

**PKCS #12 (`.p12`, `.pfx`)** — a single
password-wrapped file bundling a
certificate with its private key, for
tools that import that shape (chapter 10).

**Private key** — the secret half of a
key pair. The root's key *is* the CA;
a leaf's key lets its holder impersonate
the leaf's names to trusting clients
(chapter 2).

**Root certificate** — the self-signed
top of a chain: subject and issuer
identical, trusted because it was
installed, not because anyone vouched
for it (chapter 6).

**Self-signed certificate** — a
certificate whose issuer is itself,
signed with no authority behind it.
Roots are self-signed by nature; a
server certificate that is self-signed
is what clients refuse (chapter 1).

**Subject alternative name (SAN)** — the
list inside a certificate of the names
and addresses it answers for; the only
name list modern clients consult
(chapters 6, 9).

**Trust store** — a client's list of
accepted root certificates: system, NSS,
Java, or a program's own. Trust is
always per-store (chapters 2, 5, 8).

**Wildcard** — a SAN of the form
`*.example.test`, matching any one label
in that position, and only one
(chapter 9).
