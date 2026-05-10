import React from "react";
import {
  Streamlit,
  withStreamlitConnection
} from "streamlit-component-lib";

// ✅ FONCTION (pas class)
function TeaCard(props) {
  console.log("PROPS:", props);

  const tea = props.args?.args?.tea;

  if (!tea) {
    return <div style={{ padding: 10 }}>NO DATA</div>;
  }

  const handleClick = () => {
    if (tea.id) {
      Streamlit.setComponentValue(tea.id);
    }
  };

  return (
    <div
      onClick={handleClick}
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

export default withStreamlitConnection(TeaCard);