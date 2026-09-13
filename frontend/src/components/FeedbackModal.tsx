import React, { useState } from 'react';
import { Star, MessageSquarePlus, X, Check } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

interface FeedbackModalProps {
  advisory: any;
  onClose: () => void;
  onSubmitFeedback: (payload: any) => Promise<void>;
  lang: Language;
}

export const FeedbackModal: React.FC<FeedbackModalProps> = ({
  advisory,
  onClose,
  onSubmitFeedback,
  lang
}) => {
  const t = translations[lang];
  const [rating, setRating] = useState(5);
  const [actionTaken, setActionTaken] = useState('Irrigated 3 cm in morning via drip lines');
  const [waterSaved, setWaterSaved] = useState('12000');
  const [comments, setComments] = useState('Advisory matched physical field condition accurately.');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmitFeedback({
        advisory_id: advisory.id,
        farmer_id: 'farmer-erode-01',
        rating,
        helpful_flag: rating >= 3,
        actual_action_taken: actionTaken,
        unnecessary_irrigation_prevented_litres: parseFloat(waterSaved) || 0,
        comments
      });
      alert(t.feedback.success);
      onClose();
    } catch (e: any) {
      alert('Error submitting feedback: ' + e.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white dark:bg-slate-900 rounded-2xl max-w-lg w-full p-6 border border-slate-200 dark:border-slate-800 shadow-2xl animate-in fade-in zoom-in-95">
        <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3 mb-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <MessageSquarePlus className="text-emerald-500" size={20} />
            {t.feedback.title}
          </h3>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          {/* Star Rating */}
          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-200 mb-2">
              {t.feedback.rating}
            </label>
            <div className="flex items-center gap-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  type="button"
                  key={star}
                  onClick={() => setRating(star)}
                  className={`p-1 transition ${rating >= star ? 'text-amber-400' : 'text-slate-300 dark:text-slate-600'}`}
                >
                  <Star size={24} fill={rating >= star ? 'currentColor' : 'none'} />
                </button>
              ))}
              <span className="ml-2 font-bold text-slate-700 dark:text-slate-300">{rating} / 5 Stars</span>
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-200 mb-1">
              {t.feedback.actionTaken}
            </label>
            <input
              type="text"
              required
              value={actionTaken}
              onChange={(e) => setActionTaken(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-200 mb-1">
              {t.feedback.waterSaved}
            </label>
            <input
              type="number"
              value={waterSaved}
              onChange={(e) => setWaterSaved(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-200 mb-1">
              Farmer Observations / Comments
            </label>
            <textarea
              rows={2}
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold shadow-sm"
            >
              <Check size={15} />
              <span>{t.feedback.submit}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
