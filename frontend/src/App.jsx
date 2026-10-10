import { Canvas, useFrame } from "@react-three/fiber";
import {
  Environment,
  Float,
  OrbitControls,
  RoundedBox,
} from "@react-three/drei";
import { useEffect, useState, useRef } from "react";
import "./App.css";

function fixCurrencyEncoding(text) {
  return String(text || "")
    .replaceAll("â¹", "₹")
    .replaceAll("â‚¹", "₹");
}

/* -------------------- 3D CAPSULE -------------------- */

function Capsule3D() {
  const capsule = useRef();

  useFrame((state) => {
    if (!capsule.current) return;
    capsule.current.rotation.y =
      Math.sin(state.clock.elapsedTime * 0.35) * 0.18;
    capsule.current.rotation.x =
      Math.sin(state.clock.elapsedTime * 0.25) * 0.04;
  });

  return (
    <Float speed={1.2} rotationIntensity={0.15} floatIntensity={0.5}>
      <group ref={capsule} rotation={[0, -0.3, 0]}>
        <RoundedBox args={[3.9, 2.4, 1.15]} radius={0.55} smoothness={8}>
          <meshPhysicalMaterial
            color="#111827"
            metalness={0.8}
            roughness={0.2}
            clearcoat={1}
            clearcoatRoughness={0.12}
          />
        </RoundedBox>

        <RoundedBox
          args={[3.25, 1.75, 1.23]}
          radius={0.42}
          smoothness={8}
          position={[0, 0, 0.05]}
        >
          <meshPhysicalMaterial
            color="#0b1220"
            metalness={0.25}
            roughness={0.12}
            transmission={0.2}
            transparent
            opacity={0.9}
          />
        </RoundedBox>

        <mesh position={[0, 0, 0.68]}>
          <boxGeometry args={[3.15, 0.025, 0.025]} />
          <meshBasicMaterial color="#a371f7" />
        </mesh>

        <mesh position={[0, 0, 0.7]}>
          <sphereGeometry args={[0.22, 32, 32]} />
          <meshStandardMaterial
            color="#a371f7"
            emissive="#a371f7"
            emissiveIntensity={4}
          />
        </mesh>

        {[
          [-1.15, 0.42],
          [-0.65, -0.38],
          [0.8, 0.35],
          [1.15, -0.3],
        ].map(([x, y], index) => (
          <mesh key={index} position={[x, y, 0.7]}>
            <sphereGeometry args={[0.055, 16, 16]} />
            <meshBasicMaterial
              color={index % 2 === 0 ? "#a371f7" : "#3fb950"}
            />
          </mesh>
        ))}

        <mesh rotation={[Math.PI / 2.4, 0, 0]}>
          <torusGeometry args={[2.35, 0.012, 16, 100]} />
          <meshBasicMaterial
            color="#a371f7"
            transparent
            opacity={0.35}
          />
        </mesh>
      </group>
    </Float>
  );
}

function CapsuleScene() {
  return (
    <Canvas
      camera={{ position: [0, 0, 9.5], fov: 36 }}
      gl={{ antialias: true, alpha: true }}
    >
      <ambientLight intensity={1.2} />
      <directionalLight position={[5, 6, 7]} intensity={3.5} />
      <pointLight position={[-4, 2, 5]} color="#a371f7" intensity={14} />
      <pointLight position={[4, -2, 3]} color="#3fb950" intensity={9} />
      <Capsule3D />
      <Environment preset="city" />
      <OrbitControls
        enableZoom={false}
        enablePan={false}
        enableRotate={false}
      />
    </Canvas>
  );
}

/* -------------------- SHARED COMPONENTS -------------------- */

function CategoryRow({ name, value, percentage }) {
  return (
    <div className="category-row">
      <span className="category-name">{name}</span>
      <div className="category-progress">
        <div
          className="category-progress-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="category-value">
        ₹{Number(value).toLocaleString("en-IN")}
      </span>
    </div>
  );
}

function Sidebar({ activeSection, navigate }) {
  const items = [
    { id: "dashboard", icon: "▦", label: "Overview" },
    { id: "intelligence", icon: "✳", label: "AI Assistant" },
    { id: "memory", icon: "◈", label: "Memory" },
    { id: "privacy", icon: "⬡", label: "Privacy" },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-heading">WORKSPACE</div>

      {items.map((item) => (
        <a
          key={item.id}
          href={`#${item.id}`}
          className={`sidebar-link ${
            activeSection === item.id ? "active" : ""
          }`}
          onClick={() => navigate(item.id)}
        >
          <span>{item.icon}</span>
          {item.label}
        </a>
      ))}

      <div className="sidebar-bottom">
        <span className="sidebar-status-dot" />
        <span>Private workspace</span>
        <small>Wealth Capsule · Local UI</small>
      </div>
    </aside>
  );
}

