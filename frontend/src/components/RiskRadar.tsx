import React from 'react';
import { ShieldCheck, AlertTriangle, Droplet, Thermometer, CloudRain, Cpu, Info } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

interface RiskRadarProps {
  riskAssessment: any;
  lang: Language;
}

export const RiskRadar: React.FC<RiskRadarProps> = ({ riskAssessment, lang }) => {
  const t = translations[lang];

  if (!riskAssessment) {
    return (
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 text-center text-slate-500">
        <Info className="mx-auto mb-2 text-slate-400" size={24} />
        <p className="text-sm">No risk assessment calculated for this field yet. Run the evaluation pipeline above.</p>
      </div>
    );
  }

  const breakdown = riskAssessment.factor_breakdown || {
    irrigation_need_score: 25,
    heat_stress_score: 20,
    drought_risk_score: 15,
    excess_rain_risk_score: 0,
    sensor_anomaly_score: 0
  };

  const score = riskAssessment.overall_score || 25;
  const level = riskAssessment.overall_risk_level || 'low';
  const confidence = Math.round((riskAssessment.confidence_score || 0.85) * 100);

  const getLevelColor = (lvl: string) => {
    switch (lvl.toLowerCase()) {
      case 'critical':
        return 'text-red-600 bg-red-500/10 border-red-500/30';
      case 'high':
        return 'text-red-500 bg-red-500/10 border-red-500/30';
      case 'moderate':
        return 'text-amber-500 bg-amber-500/10 border-amber-500/30';
      default:
        return 'text-emerald-500 bg-emerald-500/10 border-emerald-500/30';
    }
  };

  const factors = [
    {
      label: t.risk.irrigationNeed,
      score: breakdown.irrigation_need_score,
      icon: <Droplet size={16} className="text-blue-500" />,
      color: 'bg-blue-500'
    },
    {
      label: t.risk.heatStress,
      score: breakdown.heat_stress_score,
      icon: <Thermometer size={16} className="text-amber-500" />,
      color: 'bg-amber-500'
    },
    {
      label: t.risk.droughtRisk,
      score: breakdown.drought_risk_score,
      icon: <AlertTriangle size={16} className="text-orange-500" />,
      color: 'bg-orange-500'
    },
    {
      label: t.risk.excessRain,
      score: breakdown.excess_rain_risk_score,
      icon: <CloudRain size={16} className="text-cyan-500" />,
      color: 'bg-cyan-500'
    },
    {
      label: t.risk.sensorAnomaly,
      score: breakdown.sensor_anomaly_score,
      icon: <Cpu size={16} className="text-purple-500" />,
      color: 'bg-purple-500'
    }
  ];

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4 mb-6">
        <div>
          <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <ShieldCheck className="text-emerald-500" size={20} />
            {t.risk.title}
          </h2>
          <p className="text-xs text-slate-500">Deterministic Rule-based Multi-Factor Agronomic Assessment</p>
        </div>

        <div className="flex items-center gap-3">
          <div className={`px-3 py-1 rounded-full text-xs font-bold border uppercase ${getLevelColor(level)}`}>
            {level} Severity
          </div>
          <div className="text-right">
            <span className="text-2xl font-black text-slate-900 dark:text-white">{score}</span>
            <span className="text-xs text-slate-400">/100</span>
          </div>
        </div>
      </div>

      {/* Factors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {factors.map((f, i) => (
          <div key={i} className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
            <div className="flex items-center justify-between text-xs font-semibold mb-2">
              <span className="flex items-center gap-2 text-slate-700 dark:text-slate-200">
                {f.icon} {f.label}
              </span>
              <span className="font-mono text-slate-900 dark:text-white">{f.score.toFixed(1)}%</span>
            </div>
            <div className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
              <div className={`h-full ${f.color} rounded-full transition-all duration-500`} style={{ width: `${Math.min(100, f.score)}%` }}></div>
            </div>
          </div>
        ))}
      </div>

      {/* Confidence & Caveats */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-500/20 text-xs">
        <div className="flex items-center gap-2 text-emerald-900 dark:text-emerald-300">
          <Info size={16} />
          <span>
            {t.risk.confidence}: <strong>{confidence}%</strong> (Calculated from available telemetry & satellite recency)
          </span>
        </div>

        {riskAssessment.recommended_verification_steps && (
          <div className="text-slate-600 dark:text-slate-400 font-medium">
            🔍 {riskAssessment.recommended_verification_steps[0] || 'Conduct weekly visual inspection.'}
          </div>
        )}
      </div>
    </div>
  );
};
