import { Canvas, useFrame } from "@react-three/fiber";
import {
  Environment,
  Float,
  OrbitControls,
  RoundedBox,
} from "@react-three/drei";
import { useEffect, useRef, useState } from "react";
import "./App.css";
function fixCurrencyEncoding(text) {
  return text
    .replaceAll("â¹", "₹")
    .replaceAll("â‚¹", "₹");
}
/* =========================================================
   3D CAPSULE
========================================================= */

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
    <Float
      speed={1.2}
      rotationIntensity={0.15}
      floatIntensity={0.5}
    >
      <group ref={capsule} rotation={[0, -0.3, 0]}>

        {/* Main capsule */}
        <RoundedBox
          args={[3.9, 2.4, 1.15]}
          radius={0.55}
          smoothness={8}
        >
          <meshPhysicalMaterial
            color="#111827"
            metalness={0.8}
            roughness={0.2}
            clearcoat={1}
            clearcoatRoughness={0.12}
          />
        </RoundedBox>

        {/* Inner glass panel */}
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

        {/* Security line */}
        <mesh position={[0, 0, 0.68]}>
          <boxGeometry args={[3.15, 0.025, 0.025]} />
          <meshBasicMaterial color="#38bdf8" />
        </mesh>

        {/* AI core */}
        <mesh position={[0, 0, 0.7]}>
          <sphereGeometry args={[0.22, 32, 32]} />
          <meshStandardMaterial
            color="#38bdf8"
            emissive="#38bdf8"
            emissiveIntensity={4}
          />
        </mesh>

        {/* Data nodes */}
        {[
          [-1.15, 0.42],
          [-0.65, -0.38],
          [0.8, 0.35],
          [1.15, -0.3],
        ].map(([x, y], index) => (
          <mesh
            key={index}
            position={[x, y, 0.7]}
          >
            <sphereGeometry
              args={[0.055, 16, 16]}
            />

            <meshBasicMaterial
              color={
                index % 2 === 0
                  ? "#38bdf8"
                  : "#34d399"
              }
            />
          </mesh>
        ))}

        {/* Orbit ring */}
        <mesh
          rotation={[
            Math.PI / 2.4,
            0,
            0,
          ]}
        >
          <torusGeometry
            args={[2.35, 0.012, 16, 100]}
          />

          <meshBasicMaterial
            color="#38bdf8"
            transparent
            opacity={0.35}
          />
        </mesh>

      </group>
    </Float>
  );
}


/* =========================================================
   CAPSULE SCENE
========================================================= */

