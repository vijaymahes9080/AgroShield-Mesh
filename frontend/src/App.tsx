import React, { useEffect, useState } from 'react';
import { Navbar } from './components/Navbar';
import { OverviewTab } from './pages/OverviewTab';
import { FieldMapTab } from './pages/FieldMapTab';
import { SensorsTab } from './pages/SensorsTab';
import { CropRiskTab } from './pages/CropRiskTab';
import { AdvisoriesTab } from './pages/AdvisoriesTab';
import { EvidenceTab } from './pages/EvidenceTab';
import { FeedbackTab } from './pages/FeedbackTab';
import { AuditTab } from './pages/AuditTab';
import { BenchmarksTab } from './pages/BenchmarksTab';
import { ReviewModal } from './components/ReviewModal';
import { FeedbackModal } from './components/FeedbackModal';
import { Language } from './i18n/translations';
import {
  fetchFields,
  fetchFieldGeoJSON,
  fetchAdvisories,
  fetchWeatherObservations,
  generateAdvisory,
  reviewAdvisory,
  submitFeedback
} from './services/api';

export function App() {
  const [currentTab, setCurrentTab] = useState('overview');
  const [lang, setLang] = useState<Language>('ta'); // Default to Tamil as requested
  const [lowBandwidth, setLowBandwidth] = useState(false);
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);

  const [fields, setFields] = useState<any[]>([]);
  const [selectedFieldId, setSelectedFieldId] = useState<string | null>(null);
  const [geojsonData, setGeojsonData] = useState<any>(null);
  const [advisories, setAdvisories] = useState<any[]>([]);
  const [weather, setWeather] = useState<any[]>([]);

  // Modals
  const [reviewModalAdvisory, setReviewModalAdvisory] = useState<any>(null);
  const [feedbackModalAdvisory, setFeedbackModalAdvisory] = useState<any>(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [fieldsData, geoData, advData, weatherData] = await Promise.all([
        fetchFields().catch(() => []),
        fetchFieldGeoJSON().catch(() => null),
        fetchAdvisories().catch(() => []),
        fetchWeatherObservations().catch(() => [])
      ]);

      setFields(fieldsData);
      if (fieldsData.length > 0 && !selectedFieldId) {
        setSelectedFieldId(fieldsData[0].id);
      }
      setGeojsonData(geoData);
      setAdvisories(advData);
      setWeather(weatherData);
    } catch (e) {
      console.error('Initial data loading error:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerAdvisory = async (fieldId: string) => {
    setEvaluating(true);
    try {
      const newAdv = await generateAdvisory(fieldId, lang);
      setAdvisories((prev) => [newAdv, ...prev]);
      alert(`Advisory created! Status: ${newAdv.review_status.toUpperCase()}`);
    } catch (e: any) {
      alert('Advisory generation failed: ' + e.message);
    } finally {
      setEvaluating(false);
    }
  };

  const handleSubmitReview = async (status: string, reviewerName: string, notes: string) => {
    if (!reviewModalAdvisory) return;
    const updated = await reviewAdvisory(reviewModalAdvisory.id, status, reviewerName, notes);
    setAdvisories((prev) => prev.map((a) => (a.id === updated.id ? updated : a)));
  };

  const handleSubmitFeedback = async (payload: any) => {
    await submitFeedback(payload);
  };

  return (
    <div className="min-h-screen bg-slate-100 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col">
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        lang={lang}
        setLang={setLang}
        lowBandwidth={lowBandwidth}
        setLowBandwidth={setLowBandwidth}
        onRefresh={loadInitialData}
        loading={loading}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {currentTab === 'overview' && (
          <OverviewTab
            fields={fields}
            selectedFieldId={selectedFieldId}
            onSelectField={setSelectedFieldId}
            advisories={advisories}
            weather={weather}
            onTriggerAdvisory={handleTriggerAdvisory}
            evaluating={evaluating}
            lang={lang}
            onOpenReviewModal={setReviewModalAdvisory}
            onOpenFeedbackModal={setFeedbackModalAdvisory}
          />
        )}

        {currentTab === 'map' && (
          <FieldMapTab
            geojsonData={geojsonData}
            fields={fields}
            selectedFieldId={selectedFieldId}
            onSelectField={setSelectedFieldId}
            lang={lang}
          />
        )}

        {currentTab === 'sensors' && (
          <SensorsTab
            fields={fields}
            selectedFieldId={selectedFieldId}
            onSelectField={setSelectedFieldId}
            lang={lang}
          />
        )}

        {currentTab === 'risk' && (
          <CropRiskTab
            fields={fields}
            selectedFieldId={selectedFieldId}
            onSelectField={setSelectedFieldId}
            lang={lang}
            onTriggerAdvisory={handleTriggerAdvisory}
            evaluating={evaluating}
          />
        )}

        {currentTab === 'advisories' && (
          <AdvisoriesTab
            advisories={advisories}
            lang={lang}
            onOpenReviewModal={setReviewModalAdvisory}
            onOpenFeedbackModal={setFeedbackModalAdvisory}
          />
        )}

        {currentTab === 'evidence' && <EvidenceTab lang={lang} />}

        {currentTab === 'feedback' && <FeedbackTab lang={lang} />}

        {currentTab === 'audit' && <AuditTab lang={lang} />}

        {currentTab === 'benchmarks' && <BenchmarksTab lang={lang} />}
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 py-4 text-center text-xs text-slate-500">
        <p>
          AGROSHIELD MESH &copy; 2026 • Evidence-Grounded Agricultural Intelligence Platform • Open Source MIT License
        </p>
        <p className="mt-1 text-[11px] text-slate-400">
          Operates strictly as a decision support system with Human-in-the-Loop review. Direct machine control is disallowed in MVP.
        </p>
      </footer>

      {/* Review Modal */}
      {reviewModalAdvisory && (
        <ReviewModal
          advisory={reviewModalAdvisory}
          onClose={() => setReviewModalAdvisory(null)}
          onSubmitReview={handleSubmitReview}
          lang={lang}
        />
      )}

      {/* Feedback Modal */}
      {feedbackModalAdvisory && (
        <FeedbackModal
          advisory={feedbackModalAdvisory}
          onClose={() => setFeedbackModalAdvisory(null)}
          onSubmitFeedback={handleSubmitFeedback}
          lang={lang}
        />
      )}
    </div>
  );
}

export default App;
