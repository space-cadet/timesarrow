#!/bin/sh
# Rebuild the paper-ready TikZ drawings as vector PDF and 300 dpi PNG.
set -eu
cd "$(dirname "$0")"
task_build_dir=$(mktemp -d /tmp/intertwiner-chain-paper-figures.XXXXXX)
task_build_log="$task_build_dir/build.log"
if ! pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$task_build_dir" figure-set.tex > "$task_build_log" 2>&1; then
    echo "Figure compilation failed; diagnostics: $task_build_log"
    tail -30 "$task_build_log"
    exit 1
fi
cp "$task_build_dir/figure-set.pdf" intertwiner-chain-paper-figures.pdf
pdfseparate intertwiner-chain-paper-figures.pdf "$task_build_dir/page-%d.pdf"
page=1
for stem in 01-two-node-contraction 02-chain-triplet-insertion 03-triplet-multiplet; do
    cp "$task_build_dir/page-$page.pdf" "$stem.pdf"
    pdftoppm -png -r 300 -singlefile "$stem.pdf" "$stem" \
        >> "$task_build_dir/render.log" 2>&1
    page=$((page + 1))
done
echo "Exported 3 vector PDFs, 3 PNGs at 300 dpi, and the combined PDF."
if rg -q 'Overfull|Underfull|Warning|^!' "$task_build_log"; then
    rg 'Overfull|Underfull|Warning|^!' "$task_build_log" | tail -12
else
    echo "LaTeX diagnostics: no warnings or box overflows."
fi
echo "Build log: $task_build_log"
