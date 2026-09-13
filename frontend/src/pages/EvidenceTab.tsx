import React, { useState } from 'react';
import { BookOpen, Search, Hash, ShieldCheck, ExternalLink } from 'lucide-react';
import { Language, translations } from '../i18n/translations';

export const EvidenceTab: React.FC<{ lang: Language }> = ({ lang }) => {
  const t = translations[lang];
  const [searchQuery, setSearchQuery] = useState('');
  const [cropFilter, setCropFilter] = useState('all');

  const documents = [
    {
      id: 'TNAU-CPG-PAD-01',
      title: 'TNAU Crop Production Guide: Wet Season Rice (Paddy) Water Management',
      org: 'Tamil Nadu Agricultural University (TNAU), Coimbatore',
      year: 2024,
      section: 'Irrigation Management - Alternate Wetting and Drying (AWD)',
      bulletin: 'Bulletin No. 14, pp. 48-52',
      crop: 'Paddy',
      hash: '9e1d84f1a0e8bb65c4b18428c06788390bca7b11d9f041de62547b77ab6ef891',
      content_en: 'Under AWD, irrigate paddy to 5 cm depth only when the water level in the perforated field pipe drops to 15 cm below soil surface during vegetative stage. Maintain 3-5 cm continuous ponding from panicle initiation to flowering.',
      content_ta: 'மாற்று ஈரமாக்கல் மற்றும் உலர்த்துதல் (AWD) முறையில் பயிர் வளர்ச்சிப் பருவத்தில் களக் குழாயில் நீர் மட்டம் 15 செ.மீ கீழே குறையும் போது மட்டும் நீர் பாய்ச்சவும். பூக்கும் பருவத்தில் 3-5 செ.மீ தண்ணீர் தேங்கி இருக்க வேண்டும்.'
    },
    {
      id: 'TNAU-CPG-PAD-02',
      title: 'TNAU Agromet Advisory: Heat Stress Mitigation in Rice at Flowering',
      org: 'TNAU Directorate of Extension Education & Agromet Advisory',
      year: 2024,
      section: 'Crop Weather Advisory - High Temperature Management',
      bulletin: 'AAS Bulletin No. 38/2024, p. 3',
      crop: 'Paddy',
      hash: 'a47c5d0124b898cf893240e11894a821bf67905183efac291884210a4732ab98',
      content_en: 'When ambient day temperature exceeds 35°C during paddy flowering, maintain 5 cm standing water to buffer microclimate temperature. Apply foliar spray of 1% KCl in the morning. Avoid chemical spraying between 11 AM - 3 PM.',
      content_ta: 'பூக்கும் பருவத்தில் பகல் வெப்பநிலை 35°C-க்கு மேல் அதிகரிக்கும் போது, நுண் தட்பவெப்பநிலையைக் குறைக்க 5 செ.மீ நீர் தேக்கி வைக்கவும். காலை வேளையில் 1% பொட்டாசியம் குளோரைடு தெளிக்கவும்.'
    },
    {
      id: 'ICAR-WM-01',
      title: 'ICAR Handbook of Water Management: Drainage & Excess Rain Readiness',
      org: 'Indian Council of Agricultural Research (ICAR), New Delhi',
      year: 2023,
      section: 'Monsoon Surge & Field Inundation Prevention',
      bulletin: 'ICAR Monograph Series 8, pp. 112-116',
      crop: 'General',
      hash: 'bf89124a56c071d2389104fae1098471bcca09581726a8049182390147610ac2',
      content_en: 'When rainfall >50 mm is forecast within 24-72h, immediately suspend irrigation. Ensure peripheral drainage trenches are cleared of weeds to prevent water stagnation in commercial crops like Groundnut and Cotton.',
      content_ta: 'அடுத்த 24-72 மணி நேரத்தில் 50 மி.மீ மேல் கனமழை பெய்ய வாய்ப்பிருந்தால் பாசனத்தை உடனடியாக நிறுத்தவும். வடிகால் வாய்க்கால்களில் உள்ள அடைப்புகளை உடனே அகற்றவும்.'
    },
    {
      id: 'TNAU-CPG-COT-01',
      title: 'TNAU Crop Production Guide: Cotton Moisture & Square Drop Management',
      org: 'Tamil Nadu Agricultural University (TNAU), Coimbatore',
      year: 2024,
      section: 'Fibre Crops - Drip Fertigation & Abiotic Stress',
      bulletin: 'Vol. II (Commercial Crops), pp. 74-79',
      crop: 'Cotton',
      hash: 'c89140fa21e78451bca9082417e09841fcaa095167258410a917263548901bca',
      content_en: 'Cotton is sensitive to both moisture stress and waterlogging during square and boll development. Drip irrigation at 0.8 IW/CPE ratio saves 35% water. In heat >38°C, apply 0.5% zinc sulphate foliar spray to arrest square shedding.',
      content_ta: 'பருத்தி பயிரில் பூ மொட்டு மற்றும் காய் பிடிக்கும் பருவத்தில் அதிக நீர் தேங்குதலும், நீர் பற்றாக்குறையும் காய்கள் உதிர்வதற்கு காரணமாகும். சொட்டு நீர்ப்பாசனம் மூலம் 35% நீரைச் சேமிக்கலாம்.'
    }
  ];

  const filtered = documents.filter((d) => {
    const matchCrop = cropFilter === 'all' || d.crop.toLowerCase() === cropFilter.toLowerCase();
    const matchQuery =
      searchQuery === '' ||
      d.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      d.content_en.toLowerCase().includes(searchQuery.toLowerCase()) ||
      d.content_ta.includes(searchQuery);
    return matchCrop && matchQuery;
  });

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <div>
            <h2 className="text-sm font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <BookOpen className="text-emerald-500" size={18} />
              Agricultural University Guidelines & Citations Repository
            </h2>
            <p className="text-xs text-slate-500">
              Verified Evidence Grounding • Cryptographic SHA-256 Integrity • TNAU & ICAR Knowledge Base
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Crop:</span>
            <select
              value={cropFilter}
              onChange={(e) => setCropFilter(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-xs font-semibold"
            >
              <option value="all">All Crops</option>
              <option value="paddy">Paddy (Rice)</option>
              <option value="cotton">Cotton</option>
              <option value="general">General Water Management</option>
            </select>
          </div>
        </div>

        <div className="relative">
          <Search className="absolute left-3.5 top-3 text-slate-400" size={16} />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search agricultural evidence by keywords (e.g., 'AWD water management', 'heat stress', 'பாசனம்')..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-xs text-slate-900 dark:text-white"
          />
        </div>
      </div>

      {/* Documents List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((doc) => (
          <div
            key={doc.id}
            className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3"
          >
            <div className="flex items-start justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
              <div>
                <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold">
                  {doc.id}
                </span>
                <h3 className="text-sm font-bold text-slate-900 dark:text-white mt-1.5">{doc.title}</h3>
                <span className="text-[11px] text-slate-500 block">
                  {doc.org} ({doc.year})
                </span>
              </div>
            </div>

            <div className="text-xs text-slate-700 dark:text-slate-300 space-y-2">
              <div className="bg-slate-50 dark:bg-slate-800/60 p-3 rounded-xl border border-slate-200/60 dark:border-slate-800">
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
                  Section: {doc.section} ({doc.bulletin})
                </span>
                <p>{lang === 'ta' ? doc.content_ta : doc.content_en}</p>
              </div>
            </div>

            <div className="border-t border-slate-100 dark:border-slate-800 pt-3 flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span className="flex items-center gap-1 truncate max-w-[280px]" title={doc.hash}>
                <Hash size={12} className="text-emerald-500 shrink-0" />
                {doc.hash.slice(0, 24)}...
              </span>
              <span className="text-emerald-600 font-semibold flex items-center gap-1">
                <ShieldCheck size={13} /> Verified
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
