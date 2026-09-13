import React, { useState } from 'react';
import { UserCheck, X, Check, AlertOctagon } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

interface ReviewModalProps {
  advisory: any;
  onClose: () => void;
  onSubmitReview: (status: string, reviewerName: string, notes: string) => Promise<void>;
  lang: Language;
}

export const ReviewModal: React.FC<ReviewModalProps> = ({
  advisory,
  onClose,
  onSubmitReview,
  lang
}) => {
  const t = translations[lang];
  const [reviewerName, setReviewerName] = useState('Dr. M. Raman, Senior Agronomist');
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleAction = async (status: string) => {
    if (!reviewerName.trim()) {
      alert('Please enter your agronomist name.');
      return;
    }
    setSubmitting(true);
    try {
      await onSubmitReview(status, reviewerName, notes);
      onClose();
    } catch (e: any) {
      alert('Error saving review: ' + e.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white dark:bg-slate-900 rounded-2xl max-w-lg w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl animate-in fade-in zoom-in-95">
        <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3 mb-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <UserCheck className="text-emerald-500" size={20} />
            {t.advisory.reviewAction}
          </h3>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400">
            <X size={18} />
          </button>
        </div>

        <div className="mb-4 bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl border border-slate-200/60 dark:border-slate-700/60 text-xs">
          <strong className="block text-slate-900 dark:text-white mb-1">{advisory.title}</strong>
          <p className="text-slate-600 dark:text-slate-300">{advisory.summary}</p>
        </div>

        <div className="space-y-4 mb-6 text-xs">
          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-200 mb-1">
              Agronomist / Expert Reviewer Name
            </label>
            <input
              type="text"
              value={reviewerName}
              onChange={(e) => setReviewerName(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-200 mb-1">
              Review Notes & Field Diagnostic Notes
            </label>
            <textarea
              rows={3}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder={t.advisory.notesPlaceholder}
              className="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white"
            />
          </div>
        </div>

        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            onClick={() => handleAction('rejected')}
            disabled={submitting}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl border border-red-500/30 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 text-xs font-semibold transition"
          >
            <AlertOctagon size={15} />
            <span>{t.advisory.rejectBtn}</span>
          </button>

          <button
            onClick={() => handleAction('expert_approved')}
            disabled={submitting}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold transition shadow-sm"
          >
            <Check size={15} />
            <span>{t.advisory.approveBtn}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
