import React from 'react';
import { Sprout, Droplets, AlertTriangle, UserCheck, Play, ArrowRight, SunMedium, Wind } from 'lucide-react';
import { Language, translations } from '../i18n/translations';
import { AdvisoryCard } from '../components/AdvisoryCard';

interface OverviewTabProps {
  fields: any[];
  selectedFieldId: string | null;
  onSelectField: (id: string) => void;
  advisories: any[];
  weather: any[];
  onTriggerAdvisory: (fieldId: string) => Promise<void>;
  evaluating: boolean;
  lang: Language;
  onOpenReviewModal: (advisory: any) => void;
  onOpenFeedbackModal: (advisory: any) => void;
}

export const OverviewTab: React.FC<OverviewTabProps> = ({
  fields,
  selectedFieldId,
  onSelectField,
  advisories,
  weather,
  onTriggerAdvisory,
  evaluating,
  lang,
  onOpenReviewModal,
  onOpenFeedbackModal
}) => {
  const t = translations[lang];

  const currentField = fields.find((f) => f.id === selectedFieldId) || fields[0];
  const pendingReviewCount = advisories.filter((a) => a.review_status === 'pending_review').length;
  const highAlertCount = advisories.filter((a) => a.requires_human_review).length;
  const latestWeather = weather[0] || {
    temperature_c: 36.5,
    relative_humidity_pct: 64,
    wind_speed_kmh: 14,
    rainfall_mm_last_24h: 0.0,
    forecast_rain_next_24h_mm: 0.0
  };

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <Sprout size={20} />
            </div>
            <div>
              <p className="text-xs text-slate-500">{t.overview.totalFields}</p>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white">{fields.length}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <Droplets size={20} />
            </div>
            <div>
              <p className="text-xs text-slate-500">{t.overview.avgMoisture}</p>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white">21.8%</h3>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center">
              <AlertTriangle size={20} />
            </div>
            <div>
              <p className="text-xs text-slate-500">{t.overview.activeAlerts}</p>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white">{highAlertCount}</h3>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center">
              <UserCheck size={20} />
            </div>
            <div>
              <p className="text-xs text-slate-500">{t.overview.pendingReview}</p>
              <h3 className="text-xl font-bold text-slate-900 dark:text-white">{pendingReviewCount}</h3>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Action & Weather Snapshot */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trigger Bounded Advisory */}
        <div className="lg:col-span-2 bg-gradient-to-br from-slate-900 to-slate-800 rounded-2xl p-6 text-white border border-emerald-500/30 shadow-md">
          <div className="flex items-center justify-between mb-4">
            <div>
              <span className="text-xs font-mono font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 uppercase tracking-wider">
                Autonomous Bounded Pipeline
              </span>
              <h2 className="text-lg font-bold mt-1 text-white">{t.overview.quickActionTitle}</h2>
            </div>
          </div>

          <p className="text-xs text-slate-300 mb-6">
            Executes the 7-stage pipeline: COLLECT telemetry, VALIDATE & PII mask, ANALYZE deterministic risks, RETRIEVE TNAU/ICAR citations, COMPOSE bilingual advisory, and enforce the Human Review Gate.
          </p>

          <div className="flex flex-wrap items-center gap-3">
            <div className="flex-1 min-w-[220px]">
              <label className="block text-[11px] font-semibold text-slate-400 mb-1">{t.overview.selectField}</label>
              <select
                value={selectedFieldId || ''}
                onChange={(e) => onSelectField(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-slate-800 border border-slate-700 text-xs text-white focus:ring-2 focus:ring-emerald-500"
              >
                {fields.map((f) => (
                  <option key={f.id} value={f.id}>
                    {f.name} ({f.area_hectares} ha - {f.soil_type})
                  </option>
                ))}
              </select>
            </div>

            <div className="mt-5">
              <button
                onClick={() => currentField && onTriggerAdvisory(currentField.id)}
                disabled={evaluating || !currentField}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-slate-950 font-bold text-xs transition shadow-lg shadow-emerald-500/20"
              >
                <Play size={14} fill="currentColor" />
                <span>{evaluating ? 'Evaluating Pipeline...' : t.overview.evaluateBtn}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Live Weather Card */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3 mb-4">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <SunMedium className="text-amber-500" size={18} />
              {t.overview.weatherOverview}
            </h3>
            <span className="text-[11px] font-mono text-slate-400">IMD Erode AWS</span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-slate-500">Air Temperature</span>
              <strong className="text-slate-900 dark:text-white text-base font-mono">{latestWeather.temperature_c}°C</strong>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500">Relative Humidity</span>
              <strong className="text-slate-900 dark:text-white font-mono">{latestWeather.relative_humidity_pct}%</strong>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-500">Wind Velocity</span>
              <strong className="text-slate-900 dark:text-white font-mono">{latestWeather.wind_speed_kmh} km/h</strong>
            </div>
            <div className="flex items-center justify-between border-t border-slate-100 dark:border-slate-800 pt-2">
              <span className="text-slate-500">24h Precip Forecast</span>
              <strong className="text-emerald-600 dark:text-emerald-400 font-mono">{latestWeather.forecast_rain_next_24h_mm} mm</strong>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Advisories Feed */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-bold text-slate-900 dark:text-white">
            {t.overview.recentAdvisories}
          </h2>
          <span className="text-xs text-slate-400">Showing latest evidence-grounded alerts</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {advisories.slice(0, 4).map((adv) => (
            <AdvisoryCard
              key={adv.id}
              advisory={adv}
              lang={lang}
              onOpenReviewModal={onOpenReviewModal}
              onOpenFeedbackModal={onOpenFeedbackModal}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
