import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Onboarding() {
  const [level, setLevel] = useState("");
  const [goal, setGoal] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!level || !goal.trim()) {
      setError("Please select your level and describe your goal.");
      return;
    }
    // Here you could save the answers to context, backend, etc.
    navigate("/assessment-quiz");
  };

  return (
    <section className="min-h-[60vh] flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="max-w-xl w-full bg-white rounded-2xl shadow-lg p-10 flex flex-col items-center text-center border border-gray-100">
        <h1 className="text-3xl font-extrabold text-gray-900 mb-6">Let's Get to Know You</h1>
        <p className="text-lg text-gray-600 mb-8">Tell us about your Estonian skills and learning goals.</p>
        <div className="mb-6 w-full text-left">
          <label className="block font-semibold mb-2">Your Estonian Level:</label>
          <div className="flex flex-col gap-2">
            <label className="flex items-center gap-2">
              <input type="radio" name="level" value="beginner" checked={level === "beginner"} onChange={() => setLevel("beginner")}/>
              Beginner
            </label>
            <label className="flex items-center gap-2">
              <input type="radio" name="level" value="intermediate" checked={level === "intermediate"} onChange={() => setLevel("intermediate")}/>
              Intermediate
            </label>
            <label className="flex items-center gap-2">
              <input type="radio" name="level" value="advanced" checked={level === "advanced"} onChange={() => setLevel("advanced")}/>
              Advanced
            </label>
          </div>
        </div>
        <div className="mb-6 w-full text-left">
          <label className="block font-semibold mb-2">What is your main goal for learning Estonian?</label>
          <textarea
            className="w-full rounded border border-gray-300 p-2 min-h-[60px] focus:outline-none focus:ring-2 focus:ring-lime-400"
            value={goal}
            onChange={e => setGoal(e.target.value)}
            placeholder="E.g., travel, work, daily conversation, etc."
          />
        </div>
        {error && <div className="text-red-500 mb-4">{error}</div>}
        <button type="submit" className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition flex items-center gap-2">
          Continue
          <span className="inline-block bg-black rounded-full w-6 h-6 flex items-center justify-center text-white">→</span>
        </button>
      </form>
    </section>
  );
} 