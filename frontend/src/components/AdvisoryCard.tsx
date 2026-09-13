import React from 'react';
import { CheckCircle2, Clock, Ban, BookOpen, AlertCircle, UserCheck, MessageSquarePlus } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

interface AdvisoryCardProps {
  advisory: any;
  lang: Language;
  onOpenReviewModal: (advisory: any) => void;
  onOpenFeedbackModal: (advisory: any) => void;
}

export const AdvisoryCard: React.FC<AdvisoryCardProps> = ({
  advisory,
  lang,
  onOpenReviewModal,
  onOpenFeedbackModal
}) => {
  const t = translations[lang];

  const isApproved = advisory.review_status === 'expert_approved';
  const isPending = advisory.review_status === 'pending_review';

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm transition hover:shadow-md">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4 mb-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            {isApproved ? (
              <span className="flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-600 border border-emerald-500/30">
                <CheckCircle2 size={13} /> {t.advisory.expertApproved}
              </span>
            ) : isPending ? (
              <span className="flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-full bg-amber-500/10 text-amber-600 border border-amber-500/30">
                <Clock size={13} /> {t.advisory.aiSuggested}
              </span>
            ) : (
              <span className="flex items-center gap-1 text-xs font-bold px-2.5 py-1 rounded-full bg-blue-500/10 text-blue-600 border border-blue-500/30">
                {t.advisory.autoDispatched}
              </span>
            )}
            <span className="text-xs text-slate-400">
              Confidence: {Math.round(advisory.confidence_level * 100)}%
            </span>
          </div>
          <h3 className="text-base font-bold text-slate-900 dark:text-white leading-snug">
            {advisory.title}
          </h3>
        </div>

        {/* Buttons */}
        <div className="flex items-center gap-2">
          {isPending && (
            <button
              onClick={() => onOpenReviewModal(advisory)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white transition shadow-sm"
            >
              <UserCheck size={14} />
              <span>{t.advisory.reviewAction}</span>
            </button>
          )}

          <button
            onClick={() => onOpenFeedbackModal(advisory)}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition"
          >
            <MessageSquarePlus size={14} />
            <span>{t.feedback.title}</span>
          </button>
        </div>
      </div>

      {/* Summary */}
      <p className="text-xs text-slate-600 dark:text-slate-300 mb-4 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-xl border border-slate-200/60 dark:border-slate-800">
        {advisory.summary}
      </p>

      {/* Action Items */}
      <div className="mb-4">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
          {t.advisory.actionItems}
        </h4>
        <ul className="space-y-1.5">
          {advisory.action_items?.map((act: string, i: number) => (
            <li key={i} className="flex items-start gap-2 text-xs text-slate-800 dark:text-slate-200">
              <span className="text-emerald-500 font-bold mt-0.5">•</span>
              <span>{act}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Prohibited Actions */}
      {advisory.prohibited_actions?.length > 0 && (
        <div className="mb-4 p-3 rounded-xl bg-red-50 dark:bg-red-950/20 border border-red-500/20">
          <h4 className="text-xs font-bold uppercase tracking-wider text-red-600 dark:text-red-400 mb-2 flex items-center gap-1.5">
            <Ban size={14} /> {t.advisory.prohibited}
          </h4>
          <ul className="space-y-1 text-xs text-red-800 dark:text-red-300">
            {advisory.prohibited_actions.map((pr: string, i: number) => (
              <li key={i} className="flex items-start gap-1.5">
                <span className="font-bold">✕</span>
                <span>{pr}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Reviewer Note */}
      {isApproved && advisory.reviewed_by && (
        <div className="mb-4 p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-500/20 text-xs text-emerald-900 dark:text-emerald-300">
          <strong>Certified by Agronomist:</strong> {advisory.reviewed_by}
          {advisory.review_notes && <p className="mt-1 text-slate-600 dark:text-slate-400">{advisory.review_notes}</p>}
        </div>
      )}

      {/* Citations */}
      {advisory.source_citations?.length > 0 && (
        <div className="border-t border-slate-200 dark:border-slate-800 pt-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
            <BookOpen size={13} /> {t.advisory.citations}
          </h4>
          <div className="space-y-1.5">
            {advisory.source_citations.map((c: any, i: number) => (
              <div key={i} className="text-xs text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-800/60 p-2 rounded-lg border border-slate-200/50 dark:border-slate-700/50">
                <span className="font-semibold text-slate-900 dark:text-slate-200">{c.source_title}</span>
                <span className="block text-[11px] text-slate-500">
                  {c.author_organization} • Section: {c.document_section} ({c.page_or_bulletin_no})
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
