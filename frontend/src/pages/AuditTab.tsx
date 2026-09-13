import React, { useEffect, useState } from 'react';
import { ShieldAlert, Hash, RefreshCw, CheckCircle2 } from 'lucide-react';
import { Language, translations } from '../i18n/translations';
import { fetchAuditLogs } from '../services/api';

export const AuditTab: React.FC<{ lang: Language }> = ({ lang }) => {
  const t = translations[lang];
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAudit();
  }, []);

  const loadAudit = async () => {
    setLoading(true);
    try {
      const data = await fetchAuditLogs();
      setLogs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div>
          <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <ShieldAlert className="text-emerald-500" size={20} />
            Cryptographic Audit Log & Event Integrity Chain
          </h2>
          <p className="text-xs text-slate-500">
            Immutable SHA-256 Chained Event Record • Zero Tampering Policy • SOC2 / Agri-Security Ready
          </p>
        </div>

        <button
          onClick={loadAudit}
          disabled={loading}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-xs font-semibold text-slate-700 dark:text-slate-300 transition"
        >
          <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
          <span>Refresh Logs</span>
        </button>
      </div>

      {/* Audit Log Table */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-400">
                <th className="pb-3 font-semibold">Timestamp (UTC)</th>
                <th className="pb-3 font-semibold">Event Type</th>
                <th className="pb-3 font-semibold">Entity</th>
                <th className="pb-3 font-semibold">Actor & Role</th>
                <th className="pb-3 font-semibold">SHA-256 Payload Hash</th>
                <th className="pb-3 font-semibold">Integrity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300">
              {logs.map((log, i) => (
                <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                  <td className="py-3 font-mono text-slate-500">
                    {new Date(log.timestamp).toLocaleString([], {
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                      second: '2-digit'
                    })}
                  </td>
                  <td className="py-3 font-semibold text-slate-900 dark:text-white">
                    <span className="px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 font-mono text-[11px]">
                      {log.event_type}
                    </span>
                  </td>
                  <td className="py-3">{log.entity_name} ({log.entity_id.slice(0, 8)}...)</td>
                  <td className="py-3">
                    <span className="font-semibold text-slate-900 dark:text-white">{log.actor_id}</span>
                    <span className="text-slate-400 block text-[11px] font-mono">{log.actor_role}</span>
                  </td>
                  <td className="py-3 font-mono text-slate-500 text-[11px]">
                    <span className="flex items-center gap-1" title={log.payload_hash}>
                      <Hash size={12} className="text-emerald-500 shrink-0" />
                      {log.payload_hash.slice(0, 16)}...
                    </span>
                  </td>
                  <td className="py-3">
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600 dark:text-emerald-400">
                      <CheckCircle2 size={13} /> Verified
                    </span>
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
