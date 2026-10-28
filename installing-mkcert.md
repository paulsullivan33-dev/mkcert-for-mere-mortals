# Installing mkcert

mkcert is a single self-contained binary
written in Go. It has no runtime, no
dependencies to resolve, and nothing to
configure before first use: you download
one file, make it executable, and run it.
That simplicity is deliberate — a tool
whose whole job is trust should not begin
by asking you to trust a long chain of
installers.

## The download

The project's releases live on GitHub
(`FiloSottile/mkcert`), and the author
also serves the current build for each
platform from `dl.filippo.io`. On Linux,
the whole install is:

```bash
curl -o mkcert https://dl.filippo.io/mkcert/latest?for=linux/amd64
chmod +x mkcert
./mkcert -version
```

On macOS and Windows the same idea holds:
a package manager if you like one
(`brew install mkcert`, `choco install
mkcert`), or the single binary from the
releases page, renamed and put somewhere
on your path. The package-manager routes
are described here from the project's
documentation; the lab verified the direct
binary route, and every command in this
guide is the binary's own, identical
whichever way it arrived.

## Confirming the install

Two checks, both in the lab's first
transcript (`mkcert-lab/transcripts/
t00-version-and-setup.txt`). The version:

```text
$ mkcert -version
v1.4.4
```

And the built-in help, which is the
tool's whole surface on one screen — five
everyday commands and a short list of
advanced flags. Keep its shape in mind;
chapter 10 is mostly an unpacking of the
bottom half:

```text
$ mkcert -help
Usage of mkcert:

	$ mkcert -install
	Install the local CA in the system trust store.

	$ mkcert example.org
	Generate "example.org.pem" and "example.org-key.pem".

	$ mkcert example.com myapp.dev localhost 127.0.0.1 ::1
	Generate "example.com+4.pem" and "example.com+4-key.pem".

	$ mkcert "*.example.it"
	Generate "_wildcard.example.it.pem" and "_wildcard.example.it-key.pem".

	$ mkcert -uninstall
	Uninstall the local CA (but do not delete it).
```

## A note on the lab's arrangement

On your machine, mkcert will work in its
default places: the real CAROOT folder
for your user, your real trust stores.
The lab, being a shared sandbox where a
mistake would outlive the experiment,
moved everything into a scratch folder
first — a private folder as `HOME`, a
scratch `CAROOT`, and an instruction
(`TRUST_STORES=nss`) to touch only the
browser-style store, never the system
one:

```text
$ echo HOME=$HOME TRUST_STORES=$TRUST_STORES
HOME=/home/hatch/workspace/build-check/mkcert-scratch/home TRUST_STORES=nss
```

Nothing about the tool's behaviour
changed — the same CA, certificates and
errors appear, only in a fenced yard.
Where a chapter's output shows a long
scratch path, read it as "your CAROOT" or
"your home folder"; the shapes are what
transfer. On your machine you will not
set any of these variables, and chapters
say so where the lab's setup differs from
yours in a way that matters — chiefly
chapter 5, where the install lands.

Check: `mkcert -version` prints a version
number, and `mkcert -CAROOT` prints a
folder that either exists or is about to.
You are ready to make the authority
itself.
