import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import FillInTheBlank from './pages/FillInTheBlank';
import LessonStart from './pages/LessonStart';
import Onboarding from './pages/Onboarding';
import AssessmentQuiz from './pages/AssessmentQuiz';
import GapFillExercise from './pages/GapFillExercise';

function Navbar() {
  return (
    <header className="w-full bg-white border-b sticky top-0 z-10">
      <nav className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2 font-bold text-xl text-gray-900">
          <span className="inline-block w-6 h-6 bg-black rounded mr-2"></span>
          Eesti ÕppeApp
        </div>
        <ul className="flex gap-8 text-gray-700 font-medium">
          <li><a href="#features" className="hover:text-purple-600 transition">Features</a></li>
          <li><a href="#lessons" className="hover:text-purple-600 transition">Lessons</a></li>
          <li><a href="#about" className="hover:text-purple-600 transition">About</a></li>
        </ul>
        <div>
          <button className="bg-black text-white px-5 py-2 rounded-full font-semibold hover:bg-gray-900 transition">Sign In</button>
        </div>
      </nav>
    </header>
  );
}

function Hero() {
  return (
    <section className="bg-gray-50 py-20 border-b">
      <div className="max-w-5xl mx-auto px-6 flex flex-col items-center text-center">
        <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6 leading-tight">
          Learn Estonian<br />
          For a Modern World
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl">
          Interactive, AI-powered language lessons. Practice with real Estonian texts, track your progress, and have fun while learning!
        </p>
        <Link to="#lessons">
          <button className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition flex items-center gap-2">
            Start Learning
            <span className="inline-block bg-black rounded-full w-6 h-6 flex items-center justify-center text-white">→</span>
          </button>
        </Link>
      </div>
    </section>
  );
}

function Features() {
  return (
    <section id="features" className="bg-white py-16">
      <div className="max-w-6xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-10 text-center">Why Choose Eesti ÕppeApp?</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="rounded-2xl bg-gray-50 p-8 shadow hover:shadow-lg transition flex flex-col items-center">
            <span className="w-12 h-12 bg-purple-200 text-purple-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">💡</span>
            <h3 className="font-semibold text-lg mb-2">Interactive Exercises</h3>
            <p className="text-gray-600">Practice with fill-in-the-blank, multiple choice, and more.</p>
          </div>
          <div className="rounded-2xl bg-gray-50 p-8 shadow hover:shadow-lg transition flex flex-col items-center">
            <span className="w-12 h-12 bg-lime-200 text-lime-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">⚡</span>
            <h3 className="font-semibold text-lg mb-2">Fast Progress</h3>
            <p className="text-gray-600">Track your learning and see your improvement every day.</p>
          </div>
          <div className="rounded-2xl bg-gray-50 p-8 shadow hover:shadow-lg transition flex flex-col items-center">
            <span className="w-12 h-12 bg-black text-white flex items-center justify-center rounded-full mb-4 text-2xl font-bold">🗣️</span>
            <h3 className="font-semibold text-lg mb-2">Real Language</h3>
            <p className="text-gray-600">Learn with real Estonian texts and conversations.</p>
          </div>
          <div className="rounded-2xl bg-gray-50 p-8 shadow hover:shadow-lg transition flex flex-col items-center">
            <span className="w-12 h-12 bg-yellow-200 text-yellow-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">🎯</span>
            <h3 className="font-semibold text-lg mb-2">Personalized</h3>
            <p className="text-gray-600">AI adapts lessons to your level and goals.</p>
          </div>
        </div>
      </div>
    </section>
  );
}

function LessonTypes() {
  return (
    <section id="lessons" className="bg-gray-100 py-16 border-t">
      <div className="max-w-6xl mx-auto px-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-10 text-center">Lesson Types</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Link to="/onboarding" className="rounded-2xl bg-white p-8 shadow hover:shadow-xl transition flex flex-col items-center border-2 border-transparent hover:border-lime-400">
            <span className="w-12 h-12 bg-lime-100 text-lime-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">✍️</span>
            <h3 className="font-semibold text-lg mb-2">Fill in the Blank</h3>
            <p className="text-gray-600 text-center">Test your vocabulary and grammar by filling in missing words.</p>
          </Link>
          <Link to="/gap-fill-exercise" className="rounded-2xl bg-white p-8 shadow hover:shadow-xl transition flex flex-col items-center border-2 border-transparent hover:border-purple-400">
            <span className="w-12 h-12 bg-purple-100 text-purple-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">📝</span>
            <h3 className="font-semibold text-lg mb-2">Lünkade täitmine</h3>
            <p className="text-gray-600 text-center">Täida lüngad või tuleta õige sõna.</p>
          </Link>
          <div className="rounded-2xl bg-white p-8 shadow flex flex-col items-center opacity-50 cursor-not-allowed">
            <span className="w-12 h-12 bg-yellow-100 text-yellow-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">❓</span>
            <h3 className="font-semibold text-lg mb-2">Multiple Choice (Coming Soon)</h3>
            <p className="text-gray-600 text-center">Choose the correct answer and learn from your mistakes.</p>
          </div>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="bg-black text-white py-10 mt-20">
      <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="flex items-center gap-2 font-bold text-lg">
          <span className="inline-block w-6 h-6 bg-white rounded mr-2"></span>
          Eesti ÕppeApp
        </div>
        <div className="text-gray-400 text-sm">&copy; {new Date().getFullYear()} Eesti ÕppeApp. All rights reserved.</div>
        <div className="flex gap-4">
          <a href="#" className="hover:text-lime-400 transition">Twitter</a>
          <a href="#" className="hover:text-lime-400 transition">GitHub</a>
        </div>
      </div>
    </footer>
  );
}

function MainLanding() {
  return (
    <>
      <Navbar />
      <Hero />
      <Features />
      <LessonTypes />
      <Footer />
    </>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainLanding />} />
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/assessment-quiz" element={<AssessmentQuiz />} />
        <Route path="/lesson-start" element={<LessonStart />} />
        <Route path="/fill-in-the-blank" element={<FillInTheBlank />} />
        <Route path="/gap-fill-exercise" element={<GapFillExercise />} />
      </Routes>
    </Router>
  );
}