function CapsuleScene() {
  return (
    <Canvas
      camera={{
        position: [0, 0, 9.5],
        fov: 36,
      }}
      gl={{
        antialias: true,
        alpha: true,
      }}
    >
      <ambientLight intensity={1.2} />

      <directionalLight
        position={[5, 6, 7]}
        intensity={3.5}
      />

      <pointLight
        position={[-4, 2, 5]}
        color="#38bdf8"
        intensity={14}
      />

      <pointLight
        position={[4, -2, 3]}
        color="#34d399"
        intensity={9}
      />

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


/* =========================================================
   CATEGORY ROW
========================================================= */

function CategoryRow({
  name,
  value,
  percentage,
}) {
  return (
    <div className="category-row">
      <span className="category-name">
        {name}
      </span>

      <div className="category-progress">
        <div
          className="category-progress-fill"
          style={{
            width: `${percentage}%`,
          }}
        />
      </div>

      <span className="category-value">
        &#8377;{value.toLocaleString("en-IN")}
      </span>
    </div>
  );
}


/* =========================================================
   MAIN APP
========================================================= */

function App() {

  /* -------------------------------------------------------
     DASHBOARD STATE
  ------------------------------------------------------- */

  const [dashboard, setDashboard] =
    useState(null);

  const [dashboardError, setDashboardError] =
    useState(false);


  /* -------------------------------------------------------
     AI ASK STATE
  ------------------------------------------------------- */

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const [privacyAudit, setPrivacyAudit] =
    useState(null);

  const [sources, setSources] =
    useState([]);

  const [asking, setAsking] =
    useState(false);

  const [askError, setAskError] =
    useState("");


  /* -------------------------------------------------------
     LOAD DASHBOARD + PRIVACY AUDIT
  ------------------------------------------------------- */

  useEffect(() => {
    Promise.all([
      fetch("/api/dashboard"),
      fetch("/api/privacy-audit"),
    ])
      .then(async ([
        dashboardResponse,
        privacyResponse,
      ]) => {
        if (!dashboardResponse.ok) {
          throw new Error(
            "Failed to load dashboard"
          );
        }

        if (!privacyResponse.ok) {
          throw new Error(
            "Failed to load privacy audit"
          );
        }

        const dashboardData =
          await dashboardResponse.json();

        const privacyData =
          await privacyResponse.json();

        return {
          dashboardData,
          privacyData,
        };
      })
      .then(({
        dashboardData,
        privacyData,
      }) => {
        setDashboard(dashboardData);
        setPrivacyAudit(privacyData);
        setDashboardError(false);
      })
      .catch((error) => {
        console.error(
          "Dashboard / Privacy Audit error:",
          error
        );

        setDashboardError(true);
      });
  }, []);


  /* -------------------------------------------------------
     ASK WEALTH CAPSULE
  ------------------------------------------------------- */

  const askCapsule = async () => {
    if (!question.trim() || asking) {
      return;
    }

    setAsking(true);
    setAnswer("");
    setSources([]);
    setAskError("");

    try {
      const response = await fetch(
        "/api/ask",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            question:
              question.trim(),
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          "Unable to get response"
        );
      }

      const data =
        await response.json();

      setAnswer(
  fixCurrencyEncoding(data.answer || "")
);

      setSources(
        data.sources || []
      );

    } catch (error) {
      console.error(
        "Ask Capsule error:",
        error
      );

      setAskError(
        "Wealth Capsule could not process your request. Please try again."
      );

    } finally {
      setAsking(false);
    }
  };


  /* -------------------------------------------------------
     OPEN CAPSULE
  ------------------------------------------------------- */

  const enterCapsule = () => {
    document
      .getElementById("dashboard")
      ?.scrollIntoView({
        behavior: "smooth",
      });
  };


  /* -------------------------------------------------------
     LOADING STATE
  ------------------------------------------------------- */

  if (
    !dashboard &&
    !dashboardError
  ) {
    return (
      <div className="app">

        <nav className="navbar">

          <div className="brand">

            <div className="brand-symbol">
              W
            </div>

            <div>

              <div className="brand-name">
                WEALTH CAPSULE
              </div>

              <div className="brand-status">
                PRIVATE AI
              </div>

            </div>

          </div>

          <div className="online-status">

            <span />

            CONNECTING

          </div>

        </nav>

        <main
          style={{
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontFamily:
              "DM Sans, sans-serif",
          }}
        >
          Loading your private capsule...
        </main>

      </div>
    );
  }


  /* -------------------------------------------------------
     BACKEND ERROR
  ------------------------------------------------------- */

  if (dashboardError) {
    return (
      <div className="app">

        <nav className="navbar">

          <div className="brand">

            <div className="brand-symbol">
              W
            </div>

            <div>

              <div className="brand-name">
                WEALTH CAPSULE
              </div>

              <div className="brand-status">
                PRIVATE AI
              </div>

            </div>

          </div>

          <div className="online-status">

            <span />

            OFFLINE

          </div>

        </nav>

        <main
          style={{
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: "12px",
            fontFamily:
              "DM Sans, sans-serif",
          }}
        >

          <h2>
            Unable to load Wealth Capsule
          </h2>

          <p>
            Make sure the FastAPI backend
            is running on port 8000.
          </p>

        </main>

      </div>
    );
  }


  /* -------------------------------------------------------
     DASHBOARD DATA
  ------------------------------------------------------- */

  const categories =
    dashboard.categories || {};

  const categoryEntries =
    Object.entries(categories);

  const categoryTotal =
    Object.values(categories).reduce(
      (sum, value) =>
        sum + Number(value),
      0
    );

const monthlySpending =
    Number(
      dashboard.monthly_spending || 0
    );

  const percentageChange =
    Number(
      dashboard.percentage_change || 0
    );

  const isIncrease =
    percentageChange > 0;


  /* -------------------------------------------------------
     RENDER
  ------------------------------------------------------- */

  return (
    <div className="app">

      {/* =================================================
          NAVIGATION
      ================================================= */}

      <nav className="navbar">

        <div className="brand">

          <div className="brand-symbol">
            W
          </div>

          <div>

            <div className="brand-name">
              WEALTH CAPSULE
            </div>

            <div className="brand-status">
              PRIVATE AI
            </div>

          </div>

        </div>


        <div className="nav-links">

          <a href="#dashboard">
            Overview
          </a>

          <a href="#intelligence">
            Intelligence
          </a>

          <a href="#privacy">
            Privacy
          </a>

        </div>


        <div className="online-status">

          <span />

          SYSTEM ONLINE

        </div>

      </nav>


      {/* =================================================
          HERO
      ================================================= */}

      <main className="hero">

        <section className="hero-content">

          <div className="hero-eyebrow">
            PRIVATE FINANCIAL INTELLIGENCE
          </div>


          <h1>

            Your money.

            <br />

            <span>
              Your control.
            </span>

          </h1>


          <p className="hero-description">

            Wealth Capsule is a privacy-first
            AI assistant that understands your
            spending, researches current public
            information and keeps your private
            financial context under your control.

          </p>


          <div className="hero-actions">

            <button
              className="primary-button"
              onClick={enterCapsule}
            >

              OPEN CAPSULE

              <span>
                &#8594;
              </span>

            </button>


            <button className="secondary-button">
              HOW IT WORKS
            </button>

          </div>


          <div className="hero-trust">

            <div>

              <strong>
                LOCAL
              </strong>

              <span>
                PRIVATE DATA
              </span>

            </div>


            <div>

              <strong>
                NEMOTRON
              </strong>

              <span>
                AI REASONING
              </span>

            </div>


            <div>

              <strong>
                TAVILY
              </strong>

              <span>
                LIVE RESEARCH
              </span>

            </div>

          </div>

        </section>


        <section className="hero-visual">

          <div className="visual-label top-label">

            <span />

            PRIVATE CORE

          </div>


          <CapsuleScene />


          <div className="visual-label bottom-label">

            ENCRYPTED CONTEXT

          </div>

        </section>

      </main>


      {/* =================================================
          DASHBOARD
      ================================================= */}

      <section
        id="dashboard"
        className="dashboard"
      >

        {/* DASHBOARD HEADER */}

        <div className="dashboard-header">

          <div>

            <div className="section-eyebrow">
              CAPSULE OVERVIEW
            </div>

            <h2>

              Financial intelligence,

              <br />

              without giving up control.

            </h2>

          </div>


          <div className="dashboard-date">

            OCTOBER 2026

            <span>
              LIVE DEMO DATA
            </span>

          </div>

        </div>


        {/* DASHBOARD GRID */}

        <div className="dashboard-grid">


          {/* =================================================
              SPENDING
          ================================================= */}

          <div className="card spending-card">

            <div className="card-top">

              <span>
                MONTHLY SPENDING
              </span>

              <div className="card-dot" />

            </div>


            <div className="big-number">

              &#8377;
              {monthlySpending.toLocaleString(
                "en-IN"
              )}

            </div>


            <div
              className={`change ${
                isIncrease
                  ? "negative"
                  : "positive"
              }`}
            >

              {isIncrease
                ? "\u2191"
                : "\u2193"}

              {" "}

              {Math.abs(
                percentageChange
              ).toFixed(2)}
              %

              <span>
                vs previous month
              </span>

            </div>


            <div className="mini-chart">

              <div className="chart-line">

                <span />
                <span />
                <span />
                <span />
                <span />
                <span />
                <span />

              </div>

            </div>

          </div>


          {/* =================================================
              CATEGORY
          ================================================= */}

          <div className="card category-card">

            <div className="card-top">

              <span>
                SPENDING BREAKDOWN
              </span>

              <span className="muted">

                {categoryEntries.length}

                {" "}

                CATEGORIES

              </span>

            </div>


            <div className="category-list">

              {categoryEntries.map(
                ([name, value]) => {

                  const numericValue =
                    Number(value);

                  const percentage =
                    categoryTotal > 0
                      ? (
                          numericValue /
                          categoryTotal
                        ) * 100
                      : 0;

                  return (
                    <CategoryRow
                      key={name}
                      name={name}
                      value={
                        numericValue
                      }
                      percentage={
                        percentage
                      }
                    />
                  );
                }
              )}

            </div>

          </div>


          {/* =================================================
              NEMOTRON
          ================================================= */}

          <div
            id="intelligence"
            className="card feature-card"
          >

            <div className="feature-number">
              01
            </div>

            <div className="feature-icon">
            MODEL  
            </div>

            <div className="feature-label">
              NEMOTRON
            </div>

            <h3>
              Private AI reasoning
            </h3>

            <p>

              Nemotron analyzes privacy-safe
              financial context instead of
              receiving raw transactions.

            </p>

            <div className="feature-footer">

              NVIDIA MODEL

              <span>

                {dashboard.nemotron ===
                "active"
                  ? "CONNECTED"
                  : "OFFLINE"}

              </span>

            </div>

          </div>


          {/* =================================================
              TAVILY
          ================================================= */}

          <div className="card feature-card">

            <div className="feature-number">
              02
            </div>

            <div className="feature-icon tavily-icon">
              WEB
            </div>

            <div className="feature-label">
              TAVILY
            </div>

            <h3>
              Current public knowledge
            </h3>

            <p>

              Public research adds current
              financial education without
              exposing private transactions.

            </p>

            <div className="feature-footer">

              WEB RESEARCH

              <span>

                {dashboard.tavily ===
                "active"
                  ? "ACTIVE"
                  : "OFFLINE"}

              </span>

            </div>

          </div>


          {/* =================================================
              PRIVACY
          ================================================= */}

          <div
            id="privacy"
            className="card feature-card privacy-feature"
          >

            <div className="feature-number">
              03
            </div>

            <div className="privacy-circle">
              100%
            </div>

            <div className="feature-label">
              PRIVACY GATEWAY
            </div>

            <h3>
              Your data stays yours
            </h3>

            <p>

              Local analysis creates a minimized
              AI context before anything reaches
              the model.

            </p>

            <div className="feature-footer">

              RAW DATA

              <span>

                {dashboard.privacy_gateway ===
                "protected"
                  ? "LOCAL ONLY"
                  : "CHECK REQUIRED"}

              </span>

            </div>

          </div>


          {/* =================================================
              MEMORY
          ================================================= */}

          <div className="card memory-card">

            <div className="memory-left">

              <div className="feature-number">
                04
              </div>

              <div className="memory-icon">
                MEM
              </div>

            </div>


            <div className="memory-content">

              <div className="feature-label">
                PRIVATE MEMORY
              </div>

              <h3>
                Context that improves over time.
              </h3>

              <p>

                Wealth Capsule stores useful
                historical context locally so
                future answers can become more
                relevant.

              </p>

            </div>


            <div className="memory-count">

              <strong>
                {dashboard?.memory_count ?? 0}
              </strong>

              <span>
                RELEVANT MEMORIES
              </span>

            </div>

          </div>


          {/* =================================================
              PRIVACY AUDIT
          ================================================= */}

          {privacyAudit && (
            <div
              className="card privacy-audit-card"
            >

              <div className="privacy-audit-header">

                <div>

                  <div className="feature-label">
                    PRIVACY AUDIT
                  </div>

                  <h3>
                    Your private data stays private.
                  </h3>

                  <p>
                    The Privacy Gateway controls
                    what can leave the private
                    environment.
                  </p>

                </div>

                <div className="privacy-status">
                  &#128274; PROTECTED
                </div>

              </div>


              <div className="privacy-audit-grid">

                <div className="privacy-item">

                  <span className="audit-check">1.</span>

                  <div>

                    <span className="audit-icon">SAFE</span>
                    <strong>
                      Raw transactions
                    </strong>

                    <small>
                      Never sent to Tavily
                    </small>

                  </div>

                </div>


                <div className="privacy-item">

                  <span className="audit-check">2.</span>

                  <div>

                    <span className="audit-icon">SAFE</span>
                    <strong>
                      Financial amounts
                    </strong>

                    <small>
                      Blocked from external research
                    </small>

                  </div>

                </div>


                <div className="privacy-item">

                  <span className="audit-check">3.</span>

                  <div>

                    <span className="audit-icon">SAFE</span>
                    <strong>
                      Personal dates
                    </strong>

                    <small>
                      Blocked from external research
                    </small>

                  </div>

                </div>


                <div className="privacy-item">

                  <span className="audit-check">4.</span>

                  <div>s

                    <span className="audit-icon">SAFE</span>
                    <strong>
                      External content
                    </strong>

                    <small>
                      Prompt injection filtered
                    </small>

                  </div>

                </div>

              </div>

            </div>
          )}


          {/* =================================================
              AI ASK PANEL
          ================================================= */}

          <div className="card ask-card">

            <div className="ask-header">

              <div>

                <div className="feature-label">
                  ASK WEALTH CAPSULE
                </div>

                <h3>
                  Your private AI assistant.
                </h3>

                <p>

                  Ask about your spending,
                  budgeting, or current
                  financial information.

                </p>

              </div>


              <div className="ask-status">

                <span />

                NEMOTRON READY

              </div>

            </div>


            {/* INPUT */}

            <div className="ask-input-area">

              <textarea
                value={question}
                onChange={(event) =>
                  setQuestion(
                    event.target.value
                  )
                }
                placeholder="Why did my spending change this month?"
                rows={3}
                disabled={asking}
              />


              <button
                className="primary-button ask-button"
                onClick={askCapsule}
                disabled={
                  !question.trim() ||
                  asking
                }
              >

                {asking
                  ? "ANALYZING..."
                  : "ASK CAPSULE"}

                <span>
                  &#8594;
                </span>

              </button>

            </div>


            {/* LOADING */}

            {asking && (
              <div className="ask-loading">

                <span />
                <span />
                <span />

                <p>

                  Analyzing private data
                  and preparing your answer...

                </p>

              </div>
            )}


            {/* ERROR */}

            {askError && (
              <div className="ask-error">
                {askError}
              </div>
            )}


            {/* RESPONSE */}

            {answer && (
              <div className="ask-response">

                <div className="response-label">
                  CAPSULE RESPONSE
                </div>


                <div className="response-text">
                  {answer}
                </div>


                <div className="response-meta">

                  <span>
                    &#128274; PRIVATE CONTEXT
                  </span>

                  <span>
                    &#129504; NEMOTRON
                  </span>


                  {sources.length > 0 && (
                    <span>
                    &#128269; TAVILY RESEARCH
                    </span>
                  )}

                </div>


                {/* SOURCES */}

                {sources.length > 0 && (
                  <div className="source-list">

                    <div className="response-label">
                      SOURCES
                    </div>


                    {sources.map(
                      (source, index) => (
                        <a
                          key={index}
                          href={source.url}
                          target="_blank"
                          rel="noreferrer"
                          className="source-item"
                        >

                          <strong>
  {source.title || "Research source"}
</strong>
<span>
  {new URL(source.url).hostname.replace(/^www\./, "")}
</span>

                        </a>
                      )
                    )}

                  </div>
                )}

              </div>
            )}

          </div>

        </div>


        {/* =================================================
            FOOTER
        ================================================= */}

        <div className="dashboard-footer">

          <span>
            WEALTH CAPSULE
          </span>

          <span>
            PRIVACY-FIRST PERSONAL AI
          </span>

          <span>
            NEBIUS TOKEN FACTORY
          </span>

        </div>

      </section>

    </div>
  );
}

export default App;
