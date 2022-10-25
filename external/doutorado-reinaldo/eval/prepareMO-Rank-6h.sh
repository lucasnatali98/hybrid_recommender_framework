#!/usr/bin/env bash

echo ""
echo "Parameters:"
for i; do
     echo "- $i"
done

DATASET=${1}
MO_01=${2}
MO_02=${3}
SO_01=${4}
SO_02=${5}

echo ""

mkdir -p ${DATASET}/RISK-6h
mv ${DATASET}/MO ${DATASET}/RISK-6h
mv ${DATASET}/SO ${DATASET}/RISK-6h
mv ${DATASET}/Predictions ${DATASET}/RISK-6h
rm -r ${DATASET}/Results

mkdir -p ${DATASET}/MO/R0
mkdir -p ${DATASET}/SO/R0

if [ "${DATASET}" = "Amazon" ]; then
    HOME="RISK-old"
else
    HOME="MF"
fi

cp ${DATASET}/${HOME}/MO/R0/MO_${MO_01}_E-false_S-false_* ${DATASET}/MO/R0/
cp ${DATASET}/${HOME}/MO/R0/MO_${MO_02}_E-false_S-false_* ${DATASET}/MO/R0/
cp ${DATASET}/${HOME}/SO/R0/SO_${SO_01}_E-false_* ${DATASET}/SO/R0/
cp ${DATASET}/${HOME}/SO/R0/SO_${SO_02}_E-false_* ${DATASET}/SO/R0/
