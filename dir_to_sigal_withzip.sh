#!/bin/sh

# Documentation: https://github.com/novoid/sigal_gallery_from_filetags_files

set -o errexit  ## halt on any error

FILENAME=$(basename $0)
DIR="${1}"
SANITIZED_DIR=$(echo $DIR|sed 's/ /_/g')
TMPDIR="${HOME}/tmp/Tools/sigal_gallery_from_filetags_files"
SCRIPTDIR="${HOME}/src/sigal_gallery_from_filetags_files"
DESTDIR="${HOME}/share/karl-voit.at/albums"

#echo "$FILENAME:  DEBUG:  DIR: $DIR"
#echo "$FILENAME:  DEBUG:  SANITIZED_DIR: $SANITIZED_DIR"
#echo "$FILENAME:  DEBUG:  TMPDIR: $TMPDIR"
#echo "$FILENAME:  DEBUG:  SCRIPTDIR: $SCRIPTDIR"
#echo "$FILENAME:  DEBUG:  DESTDIR: $DESTDIR"

errorexit()
{
    [ "$1" -lt 1 ] && echo "$FILENAME done."
    if [ "$1" -gt 0 ]; then
        echo
        echo "$FILENAME aborted with errorcode $1:  $2"
        echo
    fi

    exit $1
}

[ -d "${DIR}" ] || errorexit 1 "\"${DIR}\" is not a directory. Please provide a directory containing images for processing with sigal."

echo "\n$FILENAME: copying directory $DIR to temporary directory…    (${TMPDIR})\n"
cp -r "${DIR}" "${TMPDIR}"/

cd "${TMPDIR}"/

echo "\n$FILENAME: generating meta-data files…\n"
"${SCRIPTDIR}/generate_sigal_md.py" "${TMPDIR}"/"${DIR}"

echo "\n$FILENAME: generating gallery…\n"
sigal build -c "${SCRIPTDIR}/sigal.conf_ZIP.py" -n 3 "${DIR}" "${DESTDIR}/${SANITIZED_DIR}"

echo "$FILENAME: deleting temporary directory…    (${TMPDIR}/${DIR})\n"
rm -r "${TMPDIR}"/"${DIR}"

echo "\n$FILENAME: ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\n"
echo "$FILENAME:    test with:\n"
echo "  sigal serve -c \"${SCRIPTDIR}/sigal.conf_ZIP.py\" \"${DESTDIR}/${SANITIZED_DIR}\"\n"
echo "$FILENAME:    URL: https://Karl-Voit.at/albums/${SANITIZED_DIR}/\n"
echo "$FILENAME:    finished successfully.\n"

#end
