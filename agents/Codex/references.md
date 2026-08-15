# References — Codex

Running source ledger for Codex. Entries record what each source establishes and how it informed a project decision. Links and DOIs were verified through live searches on 2026-08-11.

## Verified sources

### Buccino et al. 2026 — anchor evaluation pipeline

**Buccino, A. P., Sridhar, A., Feng, D., Svoboda, K., & Siegle, J. H. (2026). Efficient and reproducible pipelines for spike sorting large-scale electrophysiology data. _eLife_, 15, RP110170.** [https://doi.org/10.7554/eLife.110170.3](https://doi.org/10.7554/eLife.110170.3)

Builds the SpikeInterface hybrid evaluation pipeline; injects 10 Poisson units at 15 Hz, uses 1,800 NP1 and 3,000 NP2 ground-truth units, and reports Kilosort4-versus-2.5 effects. Its Limitations section explicitly names population firing dynamics and brain-region matching as missing realism.

*How it informed the project:* Defines the control condition, the exact open question, the low-SNR stratum, the scale reference, and the need to use pairing rather than imitate a distributed benchmark on one workstation.

### Pachitariu et al. 2024 — Kilosort4 and realism-sensitive benchmarks

**Pachitariu, M., Sridhar, S., Pennington, J., & Stringer, C. (2024). Spike sorting with Kilosort4. _Nature Methods_, 21, 914–921.** [https://doi.org/10.1038/s41592-024-02232-7](https://doi.org/10.1038/s41592-024-02232-7)

Benchmarks ten sorters across hybrid and full simulations. The hybrid method modulates ISIs by local population firing rate; the full simulator shuffles empirical ISIs for single units. It also shows that unrealistic waveform duration in a biophysical benchmark generates false positives that decline when waveform timing is corrected.

*How it informed the project:* Establishes prior art for population-rate coupling, clears the ambiguity about “non-stationary waveforms” (drift-dependent waveforms, not burst-dependent amplitude attenuation), and gives direct evidence that simulator realism can change measured errors.

### Magland et al. 2020 — benchmark dependence across ground-truth classes

**Magland, J., Jun, J. J., Lovero, E., Morley, A. J., Hurwitz, C. L., Buccino, A. P., Garcia, S., & Barnett, A. H. (2020). SpikeForest, reproducible web-facing ground-truth validation of automated neural spike sorters. _eLife_, 9, e55167.** [https://doi.org/10.7554/eLife.55167](https://doi.org/10.7554/eLife.55167)

Aggregates more than 30,000 ground-truth units across many studies and sorter families. Reports no universal winner and a precision-versus-recall signature in synthetic data that differs from paired recordings.

*How it informed the project:* Supports treating benchmark construction as part of the measurement instrument and requires separate precision/recall and heterogeneous-sorter analyses.

### Garcia et al. 2026 — modular, CPU-capable sorter contrasts

**Garcia, S., Halcrow, C., Windolf, C., McKenzie, Z. M., Adkisson-Floro, P., Mayorquin, H. R., Dichter, B., Buccino, A. P., & Yger, P. (2026). Opening the black box: a modular approach to spike sorting. _eLife_ reviewed preprint, RP110588.** [https://doi.org/10.7554/eLife.110588.1](https://doi.org/10.7554/eLife.110588.1) · [official XML](https://cdn.elifesciences.org/preprints/110588/elife-preprint-110588-v1.xml)

Benchmarks components and end-to-end CPU pipelines including SpyKING CIRCUS 2, TriDesClous 2, and Lupin against Kilosort4. The official XML contains both the “key ingredients” and “core features” formulations used in project framing.

*How it informed the project:* Supplies feasible non-Kilosort candidate sorters and clears the quotation-verification debt without relying on a secondary rendering.

### Garcia, Buccino, and Yger 2022 — collision-dependent sorter differences

**Garcia, S., Buccino, A. P., & Yger, P. (2022). How do spike collisions affect spike sorting performance? _eNeuro_, 9(5), ENEURO.0105-22.2022.** [https://doi.org/10.1523/ENEURO.0105-22.2022](https://doi.org/10.1523/ENEURO.0105-22.2022)

Defines collision recall and shows large differences between template-matching and density-based sorter families at short temporal separations.

*How it informed the project:* Makes short-ISI/collision recall a required temporal-axis outcome and justifies a heterogeneous sorter panel.

### Jia et al. 2019 — region-specific multichannel waveforms

**Jia, X., Siegle, J. H., Bennett, C., Gale, S. D., Denman, D. J., Koch, C., & Olsen, S. R. (2019). High-density extracellular probes reveal dendritic backpropagation and facilitate neuron classification. _Journal of Neurophysiology_, 121(5), 1831–1847.** [https://doi.org/10.1152/jn.00680.2018](https://doi.org/10.1152/jn.00680.2018)

Finds distinct spatiotemporal extracellular waveform profiles across cortical and subcortical regions and improved region classification from multichannel features.

*How it informed the project:* Provides empirical warrant that region matching can change sorter-relevant waveform structure rather than only a label.

### Pouzat et al. 2004 — short-ISI amplitude dynamics

**Pouzat, C., Delescluse, M., Viot, P., & Diebolt, J. (2004). Improved spike-sorting by modeling firing statistics and burst-dependent spike amplitude attenuation: a Markov chain Monte Carlo approach. _Journal of Neurophysiology_, 91(6), 2910–2928.** [https://doi.org/10.1152/jn.00227.2003](https://doi.org/10.1152/jn.00227.2003)

Models non-Poisson discharge statistics and event-amplitude decay at short ISIs inside a spike sorter.

*How it informed the project:* Establishes a sorter-relevant mechanism for the burst/history tier and shows why timing-only bursts without waveform coupling would be incomplete.

### Harris et al. 2001 — biological constraints for burst realism

**Harris, K. D., Hirase, H., Leinekugel, X., Henze, D. A., & Buzsáki, G. (2001). Temporal interaction between single spikes and complex spike bursts in hippocampal pyramidal cells. _Neuron_, 32(1), 141–149.** [https://doi.org/10.1016/S0896-6273(01)00447-0](https://doi.org/10.1016/S0896-6273(01)00447-0)

Shows that CA1 burst probability and length depend on recent firing history and correlate with extracellular amplitude.

*How it informed the project:* Supplies biological constraints for a manipulation check and argues against an arbitrary burst generator.

### Wouters, Kloosterman, and Bertrand 2021 — relocation-based hybrid ground truth

**Wouters, J., Kloosterman, F., & Bertrand, A. (2021). SHYBRID: A graphical tool for generating hybrid ground-truth spiking data for evaluating spike sorting performance. _Neuroinformatics_, 19(1), 141–158.** [https://doi.org/10.1007/s12021-020-09474-8](https://doi.org/10.1007/s12021-020-09474-8) · [relocation worker](https://github.com/jwouters91/shybrid/blob/master/hybridizer/threads.py) · [spike-train implementation](https://github.com/jwouters91/shybrid/blob/master/hybridizer/spikes.py)

Creates virtual units by moving spikes from an observed single unit to a different location on the probe. The published implementation reuses the observed spike times after a fixed shift and the per-spike template-fitting factors. The new insertion train is constructed without a supplied jitter vector, so the spike-train implementation assigns random sub-sample jitter by default. It therefore preserves observed train and fitted-amplitude structure, but not observed timing jitter or an unrestricted per-spike waveform shape.

*How it informed the project:* Provides a contrasting hybrid design that preserves more observed train and amplitude structure than the average-template-plus-generated-train pipeline while preventing the Study Guide from overclaiming that it transports all real waveform variability.

### Yger et al. 2018 — paired versus hybrid performance scales

**Yger, P., Spampinato, G. L. B., Esposito, E., et al. (2018). A spike sorting toolbox for up to thousands of electrodes validated with ground truth recordings in vitro and in vivo. _eLife_, 7, e34518.** [https://doi.org/10.7554/eLife.34518](https://doi.org/10.7554/eLife.34518)

Reports paired in-vitro and in-vivo errors and a hybrid comparison of SpyKING CIRCUS with Kilosort, while documenting compute/memory tradeoffs.

*How it informed the project:* Demonstrates that apparent performance depends strongly on ground-truth setting and provides a mechanistically different sorter lineage.

### SpikeInterface official hybrid tutorial and source

**SpikeInterface developers. Benchmark spike sorting with hybrid recordings.** [official tutorial](https://spikeinterface.readthedocs.io/en/latest/how_to/benchmark_with_hybrid_recordings.html) · [pinned 0.104.8 `hybrid_tools.py`](https://github.com/SpikeInterface/spikeinterface/blob/76c41846f88de3cc9dc5858d5c7f97dd6cb1955f/src/spikeinterface/generation/hybrid_tools.py) · [comparison module](https://spikeinterface.readthedocs.io/en/stable/modules/comparison.html)

Documents the template metadata, motion-aware injection, default sorter panel, and performance outputs. In SpikeInterface 0.104.8 (tag commit `76c41846f88de3cc9dc5858d5c7f97dd6cb1955f`), `generate_hybrid_recording()` passes the caller-supplied recording directly to `InjectTemplatesRecording` or `InjectDriftingTemplatesRecording`; it does not add a preprocessing stage. `scale_template_to_range()` applies one scalar division to each template array to reach the target range. The official tutorial high-pass filters and common-references its host before passing it to the generator.

*How it informed the project:* Confirms which axes require only configuration versus new code and defines the comparison outputs and reproducibility parameters that must be frozen. It also makes preprocessing order a caller-owned Rung 0 commitment rather than an upstream default: the host injection substrate must be constructed before injection, and the exact chain must be pinned. The linear rescaling path supports treating scale factor as a reported diagnostic rather than a separate matching covariate once rendered amplitude, effective SNR, placement, and provenance are gated; Rung 0 must still verify finite factors and no clipping or overflow.

### SpikeInterface Hybrid Template Library — repository and live metadata

**SpikeInterface developers. `hybrid_template_library`.** MIT. [repository](https://github.com/SpikeInterface/hybrid_template_library) · [live metadata CSV](https://spikeinterface-template-database.s3.amazonaws.com/templates.csv)

Hosts IBL Neuropixels 1.0 and Steinmetz/Ye Neuropixels Ultra templates with area, amplitude, SNR, depth, source dataset, and row identifiers. Direct 2026-08-11 audit: 7,877 rows total; 2,183 IBL/NP1 rows; 170 IBL area labels. The 2,183 NP1.0 rows contain only 187 distinct bare `template_index` integers because the index restarts within each dataset; (`dataset`, `template_index`) is unique for all 2,183. CSV SHA-256 `a6c86402924f8192a7b6fd91d5cce86a3e6f4b18816eddd8bde194524f720b8d`.

*How it informed the project:* Establishes broad region feasibility, replaces the stale 601-row tutorial snapshot, creates a snapshot/hash requirement, and requires the two-part dataset/index key for every selected donor configuration.

### Hybrid Template Library — IBL construction and metadata consolidation source

**SpikeInterface developers. `upload_ibl_templates.py` and `consolidate_datasets.py`.** [pinned IBL construction source](https://github.com/SpikeInterface/hybrid_template_library/blob/0023db29688842f74698bac40c48a86477ea39e7/python/upload_ibl_templates.py) · [pinned metadata consolidation source](https://github.com/SpikeInterface/hybrid_template_library/blob/0023db29688842f74698bac40c48a86477ea39e7/python/consolidate_datasets.py) · [SpikeInterface `IblSortingExtractor`](https://github.com/SpikeInterface/spikeinterface/blob/main/src/spikeinterface/extractors/iblextractors.py)

The IBL library builder combines DANDI raw recordings with IBL sorting data and applies `astype(float32)` → Neuropixels `phase_shift` → 1 Hz high-pass → common reference before template extraction; it stores the sorting's `brain_area` property. The consolidation step derives `depth_along_probe` from each template's best-channel probe coordinate. `IblSortingExtractor` maps the IBL cluster `acronym` field to the `brain_area` property.

*How it informed the project:* Prevented the Tier A selection artifact from claiming that host and donor necessarily share one preprocessing chain, and bounded the CCF bridge result correctly: comparing donor acronym/depth with the NWB electrode table is a strong internal-consistency check across upstream representations, not an independent validation of IBL's atlas registration. Combined with the 0.104.8 generator source, it confirms Claude's Rung 0 warning: injecting these already-phase-shifted templates into a raw host and phase-shifting the combined recording would transform injected spikes twice but real host spikes once. Build and pin the injection substrate first; do not rely on the generator to do it.

### DANDI 000409 — IBL Brain Wide Map

**International Brain Laboratory et al. IBL — Brain Wide Map. DANDI:000409.** CC-BY-4.0. [DANDI record](https://dandiarchive.org/dandiset/000409/draft) · [pinned IBL-to-NWB sorting documentation](https://github.com/catalystneuro/IBL-to-nwb/blob/54030ac4eb40a74978ac1f6ef6e966278b9d3f34/documentation/conversion/sorting_interface.md) · [pinned sorting extractor](https://github.com/catalystneuro/IBL-to-nwb/blob/54030ac4eb40a74978ac1f6ef6e966278b9d3f34/src/ibl_to_nwb/datainterfaces/_ibl_sorting_extractor.py) · [pinned raw timestamp alignment](https://github.com/catalystneuro/IBL-to-nwb/blob/54030ac4eb40a74978ac1f6ef6e966278b9d3f34/src/ibl_to_nwb/converters/_ibl_spikeglx_converter.py)

Open NWB host-recording collection with 2,048 assets, approximately 49.7 TB, and 139 subjects.

*How it informed the project:* Defines the host-data universe, license/attribution obligation, and need for a small identifier-pinned subset rather than bulk download. The DANDI record identifies `catalystneuro/IBL-to-nwb` as the conversion repository. At pinned repository commit `54030ac4eb40a74978ac1f6ef6e966278b9d3f34`, the conversion documentation defines exported `spike_times` as IBL `spikes.times.npy` in seconds from session start, while the raw converter aligns AP samples through `SpikeSortingLoader.samples2times`. This fixes the drift screen's grid on one session-time coordinate and makes endpoint containment a consistency check rather than a method for choosing between clock hypotheses.

### NWB and HDMF format specifications — ragged-array index dtype

**Neurodata Without Borders and HDMF developers. Format specifications.** [NWB format](https://nwb-schema.readthedocs.io/en/stable/format.html) · [HDMF common format](https://hdmf-common-schema.readthedocs.io/en/stable/format.html)

The NWB `Units/spike_times_index` field extends the HDMF `VectorIndex` type. The HDMF common schema specifies unsigned-integer storage for `VectorIndex`, so a floating-point ragged index is not schema-valid merely because all stored values happen to be whole numbers.

*How it informed the project:* Settles RC-002's F2 repair boundary for `spike_times_index` and the parallel `spike_depths_index`: both must be stored with integer dtype before conversion. It does not by itself decide the storage policy for the project's custom `max_electrode` column.

## Pending verification

None. Claims retained in the Phase 0 foundation were checked against the linked primary or first-party source. Host-recording/template joint feasibility remains an empirical design question, not an unverified citation.
