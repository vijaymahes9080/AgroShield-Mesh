import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { Language, translations } from '../i18n/translations';

interface FieldMapProps {
  geojsonData: any;
  selectedFieldId: string | null;
  onSelectField: (id: string) => void;
  lang: Language;
}

export const FieldMap: React.FC<FieldMapProps> = ({
  geojsonData,
  selectedFieldId,
  onSelectField,
  lang
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const geojsonLayerRef = useRef<L.GeoJSON | null>(null);

  const t = translations[lang];

  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      // Centered on Erode / Perundurai region (11.272, 77.581)
      const map = L.map(mapContainerRef.current, {
        center: [11.3410, 77.6200],
        zoom: 11,
        zoomControl: true,
        scrollWheelZoom: false
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors | AgroShield Mesh GIS',
        maxZoom: 18
      }).addTo(map);

      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;

    // Remove previous layer
    if (geojsonLayerRef.current) {
      map.removeLayer(geojsonLayerRef.current);
    }

    if (geojsonData && geojsonData.features && geojsonData.features.length > 0) {
      const layer = L.geoJSON(geojsonData, {
        style: (feature) => {
          const isSelected = feature?.properties?.field_id === selectedFieldId;
          const color = feature?.properties?.fillColor || '#10B981';
          return {
            fillColor: color,
            fillOpacity: isSelected ? 0.75 : 0.45,
            color: isSelected ? '#047857' : color,
            weight: isSelected ? 3.5 : 2.0
          };
        },
        onEachFeature: (feature, l) => {
          const p = feature.properties;
          l.on({
            click: () => {
              if (p?.field_id) onSelectField(p.field_id);
            }
          });

          l.bindPopup(`
            <div style="font-family: sans-serif; font-size: 13px; line-height: 1.4;">
              <strong style="color: #065f46; font-size: 14px;">${p.name || 'Field'}</strong><br/>
              <b>Farmer:</b> ${p.farmer_name || 'Vijay Mahes'}<br/>
              <b>Area:</b> ${p.area_hectares || 2.45} ha (${p.soil_type || 'Red Loam'})<br/>
              <b>Soil Moisture:</b> ${p.soil_moisture_pct || 22.0}%<br/>
              <b>Sentinel-2 NDVI:</b> ${p.ndvi_mean || 0.68}<br/>
              <b>Risk Level:</b> <span style="font-weight: bold; text-transform: uppercase;">${p.risk_level || 'low'}</span>
            </div>
          `);
        }
      }).addTo(map);

      geojsonLayerRef.current = layer;

      // Fit map bounds to polygons
      try {
        const bounds = layer.getBounds();
        if (bounds.isValid()) {
          map.fitBounds(bounds, { padding: [40, 40] });
        }
      } catch (e) {
        // Fallback
      }
    }
  }, [geojsonData, selectedFieldId]);

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
        <div>
          <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
            {t.map.title}
          </h2>
          <p className="text-xs text-slate-500">CRS: EPSG:4326 (WGS 84) • Real-time Boundary Polygon Overlays</p>
        </div>

        {/* Legend */}
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1 text-slate-600 dark:text-slate-400">
            <span className="w-3 h-3 rounded-full bg-emerald-500"></span> {t.map.low}
          </span>
          <span className="flex items-center gap-1 text-slate-600 dark:text-slate-400">
            <span className="w-3 h-3 rounded-full bg-amber-500"></span> {t.map.moderate}
          </span>
          <span className="flex items-center gap-1 text-slate-600 dark:text-slate-400">
            <span className="w-3 h-3 rounded-full bg-red-500"></span> {t.map.high}
          </span>
          <span className="flex items-center gap-1 text-slate-600 dark:text-slate-400">
            <span className="w-3 h-3 rounded-full bg-red-800"></span> {t.map.critical}
          </span>
        </div>
      </div>

      <div
        ref={mapContainerRef}
        className="w-full h-[450px] rounded-xl overflow-hidden border border-slate-200 dark:border-slate-800"
      />
    </div>
  );
};
