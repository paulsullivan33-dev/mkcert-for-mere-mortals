# Reading a Certificate

Outcome of this chapter: handed any
certificate file, you can answer the four
questions every TLS error is really
asking — *who is it for, who signed it,
when does it die, and what may it do?* —
using one command, `openssl x509`.

A certificate is a text-serialisable
document; `openssl x509 -in FILE -noout`
prints selected fields of it. Everything
below is real output from the lab's files
(transcripts `t01` and `t03` in
`mkcert-lab/transcripts/`).

## The root, read

```text
$ openssl x509 -in $CAROOT/rootCA.pem -noout -subject -issuer -dates
subject=O = mkcert development CA, OU = root@htch-runtime, CN = mkcert root@htch-runtime
issuer=O = mkcert development CA, OU = root@htch-runtime, CN = mkcert root@htch-runtime
notBefore=Oct 28 18:42:03 2026 GMT
notAfter=Oct 28 18:42:03 2036 GMT
```

Three readings. **Subject and issuer are
identical**: the root vouches for itself,
which is what "root" means — trust in it
cannot come from a signature, so it comes
from the act of installing it (chapter 5).
The names are honest labels: the
organisation is literally "mkcert
development CA", and the `root@htch-
runtime` part is your username and
machine name on the day the CA was born —
your root will carry your own. And the
**dates**: ten years, to the second.
mkcert roots live a decade; you will
replace a laptop before you replace one.

Two more fields define what the root
*may* do:

```text
$ openssl x509 -in $CAROOT/rootCA.pem -noout -ext basicConstraints
X509v3 Basic Constraints: critical
    CA:TRUE, pathlen:0

$ openssl x509 -in $CAROOT/rootCA.pem -noout -ext keyUsage
X509v3 Key Usage: critical
    Certificate Sign
```

`CA:TRUE` is the bit that makes this an
authority rather than a server
certificate; `pathlen:0` forbids it
creating further CAs below itself. Its
only permitted key use is signing
certificates. Its fingerprint, the
shorthand by which people compare roots:

```text
$ openssl x509 -in $CAROOT/rootCA.pem -noout -fingerprint -sha256
sha256 Fingerprint=73:D4:ED:D3:3B:7D:28:40:2E:A3:47:D9:31:9C:3D:4F:...
```

(the lab's own root; yours differs — that
uniqueness is the point of a fingerprint).

## A leaf, read

```text
$ openssl x509 -in example.test+1.pem -noout -subject -issuer -dates -ext subjectAltName
subject=O = mkcert development certificate, OU = root@htch-runtime
issuer=O = mkcert development CA, OU = root@htch-runtime, CN = mkcert root@htch-runtime
notBefore=Oct 28 18:42:27 2026 GMT
notAfter=Jan 28 18:42:27 2029 GMT
X509v3 Subject Alternative Name:
    DNS:example.test, DNS:www.example.test
```

Now the subject and issuer *differ*: the
leaf is a "mkcert development certificate"
whose issuer is the development CA — the
signature chain a client will verify.
The names a leaf answers for live in the
**subject alternative name** (SAN) list,
and *only* there matters: modern clients
ignore the old common-name field entirely,
so when a connection fails with a name
error, this list — reproduced in full,
every time — is the document to check
against the name you asked for. The
localhost certificate shows the list
holding addresses as well as names:

```text
X509v3 Subject Alternative Name:
    DNS:localhost, IP Address:127.0.0.1, IP Address:0:0:0:0:0:0:0:1
```

The dates confirm chapter 4's term from
inside: the leaf dies 28 January 2029,
two years and three months after issue,
nearly eight years before its root. And
one more field worth knowing exists, the
**extended key usage** — what the
certificate may be used *for*:

```text
$ openssl x509 -in example.test+1.pem -noout -ext extendedKeyUsage
X509v3 Extended Key Usage:
    TLS Web Server Authentication
```

Server certificates say server; chapter
10's client certificates say client (and,
in mkcert's case, both). A client
presented with a certificate whose usage
excludes the job at hand refuses it even
if the name and signature are perfect —
the third of the checks from chapter 1,
and the rarest in practice.

Check: pick any `.pem` in your lab folder
and read it. If you can state its names,
its issuer, its death date and its usage
without the guide open, every remaining
chapter is a variation.
