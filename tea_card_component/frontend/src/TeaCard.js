import React from "react";
import {
  Streamlit,
  withStreamlitConnection
} from "streamlit-component-lib";

// ✅ FONCTION (pas class)
function TeaCard(props) {
  console.log("PROPS:", props);

  const tea = props.args?.tea || props.tea;

  if (!tea) {
    return <div style={{ padding: 10 }}>NO DATA</div>;
  }

  const handleClick = () => {
    if (tea.id) {
      Streamlit.setComponentValue(tea.id);
    }
  };

  return (
    <div onClick={handleClick} style={{ padding: 10 }}>
      🍵 {tea.name}
    </div>
  );
}

// 🔥 CRUCIAL
export default withStreamlitConnection(TeaCard);