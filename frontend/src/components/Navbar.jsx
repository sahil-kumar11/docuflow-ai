function Navbar() {
  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        <a
          href="/"
          className="text-2xl font-bold tracking-tight text-indigo-600"
        >
          DocuFlow AI
        </a>

        <div className="hidden items-center gap-8 md:flex">
          <a href="#features" className="text-sm font-medium text-slate-600 hover:text-indigo-600">
            Features
          </a>

          <a href="#about" className="text-sm font-medium text-slate-600 hover:text-indigo-600">
            About
          </a>

          <a href="#how-it-works" className="text-sm font-medium text-slate-600 hover:text-indigo-600">
            How It Works
          </a>
        </div>

        <span className="rounded-lg bg-indigo-50 px-4 py-2 text-sm font-semibold text-indigo-700">
          Coming Soon
        </span>
      </div>
    </nav>
  );
}

export default Navbar;