const { parentPort } = require('worker_threads');

try {
  const tq = require('ts-quantum');
  parentPort.postMessage({
    type: 'success',
    hasBinData: typeof tq.binData === 'function',
    keys: Object.keys(tq).slice(0, 20)
  });
} catch (err) {
  parentPort.postMessage({
    type: 'error',
    message: err.message
  });
}
