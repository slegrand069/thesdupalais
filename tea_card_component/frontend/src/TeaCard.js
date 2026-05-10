import React from "react";
import { StreamlitComponentBase, Streamlit } from "streamlit-component-lib";

class TeaCard extends StreamlitComponentBase {

  componentDidMount() {
    Streamlit.setComponentReady();
        Streamlit.setFrameHeight();
  }

  handleClick = () => {
    const tea = this.props.args?.tea;

    if (tea && tea.id) {
      Streamlit.setComponentValue(tea.id);
    }
  };

  render() {
    const tea = this.props.args?.tea ;
     if (!tea) {
        return <div>Loading...</div>;
    }
    return (
    <div
      onClick={this.handleClick}
      style={{
        padding: "14px",
        borderRadius: "16px",
        background: /*tea.bg ||*/ "#eee",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        cursor: "pointer",
        marginBottom: "10px"
      }}
    >
      {/* 🧾 Nom */}
      <div style={{ fontWeight: "bold" }}>
        🍵 {tea.name || "Sans nom"}
      </div>
    </div>
    );
    }
}

export default TeaCard;