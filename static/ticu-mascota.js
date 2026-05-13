/**
 * TICU — Mascota Pingüino
 * Uso:
 *   <div id="mi-ticu"></div>
 *   <script>TICU.render('mi-ticu', 'idle', '¡Hola! Soy TICU 🐧')</script>
 *
 * Estados: 'idle' | 'happy' | 'celebrate' | 'sad' | 'thinking'
 * Tamaños: 'sm' | 'md' (default) | 'lg'
 */

const TICU = (() => {

  const MSGS = {
    idle:      '¡Hola! Soy TICU 🐧',
    happy:     '¡Correcto! 🎉',
    celebrate: '¡Módulo completado! 🏆',
    sad:       '¡Casi! Inténtalo de nuevo 💪',
    thinking:  'Hmm... piénsalo bien 🤔',
  };

  function svgBase(cx, cy, estado) {
    const wingAnim = estado === 'celebrate'
      ? `style="transform-origin:top right; animation:ticu-wing-l-cel 0.8s ease-in-out infinite"`
      : `style="transform-origin:top right; animation:ticu-wing-l 2s ease-in-out infinite"`;
    const wingAnimR = estado === 'celebrate'
      ? `style="transform-origin:top left; animation:ticu-wing-r-cel 0.8s ease-in-out infinite"`
      : `style="transform-origin:top left; animation:ticu-wing-r 2s ease-in-out infinite"`;

    const bodyAnim = {
      idle:      'ticu-idle 2s ease-in-out infinite',
      happy:     'ticu-happy 0.6s ease-in-out infinite',
      thinking:  'ticu-thinking 1.8s ease-in-out infinite',
      celebrate: 'ticu-celebrate 0.8s ease-in-out infinite',
      sad:       'ticu-sad 2.5s ease-in-out infinite',
    }[estado] || 'ticu-idle 2s ease-in-out infinite';

    const hatColor = estado === 'celebrate' ? '#fbbf24' : '#4f8ef7';

    // Cara según estado
    let face = '';
    if (estado === 'idle' || estado === 'thinking') {
      face = `
        <g style="transform-origin:${cx-10}px ${cy-4}px; animation:ticu-blink 3s ease-in-out infinite">
          <circle cx="${cx-10}" cy="${cy-4}" r="6" fill="white"/>
          <circle cx="${cx-9}" cy="${cy-4}" r="3.5" fill="#1a1a2e"/>
          <circle cx="${cx-8}" cy="${cy-5.5}" r="1.2" fill="white"/>
        </g>
        <g style="transform-origin:${cx+10}px ${cy-4}px; animation:ticu-blink 3s ease-in-out infinite; animation-delay:.2s">
          <circle cx="${cx+10}" cy="${cy-4}" r="6" fill="white"/>
          <circle cx="${cx+11}" cy="${cy-4}" r="3.5" fill="#1a1a2e"/>
          <circle cx="${cx+12}" cy="${cy-5.5}" r="1.2" fill="white"/>
        </g>`;
    } else if (estado === 'happy' || estado === 'celebrate') {
      face = `
        <path d="M${cx-16} ${cy-4} Q${cx-10} ${cy+2} ${cx-4} ${cy-4}" fill="none" stroke="#1a1a2e" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M${cx+4} ${cy-4} Q${cx+10} ${cy+2} ${cx+16} ${cy-4}" fill="none" stroke="#1a1a2e" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="${cx-10}" cy="${cy+3}" r="5" fill="rgba(249,115,22,0.25)"/>
        <circle cx="${cx+10}" cy="${cy+3}" r="5" fill="rgba(249,115,22,0.25)"/>
        <path d="M${cx-7} ${cy+9} Q${cx} ${cy+16} ${cx+7} ${cy+9}" fill="none" stroke="#f97316" stroke-width="2.5" stroke-linecap="round"/>`;
    } else if (estado === 'sad') {
      face = `
        <path d="M${cx-16} ${cy-2} Q${cx-10} ${cy-7} ${cx-4} ${cy-2}" fill="none" stroke="#1a1a2e" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M${cx+4} ${cy-2} Q${cx+10} ${cy-7} ${cx+16} ${cy-2}" fill="none" stroke="#1a1a2e" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="${cx-10}" cy="${cy-4}" r="2.5" fill="#1a1a2e"/>
        <circle cx="${cx+10}" cy="${cy-4}" r="2.5" fill="#1a1a2e"/>
        <ellipse cx="${cx-12}" cy="${cy+4}" rx="2" ry="3" fill="#4f8ef7" opacity=".8"/>
        <path d="M${cx-7} ${cy+13} Q${cx} ${cy+8} ${cx+7} ${cy+13}" fill="none" stroke="#1a1a2e" stroke-width="2" stroke-linecap="round"/>`;
    }

    // Puntos pensamiento
    const thinkDots = estado === 'thinking' ? `
      <path d="M${cx+11} ${cy+15} Q${cx+23} ${cy+8} ${cx+27} ${cy+2}" fill="none" stroke="#1a1a2e" stroke-width="3" stroke-linecap="round"/>
      <circle cx="${cx+27}" cy="${cy-12}" r="3" fill="#4f8ef7" style="animation:ticu-dot-1 1.2s ease-in-out infinite"/>
      <circle cx="${cx+34}" cy="${cy-18}" r="4" fill="#4f8ef7" style="animation:ticu-dot-2 1.2s ease-in-out infinite"/>
      <circle cx="${cx+39}" cy="${cy-26}" r="5" fill="#4f8ef7" style="animation:ticu-dot-3 1.2s ease-in-out infinite"/>` : '';

    // Estrellas celebración
    const stars = estado === 'celebrate' ? `
      <text style="--dx:-18px;--dy:-22px; animation:ticu-star 1s ease-out infinite" x="${cx}" y="${cy-40}" text-anchor="middle" font-size="14" fill="#fbbf24">★</text>
      <text style="--dx:18px;--dy:-20px; animation:ticu-star 1s ease-out infinite; animation-delay:.15s" x="${cx}" y="${cy-40}" text-anchor="middle" font-size="12" fill="#f97316">★</text>
      <text style="--dx:0px;--dy:-28px; animation:ticu-star 1s ease-out infinite; animation-delay:.3s" x="${cx}" y="${cy-40}" text-anchor="middle" font-size="10" fill="#fbbf24">★</text>` : '';

    return `
      ${stars}
      <g style="animation:${bodyAnim}">
        <ellipse cx="${cx}" cy="${cy+75}" rx="22" ry="5" fill="rgba(0,0,0,0.08)"/>
        <g ${wingAnim}>
          <ellipse cx="${cx-27}" cy="${cy+28}" rx="10" ry="22" fill="#1a1a2e" transform="rotate(-12,${cx-27},${cy+12})"/>
        </g>
        <g ${wingAnimR}>
          <ellipse cx="${cx+27}" cy="${cy+28}" rx="10" ry="22" fill="#1a1a2e" transform="rotate(12,${cx+27},${cy+12})"/>
        </g>
        <ellipse cx="${cx}" cy="${cy+35}" rx="28" ry="38" fill="#1a1a2e"/>
        <ellipse cx="${cx}" cy="${cy+42}" rx="18" ry="26" fill="#f0f4ff"/>
        <circle cx="${cx}" cy="${cy-2}" r="26" fill="#1a1a2e"/>
        <ellipse cx="${cx}" cy="${cy}" rx="18" ry="19" fill="#f0f4ff"/>
        ${face}
        <ellipse cx="${cx}" cy="${cy+8}" rx="7" ry="4.5" fill="#f97316"/>
        <path d="M${cx-7} ${cy+8} Q${cx} ${cy+13} ${cx+7} ${cy+8}" fill="#e07010" stroke="none"/>
        <ellipse cx="${cx-10}" cy="${cy+72}" rx="10" ry="5" fill="#f97316"/>
        <ellipse cx="${cx+10}" cy="${cy+72}" rx="10" ry="5" fill="#f97316"/>
        <rect x="${cx-20}" y="${cy-26}" width="40" height="8" rx="4" fill="${hatColor}"/>
        <rect x="${cx-23}" y="${cy-22}" width="46" height="5" rx="2.5" fill="${hatColor}"/>
        <circle cx="${cx}" cy="${cy-27}" r="5" fill="${hatColor}"/>
        <circle cx="${cx}" cy="${cy-29}" r="3" fill="white"/>
        ${thinkDots}
      </g>`;
  }

  function render(containerId, estado = 'idle', mensaje = null, size = 'md') {
    const container = document.getElementById(containerId);
    if (!container) return;

    const msg = mensaje || MSGS[estado] || MSGS.idle;
    const sizeClass = size !== 'md' ? ` ticu-${size}` : '';

    const vbW = 90, vbH = 120;
    const cx = 45, cy = 38;

    container.innerHTML = `
      <div class="ticu-wrap${sizeClass}">
        <div class="ticu-bubble">${msg}</div>
        <svg viewBox="0 0 ${vbW} ${vbH}" xmlns="http://www.w3.org/2000/svg">
          ${svgBase(cx, cy, estado)}
        </svg>
      </div>`;
  }

  // Cambia el estado de un TICU ya renderizado
  function setState(containerId, estado, mensaje = null) {
    render(containerId, estado, mensaje);
  }

  return { render, setState, MSGS };
})();