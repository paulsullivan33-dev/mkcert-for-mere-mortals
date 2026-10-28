# The Neighbours

mkcert is one answer to "my client will
not trust my server". These are the
others, characterised — not benchmarked —
from their documentation, with the line
where each takes over from this guide.

## Let's Encrypt, and the servers that fetch from it

The public answer. **Let's Encrypt** is
a real CA, trusted everywhere, issuing
free certificates to anyone who proves
they control a **public** domain name.
Servers like Caddy and Traefik automate
the whole exchange — give them a public
name and they fetch, install and renew
certificates by themselves, which is the
subject of this series' *Caddy for Mere
Mortals*. If a name is public, this is
not a neighbour but the correct tool, and
mkcert should not be anywhere near it.
The boundary is exact: Let's Encrypt
cannot and will not issue for `localhost`,
`.test`, or any name only your network
can see — proof of control is the product,
and private names cannot be proved.
Public name, public CA; local name,
mkcert. The two systems never overlap,
which is why this guide can be short
about the respectable half of the world.

## OpenSSL, by hand

Everything mkcert does, `openssl` does
with more typing: generate a root key,
self-sign a root certificate with the
right extensions, write a config naming
the SANs, sign a leaf, track the serials.
This series' *OpenSSL for Mere Mortals*
walks that layer. People reach for it
when they need something mkcert will not
do — unusual extensions, an intermediate
CA (mkcert's root is `pathlen:0` by
design), signing a certificate someone
else keyed. The price is that every one
of chapter 6's fields becomes your
handwriting, and the usual failure is a
certificate that is almost right. mkcert
exists because the common case has a
correct answer and it can simply be
generated.

## A plain self-signed certificate

One command in most toolkits
(`openssl req -x509 …`, a framework's dev
certificate command) and zero installs —
the certificate vouches for itself, so
every client must be told, individually,
to accept it or to stop checking. For a
five-minute experiment on one machine
that is a fair trade. The costs arrive
with the second client and the second
week: warnings to click through, `-k`
flags that leak into scripts, and a team
trained to ignore the alarm. mkcert is
what you graduate to when the experiment
becomes infrastructure; chapter 1's
account of the alarm staying armed is the
argument.

## step-ca and the grown-up CAs

**step-ca** (from Smallstep) is a real,
small certificate authority you run as a
service: it issues short-lived
certificates to machines and people that
enrol and authenticate, with policies,
auditing and renewal as first-class
ideas. It is the honest next step when
"local" grows a team — several people,
several machines joining and leaving,
certificates that should expire in hours
not years. A **private PKI** from a cloud
provider or an enterprise product is the
same idea at organisational scale.
mkcert's position in that family is
precise: one person, files instead of a
service, no enrolment, no revocation —
correct for a desk, wrong for a fleet,
and chapter 14 says so without
embarrassment.

## Your framework's dev certificate

Some toolchains ship their own version of
this idea — `dotnet dev-certs` is the
best-known — creating and trusting a
localhost certificate inside one
ecosystem. Inside that ecosystem it is
frictionless and fine. mkcert generalises
it: any name, any server, any client, one
root for everything on the machine. If
all your local HTTPS lives in one
framework, its built-in may be all you
need; the moment a second stack joins,
one root beats two.
