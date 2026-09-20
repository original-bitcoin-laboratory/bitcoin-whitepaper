# The Bitcoin whitepaper — which version is which

> **Scope.** Experimental laboratory research, in progress and expected to change. It reports what
> published, re-runnable methods find in public material — statistical and machine-verifiable
> findings, graded by their evidence — and draws no conclusion beyond them. Not money, not advice,
> no warranty. Details in [RIGHTS.md](RIGHTS.md).

**[bitcoinwhitepaper.online](https://bitcoinwhitepaper.online)**

There is not one Bitcoin whitepaper. **At least four are known**, they differ in ways anyone can
check in seconds, and only two survive in public hands. This repository records what each version is,
how to identify any copy from its contents alone, and exactly where proof ends and inference begins.

| version | status | sha256 |
|---|---|---|
| **August 2008** — *Electronic Cash Without a Trusted Third Party* (the title from the 22 August 2008 email Wei Dai published (mirrored at gwern.net/doc/bitcoin/2008-nakamoto)) | **lost** | unknown; its link was first crawled in 2020, already dead |
| **3 October 2008** | held | `427c63b364c6db914cf23072a09ffd53ee078397b7c6ab2d604e12865a982faa` |
| **a January 2009 download** — in the court record | **not held** | no public hash; authenticated in evidence (¶271.9) and used as a control copy. Its date, hashes and text are in evidence that is not published and are not reproduced here |
| **24 March 2009** — canonical | held, chain-anchored | `b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553` |

The fourth version is in the court record and in no public hands. The judgment in **COPA v Wright
[2024] EWHC 1198 (Ch)** records (¶271.9) that Nicholas Bohm, a retired solicitor who corresponded with
Satoshi shortly after the January 2009 release and who died shortly before the trial began (¶271.9), provided a version of the whitepaper he had downloaded
in January 2009, which an expert witness (Mr Madden, ¶271.9) authenticated and which was used in the evidence as a
control copy. That is what the public record states about it, and it is what this project states.
Its creation date, hashes, size and text are in evidence that is not published; this project does not
reproduce them, so whether it carries the Section 6 fee paragraph — which would date that addition
against Satoshi's 9 November 2008 fee proposal on the mailing list — is an open question here.

### If you have an old copy

Hash it and compare against the two held versions above. A copy that matches neither is worth
reporting — please open an issue on the repository — because a third version is known to exist and is
in no public hands.

### The canonical file's identity is closed

The file recovered from the block chain hashes to:

```
MD5:    d56d71ecadf2137be09d8b1d35c6c042
SHA256: b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553
```

The judgment records (¶320) that the court's own control copy, ID_000865, bears a creation date of
24 March 2009 and is hash-identical to a `Bitcoin.pdf` captured from the SourceForge project by a web
archive on 28 November 2009 — a capture anyone can download, and which hashes to the value above.
Together with
`X-Archive-Orig-Last-Modified: Tue, 24 Mar 2009 17:33:15 GMT` from bitcoin.org's own filesystem and
the PDF's own `/CreationDate`, three independent classes of evidence — self-asserted, server-recorded
and adjudicated — agree on the same bytes and the same instant, to the second.

---

## Identify any copy

Seven plain-text tests. **Four come from Satoshi's own words in dated records** — the 20 August 2008
email the judgment quotes (¶661) and the 22 August 2008 email Wei Dai published (mirrored at gwern.net/doc/bitcoin/2008-nakamoto) — rather than from any file, which is why they identify even the lost draft.
**The court-record column is blank on purpose** — the file is in no public hands, and what is in
evidence about it is not published.

| test | Aug 2008 (lost) | 3 Oct 2008 | Jan 2009 download (court record) | 24 Mar 2009 |
|---|---|---|---|---|
| title | *Electronic Cash Without a Trusted Third Party* | *Bitcoin: A Peer-to-Peer…* | unknown | *Bitcoin: A Peer-to-Peer…* |
| "Digital signatures …" | **offer** part | **provide** part | unknown | **provide** part |
| Hashcash reference | **`[5]`** | `[6]` | unknown | `[6]` |
| b-money citation | **absent** | `[1]` … 1998 | unknown | `[1]` … 1998 |
| "the burdens of" | yes | yes | unknown | no |
| Section 6 transaction fees | unknown | **absent** | unknown | present, reworded |
| contact address | — | `satoshi@vistomail.com` | unknown | `satoshin@gmx.com` |

The reference numbering comes from Satoshi's 20 August 2008 email to Adam Back, quoted in
**COPA v Wright [2024] EWHC 1198 (Ch)** at ¶661, in which they cite their own draft as
`[5] A. Back, "Hashcash…"` and had not heard of b-money. Back told them about it the next day. If
b-money then went in as `[1]`, Hashcash must shift to `[6]` — **and it does, in both surviving
files.** A prediction from the judgment's quotation of the email, confirmed against files from an unrelated source.

## Verify

Python 3, standard library only. No API key, no login, no node.

```bash
python verify/whitepaper_from_chain.py out.pdf     # carve it out of block 230009 and re-hash
python verify/pdf_structure.py  a.pdf b.pdf        # toolchain and document lineage
python verify/pdf_fonts.py      a.pdf b.pdf        # embedded font programs — the deepest test
python verify/pdf_text.py       in.pdf out.txt     # text extraction that works on this file
python verify/audit_published_hashes.py . --artifacts /path/to/your/pdfs   # every hash we publish, checked against files you hold
```

**`pdf_fonts.py` is the one worth running.** OpenOffice embeds a *subset* of each font containing
only the glyphs used, so two exports of the same document from the same machine share byte-identical
subsets wherever the text did not change. Between the 3 October draft and the 24 March canonical:

```
byte-identical font programs: 6 of 7
```

The seventh is the body text font, and it differs only in `glyf`/`hmtx`/`loca` — which glyphs are
included — not in `cmap`/`cvt`/`fpgm`/`maxp`/`name`/`post`/`prep`. Both carry the same source-font
creation stamp, `1990-08-06 13:14:42`. That is the same font files on the same machine, with
different glyphs because the body text changed.

*`pdf_text.py` exists because the file uses per-font `ToUnicode` CMaps: merge them, as the obvious
implementation does, and the output is a substitution cipher — `"purely"` decodes as `"ranTBl"`.*

## The canonical file's creation time is confirmed by a server

The Internet Archive replays the **origin server's** headers when a capture is fetched with `id_`:

```
bitcoin.org/bitcoin.pdf, captured 2010-07-04
  X-Archive-Orig-Last-Modified:  Tue, 24 Mar 2009 17:33:15 GMT
  X-Archive-Orig-Content-Length: 184292

the PDF's own /CreationDate  D:20090324113315-06'00' = 2009-03-24 17:33:15 UTC   <- identical
SourceForge mirrors (x3)                               2009-03-24 17:50:18 GMT   <- +17 minutes
```

`Last-Modified` on a static file is its **mtime on the serving host's filesystem** — written by
bitcoin.org's web server, not by the author. A self-asserted creation date, confirmed to the second
by a server the author did not run. Run `verify/wayback_orig_headers.py`.

## How the October draft is dated without trusting the file

```
after    Wei Dai's reply to the 22 Aug 2008 email   — it carries the 1998 b-money citation
                                                      Satoshi did not have when they wrote, guessing "(2006?)"
before   9 Nov 2008                                 — it lacks the Section 6 fee paragraph they
                                                      proposed on the mailing list that day
         the file's own date, 3 Oct 2008, sits inside that window and does none of the work
```

A backdated clock can write any creation date. It cannot put a citation into a document before its
author learned it, nor remove a paragraph they had not yet written.

## What is *not* established

- **No 2008 cryptographic timestamp exists for any version.** The earliest recorded hash of the
  October draft is January 2015.
- The early-November 2008 download rests on a **pseudonymous party's word** — corroborated by the
  file's own content and by a participant from the 2008 thread, but not anchored.
- The October draft is **not demonstrated** to be the exact bytes behind the 31 October link, only
  the simplest explanation of every observation.

That residual doubt is a property of the 2008 record, not a gap in the research: nobody hashed the
file at the time, and nobody can retroactively. Anyone claiming cryptographic certainty about an
October 2008 document is overstating.

## Searched, and not there

Recorded so nobody repeats them:

- **The 31 Oct 2008 bytes** — no capture, download or published hash from 2008. The Internet
  Archive's first capture of `bitcoin.org/bitcoin.pdf` is 2010-07-04; Common Crawl's 2008–2009 crawl
  ran during the window and did not visit the domain.
- **The August draft** — its link has 20 Wayback captures, every one a 404/302/406, earliest 2020.
  No surviving copy is known; the people who received it in 2008 have not produced one, and Hal
  Finney died in August 2014.
- **The December 2008 SourceForge upload** — replaced 2009-03-24; a Wayback gap for that project from
  January to September 2009 means its size was not captured.
- **The cypherpunks cross-post** (1 Nov 2008) — that list node ran 2005–2013 without public archives.
- **A third whitepaper file, in six archives and two content searches** — Internet Archive (tested on payload bytes, not just
  capture dates), Common Crawl, archive.today, bitcoin.org's own git history, Arquivo.pt, Vefsafn.is,
  **Software Heritage by content hash**, and **GitHub code search**. Every one controlled: the two
  held versions are found, and nothing else is. Note that three of these bottom out at the *same*
  July 2010 Wayback capture — archive.today's apparently independent 2010 row is labelled
  `archived via web.archive.org`. **When two archives agree on the earliest date, check whether one is
  quoting the other.**

**Court material.** This project cites the published judgment, *COPA v Wright* [2024] EWHC 1198 (Ch),
by paragraph, and nothing else from the proceedings: the expert appendices and witness statements the
judgment refers to are not published by the court or the parties, and this project does not
reproduce, re-host or rely on copies of them in circulation. Until 14 September 2026 this page relied
on one such appendix for the fourth version's hashes, creation time and three sentences of its text;
that material was removed, and the page now states only what the judgment records.

---

## Related

- **[bitcoin-lab.org](https://bitcoin-lab.org)** — Original Bitcoin Laboratory: executable
  reconstruction of the earliest Bitcoin, from hash-verified source archives.
- **[satoshioncha.in](https://satoshioncha.in)** — Satoshi On-Chain: the verifiable on-chain and
  off-chain footprint of the original Satoshi.

Three domains, three remits: **the code**, **the footprint**, **the document**.

MIT © 2026 [parthod0x](https://github.com/parthod0x) (new project material; historical artifacts retain their original notices and licences) · not money, not financial advice · no warranty

---

**Rights, sourcing and corrections:** see [RIGHTS.md](RIGHTS.md) — what this project uses,
where it comes from, how named people are treated, and how to ask for a correction.
