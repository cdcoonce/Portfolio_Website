// @ts-check
import metrics from '../data/metrics.json';

/**
 * Renders a project's "cockpit" summary as an inline SVG straight from
 * src/data/metrics.json. Bar widths are derived from the values, so updating a
 * number is a pure data edit — the artwork never needs to be re-drawn. A
 * scheduled collector can overwrite metrics.json to keep the cards current.
 */

const GREEN = '#2f6f5f';
const GOLD = '#b0872f';
const TRACK = '#eeeeea';
const TILE_BG = '#f6f6f4';
const TILE_XS = [40, 204, 368, 532];
const BAR_X = 210;
const BAR_W = 388;
const COUNT_X = 662;

/** Rough pixel width for a pill/chip from its text length (12–13px sans). */
const pillWidth = (text) => Math.round(text.length * 7.2 + 42);
const chipWidth = (text) => Math.round(text.length * 6.3 + 28);

/**
 * @param {{ slug: string, className?: string }} props
 */
export default function Cockpit({ slug, className }) {
  const data = metrics[slug];
  if (!data) return null;

  // Lay the blocks (bar lists / chip rows) out from a running y cursor.
  const blockEls = [];
  let y = 340;
  let k = 0;
  for (const block of data.blocks ?? []) {
    if (block.title) {
      blockEls.push(
        <text key={k++} x="40" y={y + 12} fontSize="12" fontWeight="600" letterSpacing="1.2" fill="#9a9a95">
          {block.title}
        </text>,
      );
      y += 28;
    }
    if (block.type === 'bars') {
      const max = Math.max(...block.items.map((i) => i.value)) || 1;
      for (const item of block.items) {
        const w = Math.max(8, Math.round((BAR_W * item.value) / max));
        const rowY = y;
        blockEls.push(
          <text key={k++} x="40" y={rowY + 9} fontSize="13.5" fill="#3a3a3a">{item.label}</text>,
          <rect key={k++} x={BAR_X} y={rowY} width={BAR_W} height="10" rx="5" fill={TRACK} />,
          <rect key={k++} x={BAR_X} y={rowY} width={w} height="10" rx="5" fill={item.accent === 'gold' ? GOLD : GREEN} />,
          <text key={k++} x={COUNT_X} y={rowY + 9} fontSize="13.5" fill="#6a6a66" textAnchor="end" fontWeight="600">
            {item.value}
          </text>,
        );
        y += 27;
      }
      y += 8;
    } else if (block.type === 'chips') {
      let x = 40;
      const chipY = y;
      for (const label of block.items) {
        const w = chipWidth(label);
        blockEls.push(
          <rect key={k++} x={x} y={chipY} width={w} height="30" rx="15" fill={TILE_BG} />,
          <text key={k++} x={x + w / 2} y={chipY + 20} fontSize="12" fill="#6a6a66" textAnchor="middle">
            {label}
          </text>,
        );
        x += w + 10;
      }
      y += 42;
    }
  }

  const pillW = data.pill ? pillWidth(data.pill) : 0;

  return (
    <svg
      className={className}
      viewBox="0 0 720 560"
      preserveAspectRatio="xMidYMid meet"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label={`${data.headline} — ${data.tiles.map((t) => `${t.value} ${t.label}`).join(', ')}`}
      fontFamily="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
    >
      <rect width="720" height="560" fill="#ffffff" />

      <circle cx="44" cy="66" r="5" fill="#4f7a4f" />
      <text x="58" y="71" fontSize="13" fontWeight="600" letterSpacing="1.5" fill="#9a9a95">{data.eyebrow}</text>
      {data.pill && (
        <g>
          <rect x={680 - pillW} y="52" width={pillW} height="30" rx="15" fill="none" stroke="#e4e4e0" />
          <text x={680 - pillW / 2} y="72" fontSize="13" fontWeight="500" fill="#6a6a66" textAnchor="middle">
            {data.pill}
          </text>
        </g>
      )}

      <text x="40" y="130" fontSize="27" fontWeight="700" fill="#1f1f1f">{data.headline}</text>
      <text x="40" y="160" fontSize="15" fill="#8a8a86">{data.subtitle}</text>

      {data.tiles.map((tile, i) => (
        <g key={`tile-${i}`}>
          <rect x={TILE_XS[i]} y="196" width="148" height="112" rx="14" fill={TILE_BG} />
          <text x={TILE_XS[i] + 74} y="258" fontSize="36" fontWeight="700" fill={tile.accent ? GREEN : '#1f1f1f'} textAnchor="middle">
            {tile.value}
          </text>
          <text x={TILE_XS[i] + 74} y="286" fontSize="12.5" fill="#8a8a86" textAnchor="middle">{tile.label}</text>
        </g>
      ))}

      {blockEls}
    </svg>
  );
}
