import React from "react";
import { StreamlitComponentBase, Streamlit } from "streamlit-component-lib";

class TeaCard extends StreamlitComponentBase {

  componentDidMount() {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(); // 🔥 IMPORTANT
  }

  componentDidUpdate() {
    Streamlit.setFrameHeight(); // 🔥 IMPORTANT
  }

  handleClick = () => {
    const tea = this.props.args?.tea;
    if (tea && tea.id) {
      Streamlit.setComponentValue(tea.id);
    }
  };

  render() {
    const tea = this.props.args?.tea;

    // 🔍 DEBUG VISUEL
    if (!tea) {
      return <div style={{ padding: 10 }}>NO DATA</div>;
    }

    return (
      <div
        onClick={this.handleClick}
        style={{
          padding: "14px",
          borderRadius: "16px",
          background: "#eee",
          boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
          cursor: "pointer",
          marginBottom: "10px"
        }}
      >
        🍵 {tea.name}
      </div>
    );
  }
}

export default TeaCard;