import React from "react";
import { Link } from "react-router-dom";

export default function LessonStart() {
  return (
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

      <section className="min-h-[60vh] flex items-center justify-center">
        <div className="max-w-xl w-full bg-white rounded-2xl shadow-lg p-10 flex flex-col items-center text-center border border-gray-100">
          <h1 className="text-4xl font-extrabold text-gray-900 mb-4">Valmis alustama tundi?</h1>
          <p className="text-lg text-gray-600 mb-8">
            See tund viib sind läbi interaktiivsete eesti keele harjutuste. Harjuta sõnavara, grammatikat ja igapäevaseid lauseid. Edu!
          </p>
          <Link to="/fill-in-the-blank">
            <button className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition flex items-center gap-2">
              Alusta lünkade täitmist
              <span className="inline-block bg-black rounded-full w-6 h-6 flex items-center justify-center text-white">→</span>
            </button>
          </Link>
        </div>
      </section>
    </div>
  );
} 