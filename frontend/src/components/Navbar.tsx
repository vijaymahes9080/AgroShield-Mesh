import React from 'react';
import { Sprout, ShieldAlert, Globe, Wifi, WifiOff, RefreshCw } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

interface NavbarProps {
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  lang: Language;
  setLang: (lang: Language) => void;
  lowBandwidth: boolean;
  setLowBandwidth: (val: boolean) => void;
  onRefresh: () => void;
  loading: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  setCurrentTab,
  lang,
  setLang,
  lowBandwidth,
  setLowBandwidth,
  onRefresh,
  loading
}) => {
  const t = translations[lang];

  const tabs = [
    { id: 'overview', label: t.nav.overview },
    { id: 'map', label: t.nav.fieldMap },
    { id: 'sensors', label: t.nav.sensors },
    { id: 'risk', label: t.nav.cropRisk },
    { id: 'advisories', label: t.nav.advisories },
    { id: 'evidence', label: t.nav.evidence },
    { id: 'feedback', label: t.nav.feedback },
    { id: 'audit', label: t.nav.audit },
    { id: 'benchmarks', label: t.nav.benchmarks }
  ];

  return (
    <header className="bg-slate-900 border-b border-emerald-500/30 text-white sticky top-0 z-50 shadow-md">
      {/* Top Banner */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5 flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 text-xs text-slate-300">
        <div className="flex items-center gap-2">
          <span className="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="font-medium text-emerald-300">{t.header.mode}</span>
          <span className="text-slate-500">•</span>
          <span>{t.header.location}</span>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setLowBandwidth(!lowBandwidth)}
            className={`flex items-center gap-1.5 px-2 py-1 rounded transition ${
              lowBandwidth ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'hover:bg-slate-800 text-slate-400'
            }`}
            title="Toggle lightweight low-bandwidth mode"
          >
            {lowBandwidth ? <WifiOff size={14} /> : <Wifi size={14} />}
            <span>{t.header.lowBandwidth}</span>
          </button>

          <button
            onClick={onRefresh}
            disabled={loading}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 transition"
          >
            <RefreshCw size={13} className={loading ? 'animate-spin' : ''} />
            <span>{t.header.refresh}</span>
          </button>

          {/* Language Switcher */}
          <div className="flex items-center bg-slate-800 rounded-lg p-0.5 border border-slate-700">
            <button
              onClick={() => setLang('en')}
              className={`px-2.5 py-0.5 text-xs font-semibold rounded-md transition ${
                lang === 'en' ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
            >
              English
            </button>
            <button
              onClick={() => setLang('ta')}
              className={`px-2.5 py-0.5 text-xs font-semibold rounded-md transition ${
                lang === 'ta' ? 'bg-emerald-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
              }`}
            >
              தமிழ்
            </button>
          </div>
        </div>
      </div>

      {/* Main Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <Sprout size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
              {t.appTitle}
              <span className="text-xs font-mono font-medium px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                v1.0
              </span>
            </h1>
            <p className="text-xs text-slate-400">{t.appSubtitle}</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden lg:flex items-center gap-1 overflow-x-auto py-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setCurrentTab(tab.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                currentTab === tab.id
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Mobile Nav */}
      <div className="lg:hidden flex overflow-x-auto px-4 pb-2.5 gap-1.5 border-t border-slate-800">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setCurrentTab(tab.id)}
            className={`whitespace-nowrap px-3 py-1 rounded-md text-xs font-medium ${
              currentTab === tab.id ? 'bg-emerald-600 text-white' : 'text-slate-400 bg-slate-800'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </header>
  );
};
