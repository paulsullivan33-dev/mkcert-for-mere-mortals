# What mkcert Is

When a browser or an HTTP client opens an
**HTTPS** connection, it does not simply
start encrypting. First it asks the server
a question: *who are you, and who says
so?* The server answers with a
**certificate** — a small signed document
that binds a public key to a name, like
`example.com` — and the client checks two
things. Is the name on the certificate
the name I asked for? And is the signature
from a **certificate authority** (CA) I
already trust? If both answers are yes,
the conversation proceeds and you see a
padlock. If either is no, you get the
warning page, or curl's error 60, and the
conversation usually stops.

That system works beautifully for the
public web, where a handful of large CAs
— pre-installed in every operating system
and browser — vouch for everybody. It
works badly at your own desk. Your
development server is called `localhost`,
or `app.example.test`, or it has no public
name at all. No public CA will issue a
certificate for `localhost` — it is not
yours in any way they can check, and it
points at a different machine for every
person on Earth. So developers reach for
the traditional workaround, a **self-signed
certificate** (one program signs its own
document, vouching for itself), and every
client rightly refuses it: the answer to
"who says so?" is "he does". The
workarounds for the workaround are worse:
clicking through warnings, or running
clients with verification off — `curl -k`,
`verify=False` — trains you and your test
suite to ignore the exact alarm that
matters when it is real.

**mkcert removes the problem at the root,
literally.** It creates a small CA of your
own: a **root certificate** and its
private key, generated on your machine.
You install that root once into the
**trust stores** your tools consult — the
operating system's list, your browser's
list — and from then on your machine
treats your CA the way it treats the big
public ones. Then mkcert issues
**leaf certificates** signed by your root,
for whatever local names you name:

```bash
mkcert -install
mkcert localhost 127.0.0.1 example.test
```

Two files appear, a certificate and its
key, ready to hand to your development
server. Clients on your machine check the
name, check the signature against a root
they now trust, and connect quietly. No
warnings, no `-k`, no verification
switched off anywhere — the alarm system
stays armed; you have simply added one
more authority it recognises, and that
authority answers only to you.

## The rule, stated before everything else

A root CA is not a small thing to hold.
Any machine that trusts your root will
accept certificates your root signs for
*any* name — a development site, or a
bank's. That is what makes mkcert useful,
and it is also the entire risk. So this
guide has one rule, and it is not fine
print:

> **Your CA belongs on machines you own,
> signing certificates for names that stay
> local. Guard its private key like a
> password, never share the CAROOT folder,
> and remove the root when the work is
> done.**

Development on your own laptop: yes.
Your home lab's machines, with the root
installed by you, on purpose: yes — that
is chapter 12's workbench recipe. A
colleague's machine, "just to make the
demo work": no — hand them this guide and
let them make their own root; it takes a
minute, and then the key to their machine
is theirs, not yours. A production
server, a customer's machine, anything
public-facing: no, in the strongest
terms. Nothing outside your fence trusts
your root anyway, so it would not even
work — chapter 14 is honest about both
halves of that sentence.

The lab in this guide obeyed the rule
with room to spare. Its CA lived in a
scratch folder on a throwaway machine,
its trust store was a private database
created for the purpose, its names were
`localhost` and the reserved `.test`
domain, and at the end the root was
uninstalled and the whole lab deleted.
Your real setup will be less paranoid in
form — you will install into your actual
system store, that is the point of the
tool — but the shape is the same: one
person, their own machines, local names.

## Who it is for

The web developer whose dev site must be
HTTPS because the feature under test —
secure cookies, service workers, camera
and microphone permissions, HTTP/2 —
refuses to work without it. The test
engineer whose suite talks to a local
service and is tired of `verify=False`.
The home-lab keeper who wants the
dashboard at `https://nas.home` without a
warning click-through every visit. The
common thread is a machine you control, a
name only you use, and a client that
should be able to trust it *properly*.

## What it is not

mkcert is not a public CA and cannot make
your site trusted by anyone else's
machine — chapter 13 covers the system
that does that. It is not a TLS toolkit:
it sets no ciphers and tunes no protocol
versions; it makes certificates, and its
companion guide in this series,
*OpenSSL for Mere Mortals*, covers the
lower layer. It is not a secrets manager:
the root key sits in a folder on disk,
protected by your account's permissions
and nothing fancier — chapter 14 treats
that as the limit it is. And it is not
magic: when a client still refuses, the
reason is always one of the two checks at
the top of this chapter — the name, or
the trust — and chapter 6 teaches you to
read a certificate so you can tell which.
