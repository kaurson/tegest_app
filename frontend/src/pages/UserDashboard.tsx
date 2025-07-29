import { Link } from 'react-router-dom';

const UserDashboard = () => {
  // Mock user data - in a real app this would come from context/state management
  const user = {
    name: "Keeleõppija",
    level: "Algaja",
    streak: 7,
    totalLessons: 12,
    accuracy: 85
  };

  const recentActivity = [
    { type: "Lünkade täitmine", date: "2 tundi tagasi", score: "8/10" },
    { type: "Lünkade täitmise harjutus", date: "1 päev tagasi", score: "7/10" },
    { type: "Hindamistest", date: "3 päeva tagasi", score: "9/10" }
  ];

  const handleContinueLearning = () => {
    // This would navigate to the next recommended lesson
    console.log("Jätka õppimist clicked");
  };

  const handleStartNewLesson = () => {
    // This would open lesson selection
    console.log("Alusta uut tundi clicked");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-10">
        <nav className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2 font-bold text-xl text-gray-900">
            <span className="inline-block w-6 h-6 bg-black rounded mr-2"></span>
            Eesti ÕppeApp
          </div>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">Tere tulemast, {user.name}!</span>
            <button className="bg-black text-white px-4 py-2 rounded-full font-semibold hover:bg-gray-900 transition">
              Profiil
            </button>
          </div>
        </nav>
      </header>

      {/* Main Dashboard Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Welcome Section */}
        <section className="mb-8">
          <div className="bg-gradient-to-r from-lime-400 to-lime-500 rounded-2xl p-8 text-white">
            <h1 className="text-3xl font-bold mb-2">Tere tulemast tagasi, {user.name}! 👋</h1>
            <p className="text-lime-100 mb-6">Kas oled valmis jätkama oma eesti keele õppimise teekonda?</p>
            <div className="flex gap-4">
              <button 
                onClick={handleContinueLearning}
                className="bg-white text-lime-600 font-semibold px-6 py-3 rounded-full hover:bg-lime-50 transition flex items-center gap-2"
              >
                Jätka õppimist
                <span className="inline-block bg-lime-600 text-white rounded-full w-5 h-5 flex items-center justify-center text-sm">→</span>
              </button>
              <button 
                onClick={handleStartNewLesson}
                className="bg-lime-600 text-white font-semibold px-6 py-3 rounded-full hover:bg-lime-700 transition"
              >
                Alusta uut tundi
              </button>
            </div>
          </div>
        </section>

        {/* Statistics Cards */}
        <section className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Sinu areng</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <div className="flex items-center justify-between mb-4">
                <span className="text-2xl">🔥</span>
                <span className="text-sm text-gray-500">Jada</span>
              </div>
              <div className="text-3xl font-bold text-gray-900">{user.streak} päeva</div>
              <p className="text-sm text-gray-600 mt-2">Jätka samas vaimus!</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <div className="flex items-center justify-between mb-4">
                <span className="text-2xl">📚</span>
                <span className="text-sm text-gray-500">Tunnid</span>
              </div>
              <div className="text-3xl font-bold text-gray-900">{user.totalLessons}</div>
              <p className="text-sm text-gray-600 mt-2">Lõpetatud</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <div className="flex items-center justify-between mb-4">
                <span className="text-2xl">🎯</span>
                <span className="text-sm text-gray-500">Täpsus</span>
              </div>
              <div className="text-3xl font-bold text-gray-900">{user.accuracy}%</div>
              <p className="text-sm text-gray-600 mt-2">Suurepärane töö!</p>
            </div>
            
            <div className="bg-white rounded-xl p-6 shadow-sm border">
              <div className="flex items-center justify-between mb-4">
                <span className="text-2xl">⭐</span>
                <span className="text-sm text-gray-500">Tase</span>
              </div>
              <div className="text-3xl font-bold text-gray-900">{user.level}</div>
              <p className="text-sm text-gray-600 mt-2">Praegune</p>
            </div>
          </div>
        </section>

        {/* Quick Access to Lessons */}
        <section className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Harjuta kohe</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Link 
              to="/onboarding" 
              className="bg-white rounded-xl p-6 shadow-sm border hover:shadow-md transition group"
            >
              <div className="flex items-center gap-4 mb-4">
                <span className="w-12 h-12 bg-lime-100 text-lime-700 flex items-center justify-center rounded-full text-2xl font-bold group-hover:bg-lime-200 transition">✍️</span>
                <div>
                  <h3 className="font-semibold text-lg text-gray-900">Lünkade täitmine</h3>
                  <p className="text-sm text-gray-600">Kontrolli sõnavara ja grammatikat</p>
                </div>
              </div>
              <div className="text-lime-600 font-medium text-sm">Alusta harjutamist →</div>
            </Link>
            
            <Link 
              to="/gap-fill-exercise" 
              className="bg-white rounded-xl p-6 shadow-sm border hover:shadow-md transition group"
            >
              <div className="flex items-center gap-4 mb-4">
                <span className="w-12 h-12 bg-purple-100 text-purple-700 flex items-center justify-center rounded-full text-2xl font-bold group-hover:bg-purple-200 transition">📝</span>
                <div>
                  <h3 className="font-semibold text-lg text-gray-900">Lünkade täitmise harjutus</h3>
                  <p className="text-sm text-gray-600">Täida puuduvad sõnad</p>
                </div>
              </div>
              <div className="text-purple-600 font-medium text-sm">Alusta harjutamist →</div>
            </Link>
            
            <div className="bg-white rounded-xl p-6 shadow-sm border opacity-50 cursor-not-allowed">
              <div className="flex items-center gap-4 mb-4">
                <span className="w-12 h-12 bg-yellow-100 text-yellow-700 flex items-center justify-center rounded-full text-2xl font-bold">❓</span>
                <div>
                  <h3 className="font-semibold text-lg text-gray-900">Valikvastustega</h3>
                  <p className="text-sm text-gray-600">Varsti saadaval</p>
                </div>
              </div>
              <div className="text-gray-400 font-medium text-sm">Pole saadaval</div>
            </div>
          </div>
        </section>

        {/* Recent Activity */}
        <section className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Viimane tegevus</h2>
          <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
            <div className="p-6">
              <div className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-center justify-between py-3 border-b last:border-b-0">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                        <span className="text-gray-600 font-semibold">
                          {activity.type === "Lünkade täitmine" ? "✍️" : 
                           activity.type === "Lünkade täitmise harjutus" ? "📝" : "❓"}
                        </span>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900">{activity.type}</h4>
                        <p className="text-sm text-gray-500">{activity.date}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold text-gray-900">{activity.score}</div>
                      <div className="text-sm text-gray-500">Tulemus</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Learning Tips */}
        <section className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Õppenõuanded</h2>
          <div className="bg-gradient-to-r from-purple-50 to-lime-50 rounded-xl p-6 border border-purple-100">
            <div className="flex items-start gap-4">
              <span className="text-2xl">💡</span>
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Igapäevane harjutamine toob täiuslikkuse</h3>
                <p className="text-gray-700">
                  Proovi harjutada vähemalt 15 minutit iga päev. Järjepidevus on keeleõppe edu võti!
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default UserDashboard; 