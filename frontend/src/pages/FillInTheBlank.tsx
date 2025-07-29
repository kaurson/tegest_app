import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Card, CardContent, CardHeader } from "../components/ui/card";

type ExerciseResponse = {
  exercise_text: string;
  blanks: string[];
  correct_answers: string[];
  error?: string;
};

type CheckResponse = {
  score: number;
  total: number;
  feedback: string[];
};

export default function FillInTheBlank() {
  const [inputText, setInputText] = useState("");
  const [exercise, setExercise] = useState<ExerciseResponse | null>(null);
  const [userAnswers, setUserAnswers] = useState<string[]>([]);
  const [checkResult, setCheckResult] = useState<CheckResponse | null>(null);

  const generateExercise = async () => {
    setCheckResult(null);
    setExercise(null);
    setUserAnswers([]);
    const res = await fetch("/api/fill-in-blank/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: inputText }),
    });
    const data = await res.json();
    setExercise(data);
    setUserAnswers(Array(data.blanks?.length || 0).fill(""));
  };

  const checkAnswers = async () => {
    const res = await fetch("/api/fill-in-blank/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_answers: userAnswers,
        correct_answers: exercise?.correct_answers,
      }),
    });
    const data = await res.json();
    setCheckResult(data);
  };

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
      <div className="max-w-xl mx-auto mt-8">
        <Card>
          <CardHeader>
            <h2 className="text-2xl font-bold">Lünkade täitmise harjutus</h2>
          </CardHeader>
          <CardContent>
            {!exercise && (
              <>
                <Textarea
                  value={inputText}
                  onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setInputText(e.target.value)}
                  placeholder="Kleebi siia oma eestikeelne tekst (10 lauset)..."
                  className="mb-4"
                />
                <Button onClick={generateExercise}>Loo harjutus</Button>
              </>
            )}
            {exercise && !checkResult && (
              <form
                onSubmit={(e: React.FormEvent) => {
                  e.preventDefault();
                  checkAnswers();
                }}
              >
                <div className="mb-4 whitespace-pre-line">
                  {(() => {
                    const parts = exercise.exercise_text.split(/(__)/);
                    let blankIdx = 0;
                    return parts.map((part, idx) => {
                      if (part === "__") {
                        const input = (
                          <Input
                            key={idx}
                            className="inline-block w-24 mx-1"
                            value={userAnswers[blankIdx] || ""}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                              const newAnswers = [...userAnswers];
                              newAnswers[blankIdx] = e.target.value;
                              setUserAnswers(newAnswers);
                            }}
                          />
                        );
                        blankIdx++;
                        return input;
                      } else {
                        return <span key={idx}>{part}</span>;
                      }
                    });
                  })()}
                </div>
                <Button type="submit">Lõpeta</Button>
              </form>
            )}
            {checkResult && (
              <div>
                <div className="mb-2 font-semibold">
                  Tulemus: {checkResult.score} / {checkResult.total}
                </div>
                <ul>
                  {checkResult.feedback.map((f, i) => (
                    <li key={i}>{f}</li>
                  ))}
                </ul>
                <Button className="mt-4" onClick={() => { setExercise(null); setCheckResult(null); setInputText(""); }}>
                  Uus harjutus
                </Button>
              </div>
            )}
            {exercise?.error && <div className="text-red-500">{exercise.error}</div>}
          </CardContent>
        </Card>
      </div>
    </div>
  );
} 