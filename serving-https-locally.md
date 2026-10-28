# Serving HTTPS Locally

Outcome of this chapter: a real HTTPS
server on your own machine, answering
under a mkcert certificate — and the one
piece of plumbing, name resolution, that
decides whether clients can reach it by
the name on that certificate.

## The lab server

TLS does not care what serves it. Your
dev framework's server, nginx, Caddy —
each takes a certificate file and a key
file, and chapter 13's neighbours cover
those. To keep the moving parts visible,
the lab used a thirty-line Python program
(`mkcert-lab/server/serve_https.py`): it
loads a certificate and key with Python's
`ssl` module, serves one fixed page on
port 18443, and prints every request it
receives, so transcripts can show a
client's request arriving only *after* a
successful handshake:

```text
$ python3 server/serve_https.py certs/example.test+1.pem certs/example.test+1-key.pem &
$ cat server.log
serving on https://127.0.0.1:18443 with cert certs/example.test+1.pem
```

(`mkcert-lab/transcripts/
t04-the-lab-server.txt`). On your machine
the shape is identical whatever the
server: point it at the leaf's two files,
choose a port, start it. The certificate
does not know or care which program holds
it.

## The name must reach the machine

Here is the catch that produces more
confusion than any TLS error. A
certificate for `example.test` only helps
if asking for `example.test` connects to
*your machine*. Names resolve through
DNS, and `example.test` is not yours in
any public DNS. Two honest ways to close
the gap, both used constantly in real
development:

- **`/etc/hosts`** (or its Windows
  equivalent): a line `127.0.0.1
  example.test` tells your machine to
  resolve the name to itself, before DNS
  is ever asked. This is the normal route
  on your own computer, and this guide
  recommends it there. The lab did *not*
  do this: its machine was a shared
  sandbox, and editing the system hosts
  file was outside the fence it had set
  itself.
- **curl's `--resolve`**: for a single
  command, `curl --resolve
  example.test:18443:127.0.0.1
  https://example.test:18443/` overrides
  resolution for that run. The lab used
  this throughout — every curl transcript
  in the next chapters carries it — and it
  is the right tool for one-off tests
  even on your own machine.

What the lab got for skipping the hosts
file is the cautionary tale kept whole in
chapter 15: the sandbox's DNS *answered*
for `example.test` — with an address
belonging to the sandbox's network
interception, not to the lab machine. A
client that trusted DNS went somewhere
else entirely and was reset, holding a
perfectly good certificate it never got
to use. Names are plumbing before they
are cryptography.

For `localhost` none of this arises: the
name resolves to the loopback address by
universal convention, which is why the
lab ran a second copy of the server under
the localhost certificate on port 18444,
and why so much local development never
leaves `localhost` at all.

Check: your server is listening (the lab
proved it with `ss -tlnp | grep 18443`),
and one of the two name routes above
connects the certificate's name to your
machine. The server will still refuse
nobody and convince nobody — trust is the
client's side of the story, and it is the
next chapter.
