# Licensing and Citation

This file is a **scope record**, not a license. It maps which parts of this
repository fall under which license, records the dataset boundary, and tells you
how to cite the work. The licenses themselves are the standard instruments in
`LICENSE` (MIT) and `LICENSE-docs` (Creative Commons Attribution 4.0
International). Where this record and a license text ever disagree, the license
text governs.

This record applies to **Hybrid Ground Truth Realism**
(<https://github.com/Dandelion-Engineering/Hybrid-Ground-Truth-Realism>). The two
licenses and the structure below are the same for every Dandelion Engineering
research project. Version numbers are omitted while the project is in progress
and added when a release is cut.

## The two licenses

- **Code → MIT** (`LICENSE`). Covers all Dandelion-owned source code, scripts,
  configuration, and software-like reproducibility machinery. Permissive and
  commercial-use-permitting.
- **Prose → CC BY 4.0** (`LICENSE-docs`). Covers all Dandelion-owned written and
  narrative artifacts. Attribution required; commercial use permitted; no
  ShareAlike obligation, so derivatives may be released under any terms as long
  as attribution is given.

## Scope

**MIT (`LICENSE`)** covers Dandelion-owned:

- source code, scripts, and configuration anywhere in the repository
- the runnable parts of the Reproducibility Packet (scripts, configs,
  `requirements.txt`, helper utilities, the verification artifact's code)

**CC BY 4.0 (`LICENSE-docs`)** covers Dandelion-owned:

- `Project Details/Project Details.md` and the `Playbooks/`
- `Claim Sheet.md` and `Accessible Claim Sheet.md`
- the `Technical Report/` prose and the `Accessible Piece/`
- the `Study Guide/`
- the narrative prose in `Reproducibility Packet/README.md` and in `DATA.md`
- READMEs (including the root Live-Run README), progress reports, and the
  narrative material under `agents/` (session summaries, scratch analyses)
- chat records under `chats/`, if they ship publicly with the repository
- user-facing copy files for any verification viewer

## Dataset boundary

Raw datasets are **not redistributed** by this repository. They remain under
their original source licenses and must be obtained from their original hosts.
Each dataset's source, license, commercial-use status, access instructions, and
citation live in `Reproducibility Packet/DATA.md`. Nothing in `LICENSE` or
`LICENSE-docs` relicenses third-party data.

## Generated result summaries

Result summaries (tables, figures, numbers) that ship **inside** a CC BY 4.0
narrative document inherit that document's CC BY 4.0 license. Reuse should
attribute **both** this Dandelion Engineering project **and** the underlying
dataset source the result came from.

## How to attribute (CC BY 4.0)

CC BY 4.0 requires attribution. A reuser of the prose satisfies it with:

> "Hybrid Ground Truth Realism" by Dandelion Engineering, licensed under
> CC BY 4.0. Source:
> <https://github.com/Dandelion-Engineering/Hybrid-Ground-Truth-Realism>.
> Changes, if any, noted.

## How to cite this work

The work is directed by one human, Randy Crespo, and produced in collaboration
with two AI research agents, Claude (Anthropic) and Codex (OpenAI). Under current
citation and publishing norms an AI system is not listed as a formal author
because it cannot take responsibility for the work; the accountable, citable
author is the human. In keeping with Dandelion Engineering's transparency
standard, the AI collaboration is **disclosed**, not hidden. So: cite Randy
Crespo (with Dandelion Engineering as the organization), and disclose the AI
agents in a note.

The machine-readable `CITATION.cff` in the repository root is the canonical
source GitHub uses for its "Cite this repository" button. Human-readable forms:

**Plain / APA-style**

> Crespo, R. (2026). *Hybrid Ground Truth Realism: does the realism of hybrid
> ground truth change measured spike-sorting accuracy?* Dandelion Engineering.
> <https://github.com/Dandelion-Engineering/Hybrid-Ground-Truth-Realism>.
> Produced in collaboration with the AI research agents Claude (Anthropic) and
> Codex (OpenAI); the research question was selected by the agents rather than by
> the director.

**BibTeX**

```bibtex
@misc{dandelion_hybridgroundtruth_2026,
  author       = {Crespo, Randy},
  title        = {Hybrid Ground Truth Realism: does the realism of hybrid
                  ground truth change measured spike-sorting accuracy?},
  year         = {2026},
  howpublished = {Dandelion Engineering},
  url          = {https://github.com/Dandelion-Engineering/Hybrid-Ground-Truth-Realism},
  note         = {Produced by Randy Crespo in collaboration with the AI research
                  agents Claude (Anthropic) and Codex (OpenAI); the research
                  question was selected by the agents rather than by the
                  director. Exploratory research run; not peer-reviewed.}
}
```
