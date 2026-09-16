"""Generate a REDCap Data Dictionary CSV for the N-of-1 pilot.

Emits the exact 18-column REDCap "Data Dictionary" import format so you can create
the project's instruments in one upload (Project Setup -> Designer -> Upload data
dictionary). Field definitions mirror study-protocol/03-data-infrastructure.md.

No device or dosing logic. The primary-endpoint instrument uses an OPAQUE block
label (A/B) so the active/placebo assignment stays blinded in REDCap; the mapping
lives only in the sealed allocation keyfile.

Usage
-----
    python redcap_dictionary.py --out ../redcap/redcap_data_dictionary.csv
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

# REDCap Data Dictionary column order (must match exactly for import)
HEADER = [
    "Variable / Field Name", "Form Name", "Section Header", "Field Type",
    "Field Label", "Choices, Calculations, OR Slider Labels", "Field Note",
    "Text Validation Type OR Show Slider Number", "Text Validation Min",
    "Text Validation Max", "Identifier?", "Branching Logic (Show field only if...)",
    "Required Field?", "Custom Alignment", "Question Number (surveys only)",
    "Matrix Group Name", "Matrix Ranking?", "Field Annotation",
]


def F(var, form, ftype, label, *, section="", choices="", note="",
      valid="", vmin="", vmax="", identifier="", branching="", required="",
      align="", qnum="", matrix="", rank="", annotation=""):
    return {
        "Variable / Field Name": var, "Form Name": form, "Section Header": section,
        "Field Type": ftype, "Field Label": label,
        "Choices, Calculations, OR Slider Labels": choices, "Field Note": note,
        "Text Validation Type OR Show Slider Number": valid,
        "Text Validation Min": vmin, "Text Validation Max": vmax,
        "Identifier?": identifier, "Branching Logic (Show field only if...)": branching,
        "Required Field?": required, "Custom Alignment": align,
        "Question Number (surveys only)": qnum, "Matrix Group Name": matrix,
        "Matrix Ranking?": rank, "Field Annotation": annotation,
    }

GRADE = "1, Grade 1 | 2, Grade 2 | 3, Grade 3 | 4, Grade 4 | 5, Grade 5"
SRC = "1, Oura | 2, Whoop | 3, Garmin | 4, Other"
YN = ""  # yesno type needs no choices

def build_fields() -> list[dict]:
    f: list[dict] = []

    # --- enrollment (record_id MUST be the first field in REDCap) ---
    f += [
        F("record_id", "enrollment", "text", "Record ID", required="y"),
        F("subject_code", "enrollment", "text", "Subject code (de-identified)",
          note="No name/DOB — de-identified code only", identifier=""),
        F("consent_date", "enrollment", "text", "Informed-consent date",
          valid="date_ymd", required="y"),
    ]

    # --- biomarker panel ---
    f += [F("bm_draw_date", "biomarkers", "text", "Blood draw date",
            section="Biomarker panel", valid="date_ymd", required="y"),
          F("bm_week", "biomarkers", "text", "Study week", valid="integer",
            vmin="0", vmax="16")]
    biomarkers = [
        ("hs_crp", "hs-CRP", "mg/L"), ("il_6", "IL-6", "pg/mL"),
        ("vegf", "VEGF", "pg/mL"), ("tgf_b1", "TGF-β1", "ng/mL"),
        ("p1np", "P1NP", "µg/L"), ("ctx", "CTX", "ng/mL"),
        ("bdnf", "BDNF", "ng/mL"), ("nfl", "NfL", "pg/mL"),
    ]
    for var, lab, unit in biomarkers:
        f.append(F(var, "biomarkers", "text", lab, note=f"Units: {unit}",
                   valid="number", vmin="0"))

    # --- wearables (daily) ---
    f += [
        F("wd_date", "wearables_daily", "text", "Date", section="Wearable telemetry",
          valid="date_ymd", required="y"),
        F("hrv_rmssd_ms", "wearables_daily", "text", "HRV (RMSSD)", note="ms",
          valid="number", vmin="0"),
        F("resting_hr_bpm", "wearables_daily", "text", "Resting HR", note="bpm",
          valid="integer", vmin="20", vmax="200"),
        F("sleep_efficiency_pct", "wearables_daily", "text", "Sleep efficiency",
          note="%", valid="number", vmin="0", vmax="100"),
        F("deep_min", "wearables_daily", "text", "Deep sleep", note="min",
          valid="integer", vmin="0"),
        F("rem_min", "wearables_daily", "text", "REM sleep", note="min",
          valid="integer", vmin="0"),
        F("total_sleep_min", "wearables_daily", "text", "Total sleep", note="min",
          valid="integer", vmin="0"),
        F("steps", "wearables_daily", "text", "Steps", valid="integer", vmin="0"),
        F("wd_source", "wearables_daily", "dropdown", "Device source", choices=SRC),
    ]

    # --- daily journal ---
    f += [F("jd_date", "journal_daily", "text", "Date", section="Daily journal",
            valid="date_ymd", required="y")]
    for var, lab in [("energy", "Energy"), ("recovery", "Recovery"),
                     ("sleep_quality", "Sleep quality"), ("focus", "Focus"),
                     ("mood", "Mood")]:
        f.append(F(f"jd_{var}", "journal_daily", "text", f"{lab} (1–10)",
                   valid="integer", vmin="1", vmax="10"))
    f += [
        F("jd_site_reaction", "journal_daily", "dropdown", "Infusion-site reaction",
          choices="0, None | 1, Mild | 2, Moderate | 3, Severe"),
        F("jd_notes", "journal_daily", "notes", "Free-text notes"),
    ]

    # --- functional stressor test ---
    f += [
        F("ft_date", "functional_test", "text", "Test date",
          section="Stressor recovery test", valid="date_ymd"),
        F("ft_protocol", "functional_test", "text", "Protocol",
          note="e.g. 5×10 max-effort eccentric quad"),
        F("ck_24", "functional_test", "text", "CK +24h", note="U/L", valid="number", vmin="0"),
        F("ck_48", "functional_test", "text", "CK +48h", note="U/L", valid="number", vmin="0"),
        F("ck_72", "functional_test", "text", "CK +72h", note="U/L", valid="number", vmin="0"),
    ]

    # --- primary endpoint (BLINDED: opaque block label) ---
    f += [
        F("pe_pair", "primary_endpoint", "text", "Block pair #",
          section="Primary endpoint (blinded)", valid="integer", vmin="1",
          annotation="@READONLY-after-lock"),
        F("pe_block", "primary_endpoint", "dropdown", "Block label",
          choices="A, Block A | B, Block B",
          note="Opaque label — active/placebo mapping stays sealed until unblinding"),
        F("pe_ck_auc", "primary_endpoint", "text", "Post-stressor CK AUC 0–72h",
          note="U/L·h", valid="number", vmin="0"),
    ]

    # --- adverse events ---
    f += [
        F("ae_date", "adverse_events", "text", "AE date", section="Adverse events",
          valid="date_ymd"),
        F("ae_desc", "adverse_events", "notes", "Event description"),
        F("ae_ctcae", "adverse_events", "dropdown", "CTCAE grade", choices=GRADE,
          note="Grade ≥3 → mandatory stop per protocol"),
        F("ae_related", "adverse_events", "yesno", "Related to intervention?"),
        F("ae_action", "adverse_events", "notes", "Action taken"),
        F("ae_resolved", "adverse_events", "yesno", "Resolved?"),
    ]
    return f


def write_dictionary(fields: list[dict], out: str) -> None:
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for row in fields:
            w.writerow(row)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="../redcap/redcap_data_dictionary.csv")
    args = ap.parse_args()
    fields = build_fields()
    write_dictionary(fields, args.out)
    forms = sorted({r["Form Name"] for r in fields})
    print(f"[redcap_dictionary] wrote {args.out}")
    print(f"  {len(fields)} fields across {len(forms)} instruments: {', '.join(forms)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
