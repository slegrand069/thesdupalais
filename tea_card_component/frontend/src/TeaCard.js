import React from "react";
import { StreamlitComponentBase, Streamlit } from "streamlit-component-lib";

class TeaCard extends StreamlitComponentBase {

  componentDidMount() {
    Streamlit.setComponentReady();
  }

  handleClick = () => {
    const tea = this.props.args?.tea;
    if (tea?.id) {
      Streamlit.setComponentValue(tea.id);
    }
  };

  render() {
    const tea = this.props.args?.tea;
    if (!tea) {
      return <div>Loading...</div>;
    }

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
  }
}

export default TeaCard;