const features = [
  {
    icon: "📄",
    title: "Smart Document Management",
    description:
      "Upload, organize, and manage your documents in one intelligent workspace.",
  },
  {
    icon: "🤖",
    title: "AI Document Chat",
    description:
      "Ask questions about your PDFs and get answers with document references.",
  },
  {
    icon: "🔎",
    title: "Semantic Search",
    description:
      "Find relevant information across documents using AI-powered search.",
  },
  {
    icon: "⚡",
    title: "Workflow Automation",
    description:
      "Turn important document information into actionable tasks with AI.",
  },
];

function Home() {
  return (
    <main>
      {/* Hero Section */}
      <section className="bg-gradient-to-b from-indigo-50 to-white px-6 py-24">
        <div className="mx-auto max-w-5xl text-center">
          <span className="inline-block rounded-full bg-indigo-100 px-4 py-2 text-sm font-medium text-indigo-700">
            AI-Powered Productivity Platform
          </span>

          <h1 className="mt-8 text-4xl font-extrabold tracking-tight text-slate-900 md:text-6xl">
            Your Documents.
            <br />
            <span className="text-indigo-600">
              Your AI Workspace.
            </span>
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            Upload documents, ask intelligent questions, discover insights,
            and automate your workflow — all in one place.
          </p>

          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <a
              href="#features"
              className="rounded-xl bg-indigo-600 px-7 py-3 font-semibold text-white shadow-lg shadow-indigo-200 hover:bg-indigo-700"
            >
              Explore Features
            </a>

            <a
              href="#how-it-works"
              className="rounded-xl border border-slate-300 bg-white px-7 py-3 font-semibold text-slate-700 hover:bg-slate-50"
            >
              How It Works
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="px-6 py-20">
        <div className="mx-auto max-w-7xl">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-slate-900">
              Everything You Need in One Workspace
            </h2>

            <p className="mt-4 text-slate-600">
              Powerful AI features designed to simplify document workflows.
            </p>
          </div>

          <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <article
                key={feature.title}
                className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm hover:-translate-y-1 hover:shadow-lg"
              >
                <div className="mb-5 text-4xl">{feature.icon}</div>

                <h3 className="text-lg font-bold text-slate-900">
                  {feature.title}
                </h3>

                <p className="mt-3 text-sm leading-6 text-slate-600">
                  {feature.description}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section
        id="how-it-works"
        className="bg-slate-50 px-6 py-20"
      >
        <div className="mx-auto max-w-5xl text-center">
          <h2 className="text-3xl font-bold">
            How DocuFlow AI Works
          </h2>

          <div className="mt-12 grid gap-8 md:grid-cols-3">
            {[
              ["01", "Upload", "Upload your PDF documents."],
              ["02", "Ask AI", "Ask questions and find information."],
              ["03", "Take Action", "Create tasks from AI-generated insights."],
            ].map(([number, title, description]) => (
              <div key={number}>
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-indigo-600 font-bold text-white">
                  {number}
                </div>

                <h3 className="mt-5 text-xl font-semibold">{title}</h3>

                <p className="mt-2 text-slate-600">{description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About */}
      <section id="about" className="px-6 py-20">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold">
            Built for Smarter Productivity
          </h2>

          <p className="mt-5 leading-8 text-slate-600">
            DocuFlow AI combines modern web technologies with
            retrieval-augmented generation and intelligent automation
            to make document workflows easier.
          </p>
        </div>
      </section>
    </main>
  );
}

export default Home;