import { Github } from 'lucide-react';

function Header() {
  return (
    <header className="py-4 border-b border-gray-100">
      <div className="container flex justify-between items-center">
        <div className="flex items-center gap-2">
          {/* Inline SVG Logo */}
          <svg 
            width="32" 
            height="32" 
            viewBox="0 0 32 32" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
            className="h-8 w-8"
          >
            <rect width="32" height="32" rx="8" fill="url(#logoGradient)" />
            <defs>
              <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#4f46e5" />
                <stop offset="50%" stopColor="#7c3aed" />
                <stop offset="100%" stopColor="#ec4899" />
              </linearGradient>
            </defs>
            <path 
              d="M10 10L16 16M16 16L22 22M16 16L22 10M16 16L10 22" 
              stroke="white" 
              strokeWidth="2.5" 
              strokeLinecap="round" 
              strokeLinejoin="round" 
            />
            <circle 
              cx="16" 
              cy="16" 
              r="6" 
              stroke="white" 
              strokeWidth="2" 
              strokeOpacity="0.5" 
            />
          </svg>
          
          <h1 className="text-xl font-bold gradient-text">LUMA</h1>
        </div>
        
        <div className="flex items-center gap-4">
          <a 
            href="https://github.com/hariThorve/luma.git" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
            title="View on GitHub"
          >
            <Github size={20} />
            <span className="hidden sm:inline">GitHub</span>
          </a>
        </div>
      </div>
    </header>
  );
}

export default Header; 