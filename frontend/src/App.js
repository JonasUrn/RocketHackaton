import React, { useEffect, useState } from "react";
import axios from "axios";

import Body from "./Components/Body";

function App() {
  const [data, setData] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/data")
      .then(response => setData(response.data.message))
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return <Body />;
}

export default App;
