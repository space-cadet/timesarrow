/**
 * T35a: 2D Square Plaquette — CZX vs Intertwiner Overlap Test
 *
 * This script tests which CZX-symmetric states are also in the
 * gauge-invariant (intertwiner) subspace.
 */

const {
  StateVector,
  MatrixOperator,
} = require('/Users/deepak/code/ts-quantum/dist/index.js');

const math = require('mathjs');

const TOLERANCE = 1e-10;

function createPlaquetteCZX() {
  const DIM = 16;
  const matrix = [];
  for (let i = 0; i < DIM; i++) {
    const row = [];
    for (let j = 0; j < DIM; j++) {
      row.push(math.complex(0, 0));
    }
    matrix.push(row);
  }

  for (let input = 0; input < DIM; input++) {
    const cz12 = ((input >> 3) & 1) * ((input >> 2) & 1);
    const cz23 = ((input >> 2) & 1) * ((input >> 1) & 1);
    const cz34 = ((input >> 1) & 1) * ((input >> 0) & 1);
    const cz41 = ((input >> 0) & 1) * ((input >> 3) & 1);
    const phase = (cz12 + cz23 + cz34 + cz41) % 2 === 0 ? 1 : -1;
    const flipped = input ^ 0b1111;
    matrix[flipped][input] = math.complex(phase, 0);
  }

  return new MatrixOperator(matrix, 'unitary', false);
}

function constructGaugeInvariantState() {
  const amplitudes = Array(16).fill(math.complex(0, 0));

  for (let config = 0; config < 16; config++) {
    const e1 = (config >> 3) & 1;
    const e2 = (config >> 2) & 1;
    const e3 = (config >> 1) & 1;
    const e4 = (config >> 0) & 1;

    const v1Amp = (e1 === 0 && e2 === 1) ? 1 : (e1 === 1 && e2 === 0) ? -1 : 0;
    const v2Amp = (e2 === 0 && e3 === 1) ? 1 : (e2 === 1 && e3 === 0) ? -1 : 0;
    const v3Amp = (e3 === 0 && e4 === 1) ? 1 : (e3 === 1 && e4 === 0) ? -1 : 0;
    const v4Amp = (e4 === 0 && e1 === 1) ? 1 : (e4 === 1 && e1 === 0) ? -1 : 0;

    const totalAmp = v1Amp * v2Amp * v3Amp * v4Amp;
    if (totalAmp !== 0) {
      amplitudes[config] = math.complex(totalAmp, 0);
    }
  }

  const norm = Math.sqrt(amplitudes.reduce((sum, amp) => sum + math.abs(amp) ** 2, 0));
  const normalizedAmps = amplitudes.map((amp) => math.divide(amp, math.complex(norm, 0)));
  return new StateVector(16, normalizedAmps);
}

function findCZXSymmetricStates() {
  const czx = createPlaquetteCZX();
  const { values, vectors } = czx.eigenDecompose();

  const plusOneStates = [];
  for (let i = 0; i < values.length; i++) {
    const ev = values[i].re;
    if (Math.abs(ev - 1) < TOLERANCE && Math.abs(values[i].im) < TOLERANCE) {
      const vecMatrix = vectors[i].toMatrix();
      const amplitudes = [];
      for (let j = 0; j < vecMatrix.length; j++) {
        amplitudes.push(vecMatrix[j][j]);
      }
      const state = new StateVector(16, amplitudes);
      if (!state.isZero()) {
        plusOneStates.push(state.normalize());
      }
    }
  }

  return plusOneStates;
}

function main() {
  console.log('=== T35a: CZX vs Intertwiner Overlap Test ===\n');

  const gaugeInvariantState = constructGaugeInvariantState();
  console.log('Gauge-invariant state (intertwiner product):');
  console.log(`  ${gaugeInvariantState.toString()}`);
  console.log();

  const czxStates = findCZXSymmetricStates();
  console.log(`Found ${czxStates.length} CZX-symmetric states`);
  console.log();

  console.log('Overlap with gauge-invariant state:');
  let maxOverlap = 0;
  let bestMatch = -1;

  for (let i = 0; i < czxStates.length; i++) {
    const overlap = gaugeInvariantState.innerProduct(czxStates[i]);
    const absOverlap = math.abs(overlap);
    console.log(`  State ${i + 1}: |overlap| = ${absOverlap.toFixed(6)}`);

    if (absOverlap > maxOverlap) {
      maxOverlap = absOverlap;
      bestMatch = i;
    }
  }
  console.log();

  if (bestMatch >= 0) {
    console.log(`Best match: State ${bestMatch + 1} with overlap ${maxOverlap.toFixed(6)}`);
    if (maxOverlap > 1 - TOLERANCE) {
      console.log('→ This CZX-symmetric state IS the gauge-invariant state!');
    } else if (maxOverlap > 0.5) {
      console.log('→ Partial overlap - state is a superposition of gauge-invariant and non-invariant states');
    } else {
      console.log('→ No significant overlap - CZX-symmetric states are orthogonal to gauge-invariant state');
    }
  }

  console.log();
  console.log('=== Summary ===');
  console.log(`Total CZX-symmetric states: ${czxStates.length}`);
  console.log(`Gauge-invariant states in CZX +1 eigenspace: ${maxOverlap > 1 - TOLERANCE ? 1 : 0}`);
  console.log(`Max overlap: ${maxOverlap.toFixed(6)}`);
}

main();
