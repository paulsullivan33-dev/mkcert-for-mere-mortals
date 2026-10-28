# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's names are `localhost` and the reserved `.test`
   domain, and its traffic never left the machine.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 14 names what the tool
   cannot do: trust that ends at your own machines, a root key
   guarded by file permissions alone, no revocation, per-store
   trust that no install abolishes, and fixed certificate terms.
8. **The safety rule is in the text, early.** Chapter 1 and the
   README state the rule plainly — *your CA belongs on machines
   you own, signing for names that stay local; never share the
   CAROOT, and remove the root when the work is done* — before
   any procedure depends on it, and later chapters point back
   to it where the tooling would make crossing the line easy.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is an Ubuntu 24.04 sandbox (OpenSSL 3.0.13,
curl 8.5.0, Python 3.12.3). mkcert **1.4.4** was the official
binary, fetched from the author's distribution point into a
scratch folder. The lab was deliberately fenced: `HOME`,
`CAROOT` and the NSS database all lived inside that scratch
folder, and every `-install`/`-uninstall` ran with
`TRUST_STORES=nss`, so the sandbox's real system trust store
was never written — verified afterwards by fingerprint: the
lab root does not appear in `/etc/ssl/certs/ca-certificates.crt`,
`/usr/local/share/ca-certificates` gained no file, and the
system NSS database mkcert tried (`/etc/pki/nssdb`) kept its
pre-lab timestamps and read-only refusal. All transcripts live
in `mkcert-lab/transcripts/`; the server and client are
`mkcert-lab/server/`.

Run for real, with transcripts as evidence:

- Version, help, `-CAROOT`, and the empty-CAROOT starting
  state (t00).
- The first issuance creating the CA itself, the CA files'
  permissions, the root's subject, issuer, ten-year dates,
  `CA:TRUE`/`pathlen:0`, `Certificate Sign` key usage and
  SHA-256 fingerprint, and the leaf's SAN and two-year-three-
  month term, all read back with `openssl x509` (t01, t02).
- `-install` into a lab-created NSS database, proved by
  `certutil -L` before and after — including the run's real
  failure against the sandbox's read-only `/etc/pki/nssdb`
  store, reported as exit 1 while the user's store succeeded
  (t02).
- Issuing for `localhost 127.0.0.1 ::1`, for
  `example.test www.example.test`, and for `*.example.test`,
  with the SAN lists read back from each file (t03).
- A Python HTTPS server serving the issued `example.test`
  certificate on loopback, and a second instance serving the
  localhost certificate (t04).
- Three clients refusing, then trusting: curl (exit 60, then
  success with `--cacert`), `openssl s_client` (verify code
  21, then 0 with `-CAfile`), and a Python client
  (`CERTIFICATE_VERIFY_FAILED`, then HTTP 200 with the root
  loaded into its context) (t05).
- The wildcard proven both ways (`api.example.test`
  accepted, `deep.api.example.test` refused), the hostname-
  mismatch error with trust in place, `SSL_CERT_FILE` ignored
  by this curl build while `--cacert` honoured the same file,
  and the lab DNS answering `example.test` with an intercepted
  address that reset the Python client (t06).
- ECDSA (`-ecdsa`, P-256), PKCS #12 (`-pkcs12`) and client
  (`-client`) issues, each read back with openssl (t07).
- `-uninstall` removing the root from the NSS store (proved
  by `certutil -L`), the CAROOT files surviving it, and a
  `--cacert` request still succeeding afterwards — the
  chapter-11 demonstration that uninstall is not deletion
  (t08).

Documented only — described from the project's and vendors'
documentation, not run, and the text does not claim otherwise:

- The full unrestricted `mkcert -install` into a real system
  store (the lab's install was fenced to NSS on purpose, as
  chapter 5 explains), and the Windows, macOS and Java trust
  stores.
- Anything in a graphical browser: certificate settings,
  Firefox profile behaviour beyond the NSS database it keeps,
  and browser restarts after install.
- A second machine or device: the workbench recipe's CAROOT
  carry and the phone recipe in chapter 12 are assembled from
  steps the lab ran locally, and are labelled as such there.
- Editing `/etc/hosts`, which the lab deliberately did not
  do; its `--resolve` evidence is the verified half of
  chapter 7's name-resolution story.
- The comparison tools in chapter 13 are characterised, not
  benchmarked.

Fixtures are this guide's own and deliberately generic: a
thirty-line HTTPS server that serves one fixed page, a
fifteen-line checking client, and names drawn from the
reserved `.test` domain plus `localhost`. No example is
modelled on any real person, network, service or
organisation, and no certificate was issued for any name that
resolves to a real third party.
