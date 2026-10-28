# Names, Wildcards and Addresses

Outcome of this chapter: you can choose
the names a certificate carries, and you
can predict — and prove — exactly which
requests it will and will not satisfy.

## Several names, one certificate

A mkcert command takes as many names as
you give it, and folds them all into one
certificate's SAN list (chapter 6):

```text
$ mkcert localhost 127.0.0.1 ::1
Created a new certificate valid for the following names 📜
 - "localhost"
 - "127.0.0.1"
 - "::1"

The certificate is at "./localhost+2.pem" and the key at "./localhost+2-key.pem" ✅
```

(`mkcert-lab/transcripts/
t03-issuing-certificates.txt`). The file
is named for the first name, with `+N`
counting the rest. One certificate for
the name and both its loopback addresses
is the standard local-development issue:
whichever spelling a client uses —
`localhost`, `127.0.0.1`, `::1` — the SAN
list has an answer for it. DNS names and
IP addresses are different *kinds* of SAN
(the reading in chapter 6 shows `DNS:`
and `IP Address:` entries side by side),
and a client asking by address will not
accept a certificate that names only the
word. If an address matters, put the
address on the certificate.

## The wildcard, and its one level

A name may be a **wildcard**: `*.example.
test` stands for any single label in that
position. mkcert issues it like any other
name, and says the limit out loud as it
does:

```text
$ mkcert "*.example.test"
Reminder: X.509 wildcards only go one level deep, so this won't match a.b.example.test ℹ️
```

The lab proved both halves against a
server holding the wildcard certificate
(`mkcert-lab/transcripts/
t06-when-it-still-fails.txt`). One level
down works, with full verification:

```text
$ curl -sS --cacert $CAROOT/rootCA.pem --resolve api.example.test:18445:127.0.0.1 https://api.example.test:18445/
Hello from the mkcert lab server.
```

Two levels down fails, even with the
root trusted — the refusal has moved from
trust to naming, and the error says so:

```text
$ curl -sS --cacert $CAROOT/rootCA.pem --resolve deep.api.example.test:18445:127.0.0.1 https://deep.api.example.test:18445/
curl: (60) SSL: no alternative certificate subject name matches target host name 'deep.api.example.test'
```

The wildcard also does not cover the bare
domain itself: `*.example.test` says
nothing about `example.test`. The set
most test rigs actually want is one
certificate naming both: `mkcert
example.test "*.example.test"`.

## The mismatch error, for contrast

The second transcript in `t06` is the
name error in its purest form: the
*localhost* name asked of a server
holding the `example.test` certificate,
root trusted, everything else correct:

```text
curl: (60) SSL: no alternative certificate subject name matches target host name 'localhost'
```

Same exit code 60 as the trust refusal in
chapter 8, different sentence — and the
sentence is the diagnosis. *Unable to get
local issuer certificate* means fix the
trust. *No alternative certificate
subject name matches* means fix the
certificate's SAN list or the name you
are asking for. Chapter 6's `openssl`
reading always settles which: compare the
SAN list with the requested name, and the
root with the client's store, and one of
them is not what you expected.

## Choosing names well

A few habits keep local naming painless.
Use the **`.test`** top-level domain for
invented names: it is reserved, can never
be a real public domain, and so can never
collide with a site you might
legitimately visit — `example.test`
throughout this guide is exactly that
reservation at work. Favour one
certificate with the handful of names a
project needs over a certificate per
name; servers load one pair of files, and
chapter 6's reading stays short. And
when a project grows subdomains freely —
tenant sites, branch previews — that is
the wildcard's honest use, with the
one-level rule priced in.

Check: ask your server for a name on its
certificate, a name one wildcard level
out, and a name it has never heard of.
Three runs, three predicted outcomes —
page, page, and the mismatch sentence.
