import React, { useEffect, useState } from 'react';
import { Cpu, BatteryCharging, AlertTriangle, CheckCircle2, Droplets, Thermometer, RefreshCw } from 'lucide-react';
import { Language, translations } from '../i18n/translations';
import { fetchFieldSensors } from '../services/api';

interface SensorsTabProps {
  fields: any[];
  selectedFieldId: string | null;
  onSelectField: (id: string) => void;
  lang: Language;
}

export const SensorsTab: React.FC<SensorsTabProps> = ({
  fields,
  selectedFieldId,
  onSelectField,
  lang
}) => {
  const t = translations[lang];
  const [sensors, setSensors] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const currentField = fields.find((f) => f.id === selectedFieldId) || fields[0];

  useEffect(() => {
    if (currentField) {
      loadSensors(currentField.id);
    }
  }, [currentField?.id]);

  const loadSensors = async (fId: string) => {
    setLoading(true);
    try {
      const data = await fetchFieldSensors(fId);
      setSensors(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const latestReading = sensors[0] || {
    device_id: 'AGRO-NODE-ERD-004',
    soil_moisture_pct: 21.8,
    soil_temperature_c: 27.5,
    ambient_temperature_c: 34.2,
    ambient_humidity_pct: 64,
    battery_pct: 94,
    anomaly_flag: false
  };

  return (
    <div className="space-y-6">
      {/* Header Selector */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div>
          <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Cpu className="text-emerald-500" size={18} />
            IoT Agricultural Mesh Network Telemetry
          </h2>
          <p className="text-xs text-slate-500">Wireless 868MHz Mesh • Ingestion Gateway with Anomaly Detection</p>
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
            onClick={() => currentField && loadSensors(currentField.id)}
            disabled={loading}
            className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          </button>
        </div>
      </div>

      {/* Primary Telemetry Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
          <span className="text-slate-500 text-xs flex items-center gap-1.5">
            <Droplets className="text-blue-500" size={15} />
            Soil Moisture (VWC)
          </span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold font-mono text-slate-900 dark:text-white">
              {latestReading.soil_moisture_pct}%
            </span>
            <span className="text-[11px] text-slate-400">Target: 25-35%</span>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
          <span className="text-slate-500 text-xs flex items-center gap-1.5">
            <Thermometer className="text-amber-500" size={15} />
            Soil Temperature
          </span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold font-mono text-slate-900 dark:text-white">
              {latestReading.soil_temperature_c}°C
            </span>
            <span className="text-[11px] text-slate-400">Probe depth: 15cm</span>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
          <span className="text-slate-500 text-xs flex items-center gap-1.5">
            <Thermometer className="text-red-500" size={15} />
            Canopy Air Temp
          </span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold font-mono text-slate-900 dark:text-white">
              {latestReading.ambient_temperature_c}°C
            </span>
            <span className="text-[11px] text-slate-400">RH: {latestReading.ambient_humidity_pct}%</span>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
          <span className="text-slate-500 text-xs flex items-center gap-1.5">
            <BatteryCharging className="text-emerald-500" size={15} />
            Node Battery Health
          </span>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
              {latestReading.battery_pct}%
            </span>
            <span className="text-[11px] text-slate-400">Solar buffer OK</span>
          </div>
        </div>
      </div>

      {/* Historical Telemetry Table */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 dark:text-white mb-4">
          Time-Series Observation History (Mesh Ingestion Queue)
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-400">
                <th className="pb-3 font-semibold">Timestamp (UTC)</th>
                <th className="pb-3 font-semibold">Node Device ID</th>
                <th className="pb-3 font-semibold">Soil Moisture</th>
                <th className="pb-3 font-semibold">Soil Temp</th>
                <th className="pb-3 font-semibold">Air Temp</th>
                <th className="pb-3 font-semibold">Battery</th>
                <th className="pb-3 font-semibold">Anomaly Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
              {sensors.map((r, i) => (
                <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                  <td className="py-2.5 font-mono text-slate-500">
                    {new Date(r.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </td>
                  <td className="py-2.5 font-semibold text-slate-900 dark:text-white">{r.device_id}</td>
                  <td className="py-2.5 font-mono font-semibold text-blue-600 dark:text-blue-400">{r.soil_moisture_pct}%</td>
                  <td className="py-2.5 font-mono">{r.soil_temperature_c}°C</td>
                  <td className="py-2.5 font-mono">{r.ambient_temperature_c}°C</td>
                  <td className="py-2.5 font-mono">{r.battery_pct}%</td>
                  <td className="py-2.5">
                    {r.anomaly_flag ? (
                      <span className="inline-flex items-center gap-1 text-[11px] font-bold text-red-600 dark:text-red-400">
                        <AlertTriangle size={12} /> Anomaly Detected
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 text-[11px] font-medium text-emerald-600 dark:text-emerald-400">
                        <CheckCircle2 size={12} /> Valid Reading
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
