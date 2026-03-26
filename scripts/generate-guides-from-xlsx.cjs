/**
 * Build-time script: generates client/public/data/guides.json from
 * the guia-de-turismo-pf.xlsx CADASTUR source file (no database needed).
 *
 * If DATABASE_URL is set, it also marks verified (Trekko-registered) guides.
 *
 * Usage: node scripts/generate-guides-from-xlsx.cjs
 */

const XLSX = require('../node_modules/xlsx/xlsx.js');
const fs = require('fs');
const path = require('path');

const xlsxPath = path.join(__dirname, '..', 'guia-de-turismo-pf.xlsx');
if (!fs.existsSync(xlsxPath)) {
  console.error('[generate-guides] guia-de-turismo-pf.xlsx not found — skipping.');
  process.exit(0);
}

console.log('[generate-guides] Reading Excel file...');
const wb = XLSX.readFile(xlsxPath);
const ws = wb.Sheets[wb.SheetNames[0]];
const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: '' });

const guides = [];
for (let i = 1; i < rows.length; i++) {
  const [
    _activity, uf, city, name, phone, email, website,
    certNum, validUntil, _langs, _opCities, cats, _segs, isDriver,
  ] = rows[i];

  const certStr = String(certNum).trim();
  if (!certStr || certStr === '-') continue;

  // Excel serial date → ISO string
  let validUntilISO = null;
  if (validUntil && validUntil !== '-') {
    if (typeof validUntil === 'number') {
      try {
        const d = XLSX.SSF.parse_date_code(validUntil);
        validUntilISO = `${d.y}-${String(d.m).padStart(2, '0')}-${String(d.d).padStart(2, '0')}`;
      } catch (_) {}
    } else if (typeof validUntil === 'string') {
      validUntilISO = validUntil.split(' ')[0] || null;
    }
  }

  guides.push({
    id: i,
    name: String(name).trim() || null,
    cadasturNumber: certStr,
    uf: String(uf).trim() || null,
    city: (city && city !== '-') ? String(city).trim() : null,
    phone: (phone && phone !== '-') ? String(phone).trim() : null,
    email: (email && email !== '-') ? String(email).trim().toLowerCase() : null,
    website: (website && website !== '-') ? String(website).trim() : null,
    categories: (cats && cats !== '-')
      ? cats.split('|').map((s) => s.trim()).filter(Boolean)
      : null,
    validUntil: validUntilISO,
    isVerified: false,
    isDriverGuide:
      String(isDriver) === '1' || String(isDriver).toLowerCase() === 'sim',
  });
}

guides.sort((a, b) => (a.name || '').localeCompare(b.name || '', 'pt-BR'));

const outputDir = path.join(__dirname, '..', 'client', 'public', 'data');
fs.mkdirSync(outputDir, { recursive: true });
const outPath = path.join(outputDir, 'guides.json');
fs.writeFileSync(outPath, JSON.stringify(guides));

console.log(`[generate-guides] Exported ${guides.length} guides (${(fs.statSync(outPath).size / 1024 / 1024).toFixed(1)} MB).`);
