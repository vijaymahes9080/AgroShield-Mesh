import React, { useState } from 'react';
import { AdvisoryCard } from '../components/AdvisoryCard';
import { Language, translations } from '../i18n/translations';
import { Filter, Sparkles } from 'lucide-react';

interface AdvisoriesTabProps {
  advisories: any[];
  lang: Language;
  onOpenReviewModal: (advisory: any) => void;
  onOpenFeedbackModal: (advisory: any) => void;
}

export const AdvisoriesTab: React.FC<AdvisoriesTabProps> = ({
  advisories,
  lang,
  onOpenReviewModal,
  onOpenFeedbackModal
}) => {
  const t = translations[lang];
  const [filter, setFilter] = useState<'all' | 'pending_review' | 'expert_approved' | 'auto_dispatched'>('all');

  const filtered = advisories.filter((a) => {
    if (filter === 'all') return true;
    return a.review_status === filter;
  });

  return (
    <div className="space-y-6">
      {/* Header & Filter Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div>
          <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Sparkles className="text-emerald-500" size={18} />
            {t.advisory.title}
          </h2>
          <p className="text-xs text-slate-500">Human-in-the-Loop Expert Gate • Strict Anti-Hallucination Guardrails</p>
        </div>

        {/* Filter Pills */}
        <div className="flex items-center gap-1.5 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
              filter === 'all' ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-sm' : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            All ({advisories.length})
          </button>
          <button
            onClick={() => setFilter('pending_review')}
            className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
              filter === 'pending_review' ? 'bg-amber-500 text-white shadow-sm' : 'text-amber-600 hover:text-amber-700'
            }`}
          >
            Review Gate ({advisories.filter((a) => a.review_status === 'pending_review').length})
          </button>
          <button
            onClick={() => setFilter('expert_approved')}
            className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
              filter === 'expert_approved' ? 'bg-emerald-600 text-white shadow-sm' : 'text-emerald-600 hover:text-emerald-700'
            }`}
          >
            Certified ({advisories.filter((a) => a.review_status === 'expert_approved').length})
          </button>
        </div>
      </div>

      {/* Advisory Cards List */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map((adv) => (
            <AdvisoryCard
              key={adv.id}
              advisory={adv}
              lang={lang}
              onOpenReviewModal={onOpenReviewModal}
              onOpenFeedbackModal={onOpenFeedbackModal}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 text-slate-400 text-xs">
          No advisories match this filter criteria.
        </div>
      )}
    </div>
  );
};
