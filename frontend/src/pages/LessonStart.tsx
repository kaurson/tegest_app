import React from "react";
import { Link } from "react-router-dom";

export default function LessonStart() {
  return (
    <section className="min-h-[60vh] flex items-center justify-center bg-gray-50">
      <div className="max-w-xl w-full bg-white rounded-2xl shadow-lg p-10 flex flex-col items-center text-center border border-gray-100">
        <h1 className="text-4xl font-extrabold text-gray-900 mb-4">Ready to Start Your Lesson?</h1>
        <p className="text-lg text-gray-600 mb-8">
          This lesson will guide you through interactive Estonian exercises. Practice vocabulary, grammar, and real-life sentences. Good luck!
        </p>
        <Link to="/fill-in-the-blank">
          <button className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition flex items-center gap-2">
            Start Fill in the Blank
            <span className="inline-block bg-black rounded-full w-6 h-6 flex items-center justify-center text-white">→</span>
          </button>
        </Link>
      </div>
    </section>
  );
} 