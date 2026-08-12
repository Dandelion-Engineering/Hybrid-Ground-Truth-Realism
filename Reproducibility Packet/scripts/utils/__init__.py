"""Shared helpers for the Hybrid Ground Truth Realism scripts.

Modules here hold logic used by more than one script, so that no script
copy-pastes another's implementation:

- ``remote_hdf5``      read a remote HDF5/NWB file over HTTP range requests
- ``dandi``            enumerate and address DANDI assets
- ``template_metadata`` fetch, screen, and describe the hybrid template library
- ``ccf_labels``       map Allen CCF long names to the acronyms the template
                       library's ``brain_area`` column uses
- ``anatomy_index``    validate the target/gap provenance of anatomy indexes
- ``host_anatomy``     read a host electrodes table and find contiguous
                       single-structure depth bands
"""
