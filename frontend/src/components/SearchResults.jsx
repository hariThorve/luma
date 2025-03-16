import { ExternalLink } from 'lucide-react';

function SearchResults({ results }) {
  if (!results || results.length === 0) {
    return (
      <div className="card p-4">
        <p className="text-gray-500">No search results found.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {results.map((result, index) => (
        <div key={index} className="card p-4 card-hover">
          <h3 className="font-medium text-lg mb-1">
            <a 
              href={result.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="hover:gradient-text flex items-center text-indigo-700 transition-all duration-200"
            >
              {result.title}
              <ExternalLink size={14} className="ml-1 inline-block" />
            </a>
          </h3>
          <p className="text-gray-500 text-xs mb-2 truncate">{result.url}</p>
          <p className="text-gray-700 text-sm">{result.snippet}</p>
        </div>
      ))}
    </div>
  );
}

export default SearchResults; 