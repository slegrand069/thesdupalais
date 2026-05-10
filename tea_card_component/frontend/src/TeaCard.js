import React from "react";
import {
  Streamlit,
  withStreamlitConnection
} from "streamlit-component-lib";

// ✅ FONCTION (pas class)
function TeaCard(props) {
  const tea = props.args?.tea;

  console.log("ARGS:", props.args);

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

// 🔥 CRUCIAL
export default withStreamlitConnection(TeaCard);