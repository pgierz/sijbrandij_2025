#!/bin/bash
set -euo pipefail
###############################################################################
#
# Downloads the accompanying data from Zenodo
# https://doi.org/10.5281/zenodo.15497082
#
# Dr. Paul Gierz
# AWI Bremerhaven
###############################################################################

RECORD_ID="15497082"
ZENODO_URL="https://zenodo.org/api/records/${RECORD_ID}/files-archive"
DATA_DIR="data"
ZIP_FILE="data.zip"

cd "$(dirname "$0")"

if [[ -d "${DATA_DIR}" ]]; then
    echo "Data directory '${DATA_DIR}' already exists."
    read -rp "Re-download and overwrite? [y/N] " response
    case "${response}" in
        [yY][eE][sS]|[yY])
            rm -rf "${DATA_DIR}"
            ;;
        *)
            echo "Skipping download."
            exit 0
            ;;
    esac
fi

echo "Downloading data from Zenodo (record ${RECORD_ID})..."
if ! wget --progress=bar:force:noscroll -O "${ZIP_FILE}" "${ZENODO_URL}"; then
    echo "Error: Download failed." >&2
    rm -f "${ZIP_FILE}"
    exit 1
fi

echo "Extracting archive..."
if ! unzip -q "${ZIP_FILE}" -d "${DATA_DIR}"; then
    echo "Error: Extraction failed." >&2
    exit 1
fi

rm -f "${ZIP_FILE}"
echo "Done. Data available in '${DATA_DIR}/'."
