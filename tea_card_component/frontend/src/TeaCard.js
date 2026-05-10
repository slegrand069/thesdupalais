import React from "react";
import {
  Streamlit,
  withStreamlitConnection
} from "streamlit-component-lib";

// ✅ FONCTION (pas class)
function TeaCard(props) {
  console.log("PROPS:", props);

  const tea = props.args?.args?.tea || props.args?.tea;

  if (!tea) {
    return <div style={{ padding: 10 }}>NO DATA</div>;
  }

  const handleClick = () => {
    if (tea.id) {
      Streamlit.setComponentValue(tea.id);
/*      e.currentTarget.style.transform = "scale(0.98)";
        setTimeout(() => {
        e.currentTarget.style.transform = "none";
        }, 100);
*/
    }
  };

return (
  <div
    onClick={handleClick/*,  
        e.currentTarget.style.transform = "scale(0.98)",
        setTimeout(() => {
        e.currentTarget.style.transform = "none";
        }, 100)*/}
    style={{
      padding: "14px",
      borderRadius: "16px",
      background: tea.bg || "#f5f5f5",
      boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
      cursor: "pointer",
      marginBottom: "12px",
      transition: "all 0.15s ease",
      border: "1px solid rgba(0,0,0,0.05)"
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.transform = "translateY(-2px)";
      e.currentTarget.style.boxShadow = "0 6px 16px rgba(0,0,0,0.12)";
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.transform = "none";
      e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.08)";
    }}
  >

    {/* 🧾 NOM */}
    <div style={{ fontWeight: "600", fontSize: "15px" }}>
      🍵 {tea.name}
    </div>

    {/* 🌍 INFOS */}
    <div style={{ fontSize: "12px", color: "#555", marginTop: "2px" }}>
      {tea.color || "-"} • {tea.origin || "-"}
    </div>

    {/* 🏅 BADGES */}
    {tea.badges && tea.badges.length > 0 && (
      <div style={{ marginTop: "6px" }}>
        {tea.badges.map((b, i) => (
          <span
            key={i}
            style={{
              background: "#ffffffcc",
              padding: "3px 8px",
              borderRadius: "8px",
              fontSize: "11px",
              marginRight: "4px",
              border: "1px solid rgba(0,0,0,0.05)"
            }}
          >
            {b}
          </span>
        ))}
      </div>
    )}

    {/* 📊 STATS */}
    <div style={{
      marginTop: "8px",
      fontSize: "12px",
      display: "flex",
      gap: "8px",
      flexWrap: "wrap"
    }}>
      <span>⭐ {tea.rating ?? "-"}</span>
      <span>🌡 {tea.temp ?? "-"}°C</span>
      <span>⏳ {tea.duration ?? "-"} min</span>
      <span>🌇 {tea.moment ?? "-"}</span>
    </div>

  </div>
);
}

export default withStreamlitConnection(TeaCard);

