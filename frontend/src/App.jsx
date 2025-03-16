import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import SearchBar from './components/SearchBar';
import ModelSelector from './components/ModelSelector';
import SearchResults from './components/SearchResults';
import AIAnalysis from './components/AIAnalysis';
import GitHubLogo from './components/GitHubLogo';
import { searchApi } from './services/api';
import { Loader2 } from 'lucide-react';

function App() {
  const [query, setQuery] = useState('');
  const [availableModels, setAvailableModels] = useState([]);
  const [selectedModels, setSelectedModels] = useState([]);
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // Fetch available models when component mounts
    const fetchModels = async () => {
      try {
        const models = await searchApi.getModels();
        setAvailableModels(models);
        // Select the first model by default
        if (models.length > 0) {
          setSelectedModels([models[0].id]);
        }
      } catch (err) {
        console.error('Failed to fetch models:', err);
        setError('Failed to load AI models. Please try again later.');
      }
    };
    
    fetchModels();
  }, []);
  
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim() || selectedModels.length === 0) return;
    
    setLoading(true);
    setError(null);
    setSearchResults(null);
    
    try {
      const results = await searchApi.search(query, selectedModels);
      setSearchResults(results);
    } catch (err) {
      setError('Search failed. Please try again later.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-grow py-8">
        <div className="container">
          <div className="max-w-3xl mx-auto mb-8">
            <h1 className="text-3xl md:text-4xl font-bold text-center mb-6">
              <span className="gradient-text">LUMA</span> - Luminous AI Search
            </h1>
            <p className="text-gray-600 text-center mb-8">
              Enhance your search experience with AI-powered insights from multiple models
            </p>
            
            <form onSubmit={handleSearch} className="mb-6">
              <SearchBar 
                query={query} 
                setQuery={setQuery} 
                loading={loading} 
              />
              
              <div className="mt-4">
                <ModelSelector 
                  availableModels={availableModels || []}
                  selectedModels={selectedModels}
                  setSelectedModels={setSelectedModels}
                />
              </div>
            </form>
          </div>
          
          {loading && (
            <div className="flex justify-center my-12">
              <Loader2 className="h-12 w-12 text-indigo-500 animate-spin" />
            </div>
          )}
          
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg my-6">
              {error}
            </div>
          )}
          
          {searchResults && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1">
                <h2 className="text-xl font-semibold mb-4">Web Results</h2>
                <SearchResults results={searchResults.web_results} />
              </div>
              
              <div className="lg:col-span-2">
                <h2 className="text-xl font-semibold mb-4">AI Analysis</h2>
                <AIAnalysis analyses={searchResults.ai_analyses} />
              </div>
            </div>
          )}
        </div>
      </main>
      
      <Footer />
      <GitHubLogo />
    </div>
  );
}

export default App;
