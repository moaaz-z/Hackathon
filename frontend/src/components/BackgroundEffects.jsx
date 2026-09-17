import { useEffect } from "react";

const particles = [
  { left: "8%", top: "18%", delay: "-2s", duration: "15s", type: "dot" },
  { left: "16%", top: "68%", delay: "-7s", duration: "18s", type: "ring" },
  { left: "28%", top: "29%", delay: "-4s", duration: "20s", type: "dash" },
  { left: "39%", top: "82%", delay: "-10s", duration: "17s", type: "dot" },
  { left: "55%", top: "14%", delay: "-6s", duration: "22s", type: "ring" },
  { left: "66%", top: "74%", delay: "-3s", duration: "19s", type: "dash" },
  { left: "77%", top: "34%", delay: "-9s", duration: "16s", type: "dot" },
  { left: "89%", top: "63%", delay: "-5s", duration: "21s", type: "ring" },
];

const glyphs = [
  { value: "{ }", left: "7%", top: "42%", delay: "-4s" },
  { value: "</>", left: "91%", top: "26%", delay: "-10s" },
  { value: "01", left: "84%", top: "81%", delay: "-7s" },
  { value: "#", left: "18%", top: "88%", delay: "-12s" },
];

const leftNodes = [
  { x: 18, y: 18 },
  { x: 60, y: 10 },
  { x: 86, y: 43 },
  { x: 53, y: 68 },
  { x: 12, y: 58 },
];

const leftLinks = [
  { x: 18, y: 18, width: 45, angle: -10 },
  { x: 60, y: 10, width: 43, angle: 52 },
  { x: 53, y: 68, width: 40, angle: -42 },
  { x: 12, y: 58, width: 45, angle: -55 },
  { x: 12, y: 58, width: 44, angle: 12 },
];

const rightNodes = [
  { x: 13, y: 34 },
  { x: 43, y: 14 },
  { x: 78, y: 25 },
  { x: 88, y: 64 },
  { x: 46, y: 78 },
];

const rightLinks = [
  { x: 13, y: 34, width: 39, angle: -34 },
  { x: 43, y: 14, width: 38, angle: 18 },
  { x: 78, y: 25, width: 40, angle: 69 },
  { x: 46, y: 78, width: 45, angle: -18 },
  { x: 13, y: 34, width: 46, angle: 48 },
];

function Network({ className, nodes, links }) {
  return (
    <div className={`repo-network ${className}`}>
      {links.map((link, index) => (
        <span
          className="repo-network-link"
          key={`link-${index}`}
          style={{
            left: `${link.x}%`,
            top: `${link.y}%`,
            width: `${link.width}%`,
            transform: `rotate(${link.angle}deg)`,
          }}
        />
      ))}

      {nodes.map((node, index) => (
        <span
          className={`repo-network-node ${index === 2 ? "node-active" : ""}`}
          key={`node-${index}`}
          style={{ left: `${node.x}%`, top: `${node.y}%` }}
        />
      ))}
    </div>
  );
}

export default function BackgroundEffects() {
  useEffect(() => {
    const root = document.documentElement;
    const finePointer = window.matchMedia("(pointer: fine)");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    if (!finePointer.matches || reducedMotion.matches) return undefined;

    let frame = 0;

    const updatePointer = (event) => {
      cancelAnimationFrame(frame);

      frame = requestAnimationFrame(() => {
        const x = event.clientX;
        const y = event.clientY;
        const nx = x / window.innerWidth - 0.5;
        const ny = y / window.innerHeight - 0.5;

        root.style.setProperty("--pointer-x", `${x}px`);
        root.style.setProperty("--pointer-y", `${y}px`);
        root.style.setProperty("--parallax-x", `${nx * 28}px`);
        root.style.setProperty("--parallax-y", `${ny * 22}px`);
        root.style.setProperty("--parallax-x-soft", `${nx * -14}px`);
        root.style.setProperty("--parallax-y-soft", `${ny * -12}px`);

        const target = event.target.closest?.(
          ".interactive-panel, .search-stage-pro, .engine-map, .metric-card, .signal-card, .architecture-node-clean"
        );

        if (target) {
          const rect = target.getBoundingClientRect();
          const localX = ((x - rect.left) / rect.width) * 100;
          const localY = ((y - rect.top) / rect.height) * 100;

          target.style.setProperty("--shine-x", `${localX}%`);
          target.style.setProperty("--shine-y", `${localY}%`);
        }
      });
    };

    const resetPointer = () => {
      root.style.setProperty("--parallax-x", "0px");
      root.style.setProperty("--parallax-y", "0px");
      root.style.setProperty("--parallax-x-soft", "0px");
      root.style.setProperty("--parallax-y-soft", "0px");
    };

    window.addEventListener("pointermove", updatePointer, { passive: true });
    document.documentElement.addEventListener("mouseleave", resetPointer);

    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("pointermove", updatePointer);
      document.documentElement.removeEventListener("mouseleave", resetPointer);
    };
  }, []);

  return (
    <div className="background-fx" aria-hidden="true">
      <div className="pointer-aura" />
      <div className="dynamic-grid" />
      <div className="background-vignette" />

      <div className="orbit-system orbit-system-left">
        <span className="orbit-ring orbit-ring-one" />
        <span className="orbit-ring orbit-ring-two" />
        <span className="orbit-core" />
      </div>

      <div className="orbit-system orbit-system-right">
        <span className="orbit-ring orbit-ring-one" />
        <span className="orbit-ring orbit-ring-two" />
        <span className="orbit-core" />
      </div>

      <Network
        className="repo-network-left"
        nodes={leftNodes}
        links={leftLinks}
      />

      <Network
        className="repo-network-right"
        nodes={rightNodes}
        links={rightLinks}
      />

      <div className="background-particles">
        {particles.map((particle, index) => (
          <span
            className={`background-particle particle-${particle.type}`}
            key={index}
            style={{
              left: particle.left,
              top: particle.top,
              animationDelay: particle.delay,
              animationDuration: particle.duration,
            }}
          />
        ))}
      </div>

      <div className="background-glyphs">
        {glyphs.map((glyph) => (
          <span
            className="background-glyph"
            key={glyph.value}
            style={{
              left: glyph.left,
              top: glyph.top,
              animationDelay: glyph.delay,
            }}
          >
            {glyph.value}
          </span>
        ))}
      </div>

      <div className="background-scan-beam" />
    </div>
  );
}
