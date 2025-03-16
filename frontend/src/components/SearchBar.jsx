import { Search } from 'lucide-react';

function SearchBar({ query, setQuery, loading }) {
  return (
    <div className="relative">
      <div className="flex items-center bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="pl-4 pr-2 text-gray-400">
          <Search size={20} />
        </div>
        
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search anything..."
          className="w-full py-3 px-2 focus:outline-none search-glow"
          disabled={loading}
        />
        
        <button
          type="submit"
          className="btn-primary m-1 px-5 py-2"
          disabled={loading || !query.trim()}
        >
          Search
        </button>
      </div>
    </div>
  );
}

export default SearchBar; 