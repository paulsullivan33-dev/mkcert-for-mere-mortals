# Recipes

Small, complete jobs, each one assembled
from the chapters before it. Names are
illustrative; substitute your project's.

## HTTPS for a local dev site, by name

*You want `https://shop.example.test:8443`
to load in your browser with no warning
while you develop.*

Add the name to your hosts file once
(`127.0.0.1 shop.example.test`), install
the CA once (`mkcert -install`), and per
project:

```bash
mkcert shop.example.test
# point the dev server at shop.example.test.pem
# and shop.example.test-key.pem, port 8443
```

Restart the server, browse to the name.
The certificate covers only that name —
add `www.shop.example.test` to the same
command if the app redirects there
(chapter 9).

## One CA for the whole workbench

*Several of your own machines — desktop,
laptop, a home-lab box — should all trust
the same local names.*

Make the CA once, on one machine. Run
`mkcert -install` there, issue a leaf,
and then carry **the CAROOT folder**
(the whole folder, key included) to the
same CAROOT location on each other
machine and run `mkcert -install` there
too. Every machine now trusts leaves from
the one root, and a certificate issued
anywhere works everywhere. Respect
chapter 1's rule while doing it: the
key crosses machines over a channel you
trust, lands only on machines you own,
and chapter 11 is how it all comes off
again. (This flow is documented-only in
the lab, which had one machine; each step
in it is one the lab ran locally.)

## Certificates a test suite can use

*A suite spins up the service and hits it
over HTTPS; nobody wants `-k` in the
tests.*

Keep the leaf pair in the test fixtures.
In the client setup, build the TLS
context from the root file, found without
hardcoding a path:

```python
import subprocess, ssl, os
caroot = subprocess.check_output(["mkcert", "-CAROOT"], text=True).strip()
ctx = ssl.create_default_context(cafile=os.path.join(caroot, "rootCA.pem"))
```

No install, no store, nothing
machine-wide — chapter 8's route three,
which is why the lab's client was built
that way. On a fresh CI runner the same
script works the moment the project
carries its test CA, and the production
configuration remains untouched and
verifying.

## An expiring certificate, renewed

*The leaf's date (chapter 6) is near.*

```bash
mkcert example.test www.example.test   # the same command as last time
```

Restart whatever serves it, with the
fresh files. There is no renew verb
because there is nothing to preserve —
the names, not the key, are the identity.
Delete the old pair once the new one is
answering.

## A clean slate

*The project is done; the machine should
forget all of it.*

Chapter 11, in order: `mkcert
-uninstall`, delete the CAROOT folder,
remove the hosts lines you added, and let
the leaf pairs go with the project
folder. Verify with the curl that used to
work — its issuer error is the receipt.

## A name for a phone on your own Wi-Fi

*You want a device on your home network
to reach a lab service by name, with a
trusted certificate.*

Possible, and worth doing slowly: the
service's machine takes a leaf for a name
your home DNS (router, Pi-hole) resolves
to it; the phone must then trust your
root, which means installing a root CA on
the phone — a device-wide trust decision
chapter 14 weighs. The lab had no second
device and did not run this; the server
and certificate halves are chapters 7 and
9, and the phone's trust-store half is
its manufacturer's documented procedure.
Read chapter 14 first, and prefer the
workbench recipe above when the "device"
is a computer you control.
