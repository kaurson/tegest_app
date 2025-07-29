import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

type GapFillExerciseType = {
  id: number;
  prompt: string;
  blanks: string[];
  answers: string[];
  type: string;
};

type CheckResult = {
  score: number;
  total: number;
  feedback: string[];
};

export default function GapFillExercise() {
  const [exercise, setExercise] = useState<GapFillExerciseType | null>(null);
  const [userAnswers, setUserAnswers] = useState<string[]>([]);
  const [result, setResult] = useState<CheckResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/gap-fill-exercise")
      .then(res => res.json())
      .then(data => {
        setExercise(data);
        setUserAnswers(Array(data.answers.length).fill(""));
        setLoading(false);
      });
  }, []);

  const handleChange = (idx: number, value: string) => {
    setUserAnswers(a => {
      const copy = [...a];
      copy[idx] = value;
      return copy;
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!exercise) return;
    const payload = {
      exercise_id: exercise.id,
      user_answers: userAnswers,
    };
    const res = await fetch("/api/gap-fill-check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setResult(data);
  };

  if (loading) return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <nav className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
          <Link to="/dashboard" className="flex items-center gap-2 font-bold text-xl text-gray-900 hover:text-lime-600 transition">
            <span className="inline-block w-6 h-6 bg-black rounded mr-2"></span>
            Eesti ÕppeApp
          </Link>
          <Link 
            to="/dashboard" 
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-full font-semibold hover:bg-gray-200 transition"
          >
            ← Tagasi armatuurlauale
          </Link>
        </nav>
      </header>
      <div className="text-center py-20">Laen harjutust...</div>
    </div>
  );
  
  if (!exercise) return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <nav className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
          <Link to="/dashboard" className="flex items-center gap-2 font-bold text-xl text-gray-900 hover:text-lime-600 transition">
            <span className="inline-block w-6 h-6 bg-black rounded mr-2"></span>
            Eesti ÕppeApp
          </Link>
          <Link 
            to="/dashboard" 
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-full font-semibold hover:bg-gray-200 transition"
          >
            ← Tagasi armatuurlauale
          </Link>
        </nav>
      </header>
      <div className="text-center py-20">Harjutust ei leitud.</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <header className="bg-white border-b">
        <nav className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
          <Link to="/dashboard" className="flex items-center gap-2 font-bold text-xl text-gray-900 hover:text-lime-600 transition">
            <span className="inline-block w-6 h-6 bg-black rounded mr-2"></span>
            Eesti ÕppeApp
          </Link>
          <Link 
            to="/dashboard" 
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-full font-semibold hover:bg-gray-200 transition"
          >
            ← Tagasi armatuurlauale
          </Link>
        </nav>
      </header>

      {/* Main Content */}
      <div className="max-w-2xl mx-auto mt-8 bg-white rounded-2xl shadow p-10">
        <form onSubmit={handleSubmit}>
          <h2 className="text-2xl font-bold mb-8 text-center">Lünkade täitmise harjutus</h2>
          <div className="mb-8 whitespace-pre-line text-left text-lg">
            {exercise.prompt.split(/_{3,}/g).map((part, idx, arr) => (
              <span key={idx}>
                {part}
                {idx < exercise.answers.length && (
                  <input
                    type="text"
                    className="border-b-2 border-gray-400 mx-2 w-32 focus:outline-none focus:border-lime-400"
                    value={userAnswers[idx] || ""}
                    onChange={e => handleChange(idx, e.target.value)}
                    disabled={!!result}
                    required
                  />
                )}
              </span>
            ))}
          </div>
          {result && (
            <div className="mb-6">
              <div className="font-semibold mb-2">Tulemus: {result.score} / {result.total}</div>
              <ul className="text-left">
                {result.feedback.map((f, i) => (
                  <li key={i}>{f}</li>
                ))}
              </ul>
            </div>
          )}
          {!result && (
            <button type="submit" className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition w-full">Kontrolli</button>
          )}
        </form>
      </div>
    </div>
  );
} 