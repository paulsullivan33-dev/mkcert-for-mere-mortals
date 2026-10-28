# More Kinds of Certificate

Outcome of this chapter: the variations
behind the flags in `mkcert -help`'s
bottom half — different key types, a
different file format, certificates for
clients rather than servers — all issued
for real in the lab (transcript
`mkcert-lab/transcripts/
t07-more-kinds-of-certificate.txt`).

## ECDSA keys with `-ecdsa`

By default mkcert makes RSA keys (the
2048-bit keys in the earlier chapters'
file sizes). `-ecdsa` makes the leaf with
an elliptic-curve key instead:

```text
$ mkcert -ecdsa ecdsa.example.test
The certificate is at "./ecdsa.example.test.pem" and the key at "./ecdsa.example.test-key.pem" ✅
```

Reading it back confirms what changed —
the public key algorithm, and the curve:

```text
$ openssl x509 -in ecdsa.example.test.pem -noout -text | grep -E 'Public Key Algorithm|NIST|ASN1 OID' | head -3
            Public Key Algorithm: id-ecPublicKey
                ASN1 OID: prime256v1
                NIST CURVE: P-256
```

Everything else — names, issuer, term,
trust — is untouched; the CA stays RSA,
and only the leaf's key differs. ECDSA
keys are smaller and handshakes with them
are cheaper, which is why modern public
certificates increasingly use them; for a
local leaf the honest reason to choose it
is that the software you are testing
behaves differently with one, and now you
can check.

## One file instead of two with `-pkcs12`

Some tools — Java keystores' importers,
some Windows and browser tooling, various
appliances — want a certificate and its
key bundled in a single **PKCS #12** file
(the `.p12` / `.pfx` format), protected
by a password:

```text
$ mkcert -pkcs12 example.test
The PKCS#12 bundle is at "./example.test.p12" ✅

The legacy PKCS#12 encryption password is the often hardcoded default "changeit" ℹ️
```

That last line is mkcert being candid:
the bundle's password is the conventional
`changeit`, which tools that import these
files commonly expect. Treat a `.p12` as
what it is — a private key wearing a
name tag. The password is a
compatibility convention, not protection;
guard the file like any `-key.pem`. A
`-p12-file` flag names the output, as
`-cert-file` and `-key-file` name the
ordinary pair when your server's config
expects particular paths — with those
three, mkcert can write files straight
into the layout another tool demands.

## Client certificates with `-client`

Everything so far has certified
*servers*: a client checks the server's
certificate. Some systems also ask the
client to prove itself — mutual TLS,
common between internal services and to
appliances. `-client` issues a
certificate whose extended key usage
(chapter 6) permits that direction:

```text
$ mkcert -client laptop-client
The certificate is at "./laptop-client-client.pem" and the key at "./laptop-client-client-key.pem" ✅

$ openssl x509 -in laptop-client-client.pem -noout -ext extendedKeyUsage
X509v3 Extended Key Usage:
    TLS Web Client Authentication, TLS Web Server Authentication
```

Against the server certificate's plain
`TLS Web Server Authentication`, the
difference is one line in the document
and a whole direction of authentication
in the world. Configuring a server to
*demand* client certificates is the
server's own business and beyond this
guide; mkcert's half — minting a client
identity your root will vouch for — is
the one command above.

Check: issue one of each kind into a
scratch folder and read them side by
side. Key algorithm, bundle format, key
usage — the three axes are independent,
and every other knob is naming.
