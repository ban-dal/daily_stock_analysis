import { describe, expect, it } from 'vitest';

import { getSentimentLabel } from '../../types/analysis';
import { getReportText, normalizeReportLanguage } from '../reportLanguage';

describe('reportLanguage utils', () => {
  it('normalizes Korean compatibility aliases to ko', () => {
    expect(normalizeReportLanguage('ko')).toBe('ko');
    expect(normalizeReportLanguage('kr')).toBe('ko');
    expect(normalizeReportLanguage('ko-KR')).toBe('ko');
  });

  it('returns Korean fixed report copy and sentiment labels', () => {
    expect(getReportText('kr').fullReport).toBe('전체 분석 보고서');
    expect(getSentimentLabel(80, 'ko')).toBe('낙관');
  });
});
