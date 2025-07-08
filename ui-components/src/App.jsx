import React, { useEffect, useState } from "react";

function App() {
  const [actions, setActions] = useState([]);

  const fetchActions = async () => {
    try {
      const res = await fetch("https://flask-webhook-765w.onrender.com/actions");
      const data = await res.json();
      setActions(data);
    } catch (error) {
      console.error("Error fetching actions:", error);
    }
  };

  useEffect(() => {
    fetchActions();
    const interval = setInterval(fetchActions, 15000);
    return () => clearInterval(interval);
  }, []);

  const renderText = (action) => {
    if (action.action === "PUSH")
      return `${action.author} pushed to ${action.to_branch} on ${action.timestamp}`;
    if (action.action === "PULL_REQUEST")
      return `${action.author} submitted a pull request from ${action.from_branch} to ${action.to_branch} on ${action.timestamp}`;
    if (action.action === "MERGE")
      return `${action.author} merged branch ${action.from_branch} to ${action.to_branch} on ${action.timestamp}`;
    return "";
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-md w-[90%] md:w-[600px]">
        <h2 className="text-2xl font-bold mb-4 text-center">GitHub Webhook Feed</h2>
        <ul className="space-y-2">
          {actions.map((a, i) => (
            <li key={i} className="text-gray-700">{renderText(a)}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
