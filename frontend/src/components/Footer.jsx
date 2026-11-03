function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white px-6 py-8">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 md:flex-row">
        <p className="text-sm font-semibold text-indigo-600">
          DocuFlow AI
        </p>

        <p className="text-sm text-slate-500">
          © {new Date().getFullYear()} DocuFlow AI.
          Built with React, Django & AI.
        </p>
      </div>
    </footer>
  );
}

export default Footer;