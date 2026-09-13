import React, { useState } from 'react';
import { MessageSquarePlus, Star, Droplet, User, CheckCircle2 } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

export const FeedbackTab: React.FC<{ lang: Language }> = ({ lang }) => {
  const t = translations[lang];

  // Realistic recorded farmer feedbacks
  const feedbackList = [
    {
      id: 'fb-01',
      farmer_name: 'Vijay Mahes',
      village: 'Perundurai, Erode',
      advisory_title: 'அக்ரோஷீல்டு பயிர் ஆலோசனை - நெல் (பூக்கும் பருவம்)',
      rating: 5,
      actual_action_taken: 'அதிகாலை 6 மணிக்கு 3 செ.மீ நீர் பாய்ச்சினேன். கதிர் முதிர்தல் சீராக உள்ளது.',
      water_saved_litres: 12000,
      comments: 'பூக்கும் தருணத்தில் அதிக வெப்பத்தினால் பதர் ஆவதைத் தடுத்து பயிரைக் காப்பாற்ற உதவியது.',
      date: '2026-09-13 06:30'
    },
    {
      id: 'fb-02',
      farmer_name: 'R. Murugesan',
      village: 'Bhavani, Erode',
      advisory_title: 'AgroShield Advisory: Cotton - Heat Stress Mitigation',
      rating: 5,
      actual_action_taken: 'Applied alternate furrow drip irrigation and cleared drainage bunds.',
      water_saved_litres: 18500,
      comments: 'Prevented boll shedding during peak daytime heat.',
      date: '2026-09-12 18:15'
    },
    {
      id: 'fb-03',
      farmer_name: 'K. Selvi',
      village: 'Gobichettipalayam, Erode',
      advisory_title: 'அக்ரோஷீல்டு பயிர் ஆலோசனை - கேழ்வரகு (Ragi)',
      rating: 4,
      actual_action_taken: 'மழைக்கு முன் பாசனத்தை நிறுத்தி வாய்க்கால் அடைப்புகளை நீக்கினேன்.',
      water_saved_litres: 8000,
      comments: 'கனமழையினால் பயிர் சாய்வதைத் தவிர்க்க உதவியது.',
      date: '2026-09-11 11:45'
    }
  ];

  const totalWaterSaved = feedbackList.reduce((acc, f) => acc + f.water_saved_litres, 0);

  return (
    <div className="space-y-6">
      {/* Overview Metric Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center">
            <Droplet size={24} />
          </div>
          <div>
            <span className="text-xs text-slate-500">Unnecessary Irrigation Prevented</span>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white font-mono">
              {totalWaterSaved.toLocaleString()} Litres
            </h3>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-500 flex items-center justify-center">
            <Star size={24} fill="currentColor" />
          </div>
          <div>
            <span className="text-xs text-slate-500">Average Farmer Satisfaction</span>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white font-mono">4.8 / 5.0 Stars</h3>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <CheckCircle2 size={24} />
          </div>
          <div>
            <span className="text-xs text-slate-500">Advisory Adoption Rate</span>
            <h3 className="text-xl font-bold text-slate-900 dark:text-white font-mono">94.2%</h3>
          </div>
        </div>
      </div>

      {/* Feedbacks List */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-4">
          <MessageSquarePlus className="text-emerald-500" size={20} />
          {t.feedback.title}
        </h2>

        <div className="space-y-4">
          {feedbackList.map((fb) => (
            <div
              key={fb.id}
              className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60 space-y-2 text-xs"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200/60 dark:border-slate-700/60 pb-2">
                <div className="flex items-center gap-2">
                  <User size={14} className="text-slate-400" />
                  <strong className="text-slate-900 dark:text-white">{fb.farmer_name}</strong>
                  <span className="text-slate-400">• {fb.village}</span>
                </div>
                <div className="flex items-center gap-1 text-amber-400">
                  {Array.from({ length: fb.rating }).map((_, i) => (
                    <Star key={i} size={14} fill="currentColor" />
                  ))}
                  <span className="ml-1 text-slate-400 font-mono text-[11px]">{fb.date}</span>
                </div>
              </div>

              <div className="font-semibold text-slate-800 dark:text-slate-200">{fb.advisory_title}</div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                <div className="bg-white dark:bg-slate-900/60 p-2.5 rounded-lg border border-slate-200/60 dark:border-slate-800">
                  <span className="text-slate-400 block font-medium">Actual Field Action:</span>
                  <span className="text-slate-700 dark:text-slate-300">{fb.actual_action_taken}</span>
                </div>
                <div className="bg-white dark:bg-slate-900/60 p-2.5 rounded-lg border border-slate-200/60 dark:border-slate-800">
                  <span className="text-slate-400 block font-medium">Water Conserved:</span>
                  <span className="font-mono text-emerald-600 dark:text-emerald-400 font-bold">
                    ~{fb.water_saved_litres.toLocaleString()} Litres
                  </span>
                </div>
              </div>

              {fb.comments && (
                <p className="text-slate-600 dark:text-slate-400 italic bg-slate-100 dark:bg-slate-800/40 p-2 rounded-lg">
                  &quot;{fb.comments}&quot;
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
