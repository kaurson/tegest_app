import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

type Exercise = {
  id: string;
  question: string;
  options: string[];
};

type AssessmentResult = {
  score: number;
  total: number;
};

export default function AssessmentQuiz() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [answers, setAnswers] = useState<{ [id: string]: string }>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/api/assessment-exercises")
      .then(res => res.json())
      .then(data => {
        setExercises(data);
        setLoading(false);
      });
  }, []);

  const handleChange = (id: string, value: string) => {
    setAnswers(a => ({ ...a, [id]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const user_id = "test_user"; // Replace with real user/session id
    const payload = {
      user_id,
      answers: exercises.map(q => ({ id: q.id, selected_option: answers[q.id] || "" })),
    };
    const res = await fetch("/api/assessment-submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setResult(data);
  };

  if (loading) return <div className="text-center py-20">Loading assessment...</div>;
  if (result)
    return (
      <div className="max-w-xl mx-auto mt-20 bg-white rounded-2xl shadow p-10 text-center">
        <h2 className="text-3xl font-bold mb-4">Assessment Complete!</h2>
        <p className="text-lg mb-6">Your score: <span className="font-bold">{result.score} / {result.total}</span></p>
        <button className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition" onClick={() => navigate("/lesson-start")}>Continue to Lesson</button>
      </div>
    );

  return (
    <form onSubmit={handleSubmit} className="max-w-xl mx-auto mt-20 bg-white rounded-2xl shadow p-10">
      <h2 className="text-2xl font-bold mb-8 text-center">Quick Assessment</h2>
      {exercises.map((ex, idx) => (
        <div key={ex.id} className="mb-8">
          <div className="font-semibold mb-2">{idx + 1}. {ex.question}</div>
          <div className="flex flex-col gap-2">
            {ex.options.map(opt => (
              <label key={opt} className="flex items-center gap-2">
                <input
                  type="radio"
                  name={`q_${ex.id}`}
                  value={opt}
                  checked={answers[ex.id] === opt}
                  onChange={() => handleChange(ex.id, opt)}
                  required
                />
                {opt}
              </label>
            ))}
          </div>
        </div>
      ))}
      <button type="submit" className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition w-full">Submit</button>
    </form>
  );
} 