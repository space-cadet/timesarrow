"use strict";
/**
 * TimesArrow Numerics — Unified simulation package
 *
 * Core modules:
 * - intertwiner: SU(2) intertwiner states, volume operator
 * - z2GaugeTheory: Z₂ lattice gauge theory utilities
 *
 * Task modules (to be added):
 * - t25: Volume operator extension
 * - t20: Z₂ LGT Monte Carlo
 * - t23: Entanglement entropy
 * - t22: Spin foam amplitudes
 * - t21: CZX PEPS
 * - t24: Domain wall dynamics
 * - t26: Coupled matter
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
__exportStar(require("./core/intertwiner.js"), exports);
__exportStar(require("./core/z2GaugeTheory.js"), exports);
//# sourceMappingURL=index.js.map