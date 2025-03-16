import { Github } from 'lucide-react';

function Footer() {
  return (
    <footer className="py-6 mt-auto border-t border-gray-100">
      <div className="container">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div>
            <p className="text-gray-500 text-sm">
              © {new Date().getFullYear()} LUMA - Luminous AI Search
            </p>
          </div>
          
          <div className="flex items-center gap-4">
            <a 
              href="https://github.com/hariThorve/luma.git" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
              title="View on GitHub"
            >
              <Github size={18} />
              <span>GitHub</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer; 