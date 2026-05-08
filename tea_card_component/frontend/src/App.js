import React from "react";
import TeaCard from "./TeaCard";

function App() {
  return <TeaCard />;
}

export default App;

/*import React from "react";
import {
  withStreamlitConnection,
  Streamlit
} from "streamlit-component-lib";

function TeaCard({ args }) {

  const tea = args?.tea || {
    id: 1,
    name: "Thé test",
    color: "Vert",
    origin: "Chine",
    rating: 7,
    temp: 80,
    duration: 3,
    moment: "Matin",
    badges: ["Test"],
    bg: "#E8F5E9"
  };

  const handleClick = () => {
    Streamlit.setComponentValue(tea.id);
  };
  return <h1>HELLO CARD</h1>;
  /*return (
    <div
      onClick={handleClick}
      style={{
        padding: "14px",
        borderRadius: "16px",
        background: tea.bg,
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        cursor: "pointer",
        marginBottom: "10px"
      }}
    >
      <div style={{ fontWeight: "bold" }}>
        🍵 {tea.name}
      </div>

      <div style={{ fontSize: "12px", color: "#555" }}>
        {tea.color} • {tea.origin}
      </div>

      <div style={{ marginTop: "6px" }}>
        {(tea.badges || []).map((b, i) => (
          <span
            key={i}
            style={{
              background: "#eee",
              padding: "3px 8px",
              borderRadius: "8px",
              fontSize: "11px",
              marginRight: "4px"
            }}
          >
            🏅 {b}
          </span>
        ))}
      </div>

      <div style={{ marginTop: "6px", fontSize: "12px" }}>
        ⭐ {tea.rating} • 🌡 {tea.temp}°C • ⏳ {tea.duration} min • 🌇 {tea.moment}
      </div>
    </div>
  );
*/
/*}

export default withStreamlitConnection(TeaCard);
*/