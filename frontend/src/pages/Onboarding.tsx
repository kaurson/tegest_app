import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Onboarding() {
  const [level, setLevel] = useState("");
  const [goal, setGoal] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!level || !goal.trim()) {
      setError("Palun vali oma tase ja kirjelda oma eesmärki.");
      return;
    }
    // Here you could save the answers to context, backend, etc.
    navigate("/assessment-quiz");
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
          <div className="flex items-center gap-4">
            <Link 
              to="/register" 
              className="bg-lime-400 hover:bg-lime-500 text-black px-4 py-2 rounded-full font-semibold transition"
            >
              Registreeru
            </Link>
            <Link 
              to="/dashboard" 
              className="bg-gray-100 text-gray-700 px-4 py-2 rounded-full font-semibold hover:bg-gray-200 transition"
            >
              ← Tagasi armatuurlauale
            </Link>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <section className="min-h-[60vh] flex items-center justify-center">
        <form onSubmit={handleSubmit} className="max-w-xl w-full bg-white rounded-2xl shadow-lg p-10 flex flex-col items-center text-center border border-gray-100">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-6">Tutvume sinuga</h1>
          <p className="text-lg text-gray-600 mb-8">Räägi meile oma eesti keele oskustest ja õppe-eesmärkidest.</p>
          
          {/* Add registration prompt for new users */}
          <div className="w-full mb-6 p-4 bg-lime-50 border border-lime-200 rounded-lg">
            <p className="text-sm text-gray-700 mb-2">
              Uus kasutaja? <Link to="/register" className="text-lime-600 hover:text-lime-700 font-semibold underline">Loo konto</Link> enne jätkamist.
            </p>
          </div>
          
          <div className="mb-6 w-full text-left">
            <label className="block font-semibold mb-2">Sinu eesti keele tase:</label>
            <div className="flex flex-col gap-2">
              <label className="flex items-center gap-2">
                <input type="radio" name="level" value="algaja" checked={level === "algaja"} onChange={() => setLevel("algaja")}/>
                Algaja
              </label>
              <label className="flex items-center gap-2">
                <input type="radio" name="level" value="keskmine" checked={level === "keskmine"} onChange={() => setLevel("keskmine")}/>
                Keskmine
              </label>
              <label className="flex items-center gap-2">
                <input type="radio" name="level" value="kõrgem" checked={level === "kõrgem"} onChange={() => setLevel("kõrgem")}/>
                Kõrgem
              </label>
            </div>
          </div>
          <div className="mb-6 w-full text-left">
            <label className="block font-semibold mb-2">Mis on sinu peamine eesmärk eesti keele õppimisel?</label>
            <textarea
              className="w-full rounded border border-gray-300 p-2 min-h-[60px] focus:outline-none focus:ring-2 focus:ring-lime-400"
              value={goal}
              onChange={e => setGoal(e.target.value)}
              placeholder="Nt. reisimine, töö, igapäevane vestlus jne."
            />
          </div>
          {error && <div className="text-red-500 mb-4">{error}</div>}
          <button type="submit" className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition flex items-center gap-2">
            Jätka
            <span className="inline-block bg-black rounded-full w-6 h-6 flex items-center justify-center text-white">→</span>
          </button>
        </form>
      </section>
    </div>
  );
} 