import { ThemeProvider } from "@emotion/react";
import "./App.css";
import Header from "./components/Header";
import { CircularProgress, createTheme } from "@mui/material";
import Body from "./components/Body";
import { useState } from "react";

function App() {
  const [results, setResults] = useState(undefined);

  /**
   * Get data from backend given search.
   *
   * @link https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
   * @param {string} search
   */
  async function getData(search) {
    setResults(null);
    try {
      const response = await fetch("/data", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify({ search }),
      });
      const text = await response.text();
      try {
        const json = JSON.parse(text);
        setResults(json);
      } catch (e) {
        console.error("Failed to parse JSON:", e);
        console.error("Response text:", text);
        setResults(undefined);
      }
    } catch (e) {
      console.warn(e);
      setResults(undefined);
    }
  }

  return (
    <ThemeProvider theme={createTheme({ palette: { mode: "dark" } })}>
      <div className="App">
        <Header onSearch={getData} />
        {results === null ? <CircularProgress /> : <Body results={results} />}
      </div>
    </ThemeProvider>
  );
}

export default App;
