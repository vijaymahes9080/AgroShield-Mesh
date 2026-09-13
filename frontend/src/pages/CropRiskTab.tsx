import React, { useEffect, useState } from 'react';
import { RiskRadar } from '../components/RiskRadar';
import { Language, translations } from '../i18n/translations';
import { ShieldCheck, Play } from 'lucide-react';

interface CropRiskTabProps {
  fields: any[];
  selectedFieldId: string | null;
  onSelectField: (id: string) => void;
  lang: Language;
  onTriggerAdvisory: (fieldId: string) => Promise<void>;
  evaluating: boolean;
}

export const CropRiskTab: React.FC<CropRiskTabProps> = ({
  fields,
  selectedFieldId,
  onSelectField,
  lang,
  onTriggerAdvisory,
  evaluating
}) => {
  const t = translations[lang];
  const [riskData, setRiskData] = useState<any>(null);

  const currentField = fields.find((f) => f.id === selectedFieldId) || fields[0];

  useEffect(() => {
    if (currentField) {
      loadFieldRisk(currentField.id);
    }
  }, [currentField?.id]);

  const loadFieldRisk = async (fId: string) => {
    try {
      const res = await fetch(`/api/v1/fields/${fId}/risk-assessments?limit=1`);
      if (res.ok) {
        const data = await res.json();
        if (data.length > 0) {
          setRiskData(data[0]);
        } else {
          setRiskData(null);
        }
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      {/* Field selector bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div>
          <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <ShieldCheck className="text-emerald-500" size={18} />
            {t.risk.title}
          </h2>
          <p className="text-xs text-slate-500">Transparent Rule-based Multi-Factor Agronomic Assessment</p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={currentField?.id || ''}
            onChange={(e) => onSelectField(e.target.value)}
            className="px-3 py-1.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-xs font-semibold"
          >
            {fields.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name}
              </option>
            ))}
          </select>

          <button
            onClick={() => currentField && onTriggerAdvisory(currentField.id)}
            disabled={evaluating || !currentField}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold shadow-sm transition"
          >
            <Play size={13} fill="currentColor" />
            <span>{evaluating ? 'Evaluating...' : 'Re-calculate Risk'}</span>
          </button>
        </div>
      </div>

      {/* Main Risk Radar */}
      <RiskRadar riskAssessment={riskData} lang={lang} />
    </div>
  );
};
