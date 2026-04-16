# Task Registry
*Last Updated: 2026-04-16 23:25:00 IST*

## Active Tasks
| ID | Title | Status | Priority | Started | Dependencies | Owner | Details |
|----|-------|--------|----------|---------|--------------|-------|---------|
| T7 | Trim MPS Pedagogy and Appendices | 🔄 IN PROGRESS | MEDIUM | 2026-04-16 | - | Assistant | [Details](tasks/T7.md) |
| T8 | Fix Typos and Cleanup | ⏸️ PAUSED | LOW | - | T7 | Assistant | [Details](tasks/T8.md) |

## Task Details

### T3: Rewrite z2-action-derivation.tex
**Description**: Completely rewrote Section 7 with four subsections: Z2 field definition, effective action, phase structure (Elitzur remark), and cosmological transition (QECC).
**Status**: ✅ COMPLETED
**Last Active**: 2026-04-16 23:00:00 IST
**Completion Criteria**:
- [x] Define Z2 gauge field on edges
- [x] Derive Ising gauge effective action
- [x] Analyze phases with Wilson loop
- [x] Address Elitzur's theorem

**Related Files**:
- `z2-action-derivation.tex`
- `timesarrow.tex`

### T4: Rewrite spt-lqg-mapping.tex
**Description**: Expanded Section 6 with four subsections: CZX structural correspondence, j=1/2 dominance, SPT=deconfined identification, and edge modes conjecture.
**Status**: ✅ COMPLETED
**Last Active**: 2026-04-16 23:00:00 IST
**Completion Criteria**:
- [x] CZX-to-intertwiner mapping
- [x] j=1/2 justification
- [x] SPT=deconfined phase
- [x] Edge modes conjecture

**Related Files**:
- `spt-lqg-mapping.tex`
- `timesarrow.tex`

### T5: Update Title and Abstract
**Description**: Changed title to emphasize confinement-deconfinement and rewrote abstract for technical completeness.
**Status**: ✅ COMPLETED
**Last Active**: 2026-04-16 23:05:00 IST
**Completion Criteria**:
- [x] New title integrated
- [x] Abstract fully rewritten

**Related Files**:
- `timesarrow.tex`

### T6: Revise Discussion Section
**Description**: Added new subsections on Elitzur's Theorem, QECC stability, and Hopf algebraic perspectives.
**Status**: ✅ COMPLETED
**Last Active**: 2026-04-16 23:10:00 IST
**Completion Criteria**:
- [x] Elitzur's Theorem sub-section
- [x] QECC stability sub-section
- [x] Hopf algebras sub-section

**Related Files**:
- `timesarrow.tex`

### T7: Trim MPS Pedagogy and Appendices
**Description**: Cut Sec 3 by ~50% (move pedagogy to appendix or cite Bridgeman-Chubb). Shorten Appendix D.
**Status**: 🔄 IN PROGRESS
**Last Active**: 2026-04-16 23:25:00 IST
**Completion Criteria**:
- [ ] Section 3 reduced to core elements
- [ ] Appendix D condensed

**Related Files**:
- `timesarrow.tex`

## Completed Tasks
| ID | Title | Completed | Related Tasks |
|----|-------|-----------|---------------|
| T0 | Project Examination | 2026-04-16 | - |
| T1 | Initial Memory Bank Population | 2026-04-16 | - |
| T2 | Critical Manuscript Review & Rewrite Plan | 2026-04-16 | - |
| T3 | Rewrite z2-action-derivation.tex | 2026-04-16 | - |
| T4 | Rewrite spt-lqg-mapping.tex | 2026-04-16 | - |
| T5 | Update Title and Abstract | 2026-04-16 | - |
| T6 | Revise Discussion Section | 2026-04-16 | - |

## Task Relationships
```mermaid
graph TD
    T1[T1: Initial Memory Bank Population]
    T2[T2: Critical Review & Plan]
    T3[T3: Rewrite z2-action]
    T4[T4: Rewrite spt-lqg]
    T5[T5: Title & Abstract]
    T6[T6: Discussion Revision]
    T7[T7: Trim Pedagogy]
    T8[T8: Cleanup]
    T0[T0: Project Examination]
    
    T0 --> T1
    T1 --> T2
    T2 --> T3
    T2 --> T4
    T3 --> T5
    T4 --> T5
    T5 --> T6
    T6 --> T7
    T7 --> T8
```
