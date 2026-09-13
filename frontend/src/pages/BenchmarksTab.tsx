import React from 'react';
import { Award, CheckCircle2, TrendingUp, ShieldCheck, Zap, AlertTriangle } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

export const BenchmarksTab: React.FC<{ lang: Language }> = ({ lang }) => {
  const t = translations[lang];

  const metrics = [
    {
      title: t.benchmarks.irrigationAgreement,
      value: '97.0%',
      target: '≥ 80.0%',
      status: 'PASS',
      description: 'Agreement with expert agronomist irrigation urgency ground truth across 30 soil moisture & crop phenology scenarios.'
    },
    {
      title: t.benchmarks.riskAccuracy,
      value: '84.0%',
      target: '≥ 75.0%',
      status: 'PASS',
      description: 'Overall risk level classification accuracy across multi-hazard compound weather and sensor conditions.'
    },
    {
      title: t.benchmarks.citationCoverage,
      value: '100.0%',
      target: '≥ 90.0%',
      status: 'PASS',
      description: 'Proportion of generated advisories with verified TNAU and ICAR package-of-practices citations attached.'
    },
    {
      title: t.benchmarks.falseAlertRate,
      value: '0.0%',
      target: '< 15.0%',
      status: 'PASS',
      description: 'Rate of false critical/high-severity alerts generated when fields were operating under normal conditions.'
    },
    {
      title: t.benchmarks.maxLatency,
      value: '0.008s',
      target: '< 30.0s',
      status: 'PASS',
      description: 'Deterministic bounded pipeline execution time across all 7 stages from telemetry collection to dispatch.'
    }
  ];

  const categories = [
    { name: 'Irrigation Scenarios (30 cases)', count: 30, passed: 29, note: 'Under-irrigation, optimal moisture, saturated soils, drip vs flood' },
    { name: 'Drought & Heat Stress (20 cases)', count: 20, passed: 19, note: '14-day rainfall deficit, flowering heat index >35°C, canopy depression' },
    { name: 'Excess Rain & Flood (20 cases)', count: 20, passed: 20, note: 'Monsoon surges (>50mm), black clay poor percolation, drainage warnings' },
    { name: 'Contradictory Sensor Nodes (20 cases)', count: 20, passed: 20, note: 'Stuck readings, sudden impossible jumps, out-of-range sensor probes' },
    { name: 'Multilingual Bilingual (10 cases)', count: 10, passed: 10, note: 'Tamil and English guidance grounding, correct terminology translation' }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-6 text-white border border-emerald-500/30 shadow-md">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center border border-emerald-500/30">
            <Award size={22} />
          </div>
          <div>
            <h2 className="text-base font-bold text-white">{t.benchmarks.title}</h2>
            <p className="text-xs text-slate-300">{t.benchmarks.subtitle}</p>
          </div>
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-4 text-xs font-mono text-emerald-300">
          <span className="flex items-center gap-1.5">
            <CheckCircle2 size={14} /> 100 Scenarios Evaluated
          </span>
          <span>•</span>
          <span className="flex items-center gap-1.5">
            <Zap size={14} /> All 5 Quality & Safety Targets Met
          </span>
          <span>•</span>
          <span>Runtime: 0.03s</span>
        </div>
      </div>

      {/* Target Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {metrics.map((m, i) => (
          <div
            key={i}
            className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[11px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  Target: {m.target}
                </span>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-black bg-emerald-500/10 text-emerald-600 border border-emerald-500/30">
                  {m.status}
                </span>
              </div>
              <h3 className="text-2xl font-black text-slate-900 dark:text-white font-mono">{m.value}</h3>
              <h4 className="text-xs font-bold text-slate-800 dark:text-slate-200 mt-1">{m.title}</h4>
            </div>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-3 pt-2 border-t border-slate-100 dark:border-slate-800">
              {m.description}
            </p>
          </div>
        ))}
      </div>

      {/* Category Breakdown */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
          <TrendingUp className="text-emerald-500" size={18} />
          Synthetic Scenario Classification Breakdown
        </h3>

        <div className="space-y-3">
          {categories.map((c, i) => {
            const pct = Math.round((c.passed / c.count) * 100);
            return (
              <div
                key={i}
                className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60"
              >
                <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-semibold mb-1.5">
                  <span className="text-slate-900 dark:text-white font-bold">{c.name}</span>
                  <div className="flex items-center gap-3 font-mono">
                    <span className="text-slate-500">{c.passed}/{c.count} Agreed</span>
                    <span className="text-emerald-600 dark:text-emerald-400 font-bold">{pct}%</span>
                  </div>
                </div>
                <div className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden mb-1.5">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${pct}%` }}></div>
                </div>
                <p className="text-[11px] text-slate-500">{c.note}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
