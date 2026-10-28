# Teaching Clients to Trust

Outcome of this chapter: the same
certificate, refused and then accepted by
three different clients — curl, OpenSSL's
own checker, and a Python program — each
accepting for its own reason, so you can
see that "trust" is not one switch but a
per-client fact.

Everything here is transcript
`mkcert-lab/transcripts/
t05-clients-learning-to-trust.txt`, run
against the lab server of chapter 7.

## Refusal first: the healthy default

Before teaching anything, watch the
system work as designed. curl, knowing
nothing of the lab's root:

```text
$ curl -sS --resolve example.test:18443:127.0.0.1 https://example.test:18443/
curl: (60) SSL certificate problem: unable to get local issuer certificate
```

Exit 60, and the key phrase *unable to
get local issuer certificate*: the name
was right, the server answered — the
signature's issuer (your root) is simply
not in the store curl read. OpenSSL's
`s_client`, the diagnostic underneath
most TLS stacks, says the same in its own
dialect:

```text
$ echo | openssl s_client -connect 127.0.0.1:18443 -servername example.test | grep 'Verify return code'
Verify return code: 21 (unable to verify the first certificate)
```

Pin these two messages. They mean "I do
not know this authority" — and *only*
that. Chapter 15 contrasts them with the
name-mismatch error, which looks similar
and means something entirely different.

## Route one: tell the client the file

The most explicit teaching is per-command:
name the root certificate and say "trust
this":

```text
$ curl -sS --cacert $CAROOT/rootCA.pem --resolve example.test:18443:127.0.0.1 https://example.test:18443/
Hello from the mkcert lab server.
If your client shows this without a warning, it trusted the certificate.
```

No warning, no `-k`. `s_client` with
`-CAfile` flips its verdict the same way
— `Verify return code: 0 (ok)`. This
route changes nothing on the machine; it
is the right one for scripts, tests and
one-off checks, and the one to reach for
when you do not want a root installed
system-wide. Notice what it proves: the
*only* thing missing all along was the
root. The certificate was never broken.

## Route two: the store the client reads

Chapter 5 installed the root into a
trust store. A client reading *that*
store needs no flags at all — browsers
pointed at a store holding your root,
Firefox and Chromium on Linux via the
NSS database, are the everyday case; the
store lookup was proved directly with
`certutil -L`. Each client family reads
its own store (system, NSS, Java), which
is why "it works in my browser but not in
curl" is a statement about stores, not
about the certificate.

## Route three: the program's own context

Programs that make TLS connections can be
handed the root in code. The lab's small
client (`mkcert-lab/server/
check_https.py`) takes the root file as an
argument and builds an SSL context from
exactly it. First, without it, against
the localhost server:

```text
$ python3 server/check_https.py https://localhost:18444/
FAILED: URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1000)>
```

Then with it:

```text
$ python3 server/check_https.py https://localhost:18444/ $CAROOT/rootCA.pem
HTTP 200
Hello from the mkcert lab server.
```

The same pattern — a context, a CA file —
exists in every language's TLS library,
and it is how test suites should consume
mkcert: the runner builds a context from
`$(mkcert -CAROOT)/rootCA.pem`, and no
machine-wide state is involved at all.
The server's log closes the proof, one
line per accepted request:

```text
server saw: GET / HTTP/1.1
```

## The route that is not one

`curl -k`, `verify=False`, and their kin
do not teach a client to trust your root;
they teach it to stop checking. Every
transcript in this guide was produced
without them, on purpose: the day a local
setup only works with verification off,
the setup — not the checker — is the
bug, and chapter 6's reading skills will
find it. Keep the alarm armed; add the
one authority it should recognise.

Check: pick the client you actually use,
run its refusal first, then its trusting
form, and watch the server log grow by
exactly the accepted requests.
