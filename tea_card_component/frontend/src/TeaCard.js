import React from "react";
import { StreamlitComponentBase, Streamlit } from "streamlit-component-lib";

class TeaCard extends StreamlitComponentBase {

  componentDidMount() {
    Streamlit.setComponentReady();
  }

  handleClick = () => {
    const tea = this.props.args?.tea;

    if (tea && tea.id) {
      Streamlit.setComponentValue(tea.id);
    }
  };

  render() {
  return (
    <div style={{ padding: 20 }}>
      DEBUG: {JSON.stringify(this.props.args)}
    </div>
  );
}

oldrender() {
  const args = this.props.args || {};
  const tea = args.tea || null;

  // ⛑️ Sécurité : pas encore de données
  if (!tea) {
    return (
      <div style={{ padding: "10px", fontSize: "12px", color: "#888" }}>
        Loading...
      </div>
    );
  }

  // ⛑️ Sécurité badges
  const badges = Array.isArray(tea.badges) ? tea.badges : [];

  return (
    <div
      onClick={this.handleClick}
      style={{
        padding: "14px",
        borderRadius: "16px",
        background: tea.bg || "#eee",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        cursor: "pointer",
        marginBottom: "10px"
      }}
    >
      {/* 🧾 Nom */}
      <div style={{ fontWeight: "bold" }}>
        🍵 {tea.name || "Sans nom"}
      </div>

      {/* 🌍 Origine */}
      <div style={{ fontSize: "12px", color: "#555" }}>
        {(tea.color || "-")} • {(tea.origin || "-")}
      </div>

      {/* 🏅 Badges */}
      {badges.length > 0 && (
        <div style={{ marginTop: "6px" }}>
          {badges.map((b, i) => (
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
      )}

      {/* 📊 Infos */}
      <div style={{ marginTop: "6px", fontSize: "12px" }}>
        ⭐ {tea.rating ?? 0} •
        🌡 {tea.temp ?? 0}°C •
        ⏳ {tea.duration ?? 0} min •
        🌇 {tea.moment || "-"}
      </div>
    </div>
  );
  } 
}

export default TeaCard;