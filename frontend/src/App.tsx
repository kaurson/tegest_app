import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import FillInTheBlank from './pages/FillInTheBlank';
import LessonStart from './pages/LessonStart';
import Onboarding from './pages/Onboarding';
import AssessmentQuiz from './pages/AssessmentQuiz';
import GapFillExercise from './pages/GapFillExercise';
import UserDashboard from './pages/UserDashboard';
import UserRegister from './pages/UserRegister';

function Navbar() {
  return (
    <header className="w-full bg-white border-b sticky top-0 z-10">
      <nav className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
        <div className="flex items-center gap-2 font-bold text-xl text-gray-900">
          <span className="inline-block w-6 h-6 bg-black rounded mr-2"></span>
          Eesti ÕppeApp
        </div>
        <ul className="flex gap-8 text-gray-700 font-medium">
          <li><a href="#features" className="hover:text-purple-600 transition">Funktsioonid</a></li>
          <li><a href="#lessons" className="hover:text-purple-600 transition">Tunnid</a></li>
          <li><a href="#about" className="hover:text-purple-600 transition">Meist</a></li>
        </ul>
        <div className="flex items-center gap-3">
          <Link 
            to="/register" 
            className="bg-lime-400 hover:bg-lime-500 text-black px-5 py-2 rounded-full font-semibold transition"
          >
            Registreeru
          </Link>
          <button className="bg-black text-white px-5 py-2 rounded-full font-semibold hover:bg-gray-900 transition">
            Logi sisse
          </button>
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
          Õpi eesti keelt<br />
          kaasaegseks maailmaks
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl">
          Interaktiivsed, tehisintellektiga juhitud keeletunnid. Harjuta tõeliste eestikeelsete tekstidega, jälgi oma arengut ja naudi õppimist!
        </p>
        <Link to="/dashboard">
          <button className="bg-lime-400 hover:bg-lime-500 text-black font-bold px-8 py-3 rounded-full text-lg shadow transition flex items-center gap-2">
            Alusta õppimist
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
        <h2 className="text-3xl font-bold text-gray-900 mb-10 text-center">Miks valida Eesti ÕppeApp?</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="rounded-2xl bg-gray-50 p-8 shadow hover:shadow-lg transition flex flex-col items-center">
            <span className="w-12 h-12 bg-purple-200 text-purple-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">💡</span>
            <h3 className="font-semibold text-lg mb-2">Interaktiivsed harjutused</h3>
            <p className="text-gray-600">Harjuta lünkade täitmise, valikvastuste ja muudega.</p>
          </div>
          <div className="rounded-2xl bg-gray-50 p-8 shadow hover:shadow-lg transition flex flex-col items-center">
            <span className="w-12 h-12 bg-lime-200 text-lime-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">⚡</span>
            <h3 className="font-semibold text-lg mb-2">Kiire areng</h3>
            <p className="text-gray-600">Jälgi oma õppimist ja näe igapäevast arengut.</p>
          </div>
          <div className="rounded-2xl bg-gray-50 p-8 shadow hover:shadow-lg transition flex flex-col items-center">
            <span className="w-12 h-12 bg-black text-white flex items-center justify-center rounded-full mb-4 text-2xl font-bold">🗣️</span>
            <h3 className="font-semibold text-lg mb-2">Tõeline keel</h3>
            <p className="text-gray-600">Õpi tõeliste eestikeelsete tekstide ja vestlustega.</p>
          </div>
          <div className="rounded-2xl bg-gray-50 p-8 shadow hover:shadow-lg transition flex flex-col items-center">
            <span className="w-12 h-12 bg-yellow-200 text-yellow-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">🎯</span>
            <h3 className="font-semibold text-lg mb-2">Isikupärastatud</h3>
            <p className="text-gray-600">AI kohandab tunnid sinu tasemele ja eesmärkidele.</p>
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
        <h2 className="text-3xl font-bold text-gray-900 mb-10 text-center">Tunni tüübid</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Link to="/onboarding" className="rounded-2xl bg-white p-8 shadow hover:shadow-xl transition flex flex-col items-center border-2 border-transparent hover:border-lime-400">
            <span className="w-12 h-12 bg-lime-100 text-lime-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">✍️</span>
            <h3 className="font-semibold text-lg mb-2">Lünkade täitmine</h3>
            <p className="text-gray-600 text-center">Kontrolli oma sõnavara ja grammatikat puuduvate sõnade täitmisega.</p>
          </Link>
          <Link to="/gap-fill-exercise" className="rounded-2xl bg-white p-8 shadow hover:shadow-xl transition flex flex-col items-center border-2 border-transparent hover:border-purple-400">
            <span className="w-12 h-12 bg-purple-100 text-purple-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">📝</span>
            <h3 className="font-semibold text-lg mb-2">Lünkade täitmise harjutus</h3>
            <p className="text-gray-600 text-center">Täida lüngad või tuleta õige sõna.</p>
          </Link>
          <div className="rounded-2xl bg-white p-8 shadow flex flex-col items-center opacity-50 cursor-not-allowed">
            <span className="w-12 h-12 bg-yellow-100 text-yellow-700 flex items-center justify-center rounded-full mb-4 text-2xl font-bold">❓</span>
            <h3 className="font-semibold text-lg mb-2">Valikvastused (varsti)</h3>
            <p className="text-gray-600 text-center">Vali õige vastus ja õpi oma vigadest.</p>
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
        <div className="text-gray-400 text-sm">&copy; {new Date().getFullYear()} Eesti ÕppeApp. Kõik õigused kaitstud.</div>
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
        <Route path="/dashboard" element={<UserDashboard />} />
        <Route path="/onboarding" element={<Onboarding />} />
        <Route path="/assessment-quiz" element={<AssessmentQuiz />} />
        <Route path="/lesson-start" element={<LessonStart />} />
        <Route path="/fill-in-the-blank" element={<FillInTheBlank />} />
        <Route path="/gap-fill-exercise" element={<GapFillExercise />} />
        <Route path="/register" element={<UserRegister />} />
      </Routes>
    </Router>
  );
}