/* -------------------- MAIN APP -------------------- */

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [dashboardError, setDashboardError] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [privacyAudit, setPrivacyAudit] = useState(null);
  const [sources, setSources] = useState([]);
  const [asking, setAsking] = useState(false);
  const [askError, setAskError] = useState("");
  const [activeSection, setActiveSection] = useState("dashboard");

  useEffect(() => {
    let cancelled = false;

    Promise.all([
      fetch("/api/dashboard"),
      fetch("/api/privacy-audit"),
    ])
      .then(async ([dashboardResponse, privacyResponse]) => {
        if (!dashboardResponse.ok) {
          throw new Error("Failed to load dashboard");
        }
        if (!privacyResponse.ok) {
          throw new Error("Failed to load privacy audit");
        }

        const dashboardData = await dashboardResponse.json();
        const privacyData = await privacyResponse.json();

        return { dashboardData, privacyData };
      })
      .then(({ dashboardData, privacyData }) => {
        if (cancelled) return;
        setDashboard(dashboardData);
        setPrivacyAudit(privacyData);
        setDashboardError(false);
      })
      .catch((error) => {
        console.error("Dashboard / Privacy Audit error:", error);
        if (!cancelled) setDashboardError(true);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const sectionIds = [
      "dashboard",
      "intelligence",
      "memory",
      "privacy",
    ];

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort(
            (a, b) =>
              b.intersectionRatio - a.intersectionRatio
          );

        if (visible[0]) {
          setActiveSection(visible[0].target.id);
        }
      },
      {
        rootMargin: "-20% 0px -55% 0px",
        threshold: [0, 0.15, 0.35, 0.6],
      }
    );

    sectionIds.forEach((id) => {
      const element = document.getElementById(id);
      if (element) observer.observe(element);
    });

    return () => observer.disconnect();
  }, [dashboard]);

  const navigate = (sectionId) => {
    setActiveSection(sectionId);
    document.getElementById(sectionId)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  const askCapsule = async () => {
    if (!question.trim() || asking) return;

    setAsking(true);
    setAnswer("");
    setSources([]);
    setAskError("");

    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question.trim() }),
      });

      if (!response.ok) {
        throw new Error("Unable to get response");
      }

      const data = await response.json();
      setAnswer(fixCurrencyEncoding(data.answer));
      setSources(Array.isArray(data.sources) ? data.sources : []);
    } catch (error) {
      console.error("Ask Capsule error:", error);
      setAskError(
        "Wealth Capsule could not process your request. Please try again."
      );
    } finally {
      setAsking(false);
    }
  };

  if (!dashboard && !dashboardError) {
    return (
      <div className="app">
        <nav className="navbar">
          <div className="brand">
            <div className="brand-symbol">W</div>
            <div>
              <div className="brand-name">WEALTH CAPSULE</div>
              <div className="brand-status">PRIVATE AI</div>
            </div>
          </div>
          <div className="online-status">
            <span /> CONNECTING
          </div>
        </nav>
        <main className="workspace-loading">
          Loading your private capsule...
        </main>
      </div>
    );
  }

  if (dashboardError) {
    return (
      <div className="app">
        <nav className="navbar">
          <div className="brand">
            <div className="brand-symbol">W</div>
            <div>
              <div className="brand-name">WEALTH CAPSULE</div>
              <div className="brand-status">PRIVATE AI</div>
            </div>
          </div>
          <div className="online-status">
            <span /> OFFLINE
          </div>
        </nav>
        <main className="workspace-loading">
          <h2>Unable to load Wealth Capsule</h2>
          <p>Make sure the FastAPI backend is running on port 8000.</p>
          <button
            className="secondary-button"
            onClick={() => window.location.reload()}
          >
            Retry
          </button>
        </main>
      </div>
    );
  }

  const categories = dashboard.categories || {};
  const categoryEntries = Object.entries(categories);
  const categoryTotal = Object.values(categories).reduce(
    (sum, value) => sum + Number(value || 0),
    0
  );
  const monthlySpending = Number(dashboard.monthly_spending || 0);
  const percentageChange = Number(dashboard.percentage_change || 0);
  const isIncrease = percentageChange > 0;

  return (
    <div className="app">
      <nav className="navbar">
        <a
          href="#dashboard"
          className="brand"
          onClick={() => navigate("dashboard")}
        >
          <div className="brand-symbol">W</div>
          <div>
            <div className="brand-name">WEALTH CAPSULE</div>
            <div className="brand-status">PRIVATE AI WORKSPACE</div>
          </div>
        </a>

        <div className="nav-links">
          <a href="#dashboard" onClick={() => navigate("dashboard")}>
            Overview
          </a>
          <a href="#intelligence" onClick={() => navigate("intelligence")}>
            Assistant
          </a>
          <a href="#privacy" onClick={() => navigate("privacy")}>
            Privacy
          </a>
        </div>

        <div className="online-status">
          <span /> SYSTEM ONLINE
        </div>
      </nav>

      <div className="workspace-shell">
        <Sidebar activeSection={activeSection} navigate={navigate} />

        <div className="workspace-main">
          <main className="hero">
            <section className="hero-content">
              <div className="hero-eyebrow">
                PRIVATE FINANCIAL INTELLIGENCE
              </div>

              <h1>
                Your money.
                <br />
                <span>Your control.</span>
              </h1>

              <p className="hero-description">
                Wealth Capsule is a privacy-first AI assistant that
                helps you understand spending, research public
                information, and keep your financial context under
                your control.
              </p>

              <div className="hero-actions">
                <button
                  className="primary-button"
                  onClick={() => navigate("dashboard")}
                >
                  OPEN CAPSULE <span>→</span>
                </button>

                <button
                  className="secondary-button"
                  onClick={() => navigate("privacy")}
                >
                  HOW IT WORKS
                </button>
              </div>

              <div className="hero-trust">
                <div>
                  <strong>LOCAL</strong>
                  <span>PRIVATE DATA</span>
                </div>
                <div>
                  <strong>NEMOTRON</strong>
                  <span>AI REASONING</span>
                </div>
                <div>
                  <strong>TAVILY</strong>
                  <span>WEB RESEARCH</span>
                </div>
              </div>
            </section>

            <section className="hero-visual">
              <div className="visual-label top-label">
                <span /> PRIVATE CORE
              </div>
              <CapsuleScene />
              <div className="visual-label bottom-label">
                ENCRYPTED CONTEXT
              </div>
            </section>
          </main>

          <section id="dashboard" className="dashboard">
            <div className="dashboard-header">
              <div>
                <div className="section-eyebrow">CAPSULE OVERVIEW</div>
                <h2>
                  Financial intelligence,
                  <br />
                  without giving up control.
                </h2>
              </div>

              <div className="dashboard-date">
                DEMO WORKSPACE
                <span>LIVE BACKEND DATA</span>
              </div>
            </div>

            <div className="dashboard-grid">
              <div className="card spending-card">
                <div className="card-top">
                  <span>MONTHLY SPENDING</span>
                  <div className="card-dot" />
                </div>

                <div className="big-number">
                  ₹{monthlySpending.toLocaleString("en-IN")}
                </div>

                <div
                  className={`change ${
                    isIncrease ? "negative" : "positive"
                  }`}
                >
                  {isIncrease ? "↑" : "↓"}{" "}
                  {Math.abs(percentageChange).toFixed(2)}%
                  <span>vs previous month</span>
                </div>

                <div className="mini-chart">
                  <div className="chart-line">
                    {Array.from({ length: 7 }, (_, i) => (
                      <span key={i} />
                    ))}
                  </div>
                </div>
              </div>

              <div className="card category-card">
                <div className="card-top">
                  <span>SPENDING BREAKDOWN</span>
                  <span className="muted">
                    {categoryEntries.length} CATEGORIES
                  </span>
                </div>

                <div className="category-list">
                  {categoryEntries.map(([name, value]) => {
                    const numericValue = Number(value || 0);
                    const percentage =
                      categoryTotal > 0
                        ? (numericValue / categoryTotal) * 100
                        : 0;

                    return (
                      <CategoryRow
                        key={name}
                        name={name}
                        value={numericValue}
                        percentage={percentage}
                      />
                    );
                  })}
                </div>
              </div>

              <div id="intelligence" className="card feature-card">
                <div className="feature-number">01</div>
                <div className="feature-icon">AI</div>
                <div className="feature-label">NEMOTRON</div>
                <h3>Private AI reasoning</h3>
                <p>
                  Nemotron analyzes the financial context prepared
                  by your application.
                </p>
                <div className="feature-footer">
                  NVIDIA MODEL
                  <span>
                    {dashboard.nemotron === "active"
                      ? "CONNECTED"
                      : "CHECK STATUS"}
                  </span>
                </div>
              </div>

              <div className="card feature-card">
                <div className="feature-number">02</div>
                <div className="feature-icon tavily-icon">WEB</div>
                <div className="feature-label">TAVILY</div>
                <h3>Current public knowledge</h3>
                <p>
                  Research public information without sending
                  raw transactions to the research tool.
                </p>
                <div className="feature-footer">
                  WEB RESEARCH
                  <span>
                    {dashboard.tavily === "active"
                      ? "ACTIVE"
                      : "CHECK STATUS"}
                  </span>
                </div>
              </div>

              <div id="privacy" className="card feature-card privacy-feature">
                <div className="feature-number">03</div>
                <div className="privacy-circle">SAFE</div>
                <div className="feature-label">PRIVACY GATEWAY</div>
                <h3>Control what is shared</h3>
                <p>
                  The gateway helps limit which financial details
                  are included in external requests.
                </p>
                <div className="feature-footer">
                  PRIVACY STATUS
                  <span>
                    {dashboard.privacy_gateway === "protected"
                      ? "PROTECTED"
                      : "CHECK STATUS"}
                  </span>
                </div>
              </div>

              <div id="memory" className="card memory-card">
                <div className="memory-left">
                  <div className="feature-number">04</div>
                  <div className="memory-icon">MEM</div>
                </div>

                <div className="memory-content">
                  <div className="feature-label">PRIVATE MEMORY</div>
                  <h3>Context that improves over time.</h3>
                  <p>
                    Useful historical context can help make
                    future answers more relevant.
                  </p>
                </div>

                <div className="memory-count">
                  <strong>{dashboard.memory_count ?? 0}</strong>
                  <span>RELEVANT MEMORIES</span>
                </div>
              </div>

              {privacyAudit && (
                <div className="card privacy-audit-card">
                  <div className="privacy-audit-header">
                    <div>
                      <div className="feature-label">PRIVACY AUDIT</div>
                      <h3>Review your privacy controls.</h3>
                      <p>
                        Review the gateway's configured safeguards
                        and audit information.
                      </p>
                    </div>
                    <div className="privacy-status">
                      🔒 AUDIT AVAILABLE
                    </div>
                  </div>

                  <div className="privacy-audit-grid">
                    {[
                      ["01", "Raw transactions", "Not intended for public research"],
                      ["02", "Financial amounts", "Minimize external disclosure"],
                      ["03", "Personal dates", "Avoid unnecessary personal details"],
                      ["04", "External content", "Treat research content as untrusted"],
                    ].map(([number, title, description]) => (
                      <div className="privacy-item" key={number}>
                        <span className="audit-check">{number}</span>
                        <div>
                          <span className="audit-icon">CHECK</span>
                          <strong>{title}</strong>
                          <small>{description}</small>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="card ask-card">
                <div className="ask-header">
                  <div>
                    <div className="feature-label">ASK WEALTH CAPSULE</div>
                    <h3>Your private AI assistant.</h3>
                    <p>
                      Ask about spending, budgeting, or public
                      financial information.
                    </p>
                  </div>

                  <div className="ask-status">
                    <span />
                    AI ASSISTANT
                  </div>
                </div>

                <form
                  className="ask-input-area"
                  onSubmit={(event) => {
                    event.preventDefault();
                    askCapsule();
                  }}
                >
                  <textarea
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    placeholder="Why did my spending change this month?"
                    rows={3}
                    disabled={asking}
                  />

                  <button
                    type="submit"
                    className="primary-button ask-button"
                    disabled={!question.trim() || asking}
                  >
                    {asking ? "ANALYZING..." : "ASK CAPSULE"}
                    <span>→</span>
                  </button>
                </form>

                {asking && (
                  <div className="ask-loading">
                    <span />
                    <span />
                    <span />
                    <p>Analyzing your question...</p>
                  </div>
                )}

                {askError && (
                  <div className="ask-error">{askError}</div>
                )}

                {answer && (
                  <div className="ask-response">
                    <div className="response-label">CAPSULE RESPONSE</div>
                    <div className="response-text">{answer}</div>

                    <div className="response-meta">
                      <span>🔒 PRIVATE CONTEXT</span>
                      <span>AI · NEMOTRON</span>
                      {sources.length > 0 && (
                        <span>WEB RESEARCH</span>
                      )}
                    </div>

                    {sources.length > 0 && (
                      <div className="source-list">
                        <div className="response-label">SOURCES</div>

                        {sources.map((source, index) => {
                          let hostname = "External source";
                          try {
                            hostname = new URL(source.url).hostname.replace(
                              /^www\./,
                              ""
                            );
                          } catch {
                            // Keep the fallback hostname.
                          }

                          return (
                            <a
                              key={`${source.url || "source"}-${index}`}
                              href={source.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="source-item"
                            >
                              <strong>
                                {source.title || "Research source"}
                              </strong>
                              <span>{hostname}</span>
                            </a>
                          );
                        })}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="dashboard-footer">
              <span>WEALTH CAPSULE</span>
              <span>PRIVACY-FIRST PERSONAL AI</span>
              <span>NEBIUS TOKEN FACTORY</span>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;
