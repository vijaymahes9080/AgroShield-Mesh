import React, { useState } from 'react';
import { FieldMap } from '../components/FieldMap';
import { Layers, Activity, Sparkles, CheckCircle, RefreshCw } from 'lucide-react';
import { Language, translations } from '../i18n/translations';
import { fetchSyntheticRaster } from '../services/api';

interface FieldMapTabProps {
  geojsonData: any;
  fields: any[];
  selectedFieldId: string | null;
  onSelectField: (id: string) => void;
  lang: Language;
}

export const FieldMapTab: React.FC<FieldMapTabProps> = ({
  geojsonData,
  fields,
  selectedFieldId,
  onSelectField,
  lang
}) => {
  const t = translations[lang];
  const [rasterAnalysis, setRasterAnalysis] = useState<any>(null);
  const [loadingRaster, setLoadingRaster] = useState(false);
  const [stressPatch, setStressPatch] = useState(false);

  const currentField = fields.find((f) => f.id === selectedFieldId) || fields[0];

  const handleRunRaster = async () => {
    if (!currentField) return;
    setLoadingRaster(true);
    try {
      const data = await fetchSyntheticRaster(currentField.id, stressPatch);
      setRasterAnalysis(data.raster_analysis);
    } catch (e: any) {
      alert('Raster calculation error: ' + e.message);
    } finally {
      setLoadingRaster(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Interactive Map */}
      <FieldMap
        geojsonData={geojsonData}
        selectedFieldId={selectedFieldId}
        onSelectField={onSelectField}
        lang={lang}
      />

      {/* Field Inspection & Synthetic Sentinel-2 Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Field Details */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2 mb-4">
            <Activity className="text-emerald-500" size={18} />
            Field Cadastral Details
          </h3>

          {currentField ? (
            <div className="space-y-3 text-xs">
              <div className="flex justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
                <span className="text-slate-500">Field Name</span>
                <strong className="text-slate-900 dark:text-white font-semibold">{currentField.name}</strong>
              </div>
              <div className="flex justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
                <span className="text-slate-500">Area</span>
                <strong className="text-slate-900 dark:text-white font-semibold">{currentField.area_hectares} Hectares</strong>
              </div>
              <div className="flex justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
                <span className="text-slate-500">Soil Type</span>
                <strong className="text-slate-900 dark:text-white font-semibold">{currentField.soil_type}</strong>
              </div>
              <div className="flex justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
                <span className="text-slate-500">Irrigation Source</span>
                <strong className="text-slate-900 dark:text-white font-semibold">{currentField.irrigation_source}</strong>
              </div>
              <div className="flex justify-between border-b border-slate-100 dark:border-slate-800 pb-2">
                <span className="text-slate-500">Elevation</span>
                <strong className="text-slate-900 dark:text-white font-semibold">{currentField.elevation_meters} m ASL</strong>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">CRS Coordinate System</span>
                <span className="font-mono text-emerald-600 dark:text-emerald-400 font-semibold">EPSG:{currentField.srid || 4326} (WGS 84)</span>
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-400">Select a field on the map to view cadastral metrics.</p>
          )}
        </div>

        {/* Synthetic Raster Simulator */}
        <div className="lg:col-span-2 bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-800 pb-3 mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Layers className="text-blue-500" size={18} />
                Synthetic Sentinel-2 Multi-Band NDVI Analysis
              </h3>
              <p className="text-xs text-slate-500">
                Pixel-level NIR (Band 8) vs Red (Band 4) 10m Ground Sampling Distance (GSD)
              </p>
            </div>

            <div className="flex items-center gap-3">
              <label className="flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={stressPatch}
                  onChange={(e) => setStressPatch(e.target.checked)}
                  className="rounded text-emerald-600 focus:ring-emerald-500"
                />
                <span>Simulate Stressed Sector</span>
              </label>

              <button
                onClick={handleRunRaster}
                disabled={loadingRaster}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold transition"
              >
                <RefreshCw size={13} className={loadingRaster ? 'animate-spin' : ''} />
                <span>Compute Zonal Indices</span>
              </button>
            </div>
          </div>

          {rasterAnalysis ? (
            <div className="space-y-4">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60">
                  <span className="text-slate-500 block">Mean NDVI</span>
                  <strong className="text-lg font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                    {rasterAnalysis.ndvi_mean}
                  </strong>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60">
                  <span className="text-slate-500 block">Min / Max NDVI</span>
                  <strong className="text-sm font-bold text-slate-900 dark:text-white font-mono">
                    {rasterAnalysis.ndvi_min} / {rasterAnalysis.ndvi_max}
                  </strong>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60">
                  <span className="text-slate-500 block">Mean NDWI (Canopy Water)</span>
                  <strong className="text-lg font-bold text-cyan-600 dark:text-cyan-400 font-mono">
                    {rasterAnalysis.ndwi_mean}
                  </strong>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/60 dark:border-slate-700/60">
                  <span className="text-slate-500 block">Stressed Pixels (&lt;0.35)</span>
                  <strong className={`text-lg font-bold font-mono ${rasterAnalysis.stressed_area_pct > 20 ? 'text-red-500' : 'text-slate-900 dark:text-white'}`}>
                    {rasterAnalysis.stressed_area_pct}%
                  </strong>
                </div>
              </div>

              {/* Pixel Heatmap Grid Preview */}
              {rasterAnalysis.ndvi_grid && (
                <div>
                  <h4 className="text-xs font-semibold text-slate-500 mb-2">12x12 Pixel Field Grid NDVI Reflectance</h4>
                  <div className="grid grid-cols-12 gap-1 p-2 bg-slate-100 dark:bg-slate-800/40 rounded-xl max-w-sm">
                    {rasterAnalysis.ndvi_grid.flat().map((val: number, idx: number) => {
                      const bg =
                        val > 0.65 ? 'bg-emerald-500' : val > 0.45 ? 'bg-emerald-300' : val > 0.30 ? 'bg-amber-400' : 'bg-red-500';
                      return (
                        <div
                          key={idx}
                          title={`NDVI: ${val}`}
                          className={`w-full aspect-square rounded-sm ${bg} opacity-80 hover:opacity-100 transition`}
                        />
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8 text-slate-400 text-xs">
              <Sparkles className="mx-auto mb-2 text-slate-400" size={24} />
              Click &quot;Compute Zonal Indices&quot; above to simulate and analyze multispectral Sentinel-2 raster canopy data.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
