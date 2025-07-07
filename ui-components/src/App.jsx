import React, { useEffect, useState } from "react";

const App = () => {
  const [actions, setActions] = useState([]);

  const fetchData = async () => {
    try {
      const res = await fetch("http://localhost:5000/actions");
      const data = await res.json();
      setActions(data);
    } catch (error) {
      console.error("Failed to fetch:", error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, []);

  const renderMessage = (action) => {
    const { author, from_branch, to_branch, timestamp, action: type } = action;

    if (type === "PUSH") return `${author} pushed to ${to_branch} on ${timestamp}`;
    if (type === "PULL_REQUEST")
      return `${author} submitted a pull request from ${from_branch} to ${to_branch} on ${timestamp}`;
    if (type === "MERGE")
      return `${author} merged branch ${from_branch} to ${to_branch} on ${timestamp}`;
    return "";
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>GitHub Webhook Feed</h2>
      <ul>
        {actions.map((action, idx) => (
          <li key={idx}>{renderMessage(action)}</li>
        ))}
      </ul>
    </div>
  );
};

export default App;
