import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [page, setPage] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [msg, setMsg] = useState("");

  const api = axios.create({ baseURL: "http://localhost:8000" });

  const handleLogin = async () => {
    try {
      await api.post("/login", { username, password });
      setPage("search");
    } catch (err) {
      setMsg("Login failed");
    }
  };

  const handleSearch = async () => {
    try {
      const res = await api.post("/search", { keyword });
      setResults(res.data.results);
      setMsg(res.data.cached ? "Cached result" : "Fresh result");
    } catch (err) {
      setMsg("Search failed");
    }
  };

  if (page === "login") {
    return (
      <div className="App">
        <h2>Login</h2>
        <input placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
        <input placeholder="Password" type="password" onChange={(e) => setPassword(e.target.value)} />
        <button onClick={handleLogin}>Login</button>
        <p>{msg}</p>
      </div>
    );
  }

  return (
    <div className="App">
      <h2>Search Leaked Data</h2>
      <input placeholder="Enter keyword" onChange={(e) => setKeyword(e.target.value)} />
      <button onClick={handleSearch}>Search</button>
      <p>{msg}</p>
      <table>
        <thead>
          <tr>
            <th>Email</th>
            <th>Domain</th>
            <th>Source</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r, i) => (
            <tr key={i}>
              <td>{r.emails?.[0]}</td>
              <td>{r.domain}</td>
              <td>{r.source}</td>
              <td>{r.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
