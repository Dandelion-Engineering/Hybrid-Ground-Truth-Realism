"""Validate the configuration provenance carried by host-anatomy indexes."""


def validate_configuration(
    records,
    target,
    max_gap_um,
    legacy_target=None,
    legacy_max_gap_um=None,
):
    """Check that every anatomy record was built for the requested screen.

    Args:
        records: mapping from asset identifier to anatomy-index record.
        target: requested target-structure acronym, or None.
        max_gap_um: requested maximum within-band row gap in micrometres.
        legacy_target: explicit target assertion for old records that predate
            embedded configuration metadata.
        legacy_max_gap_um: explicit maximum-gap assertion for those old
            records.

    Returns:
        None. A successful return means all records have one configuration and
        it matches ``target`` and ``max_gap_um``.

    Raises:
        ValueError: if legacy provenance is undeclared or any record was built
            with a different target or gap threshold.
    """
    for asset_id, record in records.items():
        record_target = record.get("anatomy_target")
        record_gap = record.get("anatomy_max_gap_um")
        if record_target is None and "anatomy_target" not in record:
            if legacy_target is None or legacy_max_gap_um is None:
                raise ValueError(
                    "anatomy index contains legacy records without embedded target/gap "
                    "metadata; pass both --legacy-index-target and "
                    "--legacy-index-max-gap-um to assert the configuration explicitly, "
                    "or start a fresh index"
                )
            record_target = legacy_target
            record_gap = legacy_max_gap_um
        if record_target != target:
            raise ValueError(
                f"anatomy record {asset_id} was built for target {record_target!r}, "
                f"not requested target {target!r}"
            )
        if record_gap is None or float(record_gap) != float(max_gap_um):
            raise ValueError(
                f"anatomy record {asset_id} was built with max gap {record_gap!r} um, "
                f"not requested {max_gap_um!r} um"
            )
