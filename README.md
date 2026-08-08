# The Bitcoin whitepaper — which version is which

**[bitcoinwhitepaper.online](https://bitcoinwhitepaper.online)**

There is not one Bitcoin whitepaper. **At least four are known**, they differ in ways anyone can
check in seconds, and only two survive in public hands. This repository records what each version is,
how to identify any copy from its contents alone, and exactly where proof ends and inference begins.

| version | status | sha256 |
|---|---|---|
| **August 2008** — *Electronic Cash Without a Trusted Third Party* | **lost** | unknown; its link was never archived |
| **3 October 2008** | held | `427c63b364c6db914cf23072a09ffd53ee078397b7c6ab2d604e12865a982faa` |
| **11 November 2008** | **not held — but now identifiable** | `e6cc7c952c688b234f9872c3e2f50060ae6556fd27925cba503c6460048e50a9` (MD5 `3e5e11e1e3208d2829e887fb1c86bd05`), created `2008-11-11 16:00:34 UTC`, **larger than 182,801 bytes** (≈184,300 — see note) |
| **24 March 2009** — canonical | held, chain-anchored | `b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553` |

The **11 November 2008** version is dated two days after Satoshi proposed transaction fees on the
mailing list. Whether it carries the Section 6 fee paragraph would date that addition to within 48
hours. The file itself is not public — but a great deal about it is:

- **It was the version the public could download in January 2009.** Nicholas Bohm, a retired
  solicitor who read the cryptography mailing list, downloaded it on **18 January 2009 at 13:27 GMT**
  and still had it in 2023. His witness statement (§19) reports its creation stamp as
  **11 November 2008, 08:00:34 at UTC−08:00**.
- **Patrick Madden analysed it** at Appendix PM3 §§41–73 and considers it *"very likely to be an
  authentic intermediate draft"* between the October 2008 and March 2009 versions.
- **Its hashes are now known**, from Appendix PM3 §42 — so a candidate copy can be verified in one
  command, even though the file is in no public hands.
- **Its size is bounded, not measured.** No source states a byte count, but PM3 quotes the file's
  trailer, which ends `startxref 182801` — the offset of its cross-reference table. So the file is
  **provably larger than 182,801 bytes**. Calibrating the remaining tail against the two versions we
  hold (1,505 and 1,565 bytes) puts it at **≈184,306–184,366** — marginally larger than the canonical.
  *The bound is a fact; the estimate is an inference from two data points, and is labelled as one.*
  Its trailer `/ID` halves are identical, meaning the file was **written once and never re-saved** —
  the same signature the October draft carries.
- **It carries the transaction-fee text**, in a wording unique to it (PM3 §52), which we verified is
  absent from both versions we hold. Satoshi proposed fees on the list on 9 November 2008; the text
  was in the paper **two days later**, and was reworded again for March 2009.

### ★ If you have an old copy, you can check it by reading — no hashing required

Madden's Appendix PM3 §52 identifies three sentences that appear in the 11 November file and in
**neither** of the two versions that survive in public. We searched both held files directly and
confirmed all three are absent:

```
"The incentive is also funded with transaction fees"
"The output value of every transaction is equal to the input value minus a transaction fee"
"and the incentive is increased by the total transaction fees in the block"
```

**Open any old `bitcoin.pdf`, press Ctrl-F, and search for the first one.** If it is there, you have
the version nobody has — please get in touch. The canonical March 2009 text says something close but
not the same (*"can also be funded"*, *"if the output value … is less than"*); the October 2008 draft
has no transaction-fee text at all.

**These sentences matter more than the hashes.** A hash matches only one exact file and no search
engine indexes it. A sentence survives quotation, re-typing, and a paste into an old email — so it is
worth searching your mail, not just your disk.

### The canonical file's identity is closed

Madden's First Expert Report §180 publishes the hashes of the court's own control copy (ID_000865):

```
MD5:    d56d71ecadf2137be09d8b1d35c6c042
SHA256: b1674191a88ec5cdd733e4240a81803105dc412d6c6708d53ab94fc248f4f553
```

Both match the file recovered from the block chain. Together with
`X-Archive-Orig-Last-Modified: Tue, 24 Mar 2009 17:33:15 GMT` from bitcoin.org's own filesystem and
the PDF's own `/CreationDate`, three independent classes of evidence — self-asserted, server-recorded
and adjudicated — agree on the same bytes and the same instant, to the second.

---

## Identify any copy

Six plain-text tests. **Four come from Satoshi's own words in dated records** rather than from any
file, which is why they identify even the versions nobody has. **The 11 November column is blank on purpose** — those blanks are exactly what a surfacing copy would fill in.

| test | Aug 2008 (lost) | 3 Oct 2008 | 11 Nov 2008 (not held) | 24 Mar 2009 |
|---|---|---|---|---|
| title | *Electronic Cash Without a Trusted Third Party* | *Bitcoin: A Peer-to-Peer…* | unknown | *Bitcoin: A Peer-to-Peer…* |
| "Digital signatures …" | **offer** part | **provide** part | unknown | **provide** part |
| Hashcash reference | **`[5]`** | `[6]` | unknown | `[6]` |
| b-money citation | **absent** | `[1]` … 1998 | unknown | `[1]` … 1998 |
| "the burdens of" | yes | yes | unknown | no |
| Section 6 transaction fees | absent | **absent** | **present — first wording** | present, reworded |
| contact address | — | `satoshi@vistomail.com` | unknown | `satoshin@gmx.com` |

The reference numbering comes from Satoshi's 20 August 2008 email to Adam Back, quoted in
**COPA v Wright [2024] EWHC 1198 (Ch)** at ¶661, in which he cites his own draft as
`[5] A. Back, "Hashcash…"` and has never heard of b-money. Back told him about it the next day. If
b-money then went in as `[1]`, Hashcash must shift to `[6]` — **and it does, in both surviving
files.** A prediction from a court exhibit, confirmed against files from an unrelated source.

## Verify

Python 3, standard library only. No API key, no login, no node.

```bash
python verify/whitepaper_from_chain.py out.pdf     # carve it out of block 230009 and re-hash
python verify/pdf_structure.py  a.pdf b.pdf        # toolchain and document lineage
python verify/pdf_fonts.py      a.pdf b.pdf        # embedded font programs — the deepest test
python verify/pdf_text.py       in.pdf out.txt     # text extraction that works on this file
python verify/audit_published_hashes.py . --artifacts .   # every hash we publish, checked
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
                                                      Satoshi did not have when he wrote, guessing "(2006?)"
before   9 Nov 2008                                 — it lacks the Section 6 fee paragraph he
                                                      proposed on the mailing list that day
         the file's own date, 3 Oct 2008, sits inside that window and does none of the work
```

A backdated clock can write any creation date. It cannot put a citation into a document before its
author learned it, nor remove a paragraph he had not yet written.

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
  ran during the window and never visited the domain.
- **The August draft** — its link has 20 Wayback captures, every one a 404/302/406, earliest 2020.
  Wei Dai, Adam Back and Gregory Maxwell were asked years ago and do not have copies; Hal Finney was
  asked and died in August 2014.
- **The December 2008 SourceForge upload** — replaced 2009-03-24; a Wayback gap for that project from
  January to September 2009 means its size was never captured.
- **The cypherpunks cross-post** (1 Nov 2008) — that list node ran 2005–2013 without public archives.
- **The 11 November file, in eight archives** — Internet Archive (tested on payload bytes, not just
  capture dates), Common Crawl, archive.today, bitcoin.org's own git history, Arquivo.pt, Vefsafn.is,
  **Software Heritage by content hash**, and **GitHub code search**. Every one controlled: the two
  held versions are found where the target is not. Note that three of these bottom out at the *same*
  July 2010 Wayback capture — archive.today's apparently independent 2010 row is labelled
  `archived via web.archive.org`. **When two archives agree on the earliest date, check whether one is
  quoting the other.**

**Corrected — this list used to say the COPA expert reports were "not published".** They are. All six
of Patrick Madden's reports and his 48 appendices are publicly available at
[bitcoindefense.org](https://bitcoindefense.org), and the hashes and text tests above are drawn from
them. **And Madden ran this search too**: at Appendix PM3 §§53–56 he records that the disclosure
dataset, Google, and the Internet Archive's holdings of bitcoin.org produced no other instance of the
11 November document — an independent negative, given under a duty to the court, that agrees with
ours.

---

## Related

- **[bitcoin-lab.org](https://bitcoin-lab.org)** — Original Bitcoin Laboratory: executable
  reconstruction of the earliest Bitcoin, from hash-verified source archives.
- **[satoshioncha.in](https://satoshioncha.in)** — Satoshi On-Chain: the verifiable on-chain and
  off-chain footprint of the original Satoshi.

Three domains, three remits: **the code**, **the identity**, **the document**.

MIT © 2026 [parthod0x](https://github.com/parthod0x) · not money, not financial advice · no warranty

---

**Rights, sourcing and corrections:** see [RIGHTS.md](RIGHTS.md) — what this project uses,
where it comes from, how named people are treated, and how to ask for a correction.
